# INSTRUCTIONS — operating manual for slide-to-html-converter

You are an AI agent that just received this Skill bundle. The user wants you to convert a PDF (or Google Slides URL) into one beautiful HTML deck. Read this file fully before responding.

---

## The one rule

**Your output is exactly one `index.html` file (plus an optional `assets/` folder and a mandatory `_audit/` folder). Nothing else.**

The user has a source deck. You convert it. You return one HTML file with proof that you visually audited it yourself. That is your entire job.

---

## What to do, step by step

The full pipeline lives in `WORKFLOW.md`. The summary:

| Stage | What you do | Hand-off to user |
|---|---|---|
| 0 | Acknowledge source, verify company identity by domain | (none) |
| 1 | Web search 5 categories (logo / product logos / colors / fonts / photos) per `ASSET_RESEARCH.md`. Present one-click DL URLs. | "Click these URLs and attach." |
| 2 | Strip `cls-1` background rect from SVGs. Confirm asset inventory. | "Ready to proceed?" |
| 3 | Post the 10-item self-declaration from `PRE_FLIGHT_CHECKLIST.md`. | "Approve?" |
| 4 | **HARD GATE** — Build the page-mapping table (slide N → HTML section M). | "Approve mapping?" |
| 5 | For any page with 3+ positioned shapes, run `PIXEL_MEASUREMENT.md` (PIL bbox + arrow census + face detection). | (none — internal) |
| 6 | Generate `tokens.css` from brand colors / fonts. | (none — internal) |
| 7 | Write `index.html`. Use vanilla single-file by default; switch to `REACT_PIPELINE.md` if 49+ pages or pixel-precise layouts. | (none — internal) |
| 8 | **HARD GATE** — Visual audit per `VISUAL_AUDIT.md`: Playwright render → Read every PNG → `_audit/REPORT.md` → loop until 0 CRITICAL/HIGH. | (audit report shared) |
| 9 | Apply fixes. Re-run Stage 8. | (judgment calls only) |
| 10 | Run `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX`. Post the 25-gate report. Score ≥ 80 + 10 CRITICAL gates passing required. | (metric report shared) |
| 11 | Deliver `index.html` + `_audit/` + `_measurements/`. | "Done. Score XX/100." |

User's total effort: ~15 minutes spread across 6 checkpoints (Stages 1, 2, 3, 4, 9, 11).
Your total effort: ~2-4 hours of background work.

---

## The 8 known failure modes (do NOT repeat them)

### Failure mode 1: "I will build them a new toolkit"

You read this Skill, see folders / templates / scripts inside, and decide *"the user wants me to produce a similar toolkit for them"*. **NO.** The user wants the **output of running the Skill**, not a copy of the Skill itself.

If you find yourself about to create files like `QUICKSTART.md`, `INDEX.html`, `FOR_OTHER_CLAUDES.md`, `master_prompt_library.md`, `style-picker.skill.md`, or folders named `templates/` / `animations/` / `design_system/` / `workflows/` / `skills/` — **stop immediately**.

### Failure mode 2: "I will offer them a menu of styles"

You decide to ask the user *"Which style do you want — Editorial / Research Report / Dashboard / Storyboard / Landing Page?"*. **NO.** The style is dictated by the source PDF's content and the rules in `one-shot-prompt.md`. You do not present a style menu. You read the PDF, apply the rules, output one HTML.

### Failure mode 3: "I will summarize the PDF"

You decide the HTML should be a "highlights reel" with 5-10 polished slides instead of the source's 49 pages. **NO.** Source fidelity is the highest-priority rule. Every page, every claim, every number, every name from the PDF must appear in the HTML, verbatim. Re-edit layout is allowed; cutting content is not.

### Failure mode 4: "I will package the output as a ZIP"

You produce one HTML file plus an assets folder, then decide to ZIP them together for "cleaner delivery". **NO.** A ZIP signals to the user that you produced "a project". You did not. You produced one viewable HTML. Hand over the raw file with computer:// links.

### Failure mode 5: "I will skip the slow steps"

