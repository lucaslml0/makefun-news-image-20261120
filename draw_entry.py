#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world
news of Friday 20 November 2026. Pure PIL, flat colours, no assets.

Stories (all verified against reporting dated 20 Nov 2026):
 1. Trump says no rush on Iran decision; looks to 2027 (Reuters, 20 Nov)
 2. Cyclone Akvan landfall in Odisha; 300,000 evacuated (20 Nov)
 3. Kyiv hit by overnight Iskander missile barrage (early hours 20 Nov)
 4. Europe ready for talks with Russia, Berlin summit (BBC, 20 Nov)
 5. Anthropic's record $81.3bn IPO closes today; debut +17% (20 Nov)
 6. GTA 6 sales pass $1.8bn, outgrossing The Odyssey (reported 20 Nov)
Also-rans: Genoa airport drone shutdown; migrant boat sinks off Senegal;
Fiona the hippo dies at Cincinnati Zoo.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
CARD = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (74, 74, 66)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
TEAL = (14, 94, 84)
GREEN = (24, 120, 60)
DARK = (24, 34, 52)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_SERIF_BLACK = FONT_DIR + "NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = FONT_DIR + "NotoSerif-Bold.ttf"
F_SANS_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_SANS = FONT_DIR + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color=RED):
    f = font(F_SANS_BOLD, 18)
    d.text((x, y), text, font=f, fill=color)
    return y + 26


def headline(d, x, y, text, size, max_w, max_lines=3):
    f = font(F_SERIF_BOLD, size)
    lines = wrap(d, text, f, max_w)[:max_lines]
    return draw_lines(d, lines, x, y, f, INK, int(size * 1.12))


def caption(d, x, y, text, max_w, size=19, leading=25, max_lines=2):
    f = font(F_SANS, size)
    lines = wrap(d, text, f, max_w)[:max_lines]
    return draw_lines(d, lines, x, y, f, MUTED, leading)


def rule(d, x0, y, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def art_lead(d, x, y, w, h):
    """Globe over the Middle East + a 2027 calendar card + US flag bar."""
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    cx, cy, r = x + 105, y + 108, 78
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 150),
              outline=(220, 225, 230), width=3)
    for k in range(-2, 3):
        d.arc([cx - r + 18 * abs(k), cy - r, cx + r - 18 * abs(k), cy + r],
              90, 270, fill=(190, 205, 215), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(190, 205, 215), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
          fill=(190, 205, 215), width=2)
    mx, my = cx + 42, cy - 8
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=RED,
              outline=(255, 255, 255), width=2)
    d.line([(mx, my + 9), (mx, my + 26)], fill=RED, width=3)
    # calendar card: 2027
    bx, by, bw, bh = x + 205, y + 22, 112, 130
    d.rectangle([bx, by, bx + bw, by + bh], fill=CARD, outline=INK, width=3)
    d.rectangle([bx, by, bx + bw, by + 34], fill=RED)
    d.text((bx + bw // 2, by + 5), "2027", font=font(F_SANS_BOLD, 24),
           fill=(255, 255, 255), anchor="ma")
    d.text((bx + bw // 2, by + 48), "JAN 1", font=font(F_SANS_BOLD, 26),
           fill=INK, anchor="ma")
    d.text((bx + bw // 2, by + 84), "DECISION", font=font(F_SANS_BOLD, 17),
           fill=MUTED, anchor="ma")
    d.text((bx + bw // 2, by + 106), "WAITS", font=font(F_SANS_BOLD, 17),
           fill=MUTED, anchor="ma")
    # US flag bar under globe
    fx, fy, fw = x + 12, y + h - 34, 190
    for i in range(7):
        d.rectangle([fx, fy + i * 4, fx + fw, fy + i * 4 + 4],
                    fill=RED if i % 2 == 0 else CARD)
    d.rectangle([fx, fy, fx + 76, fy + 16], fill=(30, 50, 110))
    for sx in range(3):
        for sy in range(2):
            d.ellipse([fx + 8 + sx * 24, fy + 3 + sy * 7,
                       fx + 13 + sx * 24, fy + 8 + sy * 7], fill=(255, 255, 255))
    d.text((x + 218, y + h - 30), "NO RUSH",
           font=font(F_SANS_BOLD, 17), fill=(220, 225, 230))


# ---------------------------------------------------------------- cyclone art
def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 74, 96))
    cx, cy = x + 150, y + h // 2 + 2
    for i, r in enumerate(range(8, 38, 6)):
        d.arc([cx - r, cy - r, cx + r, cy + r], i * 55, i * 55 + 230,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # rain, top-left corner only
    for i, rx in enumerate(range(x + 12, x + 66, 18)):
        d.line([(rx, y + 10 + (i % 2) * 8), (rx - 6, y + 24 + (i % 2) * 8)],
               fill=(160, 200, 220), width=3)
    # coastline + shelters, right side
    d.line([(x + w - 96, y + h), (x + w - 46, y + 10)], fill=(247, 243, 232), width=4)
    d.polygon([(x + w - 88, y + h - 20), (x + w - 66, y + h - 42),
               (x + w - 44, y + h - 20)], fill=(247, 243, 232))
    d.polygon([(x + w - 42, y + h - 14), (x + w - 24, y + h - 32),
               (x + w - 8, y + h - 14)], fill=(200, 210, 215))


# ---------------------------------------------------------------- kyiv art
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 34))
    base = y + h
    for bx, bw, bh in [(8, 46, 30), (60, 30, 44), (96, 52, 26), (154, 34, 50),
                       (194, 44, 34), (244, 30, 54), (280, 52, 28), (338, 40, 42),
                       (384, 46, 32), (436, 30, 46)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(52, 58, 74))
        for wy in range(base - bh + 6, base - 5, 12):
            d.rectangle([x + bx + 6, wy, x + bx + 11, wy + 5], fill=(240, 200, 90))
    # missile trails + bursts
    d.line([(x + 60, y + 4), (x + 150, y + 38)], fill=(255, 190, 80), width=3)
    d.line([(x + 320, y + 2), (x + 260, y + 34)], fill=(255, 190, 80), width=3)
    d.ellipse([x + 56, y + 1, x + 66, y + 11], fill=(255, 220, 120))
    d.ellipse([x + 316, y + 0, x + 326, y + 10], fill=(255, 220, 120))
    for ex, ey in [(x + 150, y + 38), (x + 260, y + 34)]:
        for ang in range(0, 360, 45):
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([(ex, ey), (ex + dx * 13, ey + dy * 13)],
                   fill=(255, 140, 40), width=3)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 200, 80))


