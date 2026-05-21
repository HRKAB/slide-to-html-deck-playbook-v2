# QUALITY_GATES — machine-verifiable acceptance criteria

If you are an AI agent that just finished generating an `index.html` for a user's PDF → HTML conversion, **STOP**. Do not deliver yet. You must first run the post-flight check defined below.

The reference quality bar for this repository is the Turing company deck published at **https://tur.ing/company-deck/** — a publicly available 29-section deck whose source HTML serves as the canonical example of what a high-quality output of this prompt looks like. All reference metrics quoted below are measured directly from that production build.

If your output fails any of these gates, your deliverable is **not acceptable** and you must fix the gaps before delivering.

---

## How to run the check

```bash
python3 verify.html.py path/to/your/index.html --pdf-pages N --brand-color #XXXXXX
```

The script grep-counts each metric and prints PASS / FAIL per gate, plus a `score / 100`. Below 80 = not acceptable.

---

## The 25 gates (with minimum thresholds and Turing reference values)

For an N-page source PDF (typical N = 20-50):

| # | Gate | Metric | Min threshold | Reference (tur.ing/company-deck/) |
|---|---|---|---|---|
| 1 | **File is single HTML** | output is exactly one `.html` | required | 1 file (446 KB, ~10,850 lines) |
| 2 | **PNG-to-img participation** | (count of `<img src="slide_*.png">`) / (PNGs extracted from PDF) | ≥ 80 % | 100 % when applicable |
| 3 | **`<img>` tag count** | `grep -c '<img\b' index.html` | ≥ N × 0.8 | 51 |
| 4 | **Horizontal scrolling architecture** | `translateX` occurrences in CSS or JS | ≥ 1 | 23 |
| 5 | **Dynamic SVG drawing** | `getBoundingClientRect` calls in JS | ≥ 1 | 27 |
| 6 | **SVG line-draw animation** | `getTotalLength` calls in JS | ≥ 1 | 8 |
| 7 | **stroke-dashoffset animation** | `stroke-dashoffset` occurrences | ≥ 2 | 30 |
| 8 | **requestAnimationFrame** | calls in JS | ≥ 3 | 26 |
| 9 | **Section-active observer** | `IntersectionObserver` or `MutationObserver` calls | ≥ 1 | 8 (Mutation) |
| 10 | **Animation diversity** | `@keyframes` definitions count | ≥ 5 | 42 |
| 11 | **transition declarations** | `transition:` occurrences in CSS | ≥ 10 | 34 |
| 12 | **animation declarations** | `animation:` occurrences in CSS | ≥ 5 | 52 |
| 13 | **Brand color present** | the user-confirmed brand hex appears in CSS | ≥ 1 | 19 (Turing Red `#9B1B30`) |
| 14 | **Google Fonts loaded** | `fonts.googleapis.com` link | ≥ 1 | 2 |
| 15 | **Section element count** | `<section>` tags | ≥ ⌈N × 0.5⌉ | 29 |
| 16 | **Single-file delivery** | CSS and JS inlined (no external `<link rel="stylesheet">` / `<script src>` other than Google Fonts) | required | inlined |
| 17 | **Source-fidelity sample** | distinct ≥6-char Japanese strings from source appear in HTML | ≥ 3 | many |
| 18 | **External asset references** | unique relative paths to `logos/`, `photos/`, `assets/`, `slide_*.png` etc. | ≥ 5 | 50+ |
| 19 | **Light theme default** | background uses light hex (`#EEEEEE`, `#FFFFFF`, `#F5F5F5`, etc.) | required unless dark requested | `#EEEEEE` |
| 20 | **No meta-files produced** | output directory contains no `README.md`, `QUICKSTART.md`, `INDEX.html`, `FOR_OTHER_CLAUDES.md`, `00_*`, no folders named `templates/`, `animations/`, `design_system/`, `workflows/`, `skills/` | required | n/a |
| 21 | **Bilingual + language toggle (Rule 17)** | HTML contains `data-lang="ja"` (or equivalent) AND `data-lang="en"` AND a top-right language toggle button (`#lang-toggle` / `.lang-switcher` / similar) AND a JA-leak check passes — NO kana/kanji (incl. units like 万/個/円/名) sits outside a ja/en pair | required | implemented top-right, 0 JA leaks |
| 22 | **Visual audit completed** | `_audit/REPORT.md` exists adjacent to `index.html`, AND `_audit/page-*.png` count equals `<section>` count, AND REPORT.md contains "iteration" + "CRITICAL: 0" + "HIGH: 0" markers | required | iterations 2-4, zero CRITICAL/HIGH at final |
| 23 | **Multi-axis transition diversity (Rule 15)** | Distinct transform axes used in entrance animations: `translateY` / `translateX` / `scale` / `rotate` / `perspective` / Ken-Burns drift / letter-stagger. Single-axis (e.g., `translateY` only) = 紙芝居 / paper-shadow feel = build rejected. | ≥ 3 distinct axes | 5+ axes in Turing deck |
| 24 | **Section transition pacing (Rule 18a)** | Section-to-section cross-fade uses `transition: opacity ...` with duration 0.6–1.2s AND `cubic-bezier(...)` easing. Plain `ease` keyword or duration ≤0.4s = "snap" feel = build rejected. | opacity 0.6–1.2s + cubic-bezier | `0.7s cubic-bezier(0.65,0,0.35,1)` |
| 25 | **Content reveal stagger (Rule 18b)** | Content uses `.reveal` class with cinematic easing (`cubic-bezier(0.16,1,0.3,1)` or `cubic-bezier(0.22,1,0.36,1)`) AND ≥3 stagger delays (transition-delay / animation-delay / --d). All-content-at-once or no easing = static feel = build rejected. | `.reveal` + cinematic easing + ≥3 delays | 100+ delays in Turing deck |

