#!/usr/bin/env python3
"""
verify.html.py — post-flight quality check for PDF → HTML conversion output

Usage:
    python3 verify.html.py path/to/index.html [--pdf-pages N] [--brand-color #XXXXXX]

The 20 quality gates are documented in QUALITY_GATES.md.

Exit code:
    0 if score >= 80
    1 if score < 80
"""

import argparse
import re
import sys
from pathlib import Path


def count(text: str, pattern: str, flags: int = 0) -> int:
    return len(re.findall(pattern, text, flags))


def run_check(html_path: Path, pdf_pages: int, brand_color: str | None) -> tuple[int, list[tuple]]:
    text = html_path.read_text(encoding="utf-8")
    out_dir = html_path.parent
    results = []

    def gate(num: int, name: str, required: str, actual_value: str, passed: bool):
        results.append((num, name, required, actual_value, "✅" if passed else "❌"))

    # 1. Single HTML file
    is_html = html_path.suffix.lower() == ".html"
    gate(1, "Single HTML file", "required", "yes" if is_html else "no", is_html)

    # 2 & 3. PNG / img participation
    img_count = count(text, r"<img\b")
    png_files = list(out_dir.glob("*.png")) + list(out_dir.glob("slide_*.png"))
    img_to_png_ratio = (img_count / max(len(png_files), 1)) * 100 if png_files else 0
    expected_img = max(int(pdf_pages * 0.8), 1) if pdf_pages else 1
    gate(2, "PNG → <img> participation",
         "≥ 80%" if png_files else "n/a",
         f"{img_to_png_ratio:.0f}% ({img_count}/{len(png_files)})" if png_files else f"{img_count} imgs / 0 pngs",
         img_to_png_ratio >= 80 if png_files else True)
    gate(3, "<img> tag count",
         f"≥ {expected_img}",
         str(img_count),
         img_count >= expected_img)

    # 4. translateX
    tx = count(text, r"translateX")
    gate(4, "Horizontal scrolling (translateX)", "≥ 1", str(tx), tx >= 1)

    # 5. getBoundingClientRect
    gbcr = count(text, r"getBoundingClientRect")
    gate(5, "Dynamic SVG (getBoundingClientRect)", "≥ 1", str(gbcr), gbcr >= 1)

    # 6. getTotalLength
    gtl = count(text, r"getTotalLength")
    gate(6, "SVG line-draw (getTotalLength)", "≥ 1", str(gtl), gtl >= 1)

    # 7. stroke-dashoffset
    sdo = count(text, r"stroke-?[Dd]ashoffset", re.IGNORECASE)
    gate(7, "stroke-dashoffset animation", "≥ 2", str(sdo), sdo >= 2)

    # 8. requestAnimationFrame
    raf = count(text, r"requestAnimationFrame")
    gate(8, "requestAnimationFrame", "≥ 3", str(raf), raf >= 3)

    # 9. Section-active observer
    obs = count(text, r"IntersectionObserver") + count(text, r"MutationObserver")
    gate(9, "Section-active observer", "≥ 1", str(obs), obs >= 1)

    # 10. @keyframes diversity
    kf = count(text, r"@keyframes\b")
    gate(10, "@keyframes diversity", "≥ 5", str(kf), kf >= 5)

    # 11. transition declarations
    tr = count(text, r"transition:")
    gate(11, "transition declarations", "≥ 10", str(tr), tr >= 10)

    # 12. animation declarations
    an = count(text, r"animation:")
    gate(12, "animation declarations", "≥ 5", str(an), an >= 5)

    # 13. Brand color present
    if brand_color:
        bc_count = count(text, re.escape(brand_color), re.IGNORECASE)
        gate(13, f"Brand color {brand_color}", "≥ 1", str(bc_count), bc_count >= 1)
    else:
        gate(13, "Brand color (not specified)", "n/a (pass --brand-color)", "skipped", True)

    # 14. Google Fonts loaded
    gf = count(text, r"fonts\.googleapis\.com")
    gate(14, "Google Fonts loaded", "≥ 1", str(gf), gf >= 1)

    # 15. <section> count
    sec = count(text, r"<section\b")
    expected_sec = max(int(pdf_pages * 0.5), 1) if pdf_pages else 1
    gate(15, "<section> count",
         f"≥ {expected_sec}",
         str(sec),
         sec >= expected_sec)

    # 16. CSS/JS inlined (no external <link rel=stylesheet> except Google Fonts; no <script src> external)
    external_css = count(text, r'<link[^>]*rel="stylesheet"[^>]*>') - count(text, r'<link[^>]*fonts\.googleapis\.com[^>]*>') - count(text, r'<link[^>]*fonts\.gstatic\.com[^>]*>')
    external_js = count(text, r'<script[^>]*\bsrc=')
    inlined = (external_css <= 0 and external_js <= 0)
    gate(16, "CSS/JS inlined", "required",
         f"external_css={external_css}, external_js={external_js}",
         inlined)

    # 17. Source-fidelity samples — manual; report only that >=3 substantial Japanese strings exist
    jp_strings = re.findall(r"[ぁ-んァ-ヴ一-龯々]{6,}", text)
    distinct = len(set(jp_strings))
    gate(17, "Source-fidelity (distinct JP strings >=6 chars)",
         "≥ 3",
         str(distinct),
         distinct >= 3)

    # 18. External asset references (relative paths to logos/, photos/, assets/, slide_*.png)
    ext_assets = set()
    for m in re.finditer(r'(?:src|href|url\()\s*=?\s*[\'"]?((?:assets|logos|photos|presskits|slide_)[^\s\'"\)]+)', text):
        ext_assets.add(m.group(1))
    gate(18, "External asset references (unique)",
         "≥ 5",
         str(len(ext_assets)),
         len(ext_assets) >= 5)

    # 19. Light theme default — look for light bg colors
    light_bg = bool(re.search(r"background(?:-color)?:\s*(?:#EEE+|#FFF+|#F[5-9A-F]|white)", text, re.IGNORECASE))
    gate(19, "Light theme background", "required (unless dark requested)",
         "yes" if light_bg else "no",
         light_bg)

    # 20. No meta-files in output directory
    meta_patterns = ["README.md", "QUICKSTART.md", "INDEX.html", "FOR_OTHER_CLAUDES.md"]
    meta_folders = ["templates", "animations", "design_system", "workflows", "skills"]
    meta_found = []
    for p in meta_patterns:
        if (out_dir / p).exists():
            meta_found.append(p)
    for f in meta_folders:
        if (out_dir / f).is_dir():
            meta_found.append(f + "/")
    no_meta = (len(meta_found) == 0)
    gate(20, "No meta-files in output",
         "required",
         "clean" if no_meta else f"FOUND: {', '.join(meta_found)}",
         no_meta)

    # 21. Bilingual + language toggle (Rule 17) — MANDATORY
    has_lang_ja = bool(re.search(r'data-lang=["\']ja["\']|lang=["\']ja["\']|"ja"\s*:\s*["\'`]', text))
    has_lang_en = bool(re.search(r'data-lang=["\']en["\']|lang=["\']en["\']|"en"\s*:\s*["\'`]', text))
    has_toggle = bool(re.search(
        r'id=["\']lang-toggle["\']|class=["\'][^"\']*lang-(?:toggle|switch|switcher)|data-lang-toggle',
        text, re.IGNORECASE
    ))
    bilingual_ok = has_lang_ja and has_lang_en and has_toggle
    gate(21, "Bilingual + language toggle (Rule 17)",
         "required (ja + en + toggle)",
         f"ja={'y' if has_lang_ja else 'n'} en={'y' if has_lang_en else 'n'} toggle={'y' if has_toggle else 'n'}",
         bilingual_ok)

    # 22. Visual audit completed (WORKFLOW.md Stage 8) — MANDATORY
    audit_dir = out_dir / "_audit"
    audit_report = audit_dir / "REPORT.md"
    audit_pngs = list(audit_dir.glob("page-*.png")) if audit_dir.is_dir() else []
    sec_count_for_audit = count(text, r"<section\b")
    if not audit_report.exists():
        actual_audit = "REPORT.md missing"
        audit_ok = False
    else:
        rep_text = audit_report.read_text(encoding="utf-8", errors="replace")
        has_iter = bool(re.search(r"iteration\b", rep_text, re.IGNORECASE))
        has_zero_critical = bool(re.search(r"CRITICAL[:：]\s*0\b", rep_text, re.IGNORECASE)) or bool(re.search(r"zero CRITICAL", rep_text, re.IGNORECASE))
        has_zero_high = bool(re.search(r"HIGH[:：]\s*0\b", rep_text, re.IGNORECASE)) or bool(re.search(r"zero HIGH", rep_text, re.IGNORECASE))
        png_ok = len(audit_pngs) >= max(int(sec_count_for_audit * 0.9), 1)
        audit_ok = has_iter and has_zero_critical and has_zero_high and png_ok
        actual_audit = f"PNGs={len(audit_pngs)}/{sec_count_for_audit} iter={'y' if has_iter else 'n'} 0CRIT={'y' if has_zero_critical else 'n'} 0HIGH={'y' if has_zero_high else 'n'}"
    gate(22, "Visual audit completed (WORKFLOW Stage 8)",
         "_audit/REPORT.md + page-*.png + iter + 0CRIT + 0HIGH",
         actual_audit,
         audit_ok)

    # 24. Section transition pacing (Rule 18a) — MANDATORY
    # Detects whether section-to-section transitions use elegant duration + easing.
    # Acceptable: opacity transition between 0.6s and 1.2s with cubic-bezier easing.
    section_paced = False
    section_pacing_detail = "no section transition detected"
    # Match patterns like `transition: opacity 0.7s cubic-bezier(...)`
    sec_pacing_re = re.search(
        r"section\s*\{[^}]*transition\s*:[^;}]*opacity\s+(0?\.\d+|[12]\.\d+)s[^;}]*cubic-bezier",
        text, re.IGNORECASE | re.DOTALL
    )
    if sec_pacing_re:
        dur = float(sec_pacing_re.group(1))
        if 0.6 <= dur <= 1.2:
            section_paced = True
            section_pacing_detail = f"opacity {dur}s cubic-bezier ✅"
        else:
            section_pacing_detail = f"opacity {dur}s (out of 0.6–1.2s range)"
    else:
        # Fallback: any opacity transition with cubic-bezier on section/slide
        fallback = re.search(
            r"\.slide[^{]*\{[^}]*transition[^;}]*opacity[^;}]*cubic-bezier|opacity\s+(0?\.[6-9]|1\.[0-2])\d*s[^;]*cubic-bezier",
            text, re.IGNORECASE | re.DOTALL
        )
        if fallback:
            section_paced = True
            section_pacing_detail = "opacity + cubic-bezier detected (heuristic)"
    gate(24, "Section transition pacing (Rule 18a)",
         "opacity 0.6–1.2s + cubic-bezier",
         section_pacing_detail,
         section_paced)

    # 25. Content reveal stagger (Rule 18b) — MANDATORY
    # Detects whether content has staggered reveal with cinematic easing.
    # Look for: .reveal class + transition-delay cascade + cubic-bezier(0.16,1,0.3,1) or (0.22,1,0.36,1)
    reveal_class = bool(re.search(r"\.reveal\b", text))
    cinematic_easing = bool(re.search(
        r"cubic-bezier\(\s*0?\.16\s*,\s*1\s*,\s*0?\.3\s*,\s*1\s*\)|"
        r"cubic-bezier\(\s*0?\.22\s*,\s*1\s*,\s*0?\.36\s*,\s*1\s*\)",
        text
    ))
    stagger_delays = len(re.findall(
        r"transition-delay\s*:\s*0?\.\d+s|animation-delay\s*:\s*0?\.\d+s|--d\s*:\s*0?\.\d+s",
        text
    ))
    reveal_ok = reveal_class and cinematic_easing and stagger_delays >= 3
    gate(25, "Content reveal stagger (Rule 18b)",
         ".reveal + cubic-bezier(.16,1,.3,1)/(.22,1,.36,1) + ≥3 delays",
         f"reveal={'y' if reveal_class else 'n'} easing={'y' if cinematic_easing else 'n'} delays={stagger_delays}",
         reveal_ok)

    # 23. Multi-axis transition diversity (Rule 15) — MANDATORY
    # Detects whether section entrances use multiple transform axes,
    # not just translateX (= 紙芝居 / single-axis carousel).
    axes_found = []
    if re.search(r"translateY\s*\(", text):                 axes_found.append("translateY")
    if re.search(r"translateX\s*\(", text):                 axes_found.append("translateX")
    if re.search(r"scale\s*\(", text):                      axes_found.append("scale")
    if re.search(r"rotate(?:[XYZ])?\s*\(", text):           axes_found.append("rotate")
    if re.search(r"perspective\s*\(", text):                axes_found.append("perspective")
    # Ken-Burns / drift detection: scale + translate combined in @keyframes
    if re.search(r"@keyframes[^{]*\{[^}]*translate[^}]*scale|@keyframes[^{]*\{[^}]*scale[^}]*translate", text, re.DOTALL):
        axes_found.append("ken-burns")
    # Letter-stagger / per-char animation detection
    if re.search(r"animation-delay\s*:\s*calc|--char-d|nth-child\([^)]+\)\s*\{[^}]*animation-delay", text):
        axes_found.append("letter-stagger")
    axes_unique = list(dict.fromkeys(axes_found))  # dedupe preserving order
    multi_axis_ok = len(axes_unique) >= 3
    gate(23, "Multi-axis transition diversity (Rule 15)",
         "≥ 3 distinct transform axes",
         f"{len(axes_unique)} axes: {','.join(axes_unique) if axes_unique else 'none'}",
         multi_axis_ok)

    passed_count = sum(1 for r in results if r[4] == "✅")
    score = int(round((passed_count / len(results)) * 100))

    # CRITICAL gates — any fail forces overall reject regardless of score
    CRITICAL_GATE_NUMS = {1, 13, 16, 19, 20, 21, 22, 23, 24, 25}
    critical_fails = [r for r in results if r[0] in CRITICAL_GATE_NUMS and r[4] == "❌"]

    return score, results, critical_fails


