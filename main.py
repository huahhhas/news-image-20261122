#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Sunday 22 November 2026.

A newspaper front page summing up the day's world news in one 1024x1024
image. Pure Pillow drawing: no photos, no network, no randomness, so two
runs produce byte-identical output.

Run:  python3 main.py            (writes entry.png beside it)
      MAKEFUN_OUTPUT_DIR=out python3 main.py   (writes out/entry.png)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

PAPER = (246, 241, 227)   # newsprint cream
PANEL = (255, 253, 245)   # panel white
INK = (26, 26, 26)
RED = (176, 32, 32)
NAVY = (31, 58, 95)
TEAL = (46, 110, 106)
GREY = (110, 104, 90)
SKY = (207, 227, 238)
SEA = (31, 58, 95)

DEJAVU = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(DEJAVU, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(DEJAVU, "DejaVuSerif.ttf")
SANS = os.path.join(DEJAVU, "DejaVuSans.ttf")
SANS_B = os.path.join(DEJAVU, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, path, max_w, start, minimum=10):
    size = start
    while size > minimum and text_w(draw, text, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def panel(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANS_B, 16), fill=RED)


def headline(draw, x, y, text, fnt, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def deck(draw, x, y, text, size, max_w, leading):
    fnt = font(SANS, size)
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=(52, 52, 48))
        y += leading
    return y


# ---------------------------------------------------------------- scenes

def scene_lead(draw, x0, y0, x1, y1):
    """Baltic sea, burning cargo ship, two drones overhead."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # clouds
    for cx, cy, rx, ry in [(x0 + 90, y0 + 26, 46, 12), (x0 + 150, y0 + 40, 34, 10),
                           (x1 - 120, y0 + 22, 52, 12), (x1 - 200, y0 + 44, 30, 9)]:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 255, 255))
    # sea
    sea_y = y0 + 88
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wy in (sea_y + 22, sea_y + 48, sea_y + 72):
        for wx in range(x0 + 12, x1 - 40, 72):
            draw.arc([wx, wy, wx + 44, wy + 14], 200, 340, fill=(180, 205, 225), width=2)
    # ship hull
    hx0, hx1 = x0 + 330, x0 + 660
    hy = sea_y + 6
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 34, hy + 34), (hx0 + 30, hy + 34)],
                 fill=(34, 34, 34))
    draw.rectangle([hx0 + 6, hy - 6, hx1 - 6, hy + 2], fill=(176, 32, 32))
    # containers
    conts = [(hx0 + 34, (198, 84, 44)), (hx0 + 92, (46, 110, 106)),
             (hx0 + 150, (176, 32, 32)), (hx0 + 208, (198, 140, 40))]
    for cx, col in conts:
        draw.rectangle([cx, hy - 44, cx + 52, hy - 8], fill=col, outline=INK, width=1)
    # funnel + smoke
    draw.rectangle([hx1 - 78, hy - 66, hx1 - 44, hy - 8], fill=(240, 200, 60),
                   outline=INK, width=1)
    for i, (sx, sy, sr) in enumerate([(hx1 - 60, hy - 52, 9), (hx1 - 48, hy - 64, 11),
                                      (hx1 - 32, hy - 74, 13)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))
    # fire on the containers
    fx = hx0 + 150
    draw.polygon([(fx, hy - 44), (fx + 14, hy - 78), (fx + 28, hy - 44)], fill=(240, 120, 20))
    draw.polygon([(fx + 8, hy - 44), (fx + 18, hy - 66), (fx + 30, hy - 44)], fill=(250, 210, 40))
    # drones + dotted paths
    for dx, dy in [(x0 + 150, y0 + 34), (x1 - 170, y0 + 26)]:
        draw.line([(dx - 70, dy + 26), (dx - 8, dy + 4)], fill=INK, width=1)
        for t in range(0, 62, 10):
            px = dx - 70 + t
            py = dy + 26 - int(t * 0.35)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
        draw.line([dx - 16, dy, dx + 16, dy], fill=INK, width=3)
        draw.line([dx, dy - 10, dx, dy + 10], fill=INK, width=3)
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(60, 60, 60))
        draw.line([dx - 22, dy - 12, dx + 22, dy - 12], fill=INK, width=2)
    # caption tag
    draw.text((x1 - 12, y1 - 24), "THE SPARTA II, GULF OF FINLAND",
              font=font(SANS_B, 13), fill=(255, 255, 255), anchor="ra")


def scene_quake(draw, x0, y0, x1, y1):
    """Andes peaks and a seismograph strip with the magnitude."""
    draw.rectangle([x0, y0, x1, y1], fill=(242, 227, 200))
    draw.polygon([(x0, y1), (x0 + 70, y0 + 34), (x0 + 150, y1)], fill=(138, 123, 102))
    draw.polygon([(x0 + 110, y1), (x0 + 190, y0 + 18), (x0 + 280, y1)], fill=(110, 95, 76))
    draw.polygon([(x0 + 182, y0 + 26), (x0 + 190, y0 + 18), (x0 + 198, y0 + 26),
                  (x0 + 190, y0 + 34)], fill=(255, 255, 255))
    # seismograph strip
    sx0, sy0, sx1, sy1 = x0 + 8, y1 - 34, x1 - 8, y1 - 8
    draw.rectangle([sx0, sy0, sx1, sy1], fill=(255, 255, 255), outline=INK, width=1)
    mid = (sy0 + sy1) // 2
    pts = [(sx0 + 4, mid)]
    jolts = [0, 2, -3, 4, -14, 18, -22, 10, -6, 3, -2, 0, 0]
    step = (sx1 - sx0 - 8) / max(1, len(jolts) - 1)
    for i, j in enumerate(jolts):
        pts.append((sx0 + 4 + i * step, mid + j))
    pts.append((sx1 - 4, mid))
    draw.line(pts, fill=RED, width=2)
    # magnitude
    draw.text((x1 - 16, y0 + 8), "6.7", font=font(SERIF, 46), fill=RED, anchor="ra")


def scene_mexico(draw, x0, y0, x1, y1):
    """Sinaloa desert, mountains, helicopter, badge star."""
    draw.rectangle([x0, y0, x1, y1], fill=(246, 217, 168))
    draw.ellipse([x1 - 66, y0 + 8, x1 - 26, y0 + 48], fill=(240, 190, 70))
    draw.polygon([(x0, y1 - 30), (x0 + 90, y0 + 30), (x0 + 190, y1 - 30)],
                 fill=(122, 88, 110))
    draw.polygon([(x0 + 150, y1 - 30), (x0 + 250, y0 + 16), (x0 + 350, y1 - 30)],
                 fill=(96, 70, 88))
    draw.rectangle([x0, y1 - 30, x1, y1], fill=(201, 143, 74))
    draw.polygon([(x0 + 40, y1), (x0 + 150, y1 - 30), (x0 + 190, y1 - 30), (x0 + 90, y1)],
                 fill=(90, 70, 60))
    # helicopter
    hx, hy = x0 + 300, y0 + 30
    draw.line([hx - 46, hy - 14, hx + 46, hy - 14], fill=INK, width=3)
    draw.ellipse([hx - 26, hy - 8, hx + 26, hy + 10], fill=(40, 40, 40))
    draw.line([hx + 24, hy, hx + 52, hy - 8], fill=INK, width=3)
    draw.line([hx + 50, hy - 18, hx + 50, hy + 2], fill=INK, width=2)
    # badge star
    draw.polygon(star_points(x0 + 52, y0 + 44, 26, 11), fill=(250, 210, 40),
                 outline=INK, width=1)


def scene_cop31(draw, x0, y0, x1, y1):
    """Globe and thermometer for the climate talks."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 238, 232))
    gx, gy, gr = x0 + 62, y0 + 40, 34
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(127, 179, 213),
                 outline=NAVY, width=2)
    draw.ellipse([gx - 18, gy - 22, gx + 2, gy - 2], fill=(96, 160, 96))
    draw.ellipse([gx - 2, gy + 4, gx + 20, gy + 22], fill=(96, 160, 96))
    draw.ellipse([gx + 8, gy - 24, gx + 24, gy - 8], fill=(96, 160, 96))
    # thermometer
    tx = x1 - 52
    draw.rounded_rectangle([tx - 7, y0 + 8, tx + 7, y1 - 22], radius=7,
                           fill=(255, 255, 255), outline=INK, width=1)
    draw.ellipse([tx - 13, y1 - 30, tx + 13, y1 - 4], fill=RED, outline=INK, width=1)
    draw.rectangle([tx - 4, y0 + 18, tx + 4, y1 - 18], fill=RED)
    # rising heat lines
    for i, lx in enumerate((x0 + 130, x0 + 160, x0 + 190)):
        draw.line([(lx, y1 - 12 - i * 4), (lx, y0 + 26)], fill=(200, 90, 40), width=2)
    draw.text((x0 + 118, y0 + 6), "ANTALYA", font=font(SANS_B, 15), fill=TEAL)