You read the rules, understand them intellectually, then start writing HTML without:
- Searching the web for the company's press kit (Stage 1)
- Measuring node positions in pixels from the source raster (Stage 5)
- Implementing dynamic SVG with `getBoundingClientRect`
- Implementing count-up animations for numeric KPIs
- Sourcing brand colors from official IR / press materials

**NO.** The pre-flight (Stage 3) exists specifically to make these skips visible. The visual audit (Stage 8) catches what pre-flight missed. The post-flight (Stage 10) makes them score-penalize. If your post-flight score is below 80, or any CRITICAL gate fails, you skipped something.

### Failure mode 6: "npm run build passed, so I'm done"

You ran the build, it succeeded, you wrote a delivery message. **NO.** Build success is not visual completion. You must:

1. Render every section to PNG via Playwright headless (Stage 8 / `VISUAL_AUDIT.md`).
2. Read every PNG with the Read tool yourself.
3. Build `_audit/REPORT.md` enumerating CRITICAL / HIGH / MEDIUM / LOW defects per page.
4. Iterate fixes until zero CRITICAL and zero HIGH remain.
5. Then declare done.

This is gate 22 (CRITICAL). Skipping it = hard reject regardless of all other gates.

### Failure mode 7: "I'll draw the logo as an inline polygon"

You couldn't find the press kit so you approximated the logo with SVG `<polygon>` shapes. **NO.** The correct path is in `ASSET_RESEARCH.md`:

1. Web search `<company> press kit`, `<company> brand assets`, `site:<domain>/press`.
2. Check simple-icons.org.
3. Extract from official PDF / IR doc.
4. If genuinely unavailable, ask the user — never approximate.

Polygon substitution is forbidden. Brand colors guessed by eye are equally forbidden (this is gate 13, CRITICAL).

### Failure mode 8: "I'll eyeball the coordinates"

You looked at the source PDF, mentally estimated "the org chart node is about 30% from the left, 40% from the top", typed in those percentages, and shipped. **NO.** For any page with 3+ positioned shapes, render the page to PNG and measure with PIL (`PIXEL_MEASUREMENT.md`). Eyeballing breaks alignment and the user always notices.

---

## Self-check before you respond

Before sending your **first** response to the user, verify:

1. Will my final deliverable be **one** `.html` file (plus optional `assets/` and mandatory `_audit/`)? ✅
2. Did I avoid creating `QUICKSTART.md`, `INDEX.html`, `FOR_OTHER_CLAUDES.md`, or similar meta files? ✅
3. Did I avoid presenting a "which style do you want" menu? ✅
4. Did I avoid creating a folder structure that mirrors this Skill bundle? ✅
5. Am I about to execute Stage 1 (asset research) myself, instead of asking the user to find their own press kit? ✅
6. Did I plan to execute Stage 8 (visual audit) before delivery, not after the user spots defects? ✅

Before sending your **final** delivery message, verify:

7. Did I post the 10-item pre-flight self-declaration at Stage 3? ✅
8. Did I run `verify.html.py` at Stage 10 and post the 25-gate metric report? ✅
9. Is the post-flight score ≥ 80? ✅
10. Did all 10 CRITICAL gates pass (1, 13, 16, 19, 20, 21, 22, 23, 24, 25)? ✅
11. Did I produce `_audit/REPORT.md` with `CRITICAL: 0` and `HIGH: 0`? ✅
12. Did I produce `_audit/page-NN.png` for every section? ✅

If any answer is ❌, do not deliver. Fix and re-check.

---

## Acceptance criterion

The user holds your output and opens it. Their reaction should be:

> *"This is the same PDF I gave you, but now it's a horizontally-scrolling cinematic web experience with my brand colors and fonts, and the AI clearly audited every page itself before handing it over."*

Not:

> *"You gave me back a toolkit. I asked for a converted file."*

Or:

> *"You skipped the press kit search, used a guessed color, didn't add animations, and forgot to reference the PNG slides you extracted."*

Or (the modern failure mode):

> *"You said 'build succeeded', but page 22 has the CEO's photo cropped at the forehead, page 31's background text collides with the foreground, and the brand color in the HTML is `#2C70FF` even though the press kit says `#1A5EFF`."*

If any of those is conceivable, you have failed. Loop until you can deliver with the first quote.
