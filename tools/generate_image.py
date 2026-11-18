#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news image.

One 1024x1024 PNG, drawn with Pillow only, from the day's reported stories.
Run: python3 tools/generate_image.py  (writes entry.png next to main.ts)
Every story below was reported on 17 November 2026 in more than one
outlet searched for this entry (Reuters, Al Jazeera, Just Security and
others). No casualty figures are used: none was cross-checked.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (15, 42, 68)
PAPER = (253, 253, 248)
INK = (20, 20, 20)
GREY = (90, 90, 90)
RED = (178, 34, 34)
BLUE = (30, 90, 160)
GOLD = (200, 150, 30)
TEAL = (0, 120, 110)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, text, color):
    f = font(BOLD, 22)
    draw.text((x, y), text, font=f, fill=color)
    return y + 30


def headline(draw, x, y, text, fnt, max_w):
    return para(draw, x, y, text, fnt, max_w, leading=2)


def bridge(draw, x, y, w, h):
    """A river bridge with a broken span and a burst above it."""
    draw.rectangle([x, y, x + w, y + h], fill=(190, 220, 240))
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(70, 110, 160))
    # towers
    for tx in (x + 60, x + w - 90):
        draw.rectangle([tx, y + 30, tx + 28, y + h - 34], fill=NAVY)
    # deck, with a gap in the middle where the span broke
    draw.rectangle([x, y + 110, x + w // 2 - 30, y + 122], fill=INK)
    draw.rectangle([x + w // 2 + 30, y + 110, x + w, y + 122], fill=INK)
    # cables
    for cx in range(x + 20, x + w - 20, 44):
        draw.line([cx, y + 110, x + w // 2, y + 30], fill=GREY, width=2)
    # burst
    cx, cy = x + w // 2, y + 34
    for dx, dy in [(0, -26), (20, -18), (26, 0), (20, 18), (0, 26),
                   (-20, 18), (-26, 0), (-20, -18)]:
        draw.line([cx, cy, cx + dx, cy + dy], fill=(230, 120, 20), width=5)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(240, 180, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead: one date line, nothing at the right edge
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((32, 22), "THE WORLD IN ONE IMAGE", font=font(BOLD, 24),
           fill=(255, 210, 90))
    d.text((32, 62), "17 NOVEMBER 2026", font=font(BOLD, 48), fill=(255, 255, 255))
    d.text((720, 72), "TUESDAY", font=font(BOLD, 32), fill=(255, 255, 255))
    d.rectangle([0, 148, W, 154], fill=GOLD)

    # lead story: bridges, fixed box 164-468
    d.text((32, 168), "EUROPE  ·  WAR", font=font(BOLD, 22), fill=RED)
    d.text((32, 196), "BRIDGES UNDER FIRE", font=font(BOLD, 42),
           fill=INK)
    bridge(d, 32, 248, 600, 120)
    para(d, 32, 382, "Ukraine struck the Kerch bridge to Crimea again. "
         "Russia hit Kyiv's bridges over the Dnipro.",
         font(REG, 25), 600)
    # middle east, right column, same fixed box
    d.rectangle([672, 164, 992, 468], outline=RED, width=3)
    d.rectangle([672, 164, 992, 200], fill=RED)
    d.text((688, 172), "MIDDLE EAST", font=font(BOLD, 22), fill=(255, 255, 255))
    d.text((688, 212), "IRAN HITS BACK", font=font(BOLD, 30), fill=INK)
    para(d, 688, 252, "Iran fired drones at a US radar base in Bahrain; "
         "Bahrain said it intercepted them. Tankers were hit near "
         "Hormuz; a third US carrier arrived in the region.",
         font(REG, 22), 288)

    # middle row: three panels, fixed box 488-758
    panels = [
        ("ASIA  ·  DIPLOMACY", BLUE, "XI, TRUMP, PUTIN TO MEET",
         "The three leaders are set to meet Thu 19 Nov in Shenzhen, "
         "at APEC."),
        ("TECH  ·  MARKETS", TEAL, "AI CHIP CURBS BITE",
         "The US tightened AI-chip export rules. Stocks fell as "
         "Nvidia reported after the bell."),
        ("ISRAEL  ·  POLITICS", NAVY, "KNESSET TURNS",
         "Parliament elected Matan Kahana as speaker, a blow to "
         "Netanyahu's bloc."),
    ]
    x = 32
    for kick, color, head, body in panels:
        d.rectangle([x, 488, x + 304, 758], outline=color, width=3)
        d.rectangle([x, 488, x + 304, 520], fill=color)
        d.text((x + 12, 495), kick, font=font(BOLD, 17), fill=(255, 255, 255))
        yy = headline(d, x + 12, 532, head, font(BOLD, 29), 280)
        para(d, x + 12, yy + 6, body, font(REG, 22), 280)
        x += 320

    # also strip
    d.rectangle([0, 778, W, 784], fill=GOLD)
    yy = kicker(d, 32, 798, "ALSO ON 17 NOVEMBER", NAVY)
    items = [
        "France: public-sector strike, turnout down sharply.",
        "Japan scrambled jets after Russian aircraft entered its airspace.",
        "Geneva: 128 states debated a ban on killer robots.",
        "EU sanctioned 12 people and 101 entities over Russia.",
    ]
    for it in items:
        yy = para(d, 56, yy, "•  " + it, font(REG, 24), 920)
    d.rectangle([0, 972, W, H], fill=NAVY)
    d.text((32, 988), "Events reported on 17 November 2026  ·  One day, in one image",
           font=font(REG, 22), fill=(255, 255, 255))
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