def scene_trump(draw, x0, y0, x1, y1):
    """Two framed panels: Yalta 1945 and Shenzhen 2026, three leaders each."""
    half = (x1 - x0 - 12) // 2
    frames = [(x0, "1945", "YALTA", (216, 201, 163), (70, 60, 50)),
              (x0 + half + 12, "2026", "SHENZHEN", (191, 211, 230), NAVY)]
    for fx, year, city, bg, fg in frames:
        draw.rectangle([fx, y0, fx + half, y1], fill=bg, outline=INK, width=1)
        for i, cx in enumerate((fx + half // 4, fx + half // 2, fx + 3 * half // 4)):
            cy = y0 + 34
            draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=fg)
            draw.polygon([(cx - 16, y1 - 16), (cx - 10, cy + 10), (cx + 10, cy + 10),
                          (cx + 16, y1 - 16)], fill=fg)
        draw.text((fx + 6, y0 + 4), year, font=font(SANS_B, 13), fill=fg)
        draw.text((fx + half - 6, y0 + 4), city, font=font(SANS_B, 12), fill=fg,
                  anchor="ra")


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((MARGIN, 22), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 19), fill=RED)
    d.text((W - MARGIN, 22), "WORLD EDITION", font=font(SANS_B, 19), fill=INK, anchor="ra")
    d.line([(MARGIN, 48), (W - MARGIN, 48)], fill=INK, width=2)
    title_f = fit_font(d, "THE WORLD TODAY", SERIF, CW, 92)
    d.text((W // 2, 54), "THE WORLD TODAY", font=title_f, fill=INK, anchor="ma")
    d.text((W // 2, 140), "THE DAY'S WORLD NEWS  —  IN ONE PAGE",
           font=font(SANS, 16), fill=GREY, anchor="ma")
    d.line([(MARGIN, 164), (W - MARGIN, 164)], fill=INK, width=3)
    d.line([(MARGIN, 168), (W - MARGIN, 168)], fill=INK, width=1)

    # ---- lead story
    lx0, ly0, lx1, ly1 = MARGIN, 178, W - MARGIN, 470
    panel(d, lx0, ly0, lx1, ly1)
    scene_lead(d, lx0 + 2, ly0 + 2, lx1 - 2, ly0 + 162)
    kicker(d, lx0 + 16, ly0 + 172, "GULF OF FINLAND  ·  THE BALTIC SEA")
    hf = fit_font(d, "DRONES SET RUSSIAN CARGO SHIP ABLAZE", SERIF, CW - 32, 40)
    y = headline(d, lx0 + 16, ly0 + 196, "DRONES SET RUSSIAN CARGO SHIP ABLAZE",
                 hf, CW - 32, 46)
    deck(d, lx0 + 16, y + 4,
         "Two drones struck the Sparta II, bound for Kaliningrad, on Saturday "
         "morning. The ship caught fire and drifted into Finnish waters as "
         "Helsinki tightened air and sea security.",
         18, CW - 32, 23)

    # ---- second row: quake + cartel capture
    row2_y, row2_h = 482, 218
    pw = 472
    for px0, scene, kick, head, body in [
        (MARGIN, scene_quake, "PERU  ·  THE ANDES",
         "6.7 QUAKE SHAKES PERU'S ANDES",
         "A magnitude 6.7 tremor near Junin shook central Peru and was felt in "
         "Lima. Officials reported no deaths and no serious damage."),
        (MARGIN + pw + 24, scene_mexico, "MEXICO  ·  SINALOA",
         "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         "Troops seized Fausto Isidro Meza Flores, an FBI most-wanted cartel "
         "boss, in Guasave, Sinaloa. Gunmen answered with blockades and attacks."),
    ]:
        px1 = px0 + pw
        panel(d, px0, row2_y, px1, row2_y + row2_h)
        scene(d, px0 + 2, row2_y + 2, px1 - 2, row2_y + 98)
        kicker(d, px0 + 14, row2_y + 106, kick)
        hf = fit_font(d, head, SERIF, pw - 28, 29)
        y = headline(d, px0 + 14, row2_y + 128, head, hf, pw - 28, 33)
        deck(d, px0 + 14, y + 2, body, 15, pw - 28, 19)

    # ---- third row: COP31 + Trump post
    row3_y, row3_h = 712, 182
    for px0, scene, kick, head, body in [
        (MARGIN, scene_cop31, "ANTALYA, TURKIYE  ·  CLIMATE",
         "COP31 TALKS DEADLOCK OVER FOSSIL FUELS",
         "The climate summit ran past its Friday deadline with no final deal, "
         "split over fossil fuels, money and science."),
        (MARGIN + pw + 24, scene_trump, "WASHINGTON  ·  SHENZHEN",
         "TRUMP'S 'GREAT POWERS' POST ECHOES YALTA",
         "The president posted a two-panel image pairing the 1945 Yalta photo "
         "with his Shenzhen meeting alongside Xi and Putin."),
    ]:
        px1 = px0 + pw
        panel(d, px0, row3_y, px1, row3_y + row3_h)
        scene(d, px0 + 2, row3_y + 2, px1 - 2, row3_y + 78)
        kicker(d, px0 + 14, row3_y + 84, kick)
        hf = fit_font(d, head, SERIF, pw - 28, 25)
        y = headline(d, px0 + 14, row3_y + 104, head, hf, pw - 28, 28)
        deck(d, px0 + 14, y + 1, body, 14, pw - 28, 17)

    # ---- bottom band: also today
    by0, by1 = 906, 996
    panel(d, MARGIN, by0, W - MARGIN, by1)
    d.text((MARGIN + 14, by0 + 8), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    ticker = ("Russian missile hits Kryvyi Rih, killing 2 and wounding 60  ·  "
              "Denmark expels a Russian diplomat over an alleged murder plot  ·  "
              "Trump calls the reported FBI database breach \u201cnot good\u201d  ·  "
              "S&P 500 falls 3.7% as AI stocks slide  ·  "
              "Harden passes Kobe on 50-point games  ·  "
              "BepiColombo arrives at Mercury")
    lines = wrap(d, ticker, font(SANS, 16), CW - 28)
    y = by0 + 32
    for line in lines:
        d.text((MARGIN + 14, y), line, font=font(SANS, 16), fill=INK)
        y += 20

    d.text((W // 2, 1006), "All stories as reported on the day  ·  Sunday 22 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        out_dir = os.path.dirname(os.path.abspath(__file__))
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