The reference column shows what a fully-realized output looks like. You are not required to hit these reference numbers — only the **minimum threshold** column — but a deliverable that scores `1` where the reference scores `23` (e.g., translateX) is almost certainly missing a major capability.

---

## How to interpret your score

| Score | Meaning |
|---|---|
| 95-100 | At or above the reference quality bar. Ready to deliver. |
| 80-94 | Acceptable. Note which gates are weak; the user may ask for refinement. |
| 60-79 | Substantial work skipped. Restart the work on the failing gates BEFORE delivering. |
| Below 60 | Reject your own output. You almost certainly skipped Phase 0 (asset discovery) and/or pixel measurement. Re-read `PRE_FLIGHT_CHECKLIST.md` and run the conversion again. |

### ★ CRITICAL gates — any failure = hard reject regardless of score

The following gates are **CRITICAL**. If any one of them fails, the deliverable is rejected **even if the overall score is 95+**. The verify script exits with code 2 (not 1) when a critical gate fails, to make the distinction unmistakable.

| Gate # | Why CRITICAL |
|---|---|
| 1 | Single HTML file — if you produced a toolkit / multiple files / a ZIP, the entire task is misinterpreted |
| 13 | Brand color present — using a guessed approximate color instead of the official one is a brand violation. Get the real color from the press kit / IR docs / official SVG, do not eyeball |
| 16 | CSS/JS inlined — if external CSS/JS is referenced, the file is not self-contained |
| 19 | Light theme — dark theme without explicit user request violates Reference D |
| 20 | No meta-files — if the output directory contains `QUICKSTART.md`/`INDEX.html`/etc., you regressed into toolkit-replication |
| 21 | Bilingual + lang toggle (Rule 17) — monolingual output is a Rule 17 violation, non-negotiable |
| 22 | Visual audit completed — if no `_audit/` directory exists, you skipped Stage 8 of `WORKFLOW.md` and did not look at your own output |
| 23 | Multi-axis transition diversity — single-axis entrances (e.g., `translateY` only across all sections, or `opacity` only) feel like a paper-shadow show. The reference Turing deck mixes 5+ axes across its sections |
| 24 | Section transition pacing — without cinematic `cubic-bezier` and 0.6–1.2s duration, page navigation feels like a desktop carousel snap, killing the deck experience |
| 25 | Content reveal stagger — without staggered `.reveal` cascade, all text/images appear at once, making the page feel like a static screenshot instead of a cinematic entrance |