# ---------------------------------------------------------------- europe art
def art_europe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 110))
    cx, cy, r = x + 68, y + h // 2, 28
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 210, 60))
    d.text((cx, cy - 12), "EU", font=font(F_SANS_BOLD, 22),
           fill=(255, 255, 255), anchor="ma")
    d.text((cx, cy + 10), "TALKS", font=font(F_SANS_BOLD, 14),
           fill=(255, 255, 255), anchor="ma")
    fx = x + 128
    # UK
    d.rectangle([fx, y + 8, fx + 84, y + 28], fill=(28, 52, 110),
                outline=(255, 255, 255), width=2)
    d.line([(fx, y + 8), (fx + 84, y + 28)], fill=(255, 255, 255), width=2)
    d.line([(fx + 84, y + 8), (fx, y + 28)], fill=(255, 255, 255), width=2)
    d.line([(fx + 42, y + 8), (fx + 42, y + 28)], fill=RED, width=4)
    d.line([(fx, y + 18), (fx + 84, y + 18)], fill=RED, width=4)
    # Germany
    gy = y + 32
    d.rectangle([fx, gy, fx + 84, gy + 7], fill=(20, 20, 20))
    d.rectangle([fx, gy + 7, fx + 84, gy + 14], fill=RED)
    d.rectangle([fx, gy + 14, fx + 84, gy + 21], fill=(255, 210, 60))
    # France
    fy = y + 57
    d.rectangle([fx, fy, fx + 28, fy + 18], fill=(20, 60, 160))
    d.rectangle([fx + 28, fy, fx + 56, fy + 18], fill=(255, 255, 255))
    d.rectangle([fx + 56, fy, fx + 84, fy + 18], fill=RED)
    d.text((fx + 100, y + 20), "BERLIN", font=font(F_SANS_BOLD, 21),
           fill=(255, 255, 255))
    d.text((fx + 100, y + 46), "SUMMIT", font=font(F_SANS_BOLD, 21),
           fill=(255, 255, 255))


# ---------------------------------------------------------------- anthropic art
def art_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    d.text((x + 14, y + 6), "$81.3bn", font=font(F_SERIF_BLACK, 32), fill=INK)
    d.text((x + w - 96, y + 8), "+17%", font=font(F_SANS_BOLD, 26), fill=GREEN)
    d.text((x + w - 96, y + 38), "DAY ONE", font=font(F_SANS_BOLD, 13), fill=MUTED)
    # chart confined to the bottom band, below the text; ends before +17%
    pts = [(x + 14, y + h - 6), (x + 70, y + h - 12), (x + 120, y + h - 9),
           (x + 170, y + h - 18), (x + 225, y + h - 14), (x + 280, y + h - 24),
           (x + 330, y + h - 20)]
    d.polygon(pts + [(x + 330, y + h - 2), (x + 14, y + h - 2)],
              fill=(24, 120, 60, 36))
    d.line(pts, fill=GREEN, width=4)
    ax, ay = x + 330, y + h - 20
    d.polygon([(ax, ay), (ax - 22, ay + 2), (ax - 4, ay + 20)], fill=GREEN)


