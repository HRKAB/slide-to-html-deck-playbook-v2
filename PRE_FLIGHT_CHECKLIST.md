# PRE-FLIGHT CHECKLIST — what an AI must declare before writing HTML

If you are an AI agent executing a PDF → HTML conversion task using this repository's `prompts/one-shot-prompt.md`, you must **post the following self-declaration in chat BEFORE you start writing any HTML.**

This is non-optional. If you skip it, your deliverable is automatically failed.

---

## The 10 items you must declare before writing HTML

Post these as a numbered list in your reply, with concrete values filled in. Do not write "TBD". If you don't know, **go find out** (search the web, ask the user with one-click DL links, or measure from the source PDF).

```
## Pre-flight self-declaration

1. Source PDF / Slides URL: <exact URL or filename>
2. Company legal entity (verified via domain): <name> ← cross-checked with <URL>
3. Brand color hex codes discovered: <#XXXXXX, #YYYYYY, ...>
   Source: <exact press kit URL / IR PDF URL / official About-page URL>
   ⚠️ This must be a CONCRETE URL you actually visited. "I will search later" /
   "guessed from logo" / "approximate hex" are NOT acceptable. If no public
   source publishes the hex, extract it from the company's official logo SVG
   (open the SVG, read the `fill=` attribute of the largest path). Report
   the file path and the line number.
   The hex you report here MUST appear in your final HTML's CSS verbatim.
   `verify.html.py --brand-color <hex>` will check this and HARD-REJECT
   the deliverable if the count is 0.
4. Brand font families discovered: <font names + Google Fonts URLs>
5. Press kit URL (or "not publicly available, fallback plan below"):
   - <URL 1>
   - <URL 2>
6. Logos detected in source PDF (and how I will source each as transparent SVG):
   - <Logo A> → <official SVG URL>
   - <Logo B> → <simple-icons npm package: simple-icons/foo>
   - <Logo C> → <fallback: PDF crop, transparent rect stripped>
7. Person photos detected in source PDF (and how I will crop each):
   - <Page N, person X> → face-detected crop at face-center 30-35% Y
8. Section count after re-edit: <N sections>; sub-reels: <M>
9. Animation budget — **MULTI-AXIS REQUIRED (Rule 15 + gate 23)**. Each section's entrance must be planned, and the union must cover ≥ 3 transform axes (translateY / translateX / scale / rotate / perspective / Ken-Burns / letter-stagger). Single-axis = 紙芝居:
   - Section 1: <ken-burns background>     ← axis: scale + translate (Ken-Burns)
   - Section 2: <count-up numbers + scale-in>  ← axis: scale
   - Section 3: <draw-on SVG connector lines>  ← axis: SVG stroke-dashoffset (not a transform axis but counts as variety)
   - Section 4: <vertical reveal>          ← axis: translateY
   - Section 5: <perspective tilt finale>  ← axis: perspective + rotate
   - ... at least 5 distinct techniques AND at least 3 distinct transform axes across the deck
   - **Self-check:** if Section N and Section N+1 use the same transform axis, change one of them
10. Pixel measurements I have taken from source PDF (for non-trivial diagrams):
    - <Page X, Diagram Y>: nodes measured at (x1, y1), (x2, y2), ... ; arrow census table compiled
11. **Bilingual (JP/EN) implementation plan — MANDATORY (Rule 17):**
    - Text storage model: <data-lang spans / JS i18n object / {ja, en} pairs>
    - Language toggle button: <will be placed top-right, label "EN/JP">
    - Default active language: <ja (unless user explicitly requested en first)>
    - Translation source for English text: <user-provided / source PDF (if bilingual) / auto-generated then user-review>
```

If any of items 3, 4, 5, 6, 7, 8, 9, 10 says "skipped" or "default" without justification, the deliverable will not meet the quality bar that this repository is documenting. The reference quality bar is https://tur.ing/company-deck/.

---

## Hard rules that this checklist enforces

These are the rules from `prompts/one-shot-prompt.md` that are most often skipped. The checklist exists because AI agents read the prompt, agree intellectually, then forget to actually execute these steps.

### Phase 0 — Auto Asset Discovery (NEVER SKIP)

Before requesting any file from the user, the AI must search the open web for:

- `<company name> プレスキット` / `<company name> press kit` / `<company name> brand assets`
- `<company name> ロゴ ダウンロード`
- `site:<company-domain>/press`, `site:<company-domain>/brand`
- `<company name> IR materials` (for brand colors and logos in PDFs)

