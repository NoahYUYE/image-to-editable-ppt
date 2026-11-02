#!/usr/bin/env python3
"""Extract named image regions and optionally remove a near-white background."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


SAFE_NAME = re.compile(r"^[A-Za-z0-9_-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract regions from an image into independent PNG assets."
    )
    parser.add_argument("--input", required=True, type=Path, help="Source image")
    parser.add_argument(
        "--regions", required=True, type=Path, help="JSON region specification"
    )
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    parser.add_argument(
        "--white-offset",
        type=float,
        default=3.0,
        help="Near-white distance that becomes fully transparent",
    )
    parser.add_argument(
        "--alpha-scale",
        type=float,
        default=7.0,
        help="Alpha ramp multiplier after the white offset",
    )
    parser.add_argument(
        "--no-trim",
        action="store_true",
        help="Do not trim fully transparent borders",
    )
    return parser.parse_args()


def validate_box(box: object, width: int, height: int) -> tuple[int, int, int, int]:
    if not isinstance(box, list) or len(box) != 4 or not all(
        isinstance(value, int) for value in box
    ):
        raise ValueError("Each box must contain four integer coordinates")
    left, top, right, bottom = box
    if not (0 <= left < right <= width and 0 <= top < bottom <= height):
        raise ValueError(
            f"Box {box} is outside the {width}x{height} source image"
        )
    return left, top, right, bottom


def remove_near_white(
    image: Image.Image, white_offset: float, alpha_scale: float
) -> Image.Image:
    rgba = image.convert("RGBA")
    result: list[tuple[int, int, int, int]] = []
    pixel_data = (
        rgba.get_flattened_data()
        if hasattr(rgba, "get_flattened_data")
        else rgba.getdata()
    )
    for red, green, blue, _ in pixel_data:
        distance = max(255 - red, 255 - green, 255 - blue)
        alpha = max(0, min(255, round((distance - white_offset) * alpha_scale)))
        result.append((red, green, blue, alpha))
    rgba.putdata(result)
    return rgba


def main() -> None:
    args = parse_args()
    source = Image.open(args.input)
    spec = json.loads(args.regions.read_text(encoding="utf-8"))
    regions = spec.get("regions")
    if not isinstance(regions, list) or not regions:
        raise ValueError("Region specification must contain a non-empty regions list")

    args.out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for region in regions:
        if not isinstance(region, dict):
            raise ValueError("Each region must be a JSON object")
        name = region.get("name")
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            raise ValueError(
                "Region names may contain only letters, digits, hyphens, and underscores"
            )
        mode = region.get("mode", "near-white")
        if mode not in {"near-white", "preserve"}:
            raise ValueError(f"Unsupported mode for {name}: {mode}")

        box = validate_box(region.get("box"), source.width, source.height)
        crop = source.crop(box).convert("RGBA")
        if mode == "near-white":
            crop = remove_near_white(crop, args.white_offset, args.alpha_scale)
        if not args.no_trim:
            bounds = crop.getbbox()
            if bounds:
                crop = crop.crop(bounds)

        destination = args.out / f"{name}.png"
        crop.save(destination)
        written.append(destination)

    print(f"Extracted {len(written)} region(s) to {args.out}")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
