# ASSET_RESEARCH — collaborative asset collection protocol

This document defines how the AI gathers brand assets for a company's PDF→HTML conversion. **The user's only job is to click download URLs the AI presents.** The AI does the research.

## Absolute prohibitions

| ❌ Forbidden | ✅ Required instead |
|---|---|
| Drawing a logo as inline SVG `<polygon>` "approximately like the real one" | Find the official SVG via web search, ask the user to download it |
| Guessing a brand color as `#2C70FF` because it "looks like Acme" | Find the official hex from press kit / IR docs / official site CSS |
| Saying "I couldn't find the press kit" and moving on | Provide a fallback plan with alternative download sources |
| Asking the user "please find your company's press kit and send it" | Do the search yourself; only ask the user to **click** found URLs |

Logos and brand colors are corporate identity. A "close-enough" approximation is a brand violation. There are no exceptions.

---

## The 5 asset categories

For every PDF→HTML conversion, research these 5 categories in order. For each category, output a numbered list of **one-click download URLs**.

### Category 1 — Corporate logo SVG (3 variants)

**Search queries (in this order until found)**:
1. `<company name> press kit`
2. `<company name> プレスキット`
3. `<company name> brand assets`
4. `<company name> ロゴ ダウンロード`
5. `<company name> SVG logo`
6. `site:<company-domain>/press`, `site:<company-domain>/brand`, `site:<company-domain>/about/press`
7. `<company name> media kit`

**Required variants**:
- Color (full color, on light background)
- White (for dark backgrounds)
- Black (for monochrome contexts)

**Fallback hierarchy if no press kit exists**:
1. Extract from company website header (View Source → find `<img src="...logo.svg">` → download)
2. simple-icons npm package (`simple-icons/<company-slug>`) — for well-known tech companies
3. Wikimedia Commons (search "File:<company>_logo.svg") — CC/PD licensed
4. Last resort: crop the logo from the source PDF page 1 cover, save as PNG, ask user to verify

**Post-processing**: For every SVG received, **strip the `cls-1` background rect** (Python: `re.sub(r'<rect[^/>]*class="cls-1"[^/>]*/>', '', svg, count=1)`). Save as `<name>-transparent.svg`.

### Category 2 — Product logos (if the company has products)

**Detect from source**: Scan the PDF pages for product names mentioned. Compile the product list.

**Search queries per product**:
- `<product name> logo SVG`
- `<product name> press kit`
- `<parent company>/<product> brand assets`

**If the source PDF mentions N products and you found logos for M (M<N)**: explicitly list the missing ones and ask the user "can you provide logos for: <product-X>, <product-Y>? Or should I use simple-icons fallback?"

### Category 3 — Brand colors

**Search queries**:
1. `<company name> brand color hex`
2. `<company name> visual identity`
3. Open the press kit PDF / brand guideline → extract hex
4. View Source of `<company-domain>` → find `--brand-primary` or equivalent CSS variable
5. **Last resort**: open the official logo SVG → read the `fill="#XXXXXX"` attribute of the largest path

**Output format**:
```
Brand colors discovered:
  - Primary:   #1A5EFF  (source: https://acme.example.com/press, brand-guide.pdf p.4)
  - Secondary: #0A0D2B  (source: same press kit p.5)
  - Accent:    #FAFAFA  (source: official site header CSS)
```

If you write "approximate" or "looks like" anywhere in this section, restart the search.

### Category 4 — Fonts

**Search queries**:
1. `<company name> font family`
2. Open the official site → DevTools → Computed → `font-family`
3. Open the press kit / brand guideline PDF → look for typography spec page

**Output format**:
```
Fonts identified:
  - Display: Inter Tight  (Google Fonts: https://fonts.google.com/specimen/Inter+Tight)
  - Body:    Noto Sans JP (Google Fonts: https://fonts.google.com/noto/specimen/Noto+Sans+JP)
  - Mono:    JetBrains Mono (Google Fonts: https://fonts.google.com/specimen/JetBrains+Mono)
```

