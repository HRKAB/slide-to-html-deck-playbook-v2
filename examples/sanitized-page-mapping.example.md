# Example — Sanitized Page Mapping

A worked example of a page-mapping table for a fictional 50-slide source
deck being converted to an HTML deck. All names and content abstracted.

## Source: 50-slide corporate deck (fictional)

Brief: "Convert this into a beautiful single-file HTML deck. We want to
share it with investors and candidates."

## Step 1 — slide classification

```
Slide  Source role
01     cover
02     executive_letter        (CEO voice, ~200 words)
03     mission_statement
04     tagline_moment          (3-word claim)
05     architecture_diagram    (overview)
06     architecture_diagram    (detail)
07     timeline                (company history)
08     milestone_proof         (recent achievement, with date)
09     numbers_dashboard       (KPIs)
10     org_chart               (team layout overview)
11–18  team_role_detail        (one slide per team, 8 teams)
19     process_flow            (development lifecycle)
20     divider                 (Business chapter)
21     mission_statement       (market opportunity)
22     comparison              (legacy vs new approach)
23     roadmap                 (3-year plan)
24     milestone_proof         (recent product launch)
25     value_card              (why we'll win, 2 reasons)
26     architecture_diagram    (business model diagram)
27     numbers_dashboard       (market size)
28     divider                 (Company chapter)
29     numbers_dashboard       (company facts)
30     org_chart               (formal org chart)
31     numbers_dashboard       (member demographics)
32     team_role_detail        (executive team)
33     partner_logos           (member backgrounds)
34     feature_grid            (benefits)
35     mission_statement       (learning culture)
36     divider                 (Careers chapter)
37     value_card              (company values, 5)
38     feature_grid            (open positions)
39     process_flow            (hiring process)
40     feature_grid            (resume tips)
41     mission_statement       (stock option philosophy)
42     cta                     (we're hiring)
43     divider                 (Appendix)
44     executive_letter        (CEO bio)
45     comparison              (industry context)
46     architecture_diagram    (legacy approach detail)
47     comparison              (pain point illustration)
48     comparison              (rules vs ML)
49     comparison              (legacy vs new stack)
50     numbers_dashboard       (industry shift)
```

## Step 2 — re-edit decisions

- The strongest tagline is on slide 4. Promote to page 2 (after cover).
  The CEO letter on slide 2 was the "draft" hook — replace with the
  tagline.
- The CEO bio (slide 44, appendix) should be near the top, not buried.
  Promote to page 4.
- Slides 5–9 are heavy technical context. Consolidate into a "Technology"
  sub-reel of 6 sub-slides (slides 5, 6, 8, 9, plus material drawn from
  appendix 45–50). Drop slide 7 (timeline) into the sub-reel as one
  sub-slide.
- Slides 11–18 (8 team-role slides) plus the overview slide 10 →
  "Team" section with 9-slide sub-reel (overview as sub 01).
- Dividers (20, 28, 36, 43) don't need HTML pages; the dot-nav grouping
  handles chapter transitions.
- Slides 22, 25, 26, 27 (Business chapter content) → 4 sequential pages.
- Slides 29–35 (Company chapter) → 7 sequential pages, including the
  formal org chart redrawn as an HTML diagram with JS-drawn SVG lines.
- Slides 37–42 (Careers chapter) → 6 sequential pages.
- Slides 45–50 (appendix comparisons) → fold into Technology sub-reel
  (already covered) or cut entirely.
- Add **one new bridge page** between Tokyo30 milestone and the next
  section to give the deck a "now where are we?" breath.

## Step 3 — the table

