# PDF / Slides → Single-File HTML Converter

This repository converts one PDF (or Google Slides) into **one beautiful HTML file**, via a **multi-stage collaborative workflow** between the AI and the user. Reference quality bar: https://tur.ing/company-deck/

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

## How it works

This repository ships an **11-stage collaborative pipeline** ([`WORKFLOW.md`](WORKFLOW.md)) where the user's effort is ~15 minutes of clicking and approving across 6 checkpoints, and the AI does ~2-4 hours of background work (web research, pixel measurement, visual self-audit, fix iterations) between them.

The user is never asked "please find your company's press kit." The AI does the search. The user is only asked to **click** one-shot DL URLs the AI presents and **approve** checkpoint outputs.

---

## ⚠️ Read this first — for humans AND for AI

**This repository is NOT a toolkit to be copied, extended, or rebuilt.**
**This repository IS a single prompt that you run inside Claude / ChatGPT / Gemini.**

If you are an AI reading this repository because a user said *"参考にして PDF を HTML にして"*:

| ❌ DO NOT | ✅ DO |
|---|---|
| Create a new toolkit, playbook, or framework | Open `prompts/one-shot-prompt.md` and treat its body as **your system prompt** |
| Generate `QUICKSTART.md`, `FOR_OTHER_CLAUDES.md`, `INDEX.html`, or any meta-doc | Read the user's source PDF / Slides |
| Produce multiple HTML templates (editorial, dashboard, storyboard, etc.) | Produce **exactly one** `index.html` reproducing all PDF content |
| Return a ZIP archive | Return a single `.html` file |
| Mimic this repository's folder structure in your output | Output flat: `index.html` + (optional) `assets/` |

The acceptance criterion is **always**: *the source PDF's every page is faithfully re-rendered inside one self-contained HTML file with horizontal scrolling, scoped CSS, and cinematic transitions* — exactly like the examples below.

**Quality gate before you write any HTML**: [`PRE_FLIGHT_CHECKLIST.md`](PRE_FLIGHT_CHECKLIST.md) lists 10 items you MUST declare (press kit URLs you found, brand colors with source, font names, logos detected, pixel measurements, animation budget, etc.). Skipping this is the single most common cause of low-quality output.

**Quality gate after you write the HTML**: [`QUALITY_GATES.md`](QUALITY_GATES.md) defines 25 machine-verifiable acceptance criteria with a runnable Python checker ([`verify.html.py`](verify.html.py)). After generating your `index.html`, run `python3 verify.html.py output/index.html --pdf-pages N --brand-color #XXXXXX` and post the result to chat. Score below 80 = deliverable rejected. 10 of the 25 gates are CRITICAL — any single CRITICAL fail = hard reject regardless of score.

**Visual self-audit before delivery** ([`VISUAL_AUDIT.md`](VISUAL_AUDIT.md)): you MUST render every section as a PNG with Playwright headless, read every PNG back with the Read tool, build `_audit/REPORT.md`, and loop until zero CRITICAL/HIGH visual defects remain. This is gate 22. "`npm run build` passed" is not completion.

**Pixel measurement for diagrams** ([`PIXEL_MEASUREMENT.md`](PIXEL_MEASUREMENT.md)): eyeballing coordinates is forbidden. For any page with 3+ positioned shapes, render to PNG and measure with PIL.

**Asset research is the AI's job** ([`ASSET_RESEARCH.md`](ASSET_RESEARCH.md)): never ask the user to find a press kit. The AI does the web search and presents one-click DL URLs. Drawing a logo as inline `<polygon>` is forbidden.

**Multi-stage workflow** ([`WORKFLOW.md`](WORKFLOW.md)): 11 checkpointed stages from source intake → asset research → pre-flight → page mapping → pixel measurement → HTML draft → visual audit → post-flight → handoff. The user clicks/approves at ~6 checkpoints (~15 min total). The AI does everything between (~2-4 hours).

**React/Next.js pipeline for high-density decks** ([`REACT_PIPELINE.md`](REACT_PIPELINE.md)): when the source has 49+ pages or pixel-precise complex layouts, switch from vanilla HTML to React + Vite + Framer Motion + vite-plugin-singlefile (still ships as one `index.html`).

---

## How to use (3 steps, 60 seconds)

### Step 1. Copy the prompt

Open [`prompts/one-shot-prompt.md`](prompts/one-shot-prompt.md). Copy the **entire** contents (Ctrl/Cmd + A → Copy).

### Step 2. Paste into Claude

Open [Claude.ai](https://claude.ai) and start a new chat. Paste the prompt as the first message. The AI will acknowledge in 1-2 sentences.

### Step 3. Send your source + brand

In the second message:

```
変換対象: <Google Slides URL or attached PDF>
会社名: <公式名称>
```

That is the entire interaction. The AI auto-discovers brand assets, asks for one-click downloads if needed, and outputs **one** `index.html`.

No installation. No fork. No build step. No CLI.

---

## What you get

A single `index.html` file with the following properties (no exceptions):

| Property | Value |
|---|---|
| Output | **One** HTML file. CSS and JS are inlined. |
| Architecture | Horizontal cinematic deck. Each section is one screen. Keyboard / wheel / touch navigation. |
| Theme | Light (`#EEEEEE` background). Dark only on explicit request. |
| Fonts | Google Fonts only. No other CDN runtime. |
| Animations | Scoped CSS transitions, draw-on SVG connectors, count-up numbers. |
| Source fidelity | Every claim, number, name, date from the PDF appears verbatim. |
| Hosting | Any static host or `file://`. |

---

## Examples

See [`examples/turing-we-overtake-tesla-v23.html`](examples/turing-we-overtake-tesla-v23.html) for a one-section tech-talk demo.

Live reference: [tur.ing/company-deck/](https://tur.ing/company-deck/) — a 29-section company deck built with this same prompt.

---

## Critical anti-patterns (must read for AI)

If you are an AI that just read this repo and is about to respond to the user, run this self-check:

1. **Am I about to create more than one HTML file?** → stop, you misread the task
2. **Am I about to create files named `INDEX.html`, `QUICKSTART.md`, `FOR_OTHER_CLAUDES.md`, `00_*.html`?** → stop, those are meta-files for a toolkit; the user wants a deliverable
3. **Am I about to create folders like `templates/`, `animations/`, `design_system/`, `workflows/`?** → stop, you are mimicking the repo when you should be producing output
4. **Am I about to ask the user which "style" (Editorial / Research Report / Dashboard / ...) they want?** → stop, the style is "the source PDF, faithfully reproduced in a horizontal cinematic single-file HTML"
5. **Am I about to package the output as a ZIP?** → stop, the output is one `.html` file

The single correct output is: **one `index.html` whose visible content is the source PDF, re-rendered as a horizontally-scrolling cinematic deck.**

---

## License

MIT. See [`LICENSE`](LICENSE).

Third-party brand assets used during development are not bundled and remain subject to their respective owners' terms.