def main():
    ap = argparse.ArgumentParser(description="Post-flight quality check for PDF → HTML conversion")
    ap.add_argument("html_path", type=Path)
    ap.add_argument("--pdf-pages", type=int, default=0, help="Number of pages in source PDF (improves gate 3/15)")
    ap.add_argument("--brand-color", type=str, default=None, help="Official brand hex color, e.g. #1A5EFF")
    args = ap.parse_args()

    if not args.html_path.exists():
        print(f"❌ file not found: {args.html_path}", file=sys.stderr)
        sys.exit(2)

    score, results, critical_fails = run_check(args.html_path, args.pdf_pages, args.brand_color)

    print(f"\n=== Post-flight quality check ===")
    print(f"file: {args.html_path}")
    if args.pdf_pages:
        print(f"pdf pages assumed: {args.pdf_pages}")
    if args.brand_color:
        print(f"brand color: {args.brand_color}")
    print()
    print(f"| {'#':>2} | {'Gate':<42} | {'Required':<28} | {'Actual':<30} | {'Status':<6} |")
    print(f"|----|" + "-" * 44 + "|" + "-" * 30 + "|" + "-" * 32 + "|--------|")
    for num, name, required, actual, status in results:
        marker = " ★CRIT" if num in {1, 13, 16, 19, 20, 21, 22, 23, 24, 25} else ""
        print(f"| {num:>2} | {name:<42.42}{marker} | {required:<28.28} | {actual:<30.30} | {status:<6} |")
    print()
    print(f"Score: {score} / 100")

    if critical_fails:
        print()
        print("❌ HARD REJECT — one or more CRITICAL gates failed.")
        print("   CRITICAL gates (any fail = hard reject regardless of score):")
        for num, name, _, actual, _ in critical_fails:
            print(f"     gate {num}: {name} — actual: {actual}")
        print()
        print("   You MUST fix these and re-run. Score >= 80 does NOT override critical fails.")
        print("   gate 13 specifically: if the official brand color was not found in the press")
        print("   kit, do a real web search ('<company> press kit', 'site:<domain>/press',")
        print("   '<company> brand assets') before falling back to an approximate color.")
        sys.exit(2)

    if score >= 80:
        print("✅ acceptable — ready to deliver")
        sys.exit(0)
    else:
        print("❌ NOT acceptable — fix the failing gates before delivering")
        print("   See QUALITY_GATES.md for the standard.")
        sys.exit(1)


if __name__ == "__main__":
    main()
