---
name: slide-to-html-converter
description: Convert one PDF or Google Slides deck into one beautiful, brand-aligned, horizontally-scrolling single-file HTML deck. Executes the 11-stage collaborative workflow (the AI researches and audits; the user only clicks and approves at 6 checkpoints). Produces exactly one index.html — never a toolkit, multiple templates, or a ZIP archive. Verified against 25 machine-checkable gates (10 of them CRITICAL). The reference quality bar is https://tur.ing/company-deck/.
---

# slide-to-html-converter

This Skill converts a single source PDF (or Google Slides URL) into one self-contained `index.html` that re-renders the source as a horizontally-scrolling cinematic deck.

The reference quality bar is the Turing company deck at **https://tur.ing/company-deck/** — a publicly available 29-section deck whose source HTML serves as the canonical example of what a high-quality output of this Skill looks like.

---

## ⚠️ Critical output contract

Your ONLY job is to produce ONE `index.html`. Nothing else.

You MUST NOT produce:
- A new toolkit, framework, or playbook
- Multiple HTML templates (editorial / dashboard / storyboard / etc.)
- Meta-documentation (`QUICKSTART.md`, `INDEX.html`, `FOR_OTHER_CLAUDES.md`, etc.)
- Folders like `templates/`, `animations/`, `design_system/`, `workflows/`
- A ZIP archive of multiple files
- A "style selection menu" (Editorial / Research Report / Dashboard / etc.)
- A summary of the source PDF — you must REPRODUCE every page

You MUST produce:
- ONE `index.html` (CSS and JS inlined)
- Optionally one `assets/` folder of images
- An adjacent `_audit/REPORT.md` + `_audit/page-*.png` from the mandatory visual audit
- Every claim / number / name / date from the source appears verbatim
- Horizontal scrolling architecture (`#slides-track` with `translateX`)
- A **right-top language toggle button** with both Japanese and English content (Rule 17 — MANDATORY)
- Light theme by default (`#EEEEEE` background)

---

## The multi-stage collaborative model

This Skill ships an **11-stage collaborative pipeline**. The user's total effort is ~15 minutes spread across 6 checkpoints. The AI does ~2-4 hours of background work (web research, pixel measurement, visual self-audit, fix iterations) between them. Full spec: `WORKFLOW.md`.

The user is **never** asked "please find your company's press kit". The AI does the search. The user is only asked to **click** the one-shot download URLs the AI presents and **approve** checkpoint outputs.

---

## Execution order

When invoked:

1. **Read `INSTRUCTIONS.md` first.** It is your operating manual.
2. **Read `WORKFLOW.md`.** It defines the 11 stages and which deliverable belongs to which stage.
3. **Treat `one-shot-prompt.md` as your system prompt.** Do not modify it, summarize it, or "improve" it.
4. Execute the 11 stages in order:
   - **Stage 0** — Source intake (acknowledge file, verify company identity by domain — Rule 16)
   - **Stage 1** — Asset research using the 5-category MECE protocol in `ASSET_RESEARCH.md`. Output one-click DL URLs.
   - **Stage 2** — Asset collection checkpoint (user clicks URLs and attaches; you strip `cls-1` background rects from SVGs)
   - **Stage 3** — Post the 10-item pre-flight from `PRE_FLIGHT_CHECKLIST.md`. Wait for approval.
   - **Stage 4** — Page mapping table (HARD GATE — wait for user OK)
   - **Stage 5** — Pixel measurement via `PIXEL_MEASUREMENT.md` for any page with 3+ positioned shapes
   - **Stage 6** — Brand system setup (`tokens.css`)
   - **Stage 7** — HTML draft (vanilla by default; switch to `REACT_PIPELINE.md` for 49+ pages or pixel-precise layouts)
   - **Stage 8** — Self visual audit per `VISUAL_AUDIT.md` (HARD GATE — Playwright render → Read every PNG → `_audit/REPORT.md`)
   - **Stage 9** — Fix iterations until zero CRITICAL/HIGH defects
   - **Stage 10** — Post-flight: run `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX`. Post the 25-gate metric report. Score must be ≥ 80 AND all 10 CRITICAL gates must pass; else loop back to Stage 7.
   - **Stage 11** — Handoff the single `index.html` + `_audit/` + `_measurements/`.