If the official font is paid (e.g., proprietary type), propose 2-3 free Google Fonts alternatives that are visually closest, and ask the user which to use.

### Category 5 — People photos (executives, employees)

**Detect from source**: Identify face-bearing pages (org charts, leadership team, employee voices, culture spreads).

**Search queries per named person**:
1. `<person name> <company> profile photo`
2. `<company> leadership team`
3. `<company> about us team` (look for `<img>` tags in official site)

**For photos not publicly available** (most internal employees):
- Use OpenCV haarcascade to detect faces in the source PDF rasters
- Crop each face to a 1:1 aspect ratio with the face center at Y=30-35% (top-of-face area)
- Save as `photos/<page-N>-<face-id>.jpg`

**CRITICAL anti-pattern**: never label a photo with the wrong person's name. If the source PDF puts "CEO 田中 太郎" next to a photo, that photo is "田中 太郎", not "鈴木 一郎" (Rule 16 derivative). Verify against the source page text before writing the HTML.

---

## Output format — what the user sees

After completing all 5 categories, post this consolidated message:

```
## アセット調査完了レポート

私が見つけたものと、ダウンロードしていただきたいものをまとめました。
**あなたの作業は「URL をクリックして添付」のみ** です。

### ✅ 私が直接取得済み (添付不要)
- (none)

### 📥 クリック → 添付お願いします
1. **コーポレートロゴ SVG**: <one-click URL>
   - 取得後、私が color / white / black の 3 変種を生成 + 透過処理します
2. **製品ロゴ ZIP**: <one-click URL>  (AcmeSpend 13 製品 + Acme Workforce)
3. **ブランドガイドライン PDF**: <one-click URL>
4. **CEO ポートレート**: <one-click URL>
5. **役員 3 名のポートレート**: <one-click URL>

### ⚠️ 公開されていなかったもの (フォールバック計画)
- 社員 voice 写真 5 名: ソース PDF p.31-35 から顔検出で抽出
- 提携企業ロゴ 3 種 (NVIDIA, JST, 経産省): simple-icons + Wikimedia Commons
- 製品 X のロゴ: ソース PDF からクロップ (お客様にて確認お願いします)

### 📋 抽出済み情報 (添付不要)
- ブランドカラー: Primary #1A5EFF / Secondary #0A0D2B (出典: <URL>)
- フォント: Inter Tight + Noto Sans JP (Google Fonts)
- 公式社名: Acme Inc.（架空企業）
- 公式 X アカウント: @AcmeInc

上記を確認したら、ダウンロード → このチャットに添付してください。
全部揃ったら次のステージ (Pre-flight) に進みます。
```

This format keeps the user's effort minimal (only clicks + attaches) while making the AI's research effort completely transparent.

---

## When the user has nothing to share

If the user replies "press kit がない、社内にもブランドアセットの整理が無い":

The AI proceeds with the full fallback plan and **explicitly tells the user**:

```
了解。公式アセットなしの状態で進めます。以下のフォールバックを使います:

- ロゴ: ソース PDF 1 ページ目のカバーから 300 DPI でクロップ → 透過処理
- ブランドカラー: ロゴから dominant color を抽出 (e.g., #XXXXXX)
- フォント: ソース PDF 内で使用されているフォントを目視判定 → 近い Google Fonts を選択
- 写真: ソース PDF の人物写真を顔検出でクロップ

この方式だと品質は「公式アセットあり」より 1 段下がります。
納品物の合格基準: gate 13 (brand color) は「ロゴ抽出色」を使ってパス、
gate 18 (external asset references) は最低限の関係性のみ。
継続的に使うご予定があれば、press kit / brand guide / official logo SVG を社内整備されることを強く推奨します。
```

This way the user knows the quality trade-off explicitly.