These 6 are the spine of the deliverable. The other 14 gates are signals of completeness and depth, but failing one of them at a time is recoverable. Failing a CRITICAL gate is not.

The recent failure case that motivated this file scored **20 / 100**. The output had `<img>` count = 0 despite the source PDF being extracted to 29 PNGs, `translateX` count = 0 (no horizontal architecture), `getBoundingClientRect` count = 0 (no dynamic SVG), brand color count = 0 (used a guessed approximate hex), `@keyframes` count = 1 (no animation diversity). The user rejected it as "全然ダメ". This is the failure mode this gate set exists to prevent.

---

## Mandatory post-flight ritual

After generating `index.html`, you MUST post the following block in chat **before** declaring the work complete:

```
## Post-flight metric report

I ran `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX`
and the results are:

| # | Gate | Required | Actual | Status |
|---|---|---|---|---|
| 1 | Single HTML file | required | yes/no | ✅/❌ |
| 2 | PNG-to-img participation | ≥ 80 % | XX % | ✅/❌ |
| 3 | <img> tag count | ≥ N×0.8 | XX | ✅/❌ |
| 4 | translateX | ≥ 1 | XX | ✅/❌ |
| 5 | getBoundingClientRect | ≥ 1 | XX | ✅/❌ |
| 6 | getTotalLength | ≥ 1 | XX | ✅/❌ |
| 7 | stroke-dashoffset | ≥ 2 | XX | ✅/❌ |
| 8 | requestAnimationFrame | ≥ 3 | XX | ✅/❌ |
| 9 | Section-active observer | ≥ 1 | XX | ✅/❌ |
| 10 | @keyframes diversity | ≥ 5 | XX | ✅/❌ |
| 11 | transition declarations | ≥ 10 | XX | ✅/❌ |
| 12 | animation declarations | ≥ 5 | XX | ✅/❌ |
| 13 | Brand color present | ≥ 1 | XX | ✅/❌ |
| 14 | Google Fonts loaded | ≥ 1 | XX | ✅/❌ |
| 15 | <section> count | ≥ ⌈N×0.5⌉ | XX | ✅/❌ |
| 16 | CSS/JS inlined | required | yes/no | ✅/❌ |
| 17 | Source-fidelity samples | ≥ 3 verbatim strings | XX | ✅/❌ |
| 18 | External asset references | ≥ 5 | XX | ✅/❌ |
| 19 | Light theme | required | yes/no | ✅/❌ |
| 20 | No meta-files | required | yes/no | ✅/❌ |
| 21 | Bilingual + lang toggle (Rule 17) | required | ja+en+toggle | ✅/❌ |
| 22 | Visual audit completed (Stage 8) | _audit/REPORT.md + page-*.png + 0 CRIT + 0 HIGH | XX | ✅/❌ |
| 23 | Multi-axis transition diversity (Rule 15) | ≥ 3 axes | XX axes: ... | ✅/❌ |
| 24 | Section transition pacing (Rule 18a) | opacity 0.6–1.2s + cubic-bezier | duration + easing | ✅/❌ |
| 25 | Content reveal stagger (Rule 18b) | .reveal + cinematic + ≥3 delays | reveal+easing+delays | ✅/❌ |

Score: XX / 100
```

If your score is below 80, **or if any CRITICAL gate (1 / 13 / 16 / 19 / 20 / 21 / 22 / 23 / 24 / 25) fails**, **do not deliver**. Identify the failing gates, fix the gaps, regenerate, re-run the script, re-post the metric report. Loop until you pass.

This is the difference between an AI that *says* "I will produce a beautiful deck" and an AI that *proves* it produced one. The user cannot evaluate your output unless you give them a numeric report alongside it.
