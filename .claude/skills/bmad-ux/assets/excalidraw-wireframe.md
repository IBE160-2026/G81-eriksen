# Excalidraw Wireframe Renderer

Subagent prompt. Produce one `.excalidraw` file at `.working/ia-{date}.excalidraw` (IA diagram) or `.working/flow-{name}-{date}.excalidraw` (flow wireframe).

## CRITICAL: valid fractional `index` fields

Every element's `index` field must be a valid Excalidraw fractional index, or the import fails with a silent *"Error: invalid file"* and no diagnostic output. The leading letter sets how many base-62 digits follow: `a` takes exactly **one** digit, `b` exactly **two**, `c` exactly **three**. Digits are ordered `0-9`, then `A-Z`, then `a-z` (ASCII order). Assign sequentially across all elements:

- elements 1–62: `a0..a9, aA..aZ, aa..az`
- elements 63–3906: `b00, b01, ..., b0z, b10, ..., bzz`

So `b0` and `a00` are invalid. Verify before writing: every index matches its prefix length, and the list is strictly increasing under plain string sorting.

## Shape

Valid Excalidraw file: `{type: "excalidraw", version: 2, source: "https://excalidraw.com", elements: [...], appState: {gridSize: null, viewBackgroundColor: "#ffffff"}, files: {}}`. Each element needs the standard Excalidraw element fields (`id, type, x, y, width, height, angle, strokeColor, backgroundColor, fillStyle, strokeWidth, strokeStyle, roughness, opacity, groupIds, frameId, roundness, seed, version, versionNonce, isDeleted, boundElements, updated, link, locked, index`). Text elements add `text, fontSize, fontFamily, textAlign, verticalAlign, baseline, containerId, originalText, lineHeight`.

## Content

**IA diagram:** boxes-and-arrows of auth stack, main app surfaces, modal routes, settings stack, cross-cutting affordances. Color sparingly to distinguish category. Layout for human legibility, not graph correctness.

**Flow wireframe:** screen-by-screen rectangles left-to-right, simple shapes inside (nav bar, CTA, content blocks) at low fidelity. Arrows labeled with the user action that causes transition. Annotations alongside for climax and edge-case beats.

Return to the parent: file path, kind, one-line subject, element count, confirmation that all indices are valid and strictly increasing. Do not dump JSON into parent context. Tell the user to open in Excalidraw desktop or excalidraw.com.
