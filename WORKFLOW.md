# WORKFLOW — multi-stage collaborative pipeline

This document defines the **multi-stage workflow** for converting one PDF / Google Slides into one beautiful single-file HTML deck. The pipeline is **collaborative and checkpoint-driven** — the AI and the user work together at each stage.

## Why this is multi-stage

Asking an AI to convert a PDF in one pass is unreliable. Without explicit checkpoints, the AI silently skips: web research for press kits, pixel measurement of diagrams, visual self-audit, and re-iterations after spotting layout defects. These skips don't show up in chat output — they show up only when a human opens the final HTML and notices the problems.

This pipeline introduces **hard checkpoints** the AI cannot skip. At each checkpoint, the AI either has the user's explicit OK or stops and asks for it. The result: a single HTML at the quality bar of <https://tur.ing/company-deck/>.

## Design principle: minimum user effort × maximum collaborative quality

| The user does | The AI does |
|---|---|
| Provide source PDF + company name | Everything else researchable |
| Click one-shot download URLs the AI presents | Search the web, find press kits, propose DL URLs |
| Approve or correct page-mapping / pre-flight / pixel-measurement results | Generate the table, the pre-flight, the measurements |
| Review the visual audit report after self-audit | Render headless screenshots, read every page back, list defects |
| Receive the final HTML + metric report | Run verify.html.py, fix critical fails, loop until pass |

The user is **never** asked "please find a press kit for me" or "please tell me what color this is" — those are the AI's job. The user is only asked to **click** or **approve**.

---

## The 11-stage workflow

### Stage 0 — Source intake
**AI side**: Receive source (PDF attachment or Google Slides URL) + company legal name. Acknowledge file size, page count, and confirm domain (`<company>.com` / `tur.ing` / etc.) for company identity verification (Rule 16).

**User side**: Provide source. Nothing else required.

**Checkpoint output**:
```
Source confirmed:
  - File: <filename>.pdf (<size> MB, <N> pages)
  - Company: <Legal Entity Name>
  - Verified domain: <https://...>
  - Brand language guess (to be confirmed at Stage 4): <ja / en / both>
```

---

### Stage 1 — Asset research (web)
**AI side**: Execute web research for the company's brand assets. See `ASSET_RESEARCH.md` for the 5-category MECE search protocol (corporate logo / product logos / brand colors / fonts / people photos).

For each asset found, provide a **one-click download URL**. For each asset NOT found, declare it as a fallback (simple-icons / Wikimedia / PDF crop).

**User side**: Nothing yet — wait for the AI's research report.

**Checkpoint output**:
```
Asset research complete. Here is what I found:

[Category 1 — Corporate logo SVG]
- Found: <URL>  ← click to download
- Variants: color / white / black

[Category 2 — Product logos]
- Found 13 product logos at <URL>  ← click ZIP DL

[Category 3 — Brand colors (with source URLs)]
- Primary: #XXXXXX  (source: <press kit URL>)
- Secondary: #YYYYYY  (source: <IR PDF page X>)

[Category 4 — Fonts]
- Display: Inter Tight  (Google Fonts: <URL>)
- Body: Noto Sans JP   (Google Fonts: <URL>)

[Category 5 — People photos]
- Found 3 executive headshots in press kit  ← click to DL
- 5 employee voice photos: not publicly available, will fallback to face-detected crops from source PDF page <N>

Please click each download link, attach the files to this chat, and reply "OK" or "all attached".
```

---

### Stage 2 — Asset collection checkpoint
**AI side**: When user attaches files, confirm each file received, verify integrity (file size, SVG cls-1 background rect check, dimensions). For SVG logos, **strip the `cls-1` background rect** and save as `-transparent.svg`. List the final asset inventory.

**User side**: Attach the files the AI listed. Reply when done.

**Checkpoint output**:
```
Asset inventory confirmed:
  ✅ logos/corporate-color-transparent.svg (12 KB, 220×64)
  ✅ logos/corporate-white-transparent.svg (12 KB)
  ✅ photos/ceo-portrait.jpg (1.2 MB, 800×800, face detected at center 35% Y)
  ⚠️  product-logo-7 not received — will fallback to simple-icons npm

Ready to proceed to Stage 3 (pre-flight).
```

---

### Stage 3 — Pre-flight self-declaration
**AI side**: Post the 10-item self-declaration from `PRE_FLIGHT_CHECKLIST.md`. Every item filled with concrete values (no "TBD"). Wait for user OK.

**User side**: Read the pre-flight. Reply "承認" / "OK" / or specific correction.

---

### Stage 4 — Page mapping table (HARD GATE)
**AI side**: Read every page of the source PDF. Build the table: `<slide N → HTML section M with variant V and note>`. Note: re-edits (promote / demote / merge / cut / sub-reel) are documented per row.

**User side**: Review the page mapping. This is the **last gate** before HTML generation. Approve or request changes.

---

### Stage 5 — Pixel measurement
**AI side**: For every page with **3+ positioned shapes** (org charts, architecture diagrams, timelines, multi-column layouts), execute `PIXEL_MEASUREMENT.md`: render the source page to a high-DPI PNG, use PIL to measure node bounding boxes, build the coordinate table, build the arrow census table (if directed graph). Save to `_measurements/page-NN.json`.

**Anti-pattern this prevents**: AI eyeballs node positions and writes "approximately right" coordinates. Measurement is non-negotiable.

