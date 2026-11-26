"""Render expected priority arrivals on rotating 3D grids."""

import argparse
from math import cos, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BG = "#101c30"
TEXT = "#f5f8fd"
MUTED = "#cbd7ed"
TEAL = "#78dcd1"
CORAL = "#ffac97"
FACES = [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]


def project(point, yaw):
    x,y,z = point
    rx = x*cos(yaw)+z*sin(yaw)
    rz = z*cos(yaw)-x*sin(yaw)
    tilt = .41+.15*cos(yaw)
    ry = y*cos(tilt)-rz*sin(tilt)
    depth = y*sin(tilt)+rz*cos(tilt)
    scale = 385/(5.5-depth)
    return 238+.85*scale*rx, 278-.85*scale*ry, depth


def shade(color, factor):
    rgb = tuple(int(color[i:i+2],16) for i in (1,3,5))
    return tuple(round(x*factor) for x in rgb)


def box(x, z, height, color, yaw, shift):
    points = [project((a,b,c),yaw) for a in (x-.24,x+.24)
              for b in (-.7,-.7+height) for c in (z-.28,z+.28)]
    return [(sum(points[i][2] for i in face)/4,
             [(shift+points[i][0],points[i][1]) for i in face],
             shade(color,(.7,.8,.55,1,.64,.89)[idx]))
            for idx,face in enumerate(FACES)]


def frame(angle, fonts):
    title, label, _, body = fonts
    result = Image.new("RGB",(880,570),BG)
    draw = ImageDraw.Draw(result)
    draw.text((26,19),"Expected counts for each group",font=title,fill=TEXT)
    draw.line((28,78,852,78),fill="#395375",width=2)
    for shift, heading, uniform in ((-11,"Resolver G",False),(417,"Uniform U",True)):
        draw.rounded_rectangle((shift+32,106,shift+422,420),radius=15,fill="#1a2b47")
        draw.text((shift+226,121),heading,font=label,fill=TEXT,anchor="ma")
        polygons=[]
        for n in range(1,5):
            x=.61*(n-2.5)
            polygons.extend(box(x,-.5,1.5,CORAL,angle,shift-12))
            expected = (2/3)**n if uniform else 1
            polygons.extend(box(x,.5,1.5*expected,TEAL,angle,shift-12))
        for _, vertices, fill in sorted(polygons):
            draw.polygon(vertices,fill=fill,outline=BG,width=2)
        caption = "Both counts stay 1/2" if not uniform else "Priority 2 count shrinks"
        draw.text((shift+226,367),caption,font=body,fill=TEXT,anchor="ma")
    for x,color,caption in ((36,CORAL,"Priority 1"),(260,TEAL,"Priority 2")):
        draw.ellipse((x,457,x+19,476),fill=color)
        draw.text((x+29,449),caption,font=body,fill=MUTED)
    draw.text((36,510),"Four groups with block lengths 1 through 4",font=body,fill=MUTED)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular-font",default="DejaVuSans.ttf")
    parser.add_argument("--bold-font",default="DejaVuSans-Bold.ttf")
    parser.add_argument("--output",type=Path,default=Path("visualization/parity-blocks.gif"))
    args=parser.parse_args()
    fonts=tuple(ImageFont.truetype(font,size) for font,size in (
        (args.bold_font,42),(args.bold_font,35),(args.bold_font,40),(args.regular_font,30)
    ))
    frames=[frame(.55+i*tau/64,fonts).quantize(colors=120,method=2) for i in range(64)]
    frames[0].save(args.output,save_all=True,append_images=frames[1:],
                   duration=92,loop=0,disposal=2,optimize=True)


if __name__ == "__main__":
    main()
