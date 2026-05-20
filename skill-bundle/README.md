# slide-to-html-converter (Skill bundle)

Convert one PDF or Google Slides deck into one beautiful single-file HTML deck via an 11-stage collaborative workflow. Reference quality bar: https://tur.ing/company-deck/

This is a **Skill bundle** — a self-contained directory you can attach to a Claude / ChatGPT / Gemini chat (or drop into a Skills directory) so the AI knows how to perform this conversion correctly.

---

## How it works

This Skill ships an **11-stage collaborative pipeline** (`WORKFLOW.md`) where the user's effort is ~15 minutes of clicking/approving across 6 checkpoints, and the AI does ~2-4 hours of background work (web research, pixel measurement, visual self-audit, fix iterations) between them.

The user is **never** asked "please find your company's press kit." The AI does the search and presents one-click DL URLs. The user only **clicks** and **approves**.

---

## Two ways to use

### ① Online (via GitHub URL)

Tell Claude:

> このリポジトリを参考にして PDF を美しい HTML にして: https://github.com/HRKAB/google-slides-to-html-deck-playbook

Claude reads the repository, treats `prompts/one-shot-prompt.md` as its system prompt, executes the 11-stage workflow, and verifies against the 25-gate checklist.

### ② Offline (via this Skill bundle ZIP)

Attach this ZIP (or the unzipped folder) to your chat. The AI reads `SKILL.md` first, then follows the same workflow.

The Skill bundle is **self-contained** — no internet access required to read the prompt or run the verification.

---

## Files in this bundle

| File | Purpose |
|---|---|
| `SKILL.md` | Skill manifest (read first) |
| `INSTRUCTIONS.md` | Operating manual with 8 known failure modes |
| `WORKFLOW.md` | 11-stage collaborative pipeline definition |
| `one-shot-prompt.md` | The actual prompt body — treat as system prompt |
| `ASSET_RESEARCH.md` | 5-category MECE search protocol (logo/colors/fonts/photos) |
| `PRE_FLIGHT_CHECKLIST.md` | 10-item self-declaration before writing HTML (Stage 3) |
| `PIXEL_MEASUREMENT.md` | PIL/OpenCV measurement protocol for any page with 3+ positioned shapes (Stage 5) |
| `VISUAL_AUDIT.md` | Mandatory Playwright render → Read PNG → loop ritual (Stage 8) |
| `REACT_PIPELINE.md` | When to switch from vanilla HTML to React + Vite + vite-plugin-singlefile |
| `QUALITY_GATES.md` | 25 machine-verifiable acceptance criteria (10 are CRITICAL) |
| `verify.html.py` | Python script: grep-checks the 25 gates, prints score |

---

## Quick test

After the AI generates `output/index.html`, run:

```bash
python3 verify.html.py output/index.html --pdf-pages 29 --brand-color "#1A5EFF"
```

The script reports each of 25 gates as PASS / FAIL plus a total score / 100. Below 80 = reject and re-run. Any single CRITICAL gate failure (1 / 13 / 16 / 19 / 20 / 21 / 22 / 23 / 24 / 25) = hard reject regardless of score; the script exits with code 2.

---

## What you should expect

The AI will:

1. **Stage 0-1** — Acknowledge your source and execute web research for your press kit / brand colors / fonts / photos. Present one-click download URLs.
2. **Stage 2** — Receive your attachments, verify integrity, strip background rects from SVG logos.
3. **Stage 3** — Post a 10-item pre-flight self-declaration (press kit URLs it found, colors with sources, fonts, logos detected, pixel measurement plan, animation budget, etc.). Wait for your OK.
4. **Stage 4** — Build the page-mapping table (slide → HTML section). HARD GATE — wait for your approval.
5. **Stage 5-7** — Measure pixel coordinates for complex pages, generate the brand token CSS, write the HTML draft (vanilla or React based on page count).
6. **Stage 8** — Render every section to PNG headlessly, read every PNG back, build `_audit/REPORT.md`, loop until zero CRITICAL/HIGH defects.
7. **Stage 9-10** — Apply fixes, run `verify.html.py`, post the 25-gate metric report. Score ≥ 80 + all 10 CRITICAL gates passing required.
8. **Stage 11** — Hand over `index.html` + `_audit/` + `_measurements/`.

The AI must NOT:

- Hand you back a "toolkit" or multiple HTML templates
- Ask "which style do you want — Editorial / Dashboard / ..."
- Ask you to find your own press kit
- Draw the logo as inline `<polygon>` because it couldn't find the SVG
- Eyeball node coordinates instead of measuring with PIL
- Declare "build succeeded" without running the visual audit
- Produce a deck that summarizes (rather than reproduces) your source
- Skip the bilingual EN/JP language toggle button (Rule 17 — CRITICAL gate 21)

---

## The 10 CRITICAL gates

Any single failure of these = hard reject regardless of overall score:

| # | Gate |
|---|---|
| 1 | Single HTML file (not a toolkit / not a ZIP) |
| 13 | Official brand color hex appears in the HTML (not an approximation) |
| 16 | CSS / JS inlined (no external `<link>` / `<script src>`) |
| 19 | Light theme default (`#EEEEEE` background) unless dark explicitly requested |
| 20 | No meta-files in output directory (`QUICKSTART.md` etc.) |
| 21 | Bilingual EN/JP with top-right language toggle button |
| 22 | Visual audit completed (`_audit/REPORT.md` + `_audit/page-*.png` + iteration history) |

---

## Generic for any company

This Skill is company-agnostic. It works for Turing, Acme, and any other company. There are no hardcoded brand colors, fonts, names, or photos in the prompt or scripts. Every brand asset is discovered fresh per conversion via `ASSET_RESEARCH.md`.

---

## License

MIT. Third-party brand assets used during development are not bundled and remain subject to their respective owners' terms.