The AI presents findings as a **numbered list of one-click download URLs**, never as "please find and provide". The user's job is to click each URL, save the file, and drop it into the chat.

If a press kit is not publicly available, the AI must declare a fallback plan using the three-tier strategy:

1. IR PDF / About page extraction
2. `simple-icons` npm package (for well-known tech logos) or Wikimedia Commons (CC/PD licensed)
3. PDF crop with background-rect stripped (3-line Python `lxml` snippet that drops `<rect class="cls-1">` before use — see `ASSET_RESEARCH.md` §3)

### Pixel measurement (NEVER EYEBALL)

For diagrams with 3+ nodes or any layout containing positioned shapes (org charts, architecture diagrams, timelines):

- Render the source PDF page to a raster with `pdftoppm` (PDF → PNG at 200-300 DPI)
- Use Python PIL to measure exact bounding boxes of each visible element
- Convert pixel coordinates to percentage-of-container values for CSS
- Compile an **arrow census table** (`#, from, to, direction`) before writing any SVG path code

Never set arrow coordinates to "approximately right" or "looks fine to me". The reference deck has nodes positioned within 2 px of the source.

### Animations (REQUIRED, NOT OPTIONAL)

A deck without animations is a static rendering, not a "beautiful HTML deck". The minimum animation budget per section:

- **Text reveal**: fade-up with stagger (`--d: 0.10s` / `0.20s` / `0.30s`)
- **Number sections**: count-up animation, initial value `0`, ease-out over 1.2-1.8s
- **Diagrams with lines**: `stroke-dasharray` / `stroke-dashoffset` draw-on, using **3-stage render (null / measured / ready)**, otherwise the line stutters
- **Photo sections**: subtle Ken Burns (slow scale 1.0 → 1.05 over 8-12s)
- **Hero / cover**: video background OR pure-opacity dissolve (no rotation, no overshoot, no glow particles)

If your final HTML has no animations or only one repeated technique throughout, the deliverable fails Rule 15 (section variety).

### Source fidelity (NEVER SUMMARIZE)

Every claim, number, name, date from the source PDF appears in the HTML, verbatim. If the source has 6 items, the HTML has 6. If a number is 272 億円, it is 272 億円. If a person is named 鈴木 太郎, it is 鈴木 太郎 — not "the CEO" or "the founder".

Layout re-editing (Web flow, ordering, sub-reels) is allowed. Content cutting / paraphrasing is not.

---

## What "passed the checklist" looks like

A real, completed pre-flight self-declaration for a Turing company deck conversion would read like:

```
1. Source: Company_Deck_260415_release_light.pdf (49 pages, attached)
2. Company: Turing Inc. (チューリング株式会社) ← https://tur.ing/, https://www.tur.ing/about/
3. Brand colors: #9B1B30 (primary), #EEEEEE (canvas), #111111 (ink)
   Source: Turing Design System (TDS) tokens.css — provided by user
4. Fonts: Montserrat (display), Noto Sans JP (body), JetBrains Mono (mono)
   Source: https://fonts.google.com/specimen/Montserrat etc.
5. Press kit: https://tur.ing/press (3 logo SVG variants, brand guide PDF)
6. Logos detected:
   - Turing corporate logo → press-kit SVG (transparent version generated, background rect stripped)
   - Partner logos on slide 23 (NVIDIA, JST, etc.) → simple-icons + Wikimedia Commons
7. Person photos: 10 leadership portraits on slides 28-31 → cropped via OpenCV haarcascade
   to face-center 30-35% Y position
8. Section count: 24 sections + 2 sub-reels (Engineers 9-sub, Team 10-sub) = 44 flat pages
9. Animation budget:
   - Cover: video background (cinema-bg.mp4)
   - Mission (3 sections): fade-up stagger with --d
   - Tokyo30: count-up numbers + ken-burns photo
   - Engineers sub-reel: horizontal photo-strip with cross-fade
   - Technology architecture: draw-on SVG connectors (3-stage render)
   - Team composition: pie chart with slice-stagger animation
   - Finale: pure opacity fade for WOT logo
10. Pixel measurements complete for:
    - p-09 E2E Architecture (5 nodes, 10 arrows) → arrow census compiled
    - p-22 Organization chart (board / L1 / L2 / teams) → 25 lines, anchor table compiled

Proceeding with HTML generation.
```

That is what a serious conversion run looks like. A pre-flight that says "I'll figure it out as I go" indicates the AI is about to skip the very steps that distinguish a beautiful deck from a generic one.
