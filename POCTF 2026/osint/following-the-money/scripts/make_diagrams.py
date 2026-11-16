#!/usr/bin/env python3
"""Generate the diagrams used in the Following the Money write-up.

Only Pillow is required.  Run from anywhere:

    python3 scripts/make_diagrams.py

The PNGs are written to ../images relative to this script.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def xy(x: float, y: float) -> tuple[int, int]:
    return int(round(x)), int(round(y))


def center_text(draw: ImageDraw.ImageDraw, xy_: tuple[float, float], text: str,
                f: ImageFont.FreeTypeFont, fill: str = "black") -> None:
    box = draw.textbbox((0, 0), text, font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text((xy_[0] - w / 2, xy_[1] - h / 2), text, font=f, fill=fill)


def dashed_line(draw: ImageDraw.ImageDraw, p0, p1, fill: str,
                width: int = 2, dash: int = 10, gap: int = 8) -> None:
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    t = 0.0
    while t < length:
        a = xy(x0 + ux * t, y0 + uy * t)
        b = xy(x0 + ux * min(t + dash, length), y0 + uy * min(t + dash, length))
        draw.line([a, b], fill=fill, width=width)
        t += dash + gap


def arrow_head(draw: ImageDraw.ImageDraw, tip: tuple[float, float],
               direction: tuple[float, float], size: int = 12, fill: str = "black") -> None:
    ux, uy = direction
    px, py = -uy, ux
    p1 = xy(tip[0] - ux * size + px * size * 0.5, tip[1] - uy * size + py * size * 0.5)
    p2 = xy(tip[0] - ux * size - px * size * 0.5, tip[1] - uy * size - py * size * 0.5)
    draw.polygon([xy(*tip), p1, p2], fill=fill)


def altitude_diagram() -> None:
    W, H = 1000, 1260
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    center_text(d, (W / 2, 40), "Altitude of the WCS reference star", font(32, True))
    center_text(d, (W / 2, 82), "image height 1620 px, vertical FOV 45.9°", font(22), "#444444")

    x0, x1 = 250, 750
    y0, y1 = 140, 1140
    scale = (y1 - y0) / 1620.0
    y_h = y0 + 1443 * scale
    y_s = y0 + 660.067301432 * scale

    d.rectangle([x0, y0, x1, int(y_h)], fill="#dbeafe")
    d.rectangle([x0, int(y_h), x1, y1], fill="#9ca3af")
    d.rectangle([x0, y0, x1, y1], outline="black", width=2)

    dashed_line(d, (x0, y_h), (x1, y_h), "black", 3, 14, 10)
    d.text((x0 + 12, y_h - 30), "horizon band, y = 1443", font=font(21), fill="black")

    cx, cy, r = 500, y_s, 18
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append(xy(cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(star, fill="#facc15", outline="black")
    d.text((cx + 28, cy - 30), "WCS reference star", font=font(21), fill="black")
    d.text((cx + 28, cy - 2), "CRPIX2 = 660.07", font=font(19), fill="#333333")

    xm = 800
    d.line([xy(xm, y_s), xy(xm, y_h)], fill="black", width=2)
    d.line([xy(xm - 10, y_s), xy(xm + 10, y_s)], fill="black", width=2)
    d.line([xy(xm - 10, y_h), xy(xm + 10, y_h)], fill="black", width=2)
    d.text((xm + 18, (y_s + y_h) / 2 - 12), "Δy = 782.93 px", font=font(21), fill="black")

    box = [110, 1170, 890, 1235]
    d.rounded_rectangle(box, radius=10, fill="#fef3c7", outline="#92400e", width=2)
    center_text(
        d,
        ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
        "alt = (1443 − 660.07) × 45.9° / 1620 = 22.18°",
        font(23, True),
        "#78350f",
    )

    im.save(OUT / "07-altitude-diagram.png")
    print("07-altitude-diagram.png")


def viaduct_map() -> None:
    W, H = 1200, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    center_text(d, (W / 2, 40), "Candidate viaducts near the stated latitude", font(30, True))
    center_text(d, (W / 2, 80), "schematic; coordinates from OSM / Wikipedia", font(19), "#444444")

    left, right, top, bottom = 120, 1120, 140, 780
    lon0, lon1 = -2.56, -2.26
    lat0, lat1 = 54.08, 54.22

    def px(lon: float) -> float:
        return left + (lon - lon0) / (lon1 - lon0) * (right - left)

    def py(lat: float) -> float:
        return bottom - (lat - lat0) / (lat1 - lat0) * (bottom - top)

    for lon in [-2.55, -2.50, -2.45, -2.40, -2.35, -2.30]:
        x = px(lon)
        d.line([xy(x, top), xy(x, bottom)], fill="#e5e7eb", width=1)
        d.text((x - 28, bottom + 10), f"{lon:.2f}", font=font(17), fill="#333333")
    for lat in [54.08, 54.10, 54.12, 54.14, 54.16, 54.18, 54.20, 54.22]:
        y = py(lat)
        d.line([xy(left, y), xy(right, y)], fill="#e5e7eb", width=1)
        d.text((left - 75, y - 10), f"{lat:.2f}", font=font(17), fill="#333333")

    d.rectangle([left, top, right, bottom], outline="black", width=2)
    center_text(d, ((left + right) / 2, bottom + 42), "longitude (°E)", font(19))
    d.text((left, top - 35), "latitude (°N)", font=font(19), fill="black")

    yt = py(54.1116)
    dashed_line(d, (left, yt), (right, yt), "#dc2626", 2, 12, 8)
    d.text((left + 10, yt - 28), "target latitude 54.1116° N", font=font(19), fill="#dc2626")

    points = [
        ("Ribblehead", 54.2104, -2.3702, "#2563eb", (12, -30)),
        ("Clapham / Wenning", 54.1041, -2.4085, "#ea580c", (12, 10)),
        ("Skipton & Wennington", 54.1066, -2.4494, "#16a34a", (12, -50)),
        ("Helwith Bridge", 54.1235, -2.2909, "#7c3aed", (-165, -10)),
        ("Bentham line", 54.1125, -2.4911, "#92400e", (-150, 28)),
    ]
    for name, lat, lon, color, off in points:
        x, y = px(lon), py(lat)
        d.ellipse([xy(x - 6, y - 6), xy(x + 6, y + 6)], fill=color, outline="black")
        d.text((x + off[0], y + off[1]), name, font=font(18), fill=color)

    xr = px(-2.3702)
    yr = py(54.2104)
    yt2 = py(54.1116)
    dashed_line(d, (xr, yr), (xr, yt2), "#6b7280", 1, 6, 6)
    d.text((xr + 10, (yr + yt2) / 2 - 10), "≈ 11 km", font=font(17), fill="#4b5563")

    center_text(
        d,
        (W / 2, 845),
        "Ribblehead is visually close but about 11 km north of the target latitude.",
        font(17),
        "#4b5563",
    )

    im.save(OUT / "08-viaduct-candidates.png")
    print("08-viaduct-candidates.png")


def longitude_diagram() -> None:
    W, H = 1000, 1020
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    center_text(d, (W / 2, 40), "Longitude from sidereal time and right ascension", font(28, True))

    cx, cy, r = 500, 510, 300

    def point(ang: float, rr: float = r) -> tuple[float, float]:
        rad = math.radians(ang)
        return cx + rr * math.sin(rad), cy - rr * math.cos(rad)

    d.ellipse([xy(cx - r, cy - r), xy(cx + r, cy + r)], outline="black", width=2)
    for ang, lab in [(0, "0°"), (90, "90°"), (180, "180°"), (270, "270°")]:
        x, y = point(ang, r + 35)
        center_text(d, (x, y), lab, font(20))

    ra = 9.5355366203
    gst = 341.595636

    p_ra = point(ra)
    d.line([xy(cx, cy), xy(*p_ra)], fill="#9ca3af", width=2)
    sx, sy = p_ra
    star = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = 16 if i % 2 == 0 else 16 * 0.45
        star.append(xy(sx + rad * math.cos(a), sy + rad * math.sin(a)))
    d.polygon(star, fill="#facc15", outline="black")
    d.text((sx + 20, sy - 38), "RA = 9.5355°", font=font(20), fill="#111111")

    p_gst = point(gst)
    d.line([xy(cx, cy), xy(*p_gst)], fill="#16a34a", width=3)
    d.ellipse([xy(p_gst[0] - 9, p_gst[1] - 9), xy(p_gst[0] + 9, p_gst[1] + 9)],
              fill="#16a34a", outline="black")
    d.text((p_gst[0] - 185, p_gst[1] - 40), "GST = 341.5956°", font=font(20), fill="#166534")

    arc_r = 265
    a_start = ra
    a_end = gst - 360.0  # -18.4044, the short way from RA to GST
    arc = [point(a_start + (a_end - a_start) * i / 60, arc_r) for i in range(61)]
    d.line([xy(*p) for p in arc], fill="#dc2626", width=4)
    tip, prev = arc[-1], arc[-2]
    dx, dy = tip[0] - prev[0], tip[1] - prev[1]
    length = math.hypot(dx, dy) or 1.0
    arrow_head(d, tip, (dx / length, dy / length), 14, "#dc2626")

    mid = point((a_start + a_end) / 2, 220)
    center_text(d, mid, "−27.939901°", font(22, True), "#b91c1c")
    center_text(d, (mid[0], mid[1] + 27), "west", font(18), "#b91c1c")

    box = [80, 880, 920, 950]
    d.rounded_rectangle(box, radius=10, fill="#fef3c7", outline="#92400e", width=2)
    center_text(
        d,
        ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
        "longitude = GST − RA = 341.595636° − 9.535537° = −27.939901°",
        font(20, True),
        "#78350f",
    )
    center_text(d, (W / 2, 975), "negative = west of Greenwich", font(18), "#4b5563")

    im.save(OUT / "09-longitude-diagram.png")
    print("09-longitude-diagram.png")


if __name__ == "__main__":
    altitude_diagram()
    viaduct_map()
    longitude_diagram()