**User side**: Nothing.

**Checkpoint output**:
```
Pixel measurements complete:
  - page-09 E2E diagram: 5 nodes measured to ±2 px, 10-arrow census compiled
  - page-22 org chart: 25 nodes, 24 lines
  - ...
```

---

### Stage 6 — Brand system setup
**AI side**: Generate `tokens.css` from the brand colors / fonts gathered in Stage 1. CSS variables (`--brand-primary`, `--font-display`, etc.). Strip print-only background rects from all logo SVGs.

---

### Stage 7 — HTML draft (scaffold + sections)
**AI side**: Start with the embedded scaffold from `one-shot-prompt.md` verbatim. Insert `<section>` per the Stage 4 page-mapping table. Apply per-section CSS (scoped). Apply animations from Reference F. Implement dynamic SVG connectors via `getBoundingClientRect`.

**Hard requirement (gate 23)**: Section entrance animations across the deck must use **at least 3 distinct transform axes** (e.g., `translateY` for one section, `scale` for another, `perspective` rotation for a third). A deck where every section enters with the same `translateY` slide-up is a single-axis carousel — gate 23 fails and the build is rejected. Two consecutive sections may NOT share the same primary entrance axis.

**Hard requirement (gate 24 — Section pacing)**: The page-to-page transition itself must be a cross-fade with `transition: opacity 0.6–1.2s cubic-bezier(...)`. Recommended: `transition: opacity 0.7s cubic-bezier(0.65, 0, 0.35, 1)`. Plain `ease` keyword or `<= 0.4s` duration = snap feel = build rejected. See `prompts/one-shot-prompt.md` Inline Reference M for the exact CSS / JS templates.

**Hard requirement (gate 25 — Content reveal stagger)**: Inside each section, content elements (text / images / cards / SVGs) must use a `.reveal` class with cinematic easing (`cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.22, 1, 0.36, 1)`) and a stagger cascade (`d1` = 0.16s, `d2` = 0.30s, `d3` = 0.44s, ...). All content appearing at the same instant = static feel = build rejected. The reset-on-revisit pattern in `goTo()` is also required so the entrance replays every time.

**Default mode**: Vanilla single-file HTML.

**React mode**: For 49+ pages OR pixel-precise reproduction of complex layouts (org charts with 20+ nodes, architecture diagrams with 10+ arrows), switch to the React pipeline. See `REACT_PIPELINE.md`.

---

### Stage 8 — Self visual audit (HARD GATE)
**AI side**: Execute `VISUAL_AUDIT.md`. The summary:

1. Run `playwright` headless to capture every section as a `_audit/page-NN.png` at viewport 1920×1080.
2. **Read each PNG back** (yes, every single one — no sampling) and assess: visibility / margin / alignment / animation timing / brand color usage / typography rhythm / image crop / text legibility.
3. Build a `_audit/REPORT.md` listing every defect per page with severity (CRITICAL / HIGH / MEDIUM / LOW).
4. If any CRITICAL or HIGH defect exists, **return to Stage 7 and fix**, then re-run Stage 8.

This is the gate that catches: "background image has too much text so text on top is illegible", "section 22 photo cropped above the face", "count-up doesn't trigger", "logo too small on cover".

**User side**: Nothing during the audit. But the audit `REPORT.md` will be shown to the user for transparency.

---

### Stage 9 — Fix iterations
**AI side**: Apply fixes for each defect. Re-run Stage 8. Loop until zero CRITICAL/HIGH defects remain.

**User side**: Nothing unless asked for a judgment call ("which of these 2 layout variations do you prefer?").

---

### Stage 10 — Post-flight (verify.html.py)
**AI side**: Run `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX`. Post the 25-gate metric report. If any CRITICAL gate fails OR score < 80, return to Stage 7. **The brand color you declared in Stage 1 / Stage 3 MUST appear in the final HTML's CSS** (gate 13).

---

### Stage 11 — Handoff
**AI side**: Deliver the final `index.html` (+ optional `assets/`, `_audit/REPORT.md`, `_measurements/`). Provide a 1-paragraph summary: "Score: XX/100, all CRITICAL gates passed, X visual audit iterations performed, all assets sourced from official channels."

**User side**: Open the HTML in a browser. The acceptance criterion: *"This is the same PDF I gave you, now as a horizontal cinematic web experience with my brand colors and fonts."*

---

## The collaborative ratio

| Stage | User minutes | AI minutes |
|---|---|---|
| 0 | 1 min (send source) | 1 min |
| 1 | 0 | 15-30 min (web research) |
| 2 | 3-5 min (click + attach) | 2 min (verify) |
| 3 | 2 min (read + approve) | 5 min (write pre-flight) |
| 4 | 5 min (review table) | 10 min (build table) |
| 5 | 0 | 10-20 min (PIL measurement) |
| 6 | 0 | 5 min |
| 7 | 0 | 30-60 min (HTML generation) |
| 8 | 0 | 15-30 min (audit) |
| 9 | 0-5 min (judgment calls) | 30-90 min (fix iterations) |
| 10 | 1 min (review report) | 5 min |
| 11 | 0 | 2 min |
| **Total** | **12-20 min** | **2-4 hours** |

User effort: ~15 minutes spread across 11 checkpoints. AI effort: 2-4 hours of background work.

This is the "minimum user effort × maximum collaborative quality" principle in numbers.
