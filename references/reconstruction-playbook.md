# Reconstruction Playbook

## Implementation matrix

| Source element | Preferred PowerPoint implementation | Editability |
|---|---|---|
| Headings and body copy | Native text boxes | Full text and style editing |
| Pills, badges, cards, platforms | Native shapes with gradients and shadows | Full geometry and style editing |
| Lines, arrows, rings, connectors | Native shapes or connectors | Full position and style editing |
| Simple monochrome icons | Native shapes when quick and faithful; otherwise transparent PNG | Full if native; object-level if PNG |
| Product photos, people, 3D renders | Separate transparent PNG | Move, resize, crop, replace |
| Fine noise, dot fields, complex texture | Minimal native pattern or raster background | Limited if raster |
| Logos | Original SVG/vector when supplied; otherwise separate image | Depends on source |

## Fidelity modes

### Hybrid, recommended

Rebuild geometry and text natively. Preserve complex rendered objects as transparent image layers. This usually gives the best balance of editability and visual fidelity.

### Maximum editability

Redraw icons and decorations as native vectors. Expect visible differences in complex art, 3D objects, textures, and lighting.

### Maximum fidelity

Keep more objects as independent raster layers. The slide remains rearrangeable, but internal colors and subparts are not directly editable.

If the user asks for both pixel-perfect fidelity and full internal editability, explain the conflict. Offer the hybrid mode unless editable source files are available.

## Crop-region file

Use this JSON format with `scripts/extract_regions.py`:

```json
{
  "regions": [
    {
      "name": "gateway-device",
      "box": [220, 610, 350, 740],
      "mode": "near-white"
    },
    {
      "name": "dark-background-logo",
      "box": [40, 30, 240, 150],
      "mode": "preserve"
    }
  ]
}
```

`box` uses `[left, top, right, bottom]` pixel coordinates. Names become output filenames and must contain only letters, digits, hyphens, or underscores.

## Visual reconstruction rules

- Match the source aspect ratio before placing any content.
- Use back-to-front layer order.
- Reproduce major silhouettes and spacing before fine decoration.
- Match text hierarchy, alignment, and line breaks before tuning font sizes.
- Keep extracted image crops tight but include intentional shadows.
- Remove neighboring objects from crops; a faint unwanted line is still a defect.
- Avoid one large background image containing major foreground content.
- Preserve visible whitespace; do not fill empty areas merely because they exist.
- Prefer a slight simplification of subtle texture over creating noisy editable shapes.

## Final QA checklist

- Slide ratio matches the reference or the user-approved target.
- All visible source text is present, editable, correctly translated, and spell-checked.
- No heading intended for one line wraps unexpectedly.
- Major objects align with the source composition.
- Platforms, arrows, connectors, and badges are separate objects.
- Complex image elements have transparent or visually clean boundaries.
- Object names are meaningful in the Selection Pane.
- No unintended overlap or clipping appears in the library preview.
- No unintended overlap, clipping, or font substitution appears in the rendered PPTX.
- The overflow test passes.
- The final folder contains only requested deliverables.
- The handoff distinguishes native objects from raster image elements.

