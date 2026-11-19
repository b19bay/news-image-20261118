#!/usr/bin/env python3
"""Render the news-image-20261118 front page: 42 verified stories, 18 Nov 2026.

Self-contained, stdlib + Pillow only. Usage:
    python3 render.py A out_a.png   # map on top, 6-col grid
    python3 render.py B out_b.png   # map on top (taller), 5-col grid
    python3 render.py C out_c.png   # map at bottom, 6-col grid
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (248, 244, 234)
INK = (26, 26, 26)
RED = (176, 42, 42)
NAVY = (30, 58, 95)
GREY = (90, 88, 82)
RULE = (200, 192, 172)
MAP_BG = (217, 232, 242)
LAND = (232, 220, 192)
LAND_EDGE = (180, 164, 128)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, path, size, max_w, max_lines):
    """Shrink font until text fits in max_lines; return (font, lines)."""
    s = size
    while s >= 8:
        fnt = font(path, s)
        lines = wrap(text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        s -= 1
    return font(path, 8), wrap(text, font(path, 8), max_w)[:max_lines]


# (number, section, colour, headline, sub-fact, lon, lat, dx, dy)
# lon/lat None = no map dot (deep space).
STORIES = [
    (1, "ASIA", (176, 124, 31), "Xi greets Trump on Shenzhen tarmac",
     "Three-way talks with Putin set for Thu 19 Nov", 114, 22.5, 0, -12),
    (2, "ASIA", (176, 124, 31), "Xi, Putin meet before three-way",
     "Talks in Shenzhen focus on Ukraine", 114, 22.5, 16, 0),
    (3, "ASIA", (176, 124, 31), "Quad leaders meet in Manila",
     "First leader-level Quad in over two years", 121, 14.6, 10, -6),
    (4, "ASIA", (176, 124, 31), "Trump meets Marcos in Manila",
     "US hails old Pacific alliance; trade deal", 121, 14.6, 20, 6),
    (5, "ASIA", (176, 124, 31), "Carney meets Xi at APEC",
     "Canada and China extend trade deals", 114, 22.5, -16, 4),
    (6, "ASIA", (176, 124, 31), "Myanmar to review its ASEAN ties",
     "Junta chief says bloc treated it poorly", 96, 21, 0, 0),
    (7, "ASIA", (176, 124, 31), "Xi vows open trade; Putin hits sanctions",
     "Putin calls the West \u201cformer hegemons\u201d", 114, 22.5, 4, 14),
    (8, "ASIA", (176, 124, 31), "Dhoni retires from IPL",
     "Chennai great, 45, becomes CSK mentor", 80.3, 13, 0, 0),
    (9, "GULF", (146, 32, 32), "Iran strikes Kuwait and Bahrain",
     "Drones hit Ali Al Salem Air Base", 48, 29.3, 0, 0),
    (10, "GULF", (146, 32, 32), "US hits missile site on Qeshm Island",
     "US aircraft strike in the Strait of Hormuz", 56.3, 26.9, 0, 0),
    (11, "GULF", (146, 32, 32), "Houthis claim pipeline strikes",
     "Five drones said sent at Saudi sites", 47, 25, 14, 10),
    (12, "GULF", (146, 32, 32), "Board of Peace faults both sides",
     "Both sides failed ceasefire pledges", 34.5, 31.5, -18, -12),
    (13, "GULF", (146, 32, 32), "Kahana elected Knesset speaker",
     "Win for PM-elect Eisenkot; vote 66-52", 35.2, 31.8, 12, -14),
    (14, "GULF", (146, 32, 32), "UK sanctions West Bank settlement firms",
     "Eight firms blacklisted over violence", 35.2, 32, 16, 10),
    (15, "EUROPE", (30, 58, 95), "Kerch Bridge hit again; span falls",
     "Third strike this week; traffic halted", 36.5, 45.3, 0, 0),
    (16, "EUROPE", (30, 58, 95), "Russia claims 1,441 drones a night",
     "Moscow claims a record wave", 37.6, 55.8, 0, 0),
    (17, "EUROPE", (30, 58, 95), "EU proposes \u20ac45bn loan for Ukraine",
     "Two-thirds of Kyiv\u2019s 2027 funding gap", 4.35, 50.85, 0, 0),
    (18, "EUROPE", (30, 58, 95), "Putin \u2018not ready\u2019 for peace talks",
     "Aims to fight on through winter, per intel", 37.6, 55.8, 14, 6),
    (19, "EUROPE", (30, 58, 95), "Pistorius rebukes US over strikes",
     "German minister calls criticism \u2018stupid\u2019", 13.4, 52.5, 0, 0),
    (20, "EUROPE", (30, 58, 95), "Burnham: Brexit hasn\u2019t worked",
     "UK leader seeks much closer EU ties", -0.1, 51.5, 0, 0),
    (21, "EUROPE", (30, 58, 95), "Lammy urges EU-rejoin pledge",
     "Labour should promise to rejoin, he says", -0.1, 51.5, -12, 12),
    (22, "EUROPE", (30, 58, 95), "UK inflation hits 3.6%",
     "October rate is the highest in a year", -0.1, 51.5, 12, 12),
    (23, "AMERICAS", (0, 102, 102), "Peltola wins Alaska Senate seat",
     "Democrats take a 56-44 majority", -150, 64, 0, 0),
    (24, "AMERICAS", (0, 102, 102), "US loses measles-free status",
     "Cases top 5,400 with 10 deaths", -100, 39, 0, -10),
    (25, "AMERICAS", (0, 102, 102), "Kalshi halts \u2018mention markets\u2019",
     "CFTC order ends wagers on Trump\u2019s words", -95, 38, 14, 10),
    (26, "AMERICAS", (0, 102, 102), "FAA halts router installs",
     "Routers like the one blamed in ground stop", -90, 37, -14, 10),
    (27, "AMERICAS", (0, 102, 102), "DHS: no ships for deportations",
     "Acting ICE chief confirms in a letter", -85, 36, 10, -12),
    (28, "AMERICAS", (0, 102, 102), "New Jersey sues DHS over detention",
     "State says ICE stonewalled Delaney Hall", -74.5, 40, 0, -14),
    (29, "AMERICAS", (0, 102, 102), "Students sue over AI gun alert",
     "Omnilert mistook chips for a gun", -76.6, 39.3, 16, 8),
    (30, "AMERICAS", (0, 102, 102), "Fed\u2019s Cook may skip firing hearing",
     "Won\u2019t attend Dec 14 unless Hassett goes", -77, 38.9, -14, 10),
    (31, "AMERICAS", (0, 102, 102), "Oversight letters to Trump allies",
     "Panel sends 12 preservation letters", -82, 38, 6, 14),
    (32, "AFRICA", (122, 90, 18), "Ebola in Congo tops 11,500 cases",
     "WHO counts 5,630 deaths, as of 16 Nov", 25, -2, 0, 0),
    (33, "AFRICA", (122, 90, 18), "Sudan-Ethiopia tensions escalate",
     "Each accuses the other of backing rebels", 30, 13, 0, 0),
    (34, "AFRICA", (122, 90, 18), "Ethiopia-Eritrea troops mass",
     "Forces near Badme within striking distance", 37.9, 14.7, 0, 0),
    (35, "CLIMATE", (34, 120, 60), "COP31 split as stocktake launches",
     "Antalya deadlocked; 21 issues unresolved", 30.7, 36.9, -14, -16),
    (36, "CLIMATE", (34, 120, 60), "Gaza cold kills in the tents",
     "950,000 displaced on flood-prone ground", 34.5, 31.5, -10, 14),
    (37, "SPACE", (90, 40, 120), "Voyager 1 one light-day out",
     "First human object 25.9bn km from Earth", None, None, 0, 0),
    (38, "TECH", (150, 60, 140), "Nvidia posts $115.8bn quarter",
     "Revenue doubles; board won\u2019t reinstate Huang", -121, 37.4, 0, 0),
    (39, "TECH", (150, 60, 140), "GTA VI rollout begins",
     "Vice City opens at midnight in New Zealand", 172.6, -41, 0, 0),
    (40, "TECH", (150, 60, 140), "OpenAI ships GPT-6.2 Astra and Sol",
     "New models; Astra priced 20% cheaper", -122.4, 37.8, 12, -8),
    (41, "TECH", (150, 60, 140), "Java4Shell flaw found by AI",
     "Critical Java bug found; Oracle patched", -100, 42, 0, 0),
    (42, "TECH", (150, 60, 140), "NATO taps OpenAI for cyber defence",
     "Alliance runs 300bn tokens a month", 4.35, 50.85, 16, -14),
]

NUMBERS = [
    ("25.9bn km", "Voyager 1 from Earth"),
    ("\u20ac45bn", "EU loan for Ukraine"),
    ("$115.8bn", "Nvidia revenue, Q3"),
    ("11,504", "Ebola cases in Congo"),
    ("5,400+", "US measles cases"),
    ("1,441", "drones in one night"),
]

# Simplified continent outlines, (lon, lat) points.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 18), (-100, 16), (-105, 20),
     (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58),
     (-150, 60), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76)],
    [(-80, 10), (-75, 5), (-70, 10), (-60, 8), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-73, -53), (-70, -40), (-72, -25), (-78, -15), (-80, -5)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (40, 15), (44, 11),
     (51, 11), (48, 2), (40, -5), (40, -15), (35, -25), (28, -33),
     (20, -35), (15, -30), (12, -18), (9, -2), (9, 4), (-8, 5), (-15, 11),
     (-17, 15), (-16, 25), (-10, 30)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (12, 66), (5, 60), (5, 58), (-2, 55), (-5, 50), (-2, 48),
     (-5, 44), (-9, 38)],
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (158, 50), (142, 45), (140, 40), (130, 35), (127, 33), (122, 30),
     (120, 25), (110, 20), (105, 10), (100, 8), (98, 15), (95, 16),
     (90, 22), (85, 20), (80, 15), (77, 8), (73, 20), (68, 23), (62, 25),
     (57, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36),
     (28, 40), (30, 45), (28, 55)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (117, -20)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (142, 42), (140, 38), (137, 35), (133, 34)],
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=RULE)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 170) / 360 * w
        d.line([(gx, y0), (gx, y0 + h)], fill=(200, 214, 226), width=1)
    for lat in range(-60, 76, 30):
        gy = y0 + (75 - lat) / 133 * h
        d.line([(x0, gy), (x0 + w, gy)], fill=(200, 214, 226), width=1)

    def px(lon, lat):
        return (x0 + (lon + 170) / 360 * w, y0 + (75 - lat) / 133 * h)

    for poly in CONTINENTS:
        d.polygon([px(lo, la) for lo, la in poly], fill=LAND, outline=LAND_EDGE)
    # numbered dots (small, so clustered regions stay readable)
    fnt = font(SANS_B, 7)
    for num, sec, col, head, sub, lon, lat, dx, dy in STORIES:
        if lon is None:
            continue
        cx, cy = px(lon, lat)
        cx += dx
        cy += dy
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline="white")
        t = str(num)
        tw = fnt.getlength(t)
        d.text((cx - tw / 2, cy - 5), t, font=fnt, fill="white")


def draw_grid(d, x0, y0, w, h, cols):
    rows = (len(STORIES) + cols - 1) // cols
    cw = w / cols
    ch = h / rows
    for idx, (num, sec, col, head, sub, lon, lat, dx, dy) in enumerate(STORIES):
        r, c = divmod(idx, cols)
        cx = x0 + c * cw
        cy = y0 + r * ch
        pad = 7
        # number badge + section tag
        d.ellipse([cx + pad, cy + pad, cx + pad + 20, cy + pad + 20],
                  fill=col)
        fnt_n = font(SANS_B, 11)
        t = str(num)
        d.text((cx + pad + 10 - fnt_n.getlength(t) / 2, cy + pad + 4),
               t, font=fnt_n, fill="white")
        fnt_tag = font(SANS_B, 10)
        d.text((cx + pad + 26, cy + pad + 5), sec, font=fnt_tag, fill=col)
        # headline, up to 3 lines
        hx = cx + pad
        hy = cy + pad + 24
        hw = cw - 2 * pad
        hf, hlines = fit(head, SANS_B, 13, hw, 2)
        for i, ln in enumerate(hlines):
            d.text((hx, hy + i * 14), ln, font=hf, fill=INK)
        # sub-fact, up to 2 lines
        sy = hy + len(hlines) * 14 + 2
        sf, slines = fit(sub, SANS, 10, hw, 2)
        for i, ln in enumerate(slines):
            d.text((hx, sy + i * 12), ln, font=sf, fill=GREY)
        # row rule
        if r < rows - 1:
            d.line([(cx + pad, cy + ch - 3), (cx + cw - pad, cy + ch - 3)],
                   fill=(225, 218, 200), width=1)


def draw_numbers(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    cw = w / len(NUMBERS)
    fnt_v = font(SANS_B, 24)
    fnt_l = font(SANS, 10)
    for i, (val, lab) in enumerate(NUMBERS):
        cx = x0 + i * cw + cw / 2
        vw = fnt_v.getlength(val)
        d.text((cx - vw / 2, y0 + 8), val, font=fnt_v, fill="white")
        lw = fnt_l.getlength(lab)
        d.text((cx - lw / 2, y0 + 38), lab, font=fnt_l, fill=(190, 205, 225))


def render(variant, out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 16
    # masthead
    title = "THE WORLD IN ONE DAY"
    f_title = font(SERIF_B, 52)
    d.text(((W - f_title.getlength(title)) / 2, 8), title, font=f_title, fill=INK)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    f_date = font(SANS_B, 30)
    d.text(((W - f_date.getlength(date)) / 2, 66), date, font=f_date, fill=RED)
    check = "The day\u2019s news, checked against the wires \u2014 nothing from before 13 November"
    f_check = font(SANS, 13)
    d.text(((W - f_check.getlength(check)) / 2, 100), check, font=f_check, fill=GREY)
    d.line([(mx, 120), (W - mx, 120)], fill=RED, width=3)

    map_label = "THE DAY ON THE MAP \u2014 every number is a story below"
    f_maplab = font(SANS_B, 12)
    note = "37 Voyager 1 is in deep space, off the map"
    f_note = font(SANS, 11)

    grid_y, grid_h = 0, 0
    if variant == "A":
        d.text((mx, 128), map_label, font=f_maplab, fill=NAVY)
        nw = f_note.getlength(note)
        d.text((W - mx - nw, 129), note, font=f_note, fill=GREY)
        draw_map(d, mx, 146, W - 2 * mx, 148)
        grid_y, grid_h = 302, 620
    elif variant == "B":
        d.text((mx, 128), map_label, font=f_maplab, fill=NAVY)
        nw = f_note.getlength(note)
        d.text((W - mx - nw, 129), note, font=f_note, fill=GREY)
        draw_map(d, mx, 146, W - 2 * mx, 168)
        grid_y, grid_h = 322, 600
    else:  # C: map at bottom
        grid_y, grid_h = 128, 640
        d.text((mx, 776), map_label, font=f_maplab, fill=NAVY)
        nw = f_note.getlength(note)
        d.text((W - mx - nw, 777), note, font=f_note, fill=GREY)
        draw_map(d, mx, 794, W - 2 * mx, 128)

    cols = 5 if variant == "B" else 6
    draw_grid(d, mx, grid_y, W - 2 * mx, grid_h, cols)

    # numbers strip + footer
    draw_numbers(d, 0, 930, W, 58)
    f_foot = font(SANS, 10)
    src = "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 NYT \u00b7 BBC \u00b7 WSJ \u00b7 UN News \u00b7 NASA \u00b7 WHO \u00b7 PAHO \u00b7 UNICEF"
    d.text((mx, 996), src, font=f_foot, fill=GREY)
    tail = "42 stories, each verified against two wires"
    tw = f_foot.getlength(tail)
    d.text((W - mx - tw, 996), tail, font=f_foot, fill=GREY)

    img.save(out_path, "PNG", optimize=True)
    print(out_path, img.size)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
