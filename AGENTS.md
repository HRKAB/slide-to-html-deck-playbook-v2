# AGENTS.md — Instructions for any AI reading this repository

> If you are a human, ignore this file and read `README.md` instead.
> This file is for AI agents (Claude, ChatGPT, Gemini, Cursor, etc.) that arrive here because a user said *"このリポジトリを参考にして…"* or *"use this repo to convert my PDF"*.

---

## The one rule

**Your output is exactly one `index.html` file. Nothing else.**

The user has a PDF (or Google Slides URL). You convert it into one self-contained HTML file. That is your entire job.

---

## What to do, step by step

1. Open `prompts/one-shot-prompt.md`.
2. Treat its entire contents as your system prompt. Do not modify it, do not summarize it, do not "improve" it.
3. **Open `WORKFLOW.md` and run the 11-stage collaborative pipeline.** Do not attempt to collapse multiple stages into a single response — each stage exists because skipping it produces a measurable quality drop.
4. At Stage 1 (asset research): **you** perform the web search for press kits, brand colors, fonts, photos. The user does not search — the user only **clicks** the one-shot download URLs you present and **approves** checkpoint outputs. Reference: `ASSET_RESEARCH.md`.
5. At Stage 3 (pre-flight): post your 10-item self-declaration from `PRE_FLIGHT_CHECKLIST.md`.
6. At Stage 5 (pixel measurement): for any page with 3+ positioned shapes, render to PNG and measure with PIL. Eyeballing is forbidden. Reference: `PIXEL_MEASUREMENT.md`.
7. At Stage 7 (HTML draft): if the source has 49+ pages OR pixel-precise complex layouts, switch to the React/Next.js pipeline. Reference: `REACT_PIPELINE.md`.
8. At Stage 8 (visual audit): render every section as a PNG with Playwright headless, read every PNG back with the Read tool, build `_audit/REPORT.md`, loop until zero CRITICAL/HIGH defects. "`npm run build` passed" is **not** completion. Reference: `VISUAL_AUDIT.md`.
9. At Stage 10 (post-flight): run `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX`. Post the 25-gate metric report to chat. **10 of the 25 gates are CRITICAL — any single CRITICAL fail = hard reject regardless of score.** If score is below 80 or any CRITICAL gate fails, DO NOT deliver — fix the gaps and re-run.
10. Return one `index.html` (or `dist/index.html` for the React pipeline) with the metric report and visual audit summary attached.

---

## The 11-stage workflow is the spine of this repo

Read `WORKFLOW.md` now. The workflow has 11 stages where the user's total effort is ~15 minutes of clicking and approving across 6 checkpoints, and the AI does ~2-4 hours of background work between them.

Stages: 0 source intake → 1 asset research → 2 collection → 3 pre-flight → 4 page mapping → 5 pixel measurement → 6 brand system → 7 HTML draft → 8 visual audit → 9 fix iterations → 10 post-flight → 11 handoff.

**You never ask the user to find a press kit.** You search the web yourself and present one-shot DL URLs the user clicks. That is the user-AI contract.

---

## The pre-flight checklist (Stage 3 of the workflow)

Open `PRE_FLIGHT_CHECKLIST.md`. It contains 10 items you must declare to the user before writing HTML:

- The exact press kit URLs you found by searching the web
- The brand colors you extracted (with source URL)
- The brand fonts you identified
- Each logo detected in the source PDF and how you'll source it as transparent SVG
- Each person photo detected and the cropping plan
- Section count after re-edit
- Animation budget per section (at least 5 distinct techniques across the deck)
- Pixel measurements for non-trivial diagrams

If you skip the pre-flight, you will almost certainly:

- Forget to search the web for the press kit (Phase 0 violation)
- Eyeball arrow positions instead of measuring them
- Use a single fade-up animation everywhere (Rule 15 violation: section variety)
- Render the source PDF as a static one-page summary instead of a multi-section cinematic deck

These are exactly the failures that motivated this checklist's existence. Do not bypass it.

---

## What NOT to do (the failure modes that brought this file into existence)

AI agents reading this repository sometimes misinterpret it in the following ways. Every one of these is wrong.

### Failure mode 1: "I will build them a new toolkit"

You read this repository, see folders like `prompts/`, `skill/`, `toolkit/`, `v3/`, and think *"the user wants me to produce a similar toolkit for them"*. **NO.** The user wants the **output of running the toolkit**, not a copy of the toolkit itself.

