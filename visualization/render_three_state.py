"""Render the growing-block comparison in the three-state witness."""

import argparse
from math import tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from render import BG, CORAL, MUTED, TEAL, TEXT, box


def frame(angle, fonts):
    title, label, body = fonts
    result = Image.new("RGB", (880, 570), BG)
    draw = ImageDraw.Draw(result)
    draw.text((26, 19), "Three states, one weighted row", font=title, fill=TEXT)
    draw.line((28, 78, 852, 78), fill="#395375", width=2)
    for shift, heading, uniform in ((-11, "Weighted G", False), (417, "Uniform U", True)):
        draw.rounded_rectangle((shift + 32, 106, shift + 422, 420), radius=15, fill="#1a2b47")
        draw.text((shift + 226, 121), heading, font=label, fill=TEXT, anchor="ma")
        polygons = []
        for n in range(1, 5):
            x = .61 * (n - 2.5)
            even = (2 / 3) ** n / 2 if uniform else (4 / 3) ** n / 2
            odd = 1.5 - (2 / 3) ** n if uniform else even
            polygons.extend(box(x, -.5, odd, CORAL, angle, shift - 12))
            polygons.extend(box(x, .5, even, TEAL, angle, shift - 12))
        for _, vertices, fill in sorted(polygons):
            draw.polygon(vertices, fill=fill, outline=BG, width=2)
        caption = "Both counts grow equally" if not uniform else "Priority 2 count shrinks"
        draw.text((shift + 226, 367), caption, font=body, fill=TEXT, anchor="ma")
    for x, color, caption in ((36, CORAL, "Priority 1"), (260, TEAL, "Priority 2")):
        draw.ellipse((x, 457, x + 19, 476), fill=color)
        draw.text((x + 29, 449), caption, font=body, fill=MUTED)
    draw.text((36, 510), "Expected arrivals for block lengths 1 through 4", font=body, fill=MUTED)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular-font", default="DejaVuSans.ttf")
    parser.add_argument("--bold-font", default="DejaVuSans-Bold.ttf")
    parser.add_argument("--output", type=Path, default=Path("visualization/three-state-blocks.gif"))
    args = parser.parse_args()
    fonts = tuple(ImageFont.truetype(font, size) for font, size in (
        (args.bold_font, 42), (args.bold_font, 35), (args.regular_font, 30)
    ))
    frames = [frame(.55 + i * tau / 64, fonts).quantize(colors=120, method=2) for i in range(64)]
    frames[0].save(args.output, save_all=True, append_images=frames[1:],
                   duration=92, loop=0, disposal=2, optimize=True)


if __name__ == "__main__":
    main()
