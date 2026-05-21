# Examples

Reference HTML outputs produced with this toolkit. These are minimal samples intended to illustrate conversion patterns, not standalone presentations.

## Files

| File | Pipeline | Notes |
|---|---|---|
| [`turing-v1.html`](turing-v1.html) | Vanilla | 13-section company deck. Demonstrates the Keynote-style fixed-canvas (1728×963) scaling model, horizontal slide navigation, reveal / count-up animations, and reel sub-slides. |

## Opening locally

```bash
open turing-v1.html
```

Each file is fully self-contained. No build step or package installation is required.

## Sanitized reference documents

| File | Purpose |
|---|---|
| [`sanitized-page-mapping.example.md`](sanitized-page-mapping.example.md) | Example of a `slide N → html page M` mapping table — the canonical output of Phase 1. |
| [`sanitized-transformation-notes.example.md`](sanitized-transformation-notes.example.md) | Example of transformation notes (e.g. "promote bullet list to card grid", "replace static org chart with dynamic SVG"). |

## Notes on third-party assets

Third-party brand assets (logos, color guides, photographs) used during development are not bundled in this repository. The toolkit reproduces equivalent results from any user-supplied source.
