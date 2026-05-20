# PIXEL_MEASUREMENT — required for any non-trivial diagram

This document defines the **measurement** process that replaces "推測" (guess) with "実測" (measure). It is mandatory for: org charts (3+ nodes), architecture diagrams with arrows, timelines, multi-column layouts, and any page where elements are placed at specific coordinates rather than flowing in a single column.

## Why this exists

Common defects that result from eyeballing coordinates instead of measuring:
- Arrow tip hidden behind a box (refX / marker positioning eyeballed)
- Two nodes overlap because the AI estimated the y-coordinate
- Photo crop centered on chin instead of face (no face-detection used)
- Org chart lines pass through unrelated boxes
- Sub-reel arrow ends 30px before the target

The fix is **measurement, not retries**. One measurement run replaces 10 eyeball iterations.

## Tools required

- Python 3.10+
- `pillow` (PIL): `pip3 install pillow --break-system-packages`
- `pdftoppm` (poppler): `brew install poppler`
- `opencv-python` (for face detection): `pip3 install opencv-python --break-system-packages`

## The 4-step measurement protocol

### Step 1 — Render source page to high-DPI raster

```bash
pdftoppm -png -r 300 source.pdf _measurements/source -f <page-N> -l <page-N>
# produces _measurements/source-<page-N>.png at 300 DPI
```

### Step 2 — Measure bounding boxes

For each visible element, use PIL to find its bounding box. Example for a box-with-text element:

```python
from PIL import Image
import numpy as np

img = np.array(Image.open('_measurements/source-09.png'))
H, W = img.shape[:2]

# Detect text+box regions by finding contiguous dark pixels
# (simplified — use opencv contour detection for real cases)
nodes = {
    'camera':  {'cx': 240, 'cy': 380, 'w': 180, 'h': 80},   # measured visually with image viewer + ruler
    'infer':   {'cx': 720, 'cy': 380, 'w': 220, 'h': 80},
    'control': {'cx': 1200, 'cy': 380, 'w': 200, 'h': 80},
    'log':     {'cx': 1200, 'cy': 720, 'w': 200, 'h': 80},
}

# Convert pixel coords to percentage of container (for CSS)
for name, n in nodes.items():
    n['cx_pct'] = n['cx'] / W * 100
    n['cy_pct'] = n['cy'] / H * 100
    print(f"{name}: cx={n['cx_pct']:.1f}% cy={n['cy_pct']:.1f}%")
```

Save the result to `_measurements/page-09.json`.

### Step 3 — Build the arrow census table (for directed graphs)

For every arrow in the source, document:

```
| # | from    | to       | bowSign | note                          |
|---|---------|----------|---------|-------------------------------|
| 1 | camera  | infer    | +1      | straight bottom-to-bottom arc |
| 2 | infer   | control  | +1      |                               |
| 3 | infer   | log      | -1      | wraps around control box      |
| 4 | log     | infer    | +1      | return path                   |
```

This census is built from the source raster, NOT from the AI's intuition. Compile BEFORE writing any SVG path code.

### Step 4 — Face landmark detection for person photos

For every page containing a face:

```python
import cv2
img = cv2.imread('_measurements/source-22.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
for (x, y, w, h) in faces:
    face_center_y = y + h * 0.4  # eyebrows-to-eyes line
    # Crop with face center at Y=30% of output height
    out_h = int(h * 2.5)
    crop_top = max(0, int(face_center_y - out_h * 0.30))
    out = img[crop_top:crop_top + out_h, x - w//4 : x + w + w//4]
    cv2.imwrite(f'_measurements/face-{x}-{y}.png', out)
```

Apply this for every page with a face. Manual inspection follows: AI looks at each crop output and confirms the face is properly centered.

---

## Output format — `_measurements/REPORT.md`

After completing all measurements:

```markdown
# Pixel measurement report

## Pages requiring measurement (5 of 49)

### page-09 — E2E Architecture diagram
- 5 nodes measured: camera (24%, 38%), infer (37.5%, 38%), control (62.5%, 38%), log (62.5%, 72%), display (84%, 38%)
- 10 arrows in census table at `_measurements/page-09.json`
- Pixel tolerance: ±2 px (i.e., position error < 2 px from source)

### page-22 — Organization chart
- 25 nodes measured
- 24 lines (1 each from L0→L1, plus L1→L2 fanout)
- Pixel tolerance: ±2 px

### page-31 — Team composition pie chart
- 6 slices measured: angles 0-72°, 72-144°, ...
- Center: (50%, 50%), radius: 22vmin

### page-28 — CEO portrait
- Face detected at (1240, 580), face width 320 px
- Crop output: 1:1, face center at Y=33%

### page-40-48 — Employee voice photos (9 photos)
- Each face detected, each cropped with face center at Y=30-35%
- All crops saved to `assets/photos/voice-<N>.jpg`
```

This report is included in the hand-off package.

---

## When measurement is NOT required

Skip measurement only for:
- Cover pages (full-bleed hero, no positioned elements)
- Pure text sections (heading + paragraph + nothing else)
- Card grids where flexbox/grid handles all positioning
- Single-image full-bleed pages

For everything else, measure. The 30 minutes of measurement saves 3 hours of layout iteration.