# ---------------------------------------------------------------- gta art
def art_gta(d, x, y, w, h):
    d.rounded_rectangle([x, y + 4, x + w, y + h - 4], radius=14, fill=INK)
    d.ellipse([x + 12, y + 12, x + 34, y + 34], fill=CARD)
    d.rectangle([x + 18, y + 8, x + 28, y + 38], fill=CARD)
    d.rectangle([x + 8, y + 18, x + 38, y + 28], fill=CARD)
    for i, c in enumerate([(255, 90, 90), (255, 210, 60), (90, 200, 120), (90, 140, 255)]):
        bx = x + w - 40 + (i % 2) * 18
        by = y + 12 + (i // 2) * 18
        d.ellipse([bx, by, bx + 14, by + 14], fill=c)


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im, "RGBA")
    M = 28

    # ---------------- masthead ----------------
    d.text((W // 2, 6), "WORLD NEWS", font=font(F_SERIF_BLACK, 92),
           fill=INK, anchor="ma")
    rule(d, M, 108, W - M, 3)
    d.text((M, 116), "FRIDAY 20 NOVEMBER 2026",
           font=font(F_SANS_BOLD, 24), fill=RED)
    d.text((W - M, 116), "THE DAY IN ONE PAGE",
           font=font(F_SANS_BOLD, 24), fill=INK, anchor="ra")
    rule(d, M, 148, W - M, 2)

    # ---------------- lead: Trump / Iran ----------------
    y = 162
    y = kicker(d, M, y, "WASHINGTON  •  IRAN", RED)
    y = headline(d, M, y, "No rush on Iran: Trump pushes war decision to 2027",
                 44, 600, max_lines=3)
    y = caption(d, M, y + 8,
                "The president says he will \u201csee what happens\u201d after "
                "Jan 1, as the US weighs strikes on Iran.",
                600, size=21, leading=28)
    art_lead(d, 656, 162, 340, 240)
    rule(d, M, 414, W - M, 2)

    # ---------------- row A: Akvan | Kyiv ----------------
    y0 = 428
    col_w = (W - 2 * M - 24) // 2
    x2 = M + col_w + 24
    y = kicker(d, M, y0, "INDIA  •  WEATHER", TEAL)
    y = headline(d, M, y, "Cyclone Akvan bears down on Odisha", 32, col_w, 2)
    y = caption(d, M, y + 4,
                "300,000 people moved to shelters as the storm nears "
                "landfall at noon; 423 rescue teams on alert.", col_w)
    art_cyclone(d, M, 580, col_w, 76)
    y = kicker(d, x2, y0, "UKRAINE  •  WAR", RED)
    y = headline(d, x2, y, "Kyiv hit by overnight missile barrage", 32, col_w, 2)
    y = caption(d, x2, y + 4,
                "Russian Iskander missiles strike the capital in the early "
                "hours; air defences fire back.", col_w)
    art_kyiv(d, x2, 580, col_w, 76)
    rule(d, M, 668, W - M, 2)

    # ---------------- row B: Europe | Anthropic ----------------
    y0 = 682
    y = kicker(d, M, y0, "EUROPE  •  DIPLOMACY", BLUE)
    y = headline(d, M, y, "Europe ready for talks with Russia", 32, col_w, 2)
    y = caption(d, M, y + 4,
                "Berlin summit: allies present a united front and say they "
                "will negotiate \u2014 if Kyiv is at the table.", col_w)
    art_europe(d, M, 834, col_w, 76)
    y = kicker(d, x2, y0, "MARKETS  •  TECH", GREEN)
    y = headline(d, x2, y, "Anthropic\u2019s record $81.3bn IPO closes today",
                 32, col_w, 2)
    y = caption(d, x2, y + 4,
                "Shares ended their Nasdaq debut up 17% at $97.17 after "
                "briefly topping a $2 trillion value.", col_w)
    art_anthropic(d, x2, 834, col_w, 76)
    rule(d, M, 922, W - M, 2)

    # ---------------- GTA 6 strip ----------------
    y = 934
    art_gta(d, M, y, 78, 44)
    d.text((M + 94, y + 1), "GTA 6 sales pass $1.8bn in a day",
           font=font(F_SERIF_BOLD, 26), fill=INK)
    d.text((M + 94, y + 33),
           "Rockstar\u2019s blockbuster outgrosses The Odyssey\u2019s entire global run within hours of launch.",
           font=font(F_SANS, 18), fill=MUTED)
    rule(d, M, 988, W - M, 2)

    # ---------------- also-rans ----------------
    y = 996
    d.text((M, y), "ALSO TODAY",
           font=font(F_SANS_BOLD, 17), fill=RED)
    items = [
        "Genoa airport shut by drones",
        "Migrant boat sinks off Senegal",
        "Fiona the hippo dies at zoo",
    ]
    x = M + 138
    f = font(F_SANS, 17)
    for it in items:
        d.text((x, y), it, font=f, fill=INK)
        x += d.textlength(it, font=f) + 24
        if it is not items[-1]:
            d.text((x - 17, y), "\u2022", font=f, fill=RED)

    im.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
