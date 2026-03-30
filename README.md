# 💕 Anniversary Magazine PDF Generator

A pure Python project to create a beautiful magazine-style PDF for your 1st love anniversary.

## Pages Included
- **Cover Page** — Title, couple names, date
- **Timeline** — Relationship milestones in a visual timeline
- **Photo Pages** — Your photos with captions (2 per page)
- **Love Letter** — A personal message page
- **Closing Page** — "Here's to Forever"

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Place your photos in the `photos/` folder
2. Open `magazine.py` and customize the **CONFIG** section:
   - `COUPLE_NAMES` — Your names
   - `ANNIVERSARY_DATE` — Your special date
   - `LOVE_LETTER` — Your personal message
   - `MILESTONES` — Your relationship timeline
   - `PHOTOS` — Photo filenames and captions
   - Colors, title, subtitle, etc.
3. Run:
   ```bash
   python magazine.py
   ```
4. Open `anniversary_magazine.pdf` 🎉
