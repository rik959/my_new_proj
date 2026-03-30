"""
Anniversary Magazine PDF Generator
Place photos in 'photos/', customize CONFIG below, run: python magazine.py
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ============================================================
# CONFIG - Customize your magazine here!
# ============================================================

COUPLE_NAMES = "Sunipa & Riktam"
ANNIVERSARY_DATE = "March 31st, 2025"
MAGAZINE_TITLE = "Our Love Story"
SUBTITLE = "Celebrating 1 Year of Us"
OUTPUT_FILE = "anniversary_magazine.pdf"

PRIMARY = "#C2185B"
SECONDARY = "#F8BBD0"
ACCENT = "#880E4F"
DARK = "#4A4A4A"
WHITE = "#FFFFFF"

LOVE_LETTER = """My Dearest,

One year ago, our story began — and every single day since
has been the most beautiful chapter of my life.

You are my favorite hello and my hardest goodbye.
Thank you for 365 days of laughter, love, and magic.

Here's to a lifetime of us.

Forever yours."""

MILESTONES = [
    ("Day 1", "The day we first met — butterflies everywhere"),
    ("Month 1", "Our first official date — coffee & endless talks"),
    ("Month 3", "Said 'I love you' for the first time"),
    ("Month 6", "Our first trip together — unforgettable memories"),
    ("Month 9", "Met each other's families — it got real!"),
    ("1 Year", "365 days of pure magic — and counting!"),
]

PHOTOS = [
    ("photo1.jpg", "Where it all began"),
    ("photo2.jpg", "Our favorite adventure"),
    ("photo3.jpg", "The little moments matter most"),
    ("photo4.jpg", "Always laughing with you"),
]

# ============================================================

W, H = A4


def bg(c, color):
    c.setFillColor(HexColor(color))
    c.rect(0, 0, W, H, fill=1, stroke=0)


def text(c, s, y, font="Helvetica", size=24, color=WHITE):
    c.setFont(font, size)
    c.setFillColor(HexColor(color))
    c.drawCentredString(W / 2, y, s)


def wrapped(c, s, x, y, max_w, font="Helvetica", size=12, color=DARK, lead=18):
    c.setFont(font, size)
    c.setFillColor(HexColor(color))
    for line in s.split("\n"):
        cur = ""
        for word in line.split():
            test = f"{cur} {word}".strip()
            if c.stringWidth(test, font, size) < max_w:
                cur = test
            else:
                c.drawString(x, y, cur)
                y -= lead
                cur = word
        c.drawString(x, y, cur)
        y -= lead


def heart(c, cx, cy, sz=30, color=PRIMARY):
    c.setFillColor(HexColor(color))
    r = sz / 4
    c.circle(cx - r, cy + r * 0.5, r, fill=1, stroke=0)
    c.circle(cx + r, cy + r * 0.5, r, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(cx - sz / 2, cy + r * 0.3)
    p.lineTo(cx, cy - sz / 2)
    p.lineTo(cx + sz / 2, cy + r * 0.3)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def bar(c, y, h, color=ACCENT):
    c.setFillColor(HexColor(color))
    c.rect(0, y, W, h, fill=1, stroke=0)


def load_img(name):
    path = os.path.join("photos", name)
    return ImageReader(path) if os.path.exists(path) else None


def cover(c):
    bg(c, PRIMARY)
    bar(c, H - 80, 80)
    text(c, "SPECIAL EDITION", H - 55, size=14)
    text(c, MAGAZINE_TITLE.upper(), H - 200, "Helvetica-Bold", 48)
    c.setStrokeColor(HexColor(SECONDARY))
    c.setLineWidth(2)
    c.line(W / 2 - 100, H - 230, W / 2 + 100, H - 230)
    text(c, SUBTITLE, H - 270, size=22, color=SECONDARY)
    text(c, COUPLE_NAMES, H / 2, "Helvetica-BoldOblique", 40)
    heart(c, W / 2, H / 2 - 70, 50, SECONDARY)
    text(c, ANNIVERSARY_DATE, 150, size=18, color=SECONDARY)
    bar(c, 0, 60)
    text(c, "1st Anniversary Edition", 25, size=12)


def timeline(c):
    bg(c, "#FFF5F5")
    bar(c, H - 100, 100, PRIMARY)
    text(c, "Our Timeline", H - 65, "Helvetica-Bold", 36)

    lx, sy = W / 2, H - 160
    c.setStrokeColor(HexColor(SECONDARY))
    c.setLineWidth(3)
    c.line(lx, sy, lx, 80)

    gap = (sy - 80) / max(len(MILESTONES), 1)
    for i, (label, desc) in enumerate(MILESTONES):
        y = sy - i * gap
        c.setFillColor(HexColor(PRIMARY))
        c.circle(lx, y, 8, fill=1, stroke=0)
        c.setFillColor(HexColor(WHITE))
        c.circle(lx, y, 4, fill=1, stroke=0)

        cx = 40 if i % 2 == 0 else lx + 30
        cw = W / 2 - 70
        c.setFillColor(HexColor("#FFFFFF"))
        c.roundRect(cx, y - 25, cw, 50, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor(SECONDARY))
        c.setLineWidth(1)
        c.roundRect(cx, y - 25, cw, 50, 8, fill=0, stroke=1)

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(HexColor(PRIMARY))
        c.drawString(cx + 10, y + 8, label)
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor(DARK))
        c.drawString(cx + 10, y - 10, desc)


def photo_page(c, photos, title="Memories"):
    bg(c, "#FFFFFF")
    bar(c, H - 80, 80, PRIMARY)
    text(c, title, H - 50, "Helvetica-Bold", 28)

    for i, (fname, caption) in enumerate(photos[:2]):
        y = H - 130 - i * 350
        fx, fw, fh = 60, W - 120, 290
        c.setFillColor(HexColor("#F5F5F5"))
        c.roundRect(fx, y - fh, fw, fh, 10, fill=1, stroke=0)

        img = load_img(fname)
        if img:
            c.drawImage(img, fx + 10, y - fh + 40, fw - 20, fh - 50,
                        preserveAspectRatio=True, anchor='c', mask='auto')
        else:
            text(c, f"[ Place {fname} in photos/ ]", y - fh / 2, size=14, color=DARK)

        c.setFont("Helvetica-Oblique", 13)
        c.setFillColor(HexColor(PRIMARY))
        c.drawCentredString(W / 2, y - fh - 5, caption)


def love_letter(c):
    bg(c, ACCENT)
    m = 40
    c.setStrokeColor(HexColor(SECONDARY))
    c.setLineWidth(2)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 15, fill=0, stroke=1)

    c.setFillColor(HexColor("#FFFFFF"))
    c.setFillAlpha(0.15)
    c.roundRect(55, 55, W - 110, H - 110, 10, fill=1, stroke=0)
    c.setFillAlpha(1)

    text(c, "A Letter For You", H - 120, "Helvetica-BoldOblique", 32, SECONDARY)
    c.setStrokeColor(HexColor(SECONDARY))
    c.setLineWidth(1)
    c.line(W / 2 - 80, H - 145, W / 2 + 80, H - 145)
    wrapped(c, LOVE_LETTER, 80, H - 190, W - 160, size=15, color=WHITE, lead=24)
    heart(c, W / 2, 100, 40, SECONDARY)


def closing(c):
    bg(c, PRIMARY)
    text(c, "Here's to", H - 250, size=24, color=SECONDARY)
    text(c, "Forever", H - 320, "Helvetica-BoldOblique", 60)
    text(c, "with you", H - 370, size=24, color=SECONDARY)
    heart(c, W / 2, H / 2 - 30, 60, SECONDARY)
    text(c, COUPLE_NAMES, 200, "Helvetica-Bold", 28)
    text(c, f"Est. {ANNIVERSARY_DATE}", 165, size=16, color=SECONDARY)
    bar(c, 0, 50)
    text(c, f"Made with love — {datetime.now().year}", 20, size=10)


def generate():
    c = canvas.Canvas(OUTPUT_FILE, pagesize=A4)
    c.setTitle(f"{MAGAZINE_TITLE} — {COUPLE_NAMES}")

    for page_fn in [cover, timeline]:
        page_fn(c)
        c.showPage()

    for i in range(0, len(PHOTOS), 2):
        n = i // 2 + 1
        photo_page(c, PHOTOS[i:i + 2], "Our Memories" if n == 1 else f"More Memories — {n}")
        c.showPage()

    for page_fn in [love_letter, closing]:
        page_fn(c)
        c.showPage()

    c.save()
    print(f"Done! {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
