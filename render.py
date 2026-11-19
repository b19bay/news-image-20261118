#!/usr/bin/env python3
"""news-image-20261118 v3 renderer — hero + list front page, code-drawn.

Draws 'Wednesday 18 November 2026' as a newspaper front page: 11 hero
stories with flat code-drawn illustration panels, then a compact numbered
list of 27 more stories, a dotted world map with pins, a day-in-numbers
strip and a DATE CHECK box. All 38 stories happened or were first
reported on Wednesday 18 November 2026. PIL only, DejaVu/Liberation fonts.
Usage: python3 render.py [A|B|C]   (writes entry-<variant>.png)
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
NAVY = (16, 39, 63)
RED = (179, 38, 30)
GOLD = (201, 162, 39)

FONT_PATHS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "serif_b"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "serif"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "sans_b"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "sans"),
    ("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", "serif_b"),
    ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", "serif"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "sans_b"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "sans"),
]
FONTS = {}


def load_fonts():
    for path, kind in FONT_PATHS:
        if kind not in FONTS:
            FONTS[kind] = path


def font(kind, size):
    p = FONTS.get(kind)
    if p is None:
        return ImageFont.load_default()
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, spacing=2, max_lines=None):
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# ---------------- flat illustration panels ----------------
def panel_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.ellipse([x + w - 52, y + 8, x + w - 18, y + 42], fill=(245, 190, 80))
    for bx, bw, bh in [(0, 46, 58), (52, 34, 84), (92, 40, 66), (138, 30, 92), (174, 44, 70)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(52, 74, 96))
        d.rectangle([x + bx + 6, y + h - bh - 10, x + bx + bw - 6, y + h - bh], fill=(52, 74, 96))
    d.ellipse([x + 8, y + 16, x + 30, y + 34], fill=(255, 255, 255))
    d.ellipse([x + 24, y + 8, x + 44, y + 24], fill=(255, 255, 255))
    cx, cy = x + w // 2 + 30, y + 34
    d.ellipse([cx - 42, cy - 5, cx + 42, cy + 5], fill=(255, 255, 255))
    d.polygon([(cx + 8, cy - 4), (cx + 30, cy - 22), (cx + 38, cy - 22), (cx + 20, cy - 3)], fill=(230, 240, 248))
    d.polygon([(cx - 6, cy + 4), (cx - 26, cy + 20), (cx - 18, cy + 20), (cx + 4, cy + 5)], fill=(230, 240, 248))
    d.polygon([(cx + 38, cy - 3), (cx + 54, cy - 18), (cx + 58, cy - 18), (cx + 46, cy - 1)], fill=(200, 214, 228))


def panel_dome(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 30, 54))
    for sx, sy in [(20, 18), (60, 30), (110, 14), (160, 26), (200, 16), (240, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.arc([x + 30, y + h - 78, x + 150, y + h + 30], 180, 360, fill=(210, 220, 235), width=5)
    d.rectangle([x + 28, y + h - 34, x + 152, y + h], fill=(150, 165, 185))
    for tx, ty in [(170, 30), (205, 55), (230, 22)]:
        d.line([x + tx, y + ty, x + tx + 26, y + ty + 34], fill=(245, 180, 60), width=2)
        d.ellipse([x + tx + 24, y + ty + 32, x + tx + 30, y + ty + 38], fill=(245, 180, 60))
    for bx, by, s in [(185, 60, 9), (225, 70, 7), (160, 80, 6)]:
        for k in range(8):
            a = k * math.pi / 4
            d.line([x + bx, y + by, x + bx + s * math.cos(a), y + by + s * math.sin(a)],
                   fill=(255, 200, 90), width=2)


def panel_satellite(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 40))
    for sx, sy in [(16, 14), (48, 30), (90, 10), (140, 26), (190, 12), (230, 34), (260, 18)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x - 40, y + h - 50, x + 90, y + h + 60], fill=(38, 90, 140))
    d.ellipse([x + 6, y + h - 26, x + 60, y + h + 20], fill=(70, 140, 90))
    cx, cy = x + w // 2 + 40, y + h // 2 - 6
    d.rectangle([cx - 34, cy - 8, cx + 6, cy + 8], fill=(200, 210, 225))
    d.rectangle([cx + 6, cy - 3, cx + 52, cy + 3], fill=(150, 165, 190))
    d.rectangle([cx - 66, cy - 3, cx - 34, cy + 3], fill=(150, 165, 190))
    d.ellipse([cx + 52, cy - 12, cx + 76, cy + 12], fill=(220, 225, 235))
    d.line([cx - 10, cy + 26, cx - 60, cy + 58], fill=(245, 200, 90), width=2)
    for i in range(4):
        d.ellipse([cx - 10 - i * 13, cy + 26 + i * 8, cx - 6 - i * 13, cy + 30 + i * 8],
                  fill=(245, 200, 90))


def panel_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 74))
    d.ellipse([x + w - 46, y + 10, x + w - 14, y + 42], fill=(240, 220, 170))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(40, 44, 52))
    for dx, dy, s in [(40, 30, 16), (120, 20, 20), (200, 38, 14)]:
        d.ellipse([x + dx - s // 2, y + dy - s // 4, x + dx + s // 2, y + dy + s // 4], fill=(30, 30, 34))
        for ox in (-s // 2, s // 2):
            d.line([x + dx + ox - 7, y + dy - 6, x + dx + ox + 7, y + dy - 6], fill=(180, 190, 200), width=2)
    for bx, by, s in [(70, 62, 8), (170, 70, 10), (230, 58, 7)]:
        for k in range(8):
            a = k * math.pi / 4
            d.line([x + bx, y + by, x + bx + s * math.cos(a), y + by + s * math.sin(a)],
                   fill=(255, 190, 80), width=2)


def panel_fed(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(180, 172, 150))
    d.polygon([(x + w // 2 - 62, y + 26), (x + w // 2 + 62, y + 26), (x + w // 2, y + 6)],
              fill=(90, 100, 112))
    for i in range(5):
        cx = x + 22 + i * ((w - 44) // 4)
        d.rectangle([cx - 9, y + 30, cx + 9, y + h - 22], fill=(245, 243, 235))
        d.rectangle([cx - 12, y + 26, cx + 12, y + 30], fill=(200, 194, 178))
    d.rectangle([x + 18, y + h - 22, x + w - 18, y + h - 16], fill=(90, 100, 112))
    d.line([x + w - 30, y + 10, x + w - 30, y + 44], fill=(60, 60, 60), width=2)
    d.polygon([(x + w - 30, y + 10), (x + w - 8, y + 16), (x + w - 30, y + 22)], fill=(179, 38, 30))


def panel_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 90, 130))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 120, 80))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r in (52, 40, 28, 16):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 500, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    for rx in range(0, w, 18):
        d.line([x + rx, y + 12, x + rx - 6, y + 26], fill=(200, 220, 240), width=2)
    d.ellipse([x + 12, y + 12, x + 26, y + 24], fill=(245, 200, 90))


def panel_desert(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 160))
    d.ellipse([x + w - 50, y + 8, x + w - 16, y + 42], fill=(240, 170, 60))
    d.polygon([(x, y + h), (x + 70, y + h - 44), (x + 150, y + h)], fill=(210, 180, 120))
    d.polygon([(x + 120, y + h), (x + 200, y + h - 52), (x + w, y + h)], fill=(196, 164, 104))
    for dx, dy, s in [(60, 26, 14), (150, 18, 18), (220, 30, 12)]:
        d.ellipse([x + dx - s // 2, y + dy - s // 4, x + dx + s // 2, y + dy + s // 4], fill=(40, 38, 34))
        for ox in (-s // 2, s // 2):
            d.line([x + dx + ox - 6, y + dy - 5, x + dx + ox + 6, y + dy - 5], fill=(120, 110, 95), width=2)
    d.ellipse([x + 30, y + h - 30, x + 44, y + h - 16], fill=(120, 100, 70))
    d.ellipse([x + 44, y + h - 24, x + 58, y + h - 12], fill=(120, 100, 70))


def panel_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w // 2, y + h // 2
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + 34 * math.cos(a), cy + 34 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(255, 204, 0))
    d.text((x + 10, y + h - 21), "€45bn for Ukraine", font=font("sans_b", 12), fill=(0, 51, 153))


def panel_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    d.line([x + 14, y + 12, x + 14, y + h - 14], fill=(60, 60, 60), width=2)
    d.line([x + 14, y + h - 14, x + w - 10, y + h - 14], fill=(60, 60, 60), width=2)
    bars = [(26, 34, (120, 130, 150)), (66, 48, (90, 110, 140)), (106, 40, (120, 130, 150)),
            (146, 62, (60, 90, 130)), (186, 78, (179, 38, 30))]
    for bx, bh, col in bars:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 26, y + h - 14], fill=col)
    d.line([x + 20, y + h - 26, x + w - 16, y + 16], fill=(179, 38, 30), width=3)
    d.polygon([(x + w - 16, y + 16), (x + w - 30, y + 14), (x + w - 22, y + 28)], fill=(179, 38, 30))
    d.text((x + w - 58, y + 4), "3.6%", font=font("sans_b", 15), fill=(179, 38, 30))


def panel_tank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 180))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(150, 130, 90))
    d.ellipse([x + 30, y + 14, x + 44, y + 26], fill=(200, 200, 200))
    d.ellipse([x + 52, y + 8, x + 70, y + 24], fill=(200, 200, 200))
    d.rectangle([x + 40, y + h - 52, x + 190, y + h - 30], fill=(74, 88, 62))
    d.rectangle([x + 90, y + h - 70, x + 150, y + h - 50], fill=(90, 104, 74))
    d.rectangle([x + 148, y + h - 64, x + 218, y + h - 58], fill=(60, 72, 50))
    for wx in range(52, 182, 22):
        d.ellipse([x + wx, y + h - 28, x + wx + 12, y + h - 16], fill=(40, 44, 36))
    d.rectangle([x + 200, y + h - 44, x + 236, y + h - 34], fill=(120, 100, 70))


def panel_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.ellipse([x + 16, y + 10, x + 34, y + 26], fill=(255, 255, 255))
    d.ellipse([x + 30, y + 6, x + 48, y + 20], fill=(255, 255, 255))
    d.arc([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 76], 180, 360, fill=(245, 243, 235), width=6)
    d.rectangle([x + w // 2 - 40, y + 42, x + w // 2 + 40, y + h - 16], fill=(235, 233, 224))
    for i in range(5):
        cx = x + w // 2 - 32 + i * 16
        d.rectangle([cx - 3, y + min(48, h - 30), cx + 3, y + h - 20], fill=(200, 196, 182))
    d.rectangle([x + w // 2 - 46, y + h - 20, x + w // 2 + 46, y + h - 14], fill=(150, 146, 134))
    d.line([x + w // 2, y + 4, x + w // 2, y + 14], fill=(60, 60, 60), width=2)
    d.polygon([(x + w // 2, y + 4), (x + w // 2 + 16, y + 8), (x + w // 2, y + 12)], fill=(179, 38, 30))


ART = {
    "plane": panel_plane, "dome": panel_dome, "satellite": panel_satellite,
    "drones": panel_drones, "fed": panel_fed, "cyclone": panel_cyclone,
    "desert": panel_desert, "eu": panel_eu, "chart": panel_chart,
    "tank": panel_tank, "capitol": panel_capitol,
}


# ---------------- story data (all 18 Nov 2026) ----------------
# (n, kicker, colour, headline, deck, art, lon, lat)
HEROES = [
    (1, "ASIA · APEC", (183, 121, 31), "Xi greets Trump in Shenzhen",
     "Three-way talks with Putin set for Thursday at the APEC summit.", "plane", 114, 22),
    (2, "GULF · IRAN WAR", (139, 30, 30), "Iran strikes Kuwait and Bahrain",
     "Drones hit Ali Al Salem base; US answers with a strike on Qeshm Island.", "dome", 51, 26),
    (3, "SPACE · SCIENCE", (59, 47, 91), "Voyager 1 one light-day out",
     "First human object 25.9bn km from Earth; a signal takes a day to arrive.", "satellite", None, None),
    (4, "EUROPE · UKRAINE WAR", (31, 78, 121), "Russia fires 141 drones at Ukraine",
     "Air defences down 126 overnight; hits recorded at seven sites.", "drones", 32, 49),
    (5, "AMERICAS · MARKETS", (14, 107, 107), "Fed minutes: more hikes ahead",
     "Almost all officials see further rises; a December hike now expected.", "fed", -77, 39),
    (6, "ASIA · WEATHER", (183, 121, 31), "Cyclone Akvan bears down on Odisha",
     "Now a severe storm; landfall due 20 Nov, winds 90–100 km/h.", "cyclone", 85, 20),
    (7, "AFRICA · SUDAN WAR", (122, 90, 30), "Amnesty: RSF drones killed 37",
     "Nine strikes on El Obeid civilians; Amnesty urges a war-crimes inquiry.", "desert", 30, 13),
    (8, "EUROPE · UKRAINE AID", (31, 78, 121), "EU proposes €45bn loan for Ukraine",
     "Two-thirds of Kyiv's 2027 gap; repaid only once Russia pays reparations.", "eu", 4, 51),
    (9, "EUROPE · ECONOMY", (31, 78, 121), "UK inflation climbs to 3.6%",
     "October rate is the highest in a year; fuel and food push prices up.", "chart", 0, 51),
    (10, "MIDDLE EAST · GAZA", (139, 30, 30), "Israeli tanks roll into central Gaza",
     "Rare push past the Yellow Line near Nuseirat; three killed, army says.", "tank", 34, 31),
    (11, "AMERICAS · US POLITICS", (14, 107, 107), "Jeffries wins Speaker nod, 251–11",
     "Democrats pick him to lead the House; first Black speaker if elected in January.", "capitol", -77, 39),
]

LIST = [
    "Xi, Putin meet before three-way",
    "Quad leaders meet in Manila",
    "Trump meets Marcos in Manila",
    "Carney meets Xi at APEC",
    "Myanmar to review ASEAN ties",
    "Xi vows open trade; Putin hits sanctions",
    "Board of Peace faults both sides",
    "Kerch Bridge hit again, span falls",
    "Russia claims 1,441 drones in a night",
    "Putin 'not ready' for peace talks",
    "Pistorius rebukes US over strikes",
    "Lammy urges EU-rejoin pledge",
    "US loses measles-free status",
    "FAA halts router installs",
    "Fed's Cook may skip firing hearing",
    "Oversight letters to Trump allies",
    "Ethiopia–Eritrea troops mass",
    "COP31 split as stocktake launches",
    "Gaza cold kills in the tents",
    "GTA VI rollout begins",
    "Congo: Ebola cases pass 11,500",
    "ICJ to rule on Myanmar genocide case",
    "Poland says it foiled Russian plot",
    "Saudi coalition hits 60 Houthi sites",
    "Iran says it downed a US MQ-9 drone",
    "Sudan: army advances on RSF stronghold",
    "Moldova summons Russia envoy",
]

REGIONS = [("EUROPE 10", (31, 78, 121)), ("ASIA 8", (183, 121, 31)),
           ("AMERICAS 6", (14, 107, 107)), ("MIDDLE EAST 5", (139, 30, 30)),
           ("WORLD 5", (91, 74, 138)), ("AFRICA 4", (122, 90, 30))]

NUMBERS = [("141", "drones fired at Ukraine"), ("126", "downed overnight"),
           ("251–11", "Jeffries Speaker vote"), ("€45bn", "EU loan for Ukraine"),
           ("25.9bn", "km — Voyager 1 out"), ("37", "killed in El Obeid")]

DATE_CHECK = ("Left out on purpose — first reported 17 Nov, not today: "
              "Peltola's Alaska Senate win (56–44); Nvidia's $115.8bn quarter; "
              "OpenAI's GPT-6.2 Astra/Sol; Dhoni's IPL retirement; the Java4Shell "
              "flaw. Cyclone Akvan formed 16 Nov — card 6 is today's strengthening.")

FOOTER = ("Sources: AP · Reuters · AFP · BBC · NYT · WSJ · ONS · Fed · IMD · NASA · WHO · "
          "Amnesty · UN News — Every story verified against two wires. Illustrations drawn in code.")


def draw_masthead(d):
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.rectangle([0, 108, W, 110], fill=GOLD)
    d.rectangle([16, 14, 80, 94], fill=(255, 255, 255))
    d.rectangle([16, 14, 80, 34], fill=RED)
    d.text((24, 17), "NOV", font=font("sans_b", 13), fill=(255, 255, 255))
    d.text((28, 36), "18", font=font("sans_b", 34), fill=NAVY)
    d.text((22, 74), "WED · 2026", font=font("sans_b", 9), fill=INK)
    d.text((96, 12), "38 STORIES · 6 REGIONS · ONE PAGE", font=font("sans_b", 12), fill=GOLD)
    d.text((96, 28), "Wednesday 18 November 2026", font=font("serif_b", 44), fill=(255, 255, 255))
    d.text((98, 82), "Everything on this page happened, or was first reported, on Wednesday 18 November 2026.",
           font=font("serif", 13), fill=(232, 217, 160))


def draw_region_bar(d, y=110):
    x = 0
    total = sum(int(r[0].split()[-1]) for r in REGIONS)
    for label, col in REGIONS:
        w = int(W * int(label.split()[-1]) / total)
        d.rectangle([x, y, x + w, y + 18], fill=col)
        f = font("sans_b", 11)
        tw = d.textlength(label, font=f)
        d.text((x + (w - tw) / 2, y + 2), label, font=f, fill=(255, 255, 255))
        x += w


def hero_card(d, h, x, y, w, hh, big):
    n, kicker, col, title, deck, art, lon, lat = h
    ih = 96 if big else 62
    d.rectangle([x, y, x + w, y + hh], fill=(255, 253, 246))
    d.rectangle([x, y, x + w, y + hh], outline=(190, 180, 160))
    # Draw the illustration on a temp image so overflow is clipped to the panel.
    tmp = Image.new("RGB", (w - 2, ih), (255, 255, 255))
    td = ImageDraw.Draw(tmp)
    ART[art](td, 0, 0, w - 2, ih)
    d._image.paste(tmp, (x + 1, y + 1))
    r = 11 if big else 9
    bx, by = x + 4, y + 4
    d.ellipse([bx, by, bx + 2 * r, by + 2 * r], fill=RED)
    nf = font("sans_b", 13 if big else 11)
    nt = str(n)
    d.text((bx + r - d.textlength(nt, font=nf) / 2, by + r - nf.size / 2 - 1), nt, font=nf, fill=(255, 255, 255))
    ky = y + ih + 5
    kf = font("sans_b", 10 if big else 9)
    d.text((x + 6, ky), kicker, font=kf, fill=col)
    tf = font("serif_b", 19 if big else 14)
    ty = ky + kf.size + 4
    lines = wrap(d, title, tf, w - 12)
    ty = text_block(d, x + 6, ty, lines, tf, INK, spacing=1, max_lines=3)
    df = font("sans", 11 if big else 10)
    dlines = wrap(d, deck, df, w - 12)
    text_block(d, x + 6, ty + 2, dlines, df, (60, 60, 60), spacing=1, max_lines=2)


def draw_heroes(d, y0, rows):
    y = y0
    idx = 0
    for count, hh in rows:
        gap = 8
        w = (W - 32 - gap * (count - 1)) // count
        for i in range(count):
            x = 16 + i * (w + gap)
            hero_card(d, HEROES[idx], x, y, w, hh, big=(hh >= 190))
            idx += 1
        y += hh + 8
    return y


def draw_list(d, y0, cols, fsize=11):
    d.text((16, y0), "ALSO ON WEDNESDAY 18 NOVEMBER", font=font("sans_b", 13), fill=NAVY)
    d.line([16, y0 + 20, W - 16, y0 + 20], fill=NAVY, width=2)
    y = y0 + 28
    per = (len(LIST) + cols - 1) // cols
    cw = (W - 32 - (cols - 1) * 16) // cols
    f = font("sans", fsize)
    bf = font("sans_b", fsize)
    for c in range(cols):
        x = 16 + c * (cw + 16)
        for r in range(per):
            i = c * per + r
            if i >= len(LIST):
                break
            yy = y + r * 21
            num = str(12 + i)
            d.text((x, yy), num, font=bf, fill=RED)
            d.text((x + 22, yy), LIST[i], font=f, fill=INK)
    return y + per * 21


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.rectangle([x, y, x + w, y + h], outline=(190, 180, 160))
    blobs = [(0.18, 0.22, 0.12, 0.14), (0.09, 0.42, 0.06, 0.09), (0.30, 0.62, 0.055, 0.20),
             (0.50, 0.18, 0.06, 0.09), (0.52, 0.52, 0.07, 0.20), (0.72, 0.24, 0.15, 0.16),
             (0.78, 0.52, 0.045, 0.05), (0.86, 0.72, 0.06, 0.08)]
    for fx, fy, frx, fry in blobs:
        cx, cy = x + fx * w, y + fy * h
        d.ellipse([cx - frx * w, cy - fry * h, cx + frx * w, cy + fry * h], fill=(217, 203, 168))
    step = 7
    for gx in range(x + 3, x + w - 2, step):
        for gy in range(y + 3, y + h - 2, step):
            for fx, fy, frx, fry in blobs:
                cx, cy = x + fx * w, y + fy * h
                if ((gx - cx) / (frx * w)) ** 2 + ((gy - cy) / (fry * h)) ** 2 <= 1:
                    d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(150, 135, 100))
                    break
    pins = {}
    offsets = {9: (-9, -2), 4: (7, -7), 10: (3, 8), 2: (9, 3), 8: (-4, 6)}
    for (n, k, c, t, de, a, lon, lat) in HEROES:
        if lon is None:
            continue
        px = x + (lon + 180) / 360 * w
        py = y + (75 - lat) / 135 * h
        ox, oy = offsets.get(n, (0, 0))
        px, py = px + ox, py + oy
        if n in pins:
            px += 12
            py -= 10
        pins[n] = (px, py)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255))
        nf = font("sans_b", 9)
        nt = str(n)
        d.text((px - d.textlength(nt, font=nf) / 2, py - 5), nt, font=nf, fill=(255, 255, 255))
    d.text((x + 6, y + h - 14), "3 Voyager 1: off the map, 25.9bn km out",
           font=font("sans", 9), fill=(60, 60, 60))


def draw_numbers(d, x, y, w, h):
    d.text((x, y), "THE DAY IN NUMBERS", font=font("sans_b", 12), fill=NAVY)
    cw = w // 3
    for i, (num, lab) in enumerate(NUMBERS):
        cx = x + (i % 3) * cw
        cy = y + 20 + (i // 3) * 52
        d.text((cx, cy), num, font=font("serif_b", 18), fill=RED)
        d.text((cx, cy + 24), lab, font=font("sans", 10), fill=(60, 60, 60))


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.text((x + 8, y + 6), "DATE CHECK", font=font("sans_b", 12), fill=RED)
    f = font("sans", 10)
    lines = wrap(d, DATE_CHECK, f, w - 16)
    text_block(d, x + 8, y + 26, lines, f, INK, spacing=2)


def draw_footer(d):
    f = font("sans", 9)
    d.text((16, 1010), FOOTER, font=f, fill=(90, 84, 70))


def render(variant):
    load_fonts()
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    draw_masthead(d)
    draw_region_bar(d)
    if variant == "B":
        draw_map(d, 16, 132, W - 32, 74)
        d.text((16, 210), "WHERE IT HAPPENED — every number is a story below",
               font=font("sans_b", 11), fill=NAVY)
        y = draw_heroes(d, 230, [(3, 196), (4, 140), (4, 140)])
        y = draw_list(d, y + 4, 3)
        d.rectangle([16, y + 6, W - 16, y + 7], fill=(190, 180, 160))
        draw_numbers(d, 16, y + 14, 480, 100)
        draw_datecheck(d, 520, y + 14, W - 16 - 520, 108)
    elif variant == "C":
        y = draw_heroes(d, 132, [(3, 196), (4, 140), (4, 140)])
        y = draw_list(d, y + 4, 2, fsize=13)
        draw_map(d, 16, y + 8, 320, 108)
        draw_numbers(d, 352, y + 8, 320, 108)
        draw_datecheck(d, 688, y + 8, W - 16 - 688, 108)
    else:  # A
        y = draw_heroes(d, 132, [(3, 196), (4, 140), (4, 140)])
        y = draw_list(d, y + 4, 3)
        draw_map(d, 16, y + 8, 320, 108)
        draw_numbers(d, 352, y + 8, 320, 108)
        draw_datecheck(d, 688, y + 8, W - 16 - 688, 108)
    draw_footer(d)
    return im


if __name__ == "__main__":
    import hashlib
    import os
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    im = render(variant)
    out = f"entry-{variant}.png"
    im.save(out, optimize=True)
    data = open(out, "rb").read()
    print(out, im.size, len(data), "bytes, sha256",
          hashlib.sha256(data).hexdigest())