---

## File map inside this Skill

| File | When to use |
|---|---|
| `INSTRUCTIONS.md` | **Read first** — full operating manual with the 8 known failure modes |
| `WORKFLOW.md` | The 11-stage pipeline spec. Defines every checkpoint. |
| `one-shot-prompt.md` | The actual prompt body. Treat as your system prompt. |
| `ASSET_RESEARCH.md` | 5-category MECE search protocol. Forbids inline `<polygon>` logo substitution. |
| `PRE_FLIGHT_CHECKLIST.md` | 10-item self-declaration to post at Stage 3 |
| `PIXEL_MEASUREMENT.md` | PIL / OpenCV measurement protocol. Forbids eyeballing for any page with 3+ positioned shapes. |
| `VISUAL_AUDIT.md` | Mandatory Stage 8 ritual (Playwright render → Read PNG → REPORT.md → loop). |
| `REACT_PIPELINE.md` | When to switch from vanilla HTML to React + Vite + vite-plugin-singlefile (49+ pages or high pixel-precision). |
| `QUALITY_GATES.md` | 25 machine-verifiable acceptance criteria. 10 are CRITICAL (any fail = hard reject regardless of score). |
| `verify.html.py` | Python script that grep-checks the 25 gates and prints score / 100. Exits with code 2 on CRITICAL fail. |

---

## The 10 CRITICAL gates (any single fail = hard reject)

| # | Gate | Why CRITICAL |
|---|---|---|
| 1 | Single HTML file | Multiple files / a ZIP = task misinterpreted |
| 13 | Brand color present | Approximated color = brand violation. Get the real hex from press kit / IR / official SVG. |
| 16 | CSS/JS inlined | External `<link>` / `<script src>` = not self-contained |
| 19 | Light theme default | Dark without explicit request = Reference D violation |
| 20 | No meta-files in output | `QUICKSTART.md` / `INDEX.html` = toolkit-replication regression |
| 21 | Bilingual + language toggle | Monolingual output = Rule 17 violation, non-negotiable |
| 22 | Visual audit completed | No `_audit/REPORT.md` = Stage 8 was skipped, you never looked at your own output |

These 7 are the spine of the deliverable. The other 15 gates are signals of completeness and depth.

---

## Reference quality bar

The Turing company deck at https://tur.ing/company-deck/ is a publicly accessible reference build. Its source HTML measures approximately:

- 29 sections, ~10,850 lines, 446 KB
- 51 `<img>` references, 14 `<video>`, 40 `<svg>`
- 23 `translateX`, 27 `getBoundingClientRect`, 8 `getTotalLength`
- 42 `@keyframes`, 52 `animation:`, 34 `transition:`
- 30 `stroke-dashoffset`, 26 `requestAnimationFrame`, 8 `MutationObserver`
- 19 occurrences of Turing Red `#9B1B30`
- Implemented EN/JP language toggle at top-right

These are the numbers a fully-realized output produces. The minimum thresholds in `QUALITY_GATES.md` are much lower (the floor below which output is rejected), but a deliverable that scores `1` where the reference scores `23` is almost certainly missing a major capability.

---

## Generic for any company

This Skill is **company-agnostic**. It works for Turing, Acme, and any other company. There are no hardcoded brand colors, fonts, names, or photos in the prompt or scripts. Every brand asset is discovered at Stage 1 (`ASSET_RESEARCH.md`) and applied at Stage 6. The `--brand-color` flag in `verify.html.py` is supplied per-conversion, not baked in.

If you find yourself adding company-specific code paths, stop — that is a Skill-modification anti-pattern. Treat every conversion as if the company name was provided fresh.
