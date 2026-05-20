# CHANGELOG

All notable changes to `slide-to-html-deck-playbook` will be documented here.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/).

---

## [1.0.0] — 2026-05-19

First public release. The repository ships an **11-stage collaborative pipeline** for converting one PDF / Google Slides into one beautiful single-file HTML deck, validated against 25 machine-checkable gates (10 of them CRITICAL).

### How it works

The user's effort is ~15 minutes of clicking and approving across 6 checkpoints. The AI does ~2-4 hours of background work (web research, pixel measurement, visual self-audit, fix iterations) between them. The user is never asked to find their own press kit — the AI does the web search and presents one-click DL URLs.

### Included

**The 11-stage workflow ([`WORKFLOW.md`](WORKFLOW.md))**
- Stage 0 — Source intake (verify company identity via domain)
- Stage 1 — Asset research, 5-category MECE protocol (the AI does the web search; the user only clicks DL URLs)
- Stage 2 — Asset collection checkpoint (strip `cls-1` background rect from SVGs)
- Stage 3 — Pre-flight 10-item self-declaration
- Stage 4 — Page mapping table (HARD GATE)
- Stage 5 — Pixel measurement via PIL / OpenCV (for any page with 3+ positioned shapes)
- Stage 6 — Brand system setup (`tokens.css`)
- Stage 7 — HTML draft (vanilla or React)
- Stage 8 — Self visual audit (HARD GATE — Playwright render → Read every PNG → loop)
- Stage 9 — Fix iterations until zero CRITICAL / HIGH defects
- Stage 10 — Post-flight `verify.html.py` (25 gates, 10 CRITICAL)
- Stage 11 — Handoff

**Five new doctrine documents**
- [`ASSET_RESEARCH.md`](ASSET_RESEARCH.md) — 5-category MECE search protocol. Forbids inline `<polygon>` logo substitution and guessed brand colors.
- [`PIXEL_MEASUREMENT.md`](PIXEL_MEASUREMENT.md) — PIL + OpenCV measurement protocol. Forbids eyeballing for any page with 3+ positioned shapes.
- [`VISUAL_AUDIT.md`](VISUAL_AUDIT.md) — Mandatory Playwright render → Read PNG → `_audit/REPORT.md` → loop ritual. "Build passed" is **not** completion.
- [`REACT_PIPELINE.md`](REACT_PIPELINE.md) — When (and how) to switch from vanilla HTML to React + Vite + Framer Motion + `vite-plugin-singlefile`.
- [`WORKFLOW.md`](WORKFLOW.md) — Full 11-stage pipeline definition.

**25 quality gates ([`QUALITY_GATES.md`](QUALITY_GATES.md) + [`verify.html.py`](verify.html.py))**
- 10 CRITICAL gates (any single failure = hard reject regardless of overall score):
  - Gate 1 — Single HTML file
  - Gate 13 — Official brand color hex present (not a guess)
  - Gate 16 — CSS / JS inlined
  - Gate 19 — Light theme default unless dark explicitly requested
  - Gate 20 — No meta-files in output directory
  - Gate 21 — Bilingual EN/JP with top-right language toggle (Rule 17)
  - Gate 22 — Visual audit completed (`_audit/REPORT.md` + page-NN.png + iteration history)
  - Gate 23 — Multi-axis transition diversity (≥3 transform axes used in entrance animations)
  - Gate 24 — Section transition pacing (cross-fade 0.6–1.2s + cubic-bezier easing)
  - Gate 25 — Content reveal stagger (.reveal class + cinematic cubic-bezier + ≥3 delays)
- 15 additional signal gates (animation diversity, source fidelity, `<img>` participation, etc.)
- `verify.html.py` exits with code 2 on any CRITICAL fail (versus code 1 on score < 80)

**Skill bundle ([`skill-bundle/`](skill-bundle/) + [`dist/slide-to-html-skill.zip`](dist/))**
- Self-contained 12-file bundle attachable to any Claude / ChatGPT / Gemini chat
- Bilingual EN/JP rules embedded as Rule 17 in the prompt body
- The same 25-gate checker ships inside the bundle

**Anti-pattern protection**
- [`AGENTS.md`](AGENTS.md) lists 8 known failure modes that previously produced low-quality output
- [`PRE_FLIGHT_CHECKLIST.md`](PRE_FLIGHT_CHECKLIST.md) makes asset / measurement / animation gaps visible before HTML is written
- Both `README.md` and `AGENTS.md` open with the absolute prohibition: do not produce a toolkit, multiple HTML templates, a ZIP archive, or a style menu

### Design principle

> minimum user effort × maximum collaborative quality

The user is **never** asked to find their own press kit. The AI does the web research, presents one-click DL URLs, strips the SVG background rects, runs the visual audit, iterates on its own output, and verifies against 25 gates — before declaring completion.

### Reference quality bar

The Turing company deck at <https://tur.ing/company-deck/> is the canonical example of a fully-realized output. Its source HTML measures approximately:

- 29 sections, ~10,850 lines, 446 KB
- 51 `<img>` references, 14 `<video>`, 40 `<svg>`
- 23 `translateX`, 27 `getBoundingClientRect`, 8 `getTotalLength`
- 42 `@keyframes`, 52 `animation:`, 34 `transition:`
- 19 occurrences of Turing Red `#9B1B30`
- Implemented EN/JP language toggle at top-right

The minimum thresholds in `QUALITY_GATES.md` are much lower (the floor), but a deliverable that scores `1` where the reference scores `23` is almost certainly missing a major capability.

### Generic for any company

The system is **company-agnostic**. There are no hardcoded brand colors, fonts, names, or photos in the prompt or scripts. Every brand asset is discovered fresh per conversion via `ASSET_RESEARCH.md`. The `--brand-color` flag in `verify.html.py` is supplied per-conversion, not baked in.

---

## License

MIT. Third-party brand assets used during development are not bundled and remain subject to their respective owners' terms.
