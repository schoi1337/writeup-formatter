# Writeup Formatter
This Python automation script processes HackTheBox-style writeups written in Obsidian for Jekyll blogs. It prepares `.md` files with proper front matter, optimizes and renames images, rewrites image paths, and formats everything for SEO and publishing.

---

## 📁 Folder Structure & User Responsibilities
### Before Running (`htb_writeups/`)
```yaml
htb_writeups/
├── forest/
│   ├── forest.md             # Optional: if missing, script auto-creates
│   └── Attachments/
│       ├── screen1.png       # Optional: original images, renamed + optimized
├── monteverde/
│   ├── monteverde.md
│   └── Attachments/
│       └── screenshot.jpg
writeup-formatter.py        # The automation script
```

### After Execution
```yaml
_posts/
├── 2024-10-01-forest.md        # Front matter + updated image links
├── 2024-09-12-monteverde.md

assets/
└── images/
    ├── forest1.png             # Renamed + optimized
    ├── forest2.png
    └── monteverde1.jpg
```

## ✅ What You Need to Do
- Create one folder per box under `htb_writeups/`
- Inside each, place:
    - `boxname.md` — the writeup (same name as folder, This is optional. If missing,   script auto-creates)
    - `Attachments/` — any screenshots or images
- Then run the script from your root project directory

## 🛠️ How to Use
1. Set up Python venv (recommended)
```python
python -m venv venv
venv\\Scripts\\activate        # on Windows
pip install pillow
```

2. Run the script
```python
python upload_htb_writeups.py
```

##📦 What This Script Does
✅ Creates `boxname.md` if missing, with a template
✅ Adds front matter (title, date, categories, tags)
✅ Randomizes post dates (within past 1.5 years, no duplicates)
✅ Renames images (i.e.`forest1.png`, `forest2.png` ...)
✅ Resizes images to max 1200px width, 80% quality
✅ Moves images to `assets/images/`
✅ Replaces all image paths in .md with `/assets/images/xxx.png`
✅ Creates `_posts/` and `assets/images/` folders if missing