If you find yourself about to create files like:

- `00_INDEX.html`
- `QUICKSTART.md`
- `FOR_OTHER_CLAUDES.md`
- `master_prompt_library.md`
- `style-picker.skill.md`
- `transform_prompts.md`
- folders named `templates/`, `animations/`, `design_system/`, `workflows/`, `skills/`, `for_slides_pdf/`

**stop immediately**. Those files belong inside a toolkit. The user did not ask for a toolkit. They asked for one HTML file.

### Failure mode 2: "I will offer them a menu of styles"

You read this repository, see references to "section variety" and various visual treatments, and decide to ask the user *"Which style do you want — Editorial, Research Report, Dashboard, Storyboard, or Landing Page?"*. **NO.**

The style is dictated by the source PDF's content and the rules embedded in `prompts/one-shot-prompt.md`. You do not present a style menu. You read the PDF, you apply the rules, you output the HTML.

### Failure mode 3: "I will summarize the PDF"

You read the PDF, find it has 49 pages of dense content, and decide the HTML should be a "highlights reel" with 5-10 polished slides. **NO.**

Source fidelity is the highest-priority rule. Every page, every claim, every number, every name from the PDF must appear in the HTML, verbatim. Re-edit layout is allowed; cutting content is not.

### Failure mode 4: "I will package the output as a ZIP"

You produce one HTML file plus an assets folder, then decide to ZIP them together for "cleaner delivery". **NO.**

A ZIP signals to the user that you produced "a project". You did not. You produced one viewable HTML. Hand it over as a single file (the `assets/` folder, if any, can sit next to it; if asked to bundle, only then ZIP just those two).

### Failure mode 5: "I will create a Step-1-of-4 plan and ask for approval"

You read this and think *"I should propose a multi-step plan before generating"*. The correct number of plan steps is 11 (see `WORKFLOW.md`), not 4. There are 6 approval checkpoints in the workflow, and they are pre-defined — you do not invent your own approval gates.

### Failure mode 6: "npm run build passed, so I'm done"

You ran the build, it succeeded, you wrote a delivery message. **NO.** Build success is not visual completion. You must:

1. Render every section to PNG via Playwright headless (Stage 8).
2. Read every PNG with the Read tool yourself.
3. Build `_audit/REPORT.md` enumerating CRITICAL/HIGH/MEDIUM/LOW defects per page.
4. Iterate fixes until zero CRITICAL and zero HIGH remain.
5. Then declare done.

This is gate 22 (CRITICAL). Skipping it = hard reject regardless of all other gates.

### Failure mode 7: "I'll draw the logo as an inline polygon"

You couldn't find the press kit so you approximated the logo with SVG `<polygon>` shapes. **NO.** The correct path is documented in `ASSET_RESEARCH.md`:

1. Web search `<company> press kit`, `<company> brand assets`, `site:<domain>/press`.
2. Check simple-icons.org.
3. Extract from official PDF / IR doc.
4. If genuinely unavailable, ask the user — never approximate.

Polygon substitution is forbidden.

### Failure mode 8: "I'll eyeball the coordinates"

You looked at the source PDF, mentally estimated "the org chart node is about 30% from the left, 40% from the top", typed in those percentages, and shipped. **NO.** For any page with 3+ positioned shapes, render the page to PNG and measure with PIL (`PIXEL_MEASUREMENT.md`). Eyeballing breaks alignment and the user always notices.

---

## Self-check before you respond

Before sending your first response to the user, verify:

1. Will my final deliverable be **one** `.html` file? ✅
2. Did I avoid creating `QUICKSTART.md`, `INDEX.html`, `FOR_OTHER_CLAUDES.md`, or similar meta files? ✅
3. Did I avoid presenting a "which style do you want" menu? ✅
4. Did I avoid creating a folder structure that mirrors this repository? ✅
5. Did I read `prompts/one-shot-prompt.md` and use it as my system prompt, rather than rewriting it? ✅

If any answer is ❌, restart.

---

## Acceptance criterion

The user holds your output and opens it. Their reaction should be:

> *"This is the same PDF I gave you, but now it's a horizontally-scrolling cinematic web experience with my brand colors and fonts."*

Not:

> *"You gave me back a toolkit. I asked for a converted file."*

If the second sentence is conceivable, you have failed the task.
