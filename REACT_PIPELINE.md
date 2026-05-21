# REACT_PIPELINE — when to use React/Next.js instead of vanilla HTML

The vanilla single-file HTML approach is the default. But for some cases, React (or Next.js) produces visually superior results with less iteration. This document defines **when to switch** and **how to configure**.

## When to switch to React

Use the React pipeline when ANY of the following applies:

| Trigger | Why React is better |
|---|---|
| Source has 20+ pages | Vanilla HTML grows into a hard-to-maintain single-file monolith as page count climbs. React component reuse keeps each section as a small reusable file. |
| Pixel-precise complex layouts (org charts with 20+ nodes, architecture diagrams with 10+ arrows) | React `useRef` + `useEffect` + `useLayoutEffect` give precise control over `getBoundingClientRect` timing that vanilla JS can race with. |
| Animation density is very high (count-up + Ken Burns + SVG draw + stagger combinations) | Framer Motion handles entrance / exit / scroll-driven sequences with less manual code. |
| The deck will be iterated 5+ times (e.g., a flagship company deck) | Component refactoring is much faster in React than in vanilla HTML. |
| The deck needs a build pipeline (TypeScript, bundling, dead-code elimination) | Vite + React handles this in 3 commands. |

Use vanilla HTML when:
- Source is < 20 pages
- One-off / experimental deck
- User must edit the HTML afterwards by hand (vanilla = easier for non-engineers)
- Hosting target is a single-file environment (e.g., email attachment)

## React pipeline stack

```
Vite 5.x
+ React 18
+ TypeScript 5
+ Framer Motion (for entrance / scroll-driven / spring animations)
+ vite-plugin-singlefile (bundles everything into ONE index.html for distribution)
+ react-intersection-observer (for slide-active triggers)
+ react-spring or Framer Motion (for count-up)
+ lucide-react (icons)
+ tailwindcss (utility classes — optional, but speeds up styling)
```

## Project initialization

```bash
npm create vite@latest my-deck -- --template react-ts
cd my-deck
npm install
npm install framer-motion react-intersection-observer vite-plugin-singlefile lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

`vite.config.ts`:
```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: { outDir: 'dist', cssCodeSplit: false, assetsInlineLimit: 100_000_000 },
});
```

Build: `npm run build` → `dist/index.html` is a single self-contained file.

## Component structure (recommended)

```
src/
  main.tsx
  App.tsx                  ← horizontal scroller, key handlers, language toggle
  i18n/
    ja.ts
    en.ts
    index.ts               ← export const t = (key) => ...
  layouts/
    Cover.tsx
    Mission.tsx
    OrgChart.tsx           ← dynamic SVG with refs
    NumbersDashboard.tsx   ← count-up via Framer Motion useSpring
    SubReel.tsx
    CEOMessage.tsx         ← receives personName, photoSrc, message via props (Rule "no hardcoded names")
    Finale.tsx
  components/
    AnimatedPath.tsx       ← 3-stage render (null / measured / ready)
    LangToggle.tsx         ← top-right EN/JP button
    PageChrome.tsx         ← page counter, nav, footer
  pages.ts                 ← array of { layout: 'Cover', props: {...} }
  tokens.css               ← --brand-primary, --font-display, etc.
  index.css                ← global resets + scaffold
```

## The 3 mandatory React components

These three replace the most error-prone vanilla patterns. Use them verbatim.

### AnimatedPath (3-stage render)

The vanilla `stroke-dashoffset` pattern stutters because `len = null → measured → animation start` happens in 1 frame. React with `useEffect` + 2 `requestAnimationFrame` waits solves this:

```tsx
import { useEffect, useRef, useState } from 'react';

export function AnimatedPath({ d, delay = 0, stroke = 'currentColor' }: {
  d: string; delay?: number; stroke?: string;
}) {
  const ref = useRef<SVGPathElement>(null);
  const [len, setLen] = useState<number | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const L = ref.current.getTotalLength() || 100;
    requestAnimationFrame(() => {
      setLen(L);
      requestAnimationFrame(() => setReady(true));
    });
  }, [d]);

  return (
    <path
      ref={ref}
      d={d}
      fill="none"
      stroke={stroke}
      strokeWidth={2}
      strokeDasharray={len ?? 1}
      strokeDashoffset={ready ? 0 : (len ?? 1)}
      style={{
        opacity: len !== null ? 1 : 0,
        transition: `stroke-dashoffset 0.8s ease ${delay}s, opacity 0.15s linear ${delay}s`,
      }}
    />
  );
}
```

### CEOMessage (props-driven, no hardcoded names)

```tsx
export function CEOMessage({ personName, role, photoSrc, message, sign }: {
  personName: string; role: string; photoSrc: string; message: string; sign: 'CEO' | 'CTO' | 'CHRO';
}) {
  return (
    <section className="cmsg">
      <img src={photoSrc} alt={`${personName} (${role})`} />
      <div className="cmsg-body">
        <p>{message}</p>
        <p className="cmsg-sign">{sign} — {personName}</p>
      </div>
    </section>
  );
}
```

Never hardcode a name. Receive via props.

### NumbersDashboard (count-up with useSpring)

```tsx
import { motion, useSpring, useTransform, useInView } from 'framer-motion';
import { useRef, useEffect } from 'react';

export function CountUp({ to, suffix = '' }: { to: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true });
  const spring = useSpring(0, { stiffness: 50, damping: 20 });
  const rounded = useTransform(spring, v => Math.round(v).toLocaleString());

  useEffect(() => {
    if (inView) spring.set(to);
  }, [inView, to, spring]);

  return (
    <span ref={ref} style={{ fontVariantNumeric: 'tabular-nums' }}>
      <motion.span>{rounded}</motion.span>{suffix}
    </span>
  );
}
```

Use as `<CountUp to={272} suffix="億円" />`. Starts from 0, animates to 272 when scrolled into view.

## How the workflow changes

The 11-stage `WORKFLOW.md` applies identically. The differences:

| Stage | Vanilla HTML | React pipeline |
|---|---|---|
| 7 (HTML draft) | Edit `index.html` directly | Edit `src/` files, run `npm run build` for each preview |
| 8 (Visual audit) | Playwright against `index.html` | Playwright against `dist/index.html` (build output) |
| 10 (Post-flight) | `verify.html.py dist/index.html` (same script) | same |
| 11 (Handoff) | Ship `index.html` | Ship `dist/index.html` (build output is single-file thanks to vite-plugin-singlefile) |

## The hand-off package, React variant

```
my-deck/
  src/                    # source
  public/                 # static assets
  package.json
  vite.config.ts
  dist/
    index.html            # the deliverable (single self-contained file)
  _audit/
    page-01.png ... page-NN.png
    REPORT.md
  _measurements/
    page-09.json
    REPORT.md
```

The deliverable for the user is `dist/index.html`. The rest is the AI's working directory.

## When the React deliverable fails verify.html.py

The React build's output is single-file HTML with all CSS/JS inlined. `verify.html.py` operates on this output identically to a vanilla deliverable. If gate 16 (CSS/JS inlined) fails, check `vite.config.ts` — `viteSingleFile()` must be in the plugins array.

If gate 18 (external asset references ≥ 5) fails, your React app may have inlined everything as base64. Move large images back to `public/assets/<name>.jpg` and reference via relative paths — `vite-plugin-singlefile` will keep them external if the file is over `assetsInlineLimit`.
