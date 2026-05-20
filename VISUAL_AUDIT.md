# VISUAL_AUDIT — mandatory self-visual-audit before delivery

This document defines the **HARD GATE** that prevents "ビルド成功 = 完成" (build-passes-equals-done). After generating `index.html`, the AI must render every page to PNG, **read every PNG back**, identify defects, fix them, and loop until clean.

## Why this exists

Common defects that escape text-only review but become obvious as soon as you look at the rendered page:
- Background image had so much text on it that the foreground text was illegible
- Photo cropped above the face (showed only forehead and ceiling)
- Count-up animation never triggered (initial value stuck)
- Logo cropped at edge / displayed inside a black "sticker" box
- Two adjacent sections used identical fade-up (Rule 15 violation invisible until viewed)
- Margin imbalance (text crammed on left, empty 40% on right)
- Bilingual toggle button collided with page counter
- Sub-reel arrow disappeared at certain viewport widths

Every one of these is invisible to text-only AI reasoning. They become visible only when the AI **looks at the rendered output**.

## The 4-step audit ritual

### Step 1 — Render every section to PNG

Use Playwright (or Puppeteer) headless to capture each section. Required script (`_audit/render.js`):

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`file://${process.cwd()}/index.html`);

const sectionCount = await page.evaluate(() => document.querySelectorAll('section').length);

for (let i = 0; i < sectionCount; i++) {
  await page.evaluate(idx => window.goTo && window.goTo(idx), i);
  await page.waitForTimeout(1500);  // wait for entrance animation
  await page.screenshot({
    path: `_audit/page-${String(i+1).padStart(2,'0')}.png`,
    fullPage: false,
  });
}
await browser.close();
```

Run: `node _audit/render.js`. Output: `_audit/page-01.png` ... `_audit/page-NN.png`.

### Step 2 — Read every PNG back

This is the **non-negotiable** step. The AI MUST open every PNG with the Read tool (or equivalent multimodal viewing) and evaluate. **Sampling is forbidden** — read all N pages, even if N=49.

For each page, evaluate 8 axes:

| # | Axis | What to check |
|---|---|---|
| 1 | Text legibility | Is every visible text string readable? Contrast ≥ WCAG AA? No background-image-text-collision? |
| 2 | Margin balance | White space is evenly distributed? Not crammed left / empty right? |
| 3 | Alignment | Headings, body text, and chrome elements align to a consistent grid? |
| 4 | Image crop | Faces are centered, not cropped at forehead/chin? Logos not cut at edges? Photos not stretched? |
| 5 | Brand color usage | The official brand color appears as primary accent (not approximation)? |
| 6 | Typography rhythm | Display vs body vs mono fonts used per Reference D? No italic abuse? |
| 7 | Animation traces | Are entrance animations diverse (Rule 15)? Does count-up start from 0? Are SVG lines drawn cleanly (no stutter)? |
| 8 | Chrome integrity | Page counter / nav / language toggle don't overlap content? Logo size correct per context? |

### Step 3 — Build `_audit/REPORT.md`

For every defect found, log with severity:

```markdown
# Visual audit report — iteration N

## CRITICAL (must fix before delivery)
- page-09: 線描画アニメが途切れて見える (stroke-dashoffset 0 で開始してる、3-stage render してない)
- page-22: CEO 写真が額より上で切れてる (face center が Y=10% にあって 30-35% でない)
- page-31: 背景画像の文字が前景テキストと重なって読めない (背景に半透明オーバーレイ要追加)

## HIGH (strongly recommended fix)
- page-14: 余白が左 80% / 右 20% に偏ってる
- page-23: count-up が 0 から始まらず最終値ですぐ表示されてる

## MEDIUM
- page-05: 副題の Fraunces italic が浮いてる (Rule "no display italic")

## LOW
- page-37: パディングが他ページより 8px 多い (許容範囲だが統一推奨)

## Page-by-page check
- page-01 (Cover): ✅ clean
- page-02 (Mission): ✅ clean
- page-03 (Tokyo30): ⚠️ MEDIUM (見出しが日本語段落の途中で改行)
- ...
- page-49 (Finale): ✅ clean
```

### Step 4 — Fix and loop

For every CRITICAL and HIGH defect:
1. Modify `index.html` to fix the cause (not the symptom)
2. Re-run Step 1 (re-render)
3. Re-run Step 2 (re-audit)
4. Update `_audit/REPORT.md` (iteration N+1)

Continue until **zero CRITICAL and zero HIGH defects remain**.

MEDIUM and LOW defects can be noted in the final report but do not block delivery.

---

## Minimum iteration count

For typical 20-50 page decks: **expect 2-4 audit iterations** before achieving zero CRITICAL/HIGH.

If you complete the audit in 1 iteration with zero defects, **suspect the audit itself**. Either you didn't read all pages, or you applied an overly lax standard. Re-read 3 random pages with stricter standards before declaring complete.

---

## The hand-off package includes the audit

When delivering the final HTML, the bundle is:

```
output/
  index.html              # the deliverable
  assets/                 # images, logos
  _audit/
    page-01.png ... page-NN.png   # rendered captures
    REPORT.md             # audit history (iterations 1..N)
    render.js             # the script used
  _measurements/          # pixel measurement JSONs (from Stage 5)
```

The user can re-run the audit themselves: `node _audit/render.js` then visually compare.

---

## Why the AI is in charge of this, not the user

If the AI hands HTML to the user and the user finds the defects, the protocol has failed. This is wrong because:
- The user is not paid to be the QA of an AI-generated artifact
- Defect discovery delay grows the more the user has to bounce back

In the correct workflow, the AI is its own QA. The user only sees the final result with zero CRITICAL defects. The AI's job is not "produce HTML"; it is "produce HTML that, when I look at it, I would deliver to my own boss with pride".

If the AI cannot self-assess at this level, the React pipeline (`REACT_PIPELINE.md`) may be more appropriate — its visual fidelity is generally easier to control programmatically.
