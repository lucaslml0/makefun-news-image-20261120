#!/usr/bin/env python3
"""Draw a one-page newspaper front page summing up the world news of
Friday 20 November 2026. Output: entry.png, 1024x1024, PNG.

Everything on the page is drawn with PIL primitives and DejaVu fonts;
no external images, no network access.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (26, 26, 26)
PAPER = (253, 246, 233)
RED = (139, 26, 26)
RULE = (120, 110, 95)
MUTED = (90, 84, 72)
TINT = (243, 234, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, w, kicker, headline, body,
               head_size=27, body_size=19, head_font=SERIF_B):
    """Draw one story inside a box starting at (x, y); return bottom y."""
    pad = 16
    inner = w - 2 * pad
    cx = x + pad
    cy = y + 10
    kf = font(SANS_B, 18)
    draw.text((cx, cy), kicker, font=kf, fill=RED)
    cy += 26
    hf = font(head_font, head_size)
    for line in wrap(draw, headline, hf, inner):
        draw.text((cx, cy), line, font=hf, fill=INK)
        cy += head_size + 8
    cy += 2
    bf = font(SANS, body_size)
    for line in wrap(draw, body, bf, inner):
        draw.text((cx, cy), line, font=bf, fill=INK)
        cy += body_size + 7
    return cy + 8


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 34                      # side margin
    cw = W - 2 * mx              # content width

    # ---- Masthead ----
    y = 26
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 58)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 76
    draw.line([(mx, y), (W - mx, y)], fill=RULE, width=2)
    y += 10
    date_line = "FRIDAY  \u00b7  20 NOVEMBER 2026"
    df = font(SANS_B, 30)
    dw = draw.textlength(date_line, font=df)
    draw.text(((W - dw) / 2, y), date_line, font=df, fill=RED)
    y += 40
    draw.line([(mx, y), (W - mx, y)], fill=INK, width=3)
    y += 12

    # ---- Lead story: Shenzhen summit ----
    lead_top = y
    lead_h = 216
    draw.rectangle([mx, lead_top, W - mx, lead_top + lead_h], fill=TINT)
    draw.rectangle([mx, lead_top, W - mx, lead_top + lead_h],
                   outline=INK, width=2)
    bottom = draw_story(
        draw, mx, lead_top, cw,
        "DIPLOMACY  \u00b7  SHENZHEN, CHINA",
        "Trump, Xi and Putin sign joint peace declaration",
        "The three leaders met for the first time and pledged that nuclear "
        "war must never be fought. But after about 70 minutes of talks, "
        "there was no deal on Ukraine, Iran or nuclear arms.",
        head_size=35, body_size=21)
    assert bottom <= lead_top + lead_h, (bottom, lead_top + lead_h)
    y = lead_top + lead_h + 12

    # ---- Grid: four stories, 2 x 2 ----
    gap = 12
    col_w = (cw - gap) // 2
    row_h = 216
    grid = [
        ("JUSTICE  \u00b7  THE HAGUE",
         "World court: Myanmar committed genocide",
         "The ICJ ruled 9\u20136 that Myanmar\u2019s 2017 campaign against the "
         "Rohingya was genocide \u2014 a first against any state. "
         "Myanmar called it \u201cunfair\u201d."),
        ("WAR  \u00b7  KYIV, UKRAINE",
         "Russian missiles strike Kyiv overnight",
         "Overnight strikes hit bridges and infrastructure, killing at "
         "least three people. The Austrian and Dutch embassies were "
         "damaged; staff escaped unharmed."),
        ("CONFLICT  \u00b7  RIYADH, SAUDI ARABIA",
         "Houthi missile hits Riyadh\u2019s tallest tower",
         "A missile struck the PIF Tower in the financial district, "
         "blowing out windows across several floors. No injuries were "
         "reported."),
        ("MARKETS  \u00b7  NEW YORK & TOKYO",
         "Stocks slide as AI doubts spread",
         "The S&P 500 fell about 3.7% on Friday and Japan\u2019s Nikkei "
         "dropped about 5% as AI shares sold off. Anthropic slid about "
         "11% a day after its debut."),
    ]
    for row in range(2):
        for col in range(2):
            kicker, headline, body = grid[row * 2 + col]
            bx = mx + col * (col_w + gap)
            by = y + row * (row_h + gap)
            draw.rectangle([bx, by, bx + col_w, by + row_h],
                           outline=RULE, width=1)
            end = draw_story(draw, bx, by, col_w, kicker, headline, body,
                           head_size=26, body_size=18)
            assert end <= by + row_h, (kicker, end, by + row_h)
    y += 2 * row_h + gap + 12

    # ---- Bottom strip: COP31 ----
    strip_h = 134
    draw.rectangle([mx, y, W - mx, y + strip_h], fill=TINT)
    draw.rectangle([mx, y, W - mx, y + strip_h], outline=INK, width=2)
    end = draw_story(
        draw, mx, y, cw,
        "CLIMATE  \u00b7  ANTALYA, T\u00dcRKIYE",
        "COP31 draft drops fossil-fuel phase-out",
        "The latest draft deal removes all mention of moving away from "
        "coal, oil and gas \u2014 and drops a $120bn adaptation-finance "
        "target \u2014 as nearly 200 nations race Friday\u2019s deadline.",
        head_size=28, body_size=19)
    assert end <= y + strip_h, (end, y + strip_h)
    y += strip_h + 10

    # ---- Footer: sources ----
    foot = ("Sources: Reuters \u00b7 UN News \u00b7 ICJ / UN Mechanism for Myanmar "
            "\u00b7 Euronews \u00b7 One Turn \u2014 all dated 20 November 2026")
    ff = font(SANS, 15)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, y), foot, font=ff, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size,
          os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
