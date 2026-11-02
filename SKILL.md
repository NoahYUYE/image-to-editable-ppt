---
name: image-to-editable-ppt
description: Reconstruct flat images, screenshots, posters, diagrams, or infographics as editable PowerPoint slides while preserving the source composition and visual effect. Use when the user asks to convert an image into an editable PPT/PPTX, split image elements into editable layers, recreate a screenshot in PowerPoint, translate in-image text into editable slide copy, or says 图片转可编辑PPT、把图片元素拆出来、保留当前效果、图片重绘成PPT、截图转PPT.
---

# Image to Editable PPT

Rebuild the reference as real slide objects. Favor a hybrid result: native PowerPoint objects for text and geometry, transparent image layers for complex rendered objects.

## Required companion skill

Read and follow the available presentation/PPT skill before authoring. Use its required PowerPoint library, workspace setup, export, rendering, and overflow checks. If no presentation skill is available, report that limitation instead of inventing an unsupported PPT workflow.

## Default contract

Unless the user says otherwise:

- Create one slide per reference image.
- Match the source aspect ratio with a custom slide size.
- Preserve the layout, hierarchy, palette, shadows, gradients, and visual direction.
- Make text, headings, badges, pills, arrows, platforms, lines, rings, and simple geometry native and editable.
- Keep complex products, people, 3D renders, and detailed illustrations as separate transparent image elements.
- Name every object clearly for the PowerPoint Selection Pane.
- Translate visible text only when requested; use natural audience-facing language and keep it editable.
- Deliver only the final PPTX unless another artifact is requested.

Do not claim that an embedded raster object is internally vector-editable. It is editable only as an independent image: move, resize, crop, recolor externally, or replace.

## Workflow

### 1. Inspect the reference

View the image at original detail. Record its pixel dimensions and aspect ratio. Inventory every visible layer before authoring:

1. background and decorative texture;
2. connectors, arrows, platforms, and structural geometry;
3. number badges, labels, titles, and body copy;
4. simple icons;
5. complex objects or renders;
6. lighting effects, shadows, glows, and overlays.

Read [references/reconstruction-playbook.md](references/reconstruction-playbook.md) when choosing how each layer should be implemented.

### 2. Establish the editability plan

Choose the implementation per layer before building:

- Native text boxes for all visible copy.
- Native shapes for simple geometry and effects PowerPoint can reproduce reliably.
- Native lines/connectors for relationships and arrows when practical.
- Independent transparent PNGs for complex objects whose internal redraw would reduce fidelity.
- A single raster background only for texture that is not meaningfully editable; never include text or major foreground objects in that background.

Never use the complete source image as the visible slide background and cover it with editable duplicates. That is not a genuinely editable reconstruction.

### 3. Prepare the task workspace

Follow the active file-output rules. For a project task, use one directory under `<project-root>/_codex/YYYYMMDD-task-slug/` with `final/`, `working/`, and `_tmp/`. Put extracted crops, preview renders, and QA evidence in `_tmp/`; put only final deliverables in `final/`.

### 4. Extract complex elements

Create a region JSON after visually identifying crop boxes, then run:

```bash
python scripts/extract_regions.py \
  --input <reference.png> \
  --regions <regions.json> \
  --out <tmp-assets-dir>
```

Use `mode: near-white` only when the crop is surrounded by a white or nearly white background. Use `mode: preserve` when transparency removal would damage the object. Inspect every extracted asset at full size and tighten crop boxes to remove neighboring lines, platforms, text, or arrows.

The script is for cropping and transparency masking only. Do not use Python to redraw presentation visuals.

### 5. Reconstruct in back-to-front order

Author layers in this order:

1. slide background and subtle decorative texture;
2. arrows and connectors;
3. platforms and large structural shapes;
4. guide lines and number badges;
5. text boxes and pills;
6. extracted image elements;
7. foreground accents.

Use the source pixel coordinate system as the slide coordinate system when the presentation library supports pixel units. This makes placement predictable and preserves the original ratio.

Keep each meaningful item separate. For repeated structures, use consistent naming such as `Stage 2 transport icon`, `Stage 2 transport label`, and `Stage 2 platform top`.

### 6. Rebuild and localize text

Transcribe every visible text element. Preserve hierarchy rather than blindly preserving font size. Use condensed fonts only when needed to fit the original width. Keep headings on one line when the design requires it.

For translation:

- preserve the business meaning;
- prefer natural presentation English over word-for-word translation;
- keep terminology consistent across the slide;
- verify spelling, capitalization, separators, and line breaks after rendering.

### 7. Validate in three views

Always perform all three checks:

1. inspect the source image at original detail;
2. export and inspect the presentation-library preview;
3. render the final PPTX with the presentation skill's renderer and inspect that result at full size.

Run the presentation skill's overflow test. Fix every unintended overflow, overlap, clipping, text wrap, missing glyph, crop artifact, or shifted icon. Do not treat the programmatic preview as sufficient proof because PowerPoint rendering can differ.

Use [references/reconstruction-playbook.md](references/reconstruction-playbook.md) for the final QA checklist and fidelity tradeoffs.

### 8. Deliver transparently

Return the final PPTX and state:

- which element families are native and fully editable;
- which elements remain independent raster images;
- whether the source aspect ratio was preserved;
- whether the overflow and final-render checks passed.

Do not overstate fidelity. Describe the reconstruction as approximate when exact fonts, source vectors, or layered design files were unavailable.

