# Example — Sanitized Transformation Notes

Notes that accompany a page-mapping table, capturing the design decisions
that distinguish "thoughtful conversion" from "1:1 trace."

## Cover (HTML 01 / 41)

**Source:** slide 1 — brand mark + "Company Deck" + date.

**Decision:** keep it sparse. The cover's job is mood, not information.
Full-bleed video background (mp4 H.264, ~12s loop, muted), brand logo
plus one-line tagline.

**Implementation notes:**

- Video: `<video autoplay muted loop playsinline preload="metadata">`,
  opacity 0.55, dark overlay on top.
- Tagline split into two lines, second line in `--brand-primary`.
- No CTA on this page. The CTA lives on the final page.

## Tagline moment (HTML 02 / 41)

**Source:** slide 4 — three-word claim.

**Decision:** make it the loudest page in the deck. Massive type
(80–96px), black background, optional ken-burns subtle photo behind.
This is the page that gets screenshot and shared.

**Implementation notes:**

- `clamp(72px, 8vw, 120px)` for the type.
- Background photo: opacity 0.18, ken-burns 22s loop.
- One animation: fade-up the type, 1.4s with light overshoot.

## Mission statement (HTML 03 / 41)

**Source:** slide 3.

**Decision:** the calm after the tagline moment. Light theme, centered
content, generous whitespace. The visitor reads, breathes, continues.

**Implementation notes:**

- Eyebrow tag in brand color.
- Title in 64px max, line-height 1.15.
- Body in 16px, max-width 48 characters per line.

## CEO portrait + voice (HTML 04 / 41)

**Source:** slide 44 (appendix CEO bio).

**Decision:** promoted from appendix because the CEO's voice / authority
is one of this deck's strongest assets. Two-column: photo (left, 4.5fr)
+ body (right, 5.5fr). Quote-style typography.

**Implementation notes:**

- Photo container with `aspect-ratio: 3 / 4`, `object-fit: cover`,
  `object-position: center top`.
- Body has a max-width of 56 characters per line for readability.
- "Read more" link out to a longer interview if available.

## Milestone proof (HTML 05 / 41)

**Source:** slide 8 — dated achievement.

**Decision:** one big number, one big date, supporting line. Treat as a
numbers-dashboard archetype but in dark theme for emphasis.

**Implementation notes:**

- Number animates from 0 to target with `data-count`.
- Number in `clamp(120px, 14vw, 220px)`.
- Date below in `--brand-primary` mono font.
- Subtitle in 18px secondary text.

## New bridge: "6 months later" (HTML 06 / 41)

**Source:** none — newly written for the HTML deck.

**Decision:** the milestone is exciting but feels like a peak; we need to
narrate "and we kept going" before diving into Technology. A short bridge
page with one statement + small supporting copy.

**Implementation notes:**

- Same layout family as the milestone page so they feel paired.
- Lighter background to start the rhythm shift toward Technology.

## Technology sub-reel (HTML 07–12 / 41)

**Source:** slides 5, 6, 9, 19, 45, 46, 48, 49.

**Decision:** these source slides all explain technical context but
overlap heavily. Re-edit into a 6-sub-slide reel:

- **Sub 01** — "Why End-to-End" (comparison: legacy stack vs E2E)
- **Sub 02** — Architecture overview (from slide 5)
- **Sub 03** — Foundation model (from slide 6 + 9)
- **Sub 04** — Long-tail problem (from slide 47)
- **Sub 05** — Industry shift (from slide 50)
- **Sub 06** — MLOps cycle (from slide 19)

**Implementation notes:**

- Each sub-slide uses the same two-column layout for visual consistency:
  left text spec, right visual.
- Sub-reel arrows / dots inside `#group-dots` for clear in-section
  navigation.
- Each sub-slide has its own dynamic SVG diagram drawn from anchored
  boxes (no hard-coded coords).
- The h-meta dynamically shows "07–12 / 41" depending on sub position.

## Team sub-reel (HTML 14–22 / 41)

**Source:** slide 10 (overview) + slides 11–18 (one per team).

**Decision:** 9-slide sub-reel. Sub 01 is the org map (slide 10
re-drawn as HTML+SVG), subs 02–09 are individual team detail pages.

**Implementation notes:**

- Sub 01 uses dynamic SVG to draw lines connecting team boxes to
  hardware / OS / application layers. Visitors can mentally map the
  upcoming sub-slides to their position in this diagram.
- Subs 02–09 share the same 4.5:5.5 grid (text-spec left, visual right).
  Within that, each team can use its own diagram style — flow chart,
  before/after, code snippet, GIF, etc. — to convey what it does.
- The h-meta sub-step counter ("01 / 09" through "09 / 09") shows
  position.

## Org chart (HTML 32 / 41)

**Source:** slide 30 (formal org chart with boxes and dotted lines).

**Decision:** this is the highest-risk page for hard-coded SVG. Source
has ~25 connector lines between boxes that span 6 columns and 4 hierarchy
levels. Implement entirely with `data-anchor` attributes and JS-drawn
connectors.

**Implementation notes:**

- 6-column grid. Vertical "department spine" boxes use `writing-mode:
  vertical-rl` for compact labels.
- `drawOrgLines()` reads `getBoundingClientRect()` for every anchor,
  produces ~25 right-angle paths.
- Redraws on resize, language switch, slide-active (via
  MutationObserver).
- Each line has `--line-delay` staggered for a draw-in cascade
  (0.10s, 0.15s, 0.20s, …).

## CTA (HTML 41 / 41)

**Source:** slide 42 ("we're hiring").

**Decision:** the deck's final visual hit. Dark theme, large type, single
clear action ("Apply"), plus SNS icons for follow-on engagement.

**Implementation notes:**

- One H1 in `--brand-primary`, ~72px.
- Four action buttons in a 2×2 grid: Apply, Company Site, Press,
  Investor Relations.
- Four SNS icons (X / YouTube / LinkedIn / Facebook) below.
- A subtle "Built with [playbook-name]" attribution in the footer is
  optional and tasteful.

## What these notes accomplish

Reading these transformation notes alongside the page-mapping table, a
reviewer can quickly understand:

- Why this page is where it is in the deck order.
- What design decisions were made and why.
- Where the technical complexity lives (sub-reels, dynamic SVG).
- What the new bridge pages contribute that the source didn't.

The notes don't repeat the obvious (CSS variables, design tokens) — those
live in the references. They focus on the **decisions specific to this
deck**, which is what reviewers and future maintainers need.
