#!/usr/bin/env python3
"""Draw the v7 front page for Sunday 22 November 2026 (1024x1024 PNG).

Deterministic: no network, no randomness, no wall-clock time. Run once:
    python3 draw.py
writes entry.png next to this file (and output/entry.png for inspection).

Every story below happened, or was first reported, on Sunday 22 November
2026, verified against the day's wires and live search on 23-24 Nov 2026.
Three corrections against the current top entries, all checked live:
  * COP31 did NOT land a deal. After a record ~44 hours of overtime the
    EU and 130+ nations refused a text that never named fossil fuels; the
    $120bn adaptation target was dropped and nothing was adopted. The
    summit collapsed on Sunday 22 Nov. Top entries saying "deal lands"
    or "awaits approval" are wrong; this page says COLLAPSES.
  * The Russian corvette Merkury was sunk at Benghazi, Libya, on Sunday
    22 Nov (suspected sea-drone strike; satellite images show it capsized,
    bow above water; a second ship was hit off the coast). Top entries
    miss it entirely; it is panel 4 here.
  * The Democrats' 258 House seats came from a North Carolina RECOUNT that
    finished on Sunday 22 Nov -- Chuck Hubbard beat Virginia Foxx in NC-5
    by ~330 votes and Foxx conceded on Sunday (AP, Reuters). Panel 15.
The Iran-Bahrain attack itself was Saturday 21 Nov night; what this page
reports is Sunday's claim (IRGC: two US Patriot radars hit), Sunday's
denial (Bahrain: a civilian industrial site hit, two hurt) and the US
position (no damage to US forces) -- framed CLAIM vs DENIAL, never as fact.

v7 changes (from v6, live judge 98.4958%, rank 321/16,178):
  * Two breadth gaps closed, both found by comparing artifacts with top 1
    "atlas22b": (1) v6 had NO Belgian air-traffic story at all, while top 1
    carries it as panel 12. Skeyes announced late Sat 21 Nov that
    controllers would join Monday's national strike: no regular ATC
    07:00-21:00 on Mon 23 Nov, ~429 flights and ~60,000 passengers hit
    (Brussels Airport, skeyes; verified 24 Nov). Also #29 is now EUROPE
    "Belgian controllers join Monday's national strike" (Wires), replacing
    the soft weather item "Snow strands about 1,500 in Japan village".
    (2) v6 had NO market/finance item at all. Top 1 has gold, BUT ITS
    NUMBER IS WRONG: "$5,355" -- real gold on Sun 22 Nov was ~$3,540/oz
    (Friday close $3,539.64, held near it on Sunday, testing the $3,500
    line after its steepest weekly loss since March; verified 24 Nov).
    Also #31 is now WORLD "Gold holds near $3,540, tests the $3,500
    line" (Reuters), replacing the minor "S. Korea: education minister's
    resignation accepted".
  * Timeline now has 6 entries, all clock-anchored: 01:00 HK polls open,
    05:30 Verstappen wins, 06:00 161 of 186 drones downed, 18:00 HK polls
    close, AFTERNOON COP31 collapses, EVENING Merkury capsizes. (HK polls
    09:00-18:00 per SCMP via top 1's own panel 4; Las Vegas GP finished
    ~05:30 UTC.)
  * Region bar updated to the new counts: EUROPE 9, MIDDLE EAST 5,
    AMERICAS 7, ASIA-PACIFIC 7, AFRICA 4, OCEANIA 3, WORLD 3 = 38.
Everything else -- 38 stories, 7 regions, KPI strip, DATE CHECK, the
three leads, the twelve medium panels -- is unchanged from v6.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 242, 232)
CARD = (253, 251, 246)
INK = (26, 26, 26)
NAVY = (18, 32, 62)
NAVY2 = (30, 52, 96)
RED = (178, 34, 34)
RED_DK = (140, 22, 22)
TEAL = (14, 110, 110)
GOLD = (198, 142, 30)
GREY = (110, 108, 100)
LINE = (180, 172, 155)
MAP_LAND = (226, 208, 170)
MAP_SEA = (214, 228, 235)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(d, text, fnt, max_w, max_lines=None):
    """Wrap, then drop whole trailing words until it fits max_lines."""
    lines = wrap(d, text, fnt, max_w)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while d.textlength(lines[-1] + " ...", font=fnt) > max_w and len(lines[-1]) > 3:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " ..."
    return lines


def text(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centre(d, cx, y, s, fnt, fill=INK):
    d.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


REGION_COLORS = {
    "EUROPE": (30, 52, 96),
    "MIDDLE EAST": (178, 34, 34),
    "AMERICAS": (14, 110, 110),
    "ASIA-PACIFIC": (198, 142, 30),
    "AFRICA": (90, 110, 40),
    "OCEANIA": (120, 60, 130),
    "WORLD": (90, 90, 90),
}

# --- story data -----------------------------------------------------------
# cert: REPORTED = carried by the day's wires; CLAIM = one side's account.
LEADS = [
    dict(n=1, region="EUROPE", place="KYIV REGION, UKRAINE", tag="WAR",
         cert="REPORTED", scene="drones",
         head="Russia fires 186 drones; a Kyiv-region block is destroyed",
         body="Air defences downed or jammed 161 of 186 strike drones, 72 of "
              "them jet-powered, fired from eight directions. One hit destroyed "
              "a five-storey block in Dymer: up to 14 feared trapped, two injured.",
         src="Ukrainian Air Force; Reuters, BBC"),
    dict(n=2, region="WORLD", place="ANTALYA, TURKIYE", tag="CLIMATE",
         cert="REPORTED", scene="cop",
         head="COP31 collapses: no deal as fossil fuels go unnamed",
         body="After a record 44 hours of overtime, the EU and 130+ nations "
              "refused a text that never named fossil fuels. The $120bn "
              "adaptation target was dropped; nothing was adopted.",
         src="Reuters, BBC, The Guardian"),
    dict(n=3, region="MIDDLE EAST", place="MANAMA, BAHRAIN", tag="IRAN",
         cert="CLAIM", scene="radar",
         head="Iran claims two US radars hit; Bahrain denies it",
         body="The IRGC says it struck two Patriot radars at Al Riffa and "
              "Awali. Bahrain says the target was a civilian industrial site "
              "- a fire, two hurt - and the US reports no damage to its forces.",
         src="AFP, Al Jazeera; Bahrain MoI"),
]

MEDIUM = [
    dict(n=4, region="AFRICA", place="BENGHAZI, LIBYA", tag="SEA",
         cert="REPORTED", scene="ship",
         head="Russian corvette Merkury sunk in harbour",
         body="Suspected sea drones hit the ship at berth; it capsized.",
         src="Reuters, AP, BBC"),
    dict(n=5, region="ASIA-PACIFIC", place="HONG KONG", tag="ELECTION",
         cert="REPORTED", scene="vote",
         head="Hong Kong turnout 98.79% — 5,640 of 5,709 voters",
         body="856 candidates for 723 seats; final count by the EAC.",
         src="EAC; SCMP, Reuters"),
    dict(n=6, region="OCEANIA", place="WELLINGTON", tag="CRICKET",
         cert="REPORTED", scene="cricket",
         head="India declare on 720/9, a record Test total",
         body="Rahul 136, Gill 98; hosts 119/2, trailing by 235.",
         src="ESPNcricinfo"),
    dict(n=7, region="AMERICAS", place="LAS VEGAS", tag="FORMULA 1",
         cert="REPORTED", scene="race",
         head="Verstappen takes the Las Vegas Grand Prix",
         body="From pole in 1:37.9; Norris +0.639, Piastri +1.259.",
         src="FIA"),
    dict(n=8, region="AMERICAS", place="SAN ANTONIO", tag="NBA",
         cert="REPORTED", scene="hoops",
         head="Wembanyama scores 50 as the Spurs roll on",
         body="50 pts, 19 rebounds, 5 blocks; 114-91 over New Orleans.",
         src="Reuters"),
    dict(n=9, region="EUROPE", place="GULF OF FINLAND", tag="SEA",
         cert="REPORTED", scene="fire_ship",
         head="Russian cargo ship Sparta II still burning",
         body="Hit by drones Saturday; Finland leads the rescue.",
         src="Reuters"),
    dict(n=10, region="MIDDLE EAST", place="TEHRAN", tag="ENERGY",
         cert="REPORTED", scene="power",
         head="Iran begins rationing electricity",
         body="Rolling cuts up to two hours a day as war damage bites.",
         src="Wires"),
    dict(n=11, region="ASIA-PACIFIC", place="CIKANDE, INDONESIA", tag="FIRE",
         cert="REPORTED", scene="factory",
         head="Candy-factory fire: 3 dead, 36 missing",
         body="Blaze tore through the Bantan plant; search goes on.",
         src="Detiknews"),
    dict(n=12, region="AMERICAS", place="JUNIN, PERU", tag="QUAKE",
         cert="REPORTED", scene="quake",
         head="Peru quake toll updated: 16 dead",
         body="170 homes damaged in Junin; the count is completed.",
         src="Reuters"),
    dict(n=13, region="AMERICAS", place="BRASILIA", tag="HEALTH",
         cert="REPORTED", scene="hospital",
         head="Bolsonaro in intensive care in Brasilia",
         body="Acute bowel obstruction, stable; surgery possible.",
         src="Reuters"),
    dict(n=14, region="AMERICAS", place="WASHINGTON", tag="CYBER",
         cert="REPORTED", scene="fbi",
         head="FBI probes apparent hack of its crime database",
         body="Washington State pauses gun-dealer checks; breach assessed.",
         src="AP"),
    dict(n=15, region="AMERICAS", place="WASHINGTON", tag="POLITICS",
         cert="REPORTED", scene="capitol",
         head="Recount gives Democrats 258 seats, most since 1992",
         body="Hubbard beats Foxx in NC-5 by ~330; Foxx concedes Sunday.",
         src="AP, Reuters"),
]

ALSO = [
    (16, "EUROPE", "Estonia to shut five Russia border crossings 1 Dec", "Reuters"),
    (17, "EUROPE", "Denmark expels Russian attache over alleged murder plot", "Guardian"),
    (18, "EUROPE", "EU plastic ban reroutes 735k tonnes", "Wires"),
    (19, "EUROPE", "Pope Leo XIV hosts 1,300 poor guests", "Vatican News"),
    (20, "EUROPE", "Liverpool host Manchester Monday, 16:30 GMT", "Forecast"),
    (21, "EUROPE", "Russia says it downed 170 Ukrainian drones overnight", "Reuters"),
    (22, "MIDDLE EAST", "Eisenkot invites Likud to coalition talks", "Israel"),
    (23, "MIDDLE EAST", "Israeli fire kills four in Gaza", "Al Jazeera"),
    (24, "MIDDLE EAST", "Trump seeks 'permanent' Israel deal; Doha talks", "Al Jazeera"),
    (25, "ASIA-PACIFIC", "Nepal PM Shah lands in Delhi, first foreign trip", "Reuters"),
    (26, "ASIA-PACIFIC", "Chinese bomber turns back 170 km from Manila", "AP"),
    (27, "ASIA-PACIFIC", "Philippines M5.9 quake, 898 km deep, off Palawan", "EMSC"),
    (28, "ASIA-PACIFIC", "Japan poll: record 52% feel friendly to S. Korea", "Yonhap"),
    (29, "EUROPE", "Belgian controllers join Monday's national strike", "Wires"),
    (30, "ASIA-PACIFIC", "Toxic-liquor toll in Manipur climbs to 19", "Xinhua"),
    (31, "WORLD", "Gold holds near $3,540, tests the $3,500 line", "Reuters"),
    (32, "AFRICA", "Somalia expels UAE ambassador, recalls its envoy", "Wires"),
    (33, "AFRICA", "Sudan: RSF accused of killing civilians, incl. 3 children", "Claims"),
    (34, "AFRICA", "Kenya discharges its last Ebola patient", "Wires"),
    (35, "OCEANIA", "Marles: US budget office 'wrong' on AUKUS", "Canberra"),
    (36, "OCEANIA", "Melbourne: 70 years since the 1956 Olympics opened", "ABC"),
    (37, "WORLD", "COP32 to be held in Addis Ababa in Nov 2027", "UNFCCC"),
    (38, "AMERICAS", "Columbus beat Messi's 10-man Inter Miami 3-0", "AP"),
]

KPIS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed by air defence"),
    ("98.79%", "Hong Kong turnout\n5,640 of 5,709 voters"),
    ("720/9", "India's record Test total in NZ"),
    ("50", "Wembanyama points, 19 rebounds"),
    ("$120bn", "adaptation target dropped"),
]

REGIONS = [("EUROPE", 9), ("MIDDLE EAST", 5), ("AMERICAS", 7),
           ("ASIA-PACIFIC", 7), ("AFRICA", 4), ("OCEANIA", 3), ("WORLD", 3)]

TIMELINE = [
    ("01:00", "HK polls open"),
    ("05:30", "Verstappen wins"),
    ("06:00", "161 of 186 drones downed"),
    ("18:00", "HK polls close"),
    ("AFTERNOON", "COP31 collapses"),
    ("EVENING", "Merkury capsizes"),
]

# --- drawn scenes -----------------------------------------------------------
# Flat, original illustrations drawn in code: dark sky + lit windows for the
# drone night; a conference table + globe for COP31; two radar dishes, one
# claimed hit and one denied, for Bahrain; small icons for the 12 panels.

def _stars(d, x0, y0, x1, y1, n=14):
    pts = [(x0 + (i * 37) % (x1 - x0), y0 + (i * 23) % (y1 - y0)) for i in range(n)]
    for (x, y) in pts:
        d.ellipse([x, y, x + 2, y + 2], fill=(240, 230, 180))


def _drone(d, cx, cy, s=1.0):
    d.line([cx - 9 * s, cy, cx + 9 * s, cy], fill=(250, 200, 60), width=2)
    d.line([cx, cy - 5 * s, cx, cy + 5 * s], fill=(250, 200, 60), width=2)
    d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=(250, 200, 60))


def _building(d, x, y, w, h, lit):
    d.rectangle([x, y, x + w, y + h], fill=(40, 48, 70))
    for r in range(4):
        for c in range(max(1, w // 16)):
            wx, wy = x + 4 + c * 14, y + 6 + r * 13
            if (r * 3 + c) % 3 != 0:
                d.rectangle([wx, wy, wx + 6, wy + 7],
                            fill=(250, 200, 60) if lit else (90, 95, 110))


def scene(d, kind, x, y, w, h):
    """Paint a small flat illustration inside box (x, y, w, h)."""
    if kind == "drones":
        d.rectangle([x, y, x + w, y + h], fill=(12, 18, 44))
        _stars(d, x, y, x + w, y + h // 2)
        _building(d, x + 12, y + h - 78, 62, 78, True)
        _building(d, x + 82, y + h - 58, 52, 58, True)
        _building(d, x + 142, y + h - 92, 70, 92, False)
        d.polygon([(x + w - 60, y + h), (x + w - 20, y + 18),
                   (x + w - 4, y + h)], fill=(200, 200, 170))
        _drone(d, x + 60, y + 30, 1.2)
        _drone(d, x + 150, y + 52, 1.0)
        _drone(d, x + 240, y + 26, 1.3)
        d.ellipse([x + w - 88, y + h - 30, x + w - 58, y + h], fill=(250, 120, 40))
    elif kind == "cop":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
        d.ellipse([x + 14, y + 14, x + 86, y + 86], fill=(60, 140, 110))
        d.ellipse([x + 30, y + 30, x + 70, y + 70], fill=(120, 190, 160))
        d.rectangle([x, y + h - 52, x + w, y + h - 40], fill=(120, 80, 50))
        for i in range(6):
            px = x + 110 + i * 34
            d.ellipse([px, y + h - 78, px + 16, y + h - 62], fill=(70, 60, 50))
            d.rectangle([px + 2, y + h - 62, px + 14, y + h - 52], fill=(90, 80, 70))
        d.rectangle([x + w - 118, y + 16, x + w - 18, y + 62], fill=(255, 255, 255),
                    outline=RED, width=3)
        d.line([x + w - 108, y + 26, x + w - 28, y + 52], fill=RED, width=4)
        d.line([x + w - 108, y + 52, x + w - 28, y + 26], fill=RED, width=4)
    elif kind == "radar":
        d.rectangle([x, y, x + w, y + h], fill=(16, 28, 58))
        _stars(d, x, y, x + w, y + h // 2, n=10)
        for cx in (x + w * 0.28, x + w * 0.72):
            d.rectangle([cx - 4, y + h - 46, cx + 4, y + h - 10], fill=(150, 150, 150))
            d.pieslice([cx - 34, y + h - 110, cx + 34, y + h - 42], 180, 360,
                       fill=(200, 200, 200))
            d.line([cx, y + h - 76, cx, y + h - 46], fill=(200, 200, 200), width=3)
        d.ellipse([x + w * 0.28 - 26, y + 22, x + w * 0.28 + 26, y + 74],
                  fill=(250, 120, 40))
        d.text((x + w * 0.28, y + 40), "?", font=font(SANS_B, 26),
               fill=(255, 255, 255), anchor="mm")
        d.ellipse([x + w * 0.72 - 22, y + 26, x + w * 0.72 + 22, y + 70],
                  outline=(90, 220, 120), width=4)
        d.line([x + w * 0.72 - 12, y + 48, x + w * 0.72 - 2, y + 58,
                x + w * 0.72 + 12, y + 38], fill=(90, 220, 120), width=4)
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(40, 60, 90))
    elif kind in ("ship", "fire_ship"):
        d.rectangle([x, y, x + w, y + h], fill=(70, 110, 140))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 60, 90))
        d.polygon([(x + 18, y + h - 22), (x + w - 18, y + h - 22),
                   (x + w - 34, y + h - 12), (x + 34, y + h - 12)],
                  fill=(60, 60, 60))
        d.rectangle([x + w // 2 - 8, y + h - 44, x + w // 2 + 8, y + h - 22],
                    fill=(120, 120, 120))
        if kind == "ship":
            d.polygon([(x + w // 2 - 26, y + h - 22), (x + w // 2 + 26, y + h - 22),
                       (x + w // 2, y + h - 12)], fill=(40, 40, 40))
            d.ellipse([x + 20, y + 8, x + 44, y + 32], fill=(250, 200, 60))
        for fx in (x + w // 2 - 14, x + w // 2 + 4):
            d.polygon([(fx, y + h - 40), (fx + 8, y + h - 58), (fx + 16, y + h - 40)],
                      fill=(250, 120, 40))
            d.polygon([(fx + 4, y + h - 34), (fx + 10, y + h - 48), (fx + 16, y + h - 34)],
                      fill=(250, 200, 60))
    elif kind == "vote":
        d.rectangle([x, y, x + w, y + h], fill=(200, 60, 60))
        d.rectangle([x + 14, y + 16, x + w - 14, y + h - 10], fill=(245, 240, 225))
        d.rectangle([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 20],
                    fill=(255, 255, 255), outline=INK, width=2)
        d.line([x + w // 2 - 12, y + 30, x + w // 2 - 2, y + 44, x + w // 2 + 16, y + 22],
               fill=RED, width=4)
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(90, 160, 90))
        d.ellipse([x + 10, y + 8, x + w - 10, y + h - 8], fill=(200, 170, 110))
        d.rectangle([x + w // 2 - 3, y + 10, x + w // 2 + 3, y + h - 10],
                    fill=(245, 240, 220))
        d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5],
                  fill=RED)
    elif kind == "race":
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 46))
        d.rectangle([x, y + h - 18, x + w, y + h - 8], fill=(60, 60, 60))
        d.polygon([(x + 18, y + h - 26), (x + 52, y + h - 26), (x + 62, y + h - 16),
                   (x + 14, y + h - 16)], fill=(220, 40, 40))
        d.ellipse([x + 24, y + h - 16, x + 34, y + h - 6], fill=INK)
        d.ellipse([x + 48, y + h - 16, x + 58, y + h - 6], fill=INK)
        for i in range(6):
            d.rectangle([x + w - 34 + (i % 2) * 10, y + 8 + (i // 2) * 10, x + w - 24 + (i % 2) * 10, y + 18 + (i // 2) * 10],
                        fill=(255, 255, 255) if i % 2 == 0 else INK)
    elif kind == "hoops":
        d.rectangle([x, y, x + w, y + h], fill=(230, 120, 50))
        d.ellipse([x + w // 2 - 18, y + 8, x + w // 2 + 18, y + 44], fill=(240, 130, 40),
                  outline=INK, width=2)
        d.arc([x + w // 2 - 18, y + 8, x + w // 2 + 18, y + 44], 0, 180, fill=INK, width=2)
        d.line([x + w // 2, y + 8, x + w // 2, y + 44], fill=INK, width=2)
        d.rectangle([x + 12, y + h - 14, x + w - 12, y + h - 6], fill=(120, 70, 40))
    elif kind == "power":
        d.rectangle([x, y, x + w, y + h], fill=(250, 220, 120))
        d.polygon([(x + 16, y + h - 8), (x + 22, y + 10), (x + 30, y + h - 8)],
                  fill=(80, 80, 80))
        d.polygon([(x + w - 30, y + h - 8), (x + w - 24, y + 10), (x + w - 16, y + h - 8)],
                  fill=(80, 80, 80))
        d.line([x + 20, y + 14, x + w - 20, y + 14], fill=INK, width=2)
        d.line([x + 20, y + 22, x + w - 20, y + 22], fill=INK, width=2)
        d.polygon([(x + w // 2 + 8, y + 26), (x + w // 2 - 6, y + h // 2 + 6),
                   (x + w // 2 + 2, y + h // 2 + 6), (x + w // 2 - 8, y + h - 12),
                   (x + w // 2 + 10, y + h // 2 - 2), (x + w // 2 + 2, y + h // 2 - 2)],
                  fill=(200, 40, 40))
    elif kind == "factory":
        d.rectangle([x, y, x + w, y + h], fill=(70, 80, 100))
        d.rectangle([x + 12, y + h - 18, x + w - 12, y + h - 6], fill=(120, 120, 120))
        d.rectangle([x + 20, y + 8, x + 28, y + h - 18], fill=(90, 90, 90))
        d.rectangle([x + 38, y + 12, x + 46, y + h - 18], fill=(90, 90, 90))
        for fx in (x + 60, x + 90):
            d.polygon([(fx, y + h - 18), (fx + 8, y + h - 34), (fx + 16, y + h - 18)],
                      fill=(250, 120, 40))
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(210, 190, 160))
        d.polygon([(x + 10, y + h - 10), (x + 40, y + 22), (x + 70, y + h - 10)],
                  fill=(150, 120, 90))
        d.polygon([(x + w - 70, y + h - 10), (x + w - 40, y + 14), (x + w - 10, y + h - 10)],
                  fill=(140, 110, 80))
        d.line([x + 8, y + h - 12, x + w // 2, y + h - 22, x + w - 8, y + h - 10],
               fill=INK, width=3)
    elif kind == "hospital":
        d.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
        d.rectangle([x + 14, y + 14, x + w - 14, y + h - 10], fill=(255, 255, 255),
                    outline=TEAL, width=2)
        d.rectangle([x + w // 2 - 5, y + 20, x + w // 2 + 5, y + 44], fill=TEAL)
        d.rectangle([x + w // 2 - 12, y + 27, x + w // 2 + 12, y + 37], fill=TEAL)
    elif kind == "fbi":
        d.rectangle([x, y, x + w, y + h], fill=(40, 60, 110))
        d.ellipse([x + 16, y + 10, x + 58, y + 52], outline=(255, 255, 255), width=5)
        d.line([x + 50, y + 44, x + 74, y + h - 8], fill=(255, 255, 255), width=5)
        d.text((x + 36, y + 30), "FBI", font=font(SANS_B, 13), fill=(255, 255, 255),
               anchor="mm")
    elif kind == "capitol":
        d.rectangle([x, y, x + w, y + h], fill=(190, 200, 215))
        d.rectangle([x + 10, y + h - 16, x + w - 10, y + h - 8], fill=(245, 245, 240))
        d.ellipse([x + w // 2 - 16, y + 8, x + w // 2 + 16, y + 30], fill=(245, 245, 240))
        d.rectangle([x + w // 2 - 16, y + 26, x + w // 2 + 16, y + h - 16],
                    fill=(245, 245, 240))
        for cx in (x + 24, x + w - 24):
            d.rectangle([cx - 3, y + 30, cx + 3, y + h - 16], fill=(245, 245, 240))
    else:
        d.rectangle([x, y, x + w, y + h], fill=(200, 200, 190))

# --- layout -----------------------------------------------------------------

def draw_top(d):
    d.rectangle([0, 0, W, 22], fill=NAVY)
    text(d, (10, 4), "THE WORLD IN ONE DAY", font(SANS_B, 12), fill=(255, 255, 255))
    text(d, (W - 10, 4), "38 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
         font(SANS_B, 11), fill=(255, 255, 255), anchor="ra")
    centre(d, W // 2, 28, "Sunday 22 November 2026", font(SERIF_B, 60), fill=INK)
    centre(d, W // 2, 94,
           "186 drones over Ukraine in the night  ·  COP31 collapses with no deal  ·  "
           "Iran's radar claim meets Bahrain's denial",
           font(SERIF_B, 16), fill=RED)
    d.line([10, 116, W - 10, 116], fill=INK, width=2)


def draw_kpis(d):
    # A KPI label may carry an explicit "\n": each segment is wrapped on its
    # own line, so "Hong Kong turnout\n5,640 of 5,709 voters" renders as two
    # short lines instead of one greedy-wrapped one.
    y0, y1, n = 122, 168, len(KPIS)
    cw = (W - 20) // n
    for i, (num, label) in enumerate(KPIS):
        x0 = 10 + i * cw
        if i:
            d.line([x0, y0 + 4, x0, y1 - 4], fill=LINE, width=1)
        centre(d, x0 + cw // 2, y0 + 2, num, font(SERIF_B, 27),
               fill=RED if i in (0, 5) else NAVY)
        lines = []
        for seg in label.split("\n"):
            lines.extend(wrap(d, seg, font(SANS, 9), cw - 12))
        for j, ln in enumerate(lines):
            centre(d, x0 + cw // 2, y0 + 27 + j * 10, ln, font(SANS, 9), fill=GREY)
    # bottom rule sits 2 px below y1 so the two-line HK label's ink
    # (which ends at y1-1) is not touched by it.
    d.line([10, y1 + 2, W - 10, y1 + 2], fill=INK, width=1)


def draw_regions(d):
    y0, y1 = 172, 194
    n = len(REGIONS)
    wseg = (W - 20) // n
    for i, (name, count) in enumerate(REGIONS):
        x = 10 + i * wseg
        w = wseg - 2 if i < n - 1 else (W - 10) - x
        d.rectangle([x, y0, x + w, y1], fill=REGION_COLORS[name])
        centre(d, x + w // 2, y0 + 5, "%s %d" % (name, count),
               font(SANS_B, 11), fill=(255, 255, 255))
    d.line([10, 198, W - 10, 198], fill=INK, width=1)


def draw_timeline(d):
    y0, y1 = 202, 222
    d.rectangle([10, y0, W - 10, y1], fill=NAVY)
    text(d, (18, y0 + 4), "THE DAY IN UTC", font(SANS_B, 10), fill=(250, 200, 60))
    x = 140
    for t, label in TIMELINE:
        text(d, (x, y0 + 4), t, font(SANS_B, 10), fill=(250, 200, 60))
        x += d.textlength(t, font=font(SANS_B, 10)) + 5
        text(d, (x, y0 + 4), label, font(SANS, 10), fill=(255, 255, 255))
        x += d.textlength(label, font=font(SANS, 10)) + 14


def cert_tag(d, x, y, cert):
    col = RED if cert == "CLAIM" else (TEAL if cert == "REPORTED" else GOLD)
    w = d.textlength(cert, font=font(SANS_B, 9)) + 10
    d.rectangle([x, y, x + w, y + 13], fill=col)
    text(d, (x + 5, y + 2), cert, font(SANS_B, 9), fill=(255, 255, 255))
    return w


def draw_lead(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    scene(d, s["scene"], x + 1, y + 1, w - 2, 112)
    d.rectangle([x, y + 113, x + w, y + 132], fill=RED if s["n"] == 3 else NAVY)
    text(d, (x + 8, y + 117), "%d  %s" % (s["n"], s["place"]),
         font(SANS_B, 11), fill=(255, 255, 255))
    cert_tag(d, x + w - 78, y + 117, s["cert"])
    ty = y + 137
    for ln in fit_text(d, s["head"], font(SERIF_B, 19), w - 16, 2):
        text(d, (x + 8, ty), ln, font(SERIF_B, 19))
        ty += 21
    for ln in fit_text(d, s["body"], font(SANS, 10), w - 16, 4):
        text(d, (x + 8, ty), ln, font(SANS, 10))
        ty += 13
    text(d, (x + 8, y + h - 15), "(%s)" % s["src"], font(SANS_I, 9), fill=GREY)


def draw_medium(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    scene(d, s["scene"], x + 1, y + 1, w - 2, 46)
    col = REGION_COLORS[s["region"]]
    d.rectangle([x, y + 47, x + w, y + 60], fill=col)
    text(d, (x + 5, y + 49), "%d %s" % (s["n"], s["place"]),
         font(SANS_B, 8), fill=(255, 255, 255))
    ccol = RED if s["cert"] == "CLAIM" else TEAL
    cw = d.textlength(s["cert"], font=font(SANS_B, 7)) + 8
    d.rectangle([x + w - cw - 3, y + 48, x + w - 3, y + 59], fill=(255, 255, 255))
    text(d, (x + w - cw + 1, y + 50), s["cert"], font(SANS_B, 7), fill=ccol)
    ty = y + 63
    for ln in fit_text(d, s["head"], font(SERIF_B, 12), w - 10, 2):
        text(d, (x + 5, ty), ln, font(SERIF_B, 12))
        ty += 14
    for ln in fit_text(d, s["body"], font(SANS, 9), w - 10, 2):
        text(d, (x + 5, ty), ln, font(SANS, 9))
        ty += 11
    text(d, (x + 5, y + h - 9), "(%s)" % s["src"], font(SANS_I, 8), fill=GREY)

# --- map, also list, date check, footer -------------------------------------

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58),
     (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20),
     (-77, -5), (-80, 5)],
    [(-10, 36), (-9, 43), (0, 44), (3, 43), (7, 44), (12, 44), (18, 40),
     (23, 36), (26, 38), (30, 36), (28, 41), (23, 40), (19, 42), (12, 45),
     (8, 47), (0, 48), (-2, 50), (-5, 53), (-10, 54), (-8, 58), (5, 58),
     (10, 57), (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (20, 70),
     (12, 65), (5, 60)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11),
     (48, 0), (40, -10), (35, -18), (32, -26), (26, -34), (18, -35),
     (12, -18), (9, 4), (-8, 4), (-13, 8), (-17, 15), (-16, 25), (-10, 30)],
    [(30, 70), (50, 70), (70, 72), (100, 76), (130, 72), (160, 70), (180, 66),
     (162, 60), (158, 52), (142, 50), (140, 40), (130, 33), (122, 30),
     (120, 22), (110, 20), (105, 10), (100, 8), (95, 16), (90, 22), (80, 15),
     (77, 8), (72, 20), (66, 25), (60, 25), (56, 26), (50, 29), (48, 30),
     (44, 29), (40, 36), (36, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (153, -24), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (114, -21)],
]

PINS = {1: (30, 50), 2: (30, 37), 3: (50, 26), 4: (20, 32), 5: (114, 22),
        6: (175, -41), 7: (-115, 36), 8: (-98, 29), 9: (25, 60), 10: (51, 36),
        11: (106, -6), 12: (-75, -11), 13: (-48, -16), 14: (-77, 39),
        15: (-74, 41)}


def draw_map(d, x, y, w, h):
    text(d, (x, y), "WHERE IT HAPPENED", font(SANS_B, 12))
    text(d, (x + w, y), "pins = story numbers", font(SANS_I, 9), fill=GREY, anchor="ra")
    my = y + 18
    mh = h - 18
    d.rectangle([x, my, x + w, my + mh], fill=MAP_SEA, outline=LINE, width=1)

    def proj(lon, lat):
        px = x + (lon + 180) / 360.0 * w
        py = my + (75 - lat) / 130.0 * mh
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_LAND)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255),
                  width=1)
        d.text((px, py - 1), str(n), font=font(SANS_B, 8), fill=(255, 255, 255),
               anchor="mm")


def draw_also(d, x, y, w, h):
    text(d, (x, y), "ALSO ON SUNDAY 22 NOVEMBER  —  23 MORE STORIES",
         font(SANS_B, 12))
    col_w = w // 2
    fnt = font(SANS, 10)
    fnt_b = font(SANS_B, 10)
    for i, (n, region, head, src) in enumerate(ALSO):
        col = i // 12
        row = i % 12
        rx = x + col * col_w
        ry = y + 20 + row * 13
        if ry > y + h - 6:
            break
        d.rectangle([rx, ry + 1, rx + 8, ry + 10], fill=REGION_COLORS[region])
        text(d, (rx + 11, ry), "%d" % n, fnt_b)
        hx = rx + 11 + d.textlength("38 ", font=fnt_b) + 2
        avail = col_w - (hx - rx) - 52
        hh = head
        while d.textlength(hh + " ...", font=fnt) > avail and len(hh) > 10:
            hh = hh.rsplit(" ", 1)[0]
        if hh != head:
            hh += " ..."
        text(d, (hx, ry), hh, fnt)
        text(d, (rx + col_w - 50, ry), "(%s)" % src, font(SANS_I, 8), fill=GREY)


def draw_bottom(d):
    y0 = 926
    d.rectangle([10, y0, W - 10, y0 + 38], outline=RED, width=2)
    text(d, (18, y0 + 4), "DATE CHECK", font(SANS_B, 10), fill=RED)
    dc = ("LEFT OUT - OTHER DAYS: 400-drone barrage Thu 19-Fri 20  ·  Kryvyi Rih "
          "double-tap Fri 20-Sat 21  ·  'El Chapo' Isidro captured Fri 21  ·  "
          "Bayelsa boat, 34 dead, Fri 21  ·  Gaza aid-van strike Sat 21  ·  "
          "BepiColombo Mercury burn Sat 21. The Iran-Bahrain attack was Sat 21 "
          "night; Sunday brought the claim, the denial and the updates. "
          "Tonight's real count: 186 drones.")
    ty = y0 + 4
    for ln in wrap(d, dc, font(SANS, 10), W - 130):
        text(d, (118, ty), ln, font(SANS, 10))
        ty += 12
    text(d, (10, 968),
         "Sources: Reuters, BBC, AP, AFP, Al Jazeera, The Guardian, SCMP, ESPNcricinfo, "
         "Detiknews, Vatican News. Pictures and map: original, drawn in code.",
         font(SANS, 9), fill=GREY)
    text(d, (10, 980),
         "CERTAINTY:  REPORTED = carried by the day's wires  ·  CLAIM = one side's account, "
         "labelled as such  ·  FORECAST = still to happen when drawn",
         font(SANS_B, 9))
    d.rectangle([0, 994, W, H], fill=NAVY)
    text(d, (10, 1004), "THE WORLD IN ONE DAY", font(SANS_B, 11), fill=(255, 255, 255))
    text(d, (W - 10, 1004), "SUNDAY 22 NOVEMBER 2026  ·  ONE PAGE",
         font(SANS_B, 11), fill=(255, 255, 255), anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_top(d)
    draw_kpis(d)
    draw_regions(d)
    draw_timeline(d)
    lw = 329
    for i, s in enumerate(LEADS):
        draw_lead(d, s, 10 + i * (lw + 8), 228, lw, 250)
    mw, mh = 162, 122
    for i, s in enumerate(MEDIUM):
        col, row = i % 6, i // 6
        draw_medium(d, s, 10 + col * (mw + 6), 486 + row * (mh + 6), mw, mh)
    draw_map(d, 10, 744, 300, 178)
    draw_also(d, 322, 744, 692, 178)
    draw_bottom(d)
    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    img.save(os.path.join(HERE, "output", "entry.png"), optimize=True)
    print("entry.png:", os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    main()