```markdown
| Source Slide | Source Role               | HTML Page  | Transformation | Notes |
|--------------|---------------------------|------------|----------------|-------|
| 1            | cover                     | 01 / 41    | 1:1 adapted    | video bg, dark theme |
| 4 (tagline)  | tagline_moment            | 02 / 41    | promoted       | massive type, black bg |
| 2 (body)     | executive_letter          | —          | cut            | replaced by tagline; CEO voice covered on page 4 |
| 3            | mission_statement         | 03 / 41    | 1:1 adapted    | light theme, centered |
| 44           | executive_letter (CEO)    | 04 / 41    | promoted       | brought up from appendix |
| 8            | milestone_proof           | 05 / 41    | 1:1 adapted    | one big number + date |
| (new)        | milestone_proof           | 06 / 41    | new_bridge     | "6 months later" follow-up |
| 5, 6, 9, 45, 46, 48, 49 + 19 | various tech | 07–12 / 41 | subreel  | Technology section, 6 sub-slides |
| 50           | numbers_dashboard         | 13 / 41    | 1:1 adapted    | "industry by the numbers" |
| 10, 11–18    | team_role_detail (×9)     | 14–22 / 41 | subreel        | Team section, 9 sub-slides (10 = overview sub 01) |
| 27           | numbers_dashboard         | 23 / 41    | 1:1 adapted    | "right place, right time" |
| 22           | comparison                | 24 / 41    | 1:1 adapted    | legacy vs new |
| 21           | mission_statement         | 25 / 41    | 1:1 adapted    | market opportunity |
| 25           | value_card                | 26 / 41    | 1:1 adapted    | "why we win", 2 cards |
| 26           | architecture_diagram      | 27 / 41    | 1:1 adapted    | business model, JS-drawn |
| 34           | feature_grid              | 28 / 41    | 1:1 adapted    | benefits, 6 cards |
| 35           | mission_statement         | 29 / 41    | 1:1 adapted    | learning culture |
| 29           | numbers_dashboard         | 30 / 41    | 1:1 adapted    | company facts |
| 32           | team_role_detail (exec)   | 31 / 41    | 1:1 adapted    | exec cards |
| 30           | org_chart                 | 32 / 41    | expanded       | full org chart, JS-drawn lines |
| 31           | numbers_dashboard         | 33 / 41    | 1:1 adapted    | demographics donut |
| 33           | partner_logos             | 34 / 41    | 1:1 adapted    | logo grid |
| 41           | mission_statement         | 35 / 41    | 1:1 adapted    | SO philosophy |
| (new)        | numbers_dashboard         | 36 / 41    | new_bridge     | cumulative milestones |
| 38           | feature_grid              | 37 / 41    | 1:1 adapted    | open positions |
| 39           | process_flow              | 38 / 41    | 1:1 adapted    | hiring process |
| 40           | feature_grid              | 39 / 41    | 1:1 adapted    | resume tips |
| 37           | value_card                | 40 / 41    | demoted        | values, 5 cards |
| 42           | cta                       | 41 / 41    | 1:1 adapted    | hiring CTA, social |
| 7, 20, 23, 24, 28, 36, 43, 47 | various | —      | cut            | dividers, timeline (folded into reel), or redundant |
```

50 slides → 41 HTML pages. Of those, 12 are sub-slides in two sub-reels.

## Step 4 — show to deck owner

Before writing any HTML, this table is shown to the deck owner. They might
say:

> "Looks good. But page 4 (CEO bio) feels odd that early — can we make
> page 4 the milestone instead, and CEO bio at page 10 between Tokyo30
> follow-up and Technology sub-reel?"

Adjust the table; show again; get sign-off.

## Step 5 — the deck-owner question template

A useful prompt structure for this conversation:

```
Above is the proposed page-mapping. Before I generate the HTML, please confirm or correct:

1. Is the re-ordering acceptable, especially the promotions/demotions?
2. Are any "cut" slides surprising? (slides marked cut will not appear)
3. Should any "new_bridge" pages be added / removed?
4. Is the sub-reel grouping right? (currently 2 sub-reels: Technology, Team)
5. Any role classification that feels wrong?

Reply with corrections or "go ahead" to proceed.
```

## Notes on this example

- All slide content is hypothetical. The decisions reflect patterns
  observed in real conversions; the specific role assignments are
  illustrative.
- Real conversions usually involve 2–3 rounds of table revision with the
  deck owner before sign-off.
- This example produces a 41-page flat HTML deck. Typical range is 30–50.
- The two sub-reels eat 12 sub-slides; without sub-reels, the deck would
  have been 41 + 12 = 53 sections, which is too many. Sub-reels are
  essential for sections with > 5 sibling sub-topics.
