"""Build one static page per language from src/template.html and i18n/*.json.

    python3 src/build.py

English goes to index.html; every other language to <code>/index.html.
"""
import html
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://alokverma2004.github.io/sellfront-proposal/"

# code, native name, OG locale, Google Fonts family for the script (None = Latin)
LANGS = [
    ("en", "English", "en_IN", None),
    ("hi", "हिन्दी", "hi_IN", "Mukta"),
    ("mr", "मराठी", "mr_IN", "Mukta"),
    ("gu", "ગુજરાતી", "gu_IN", "Mukta Vaani"),
    ("pa", "ਪੰਜਾਬੀ", "pa_IN", "Mukta Mahee"),
    ("bn", "বাংলা", "bn_IN", "Hind Siliguri"),
    ("te", "తెలుగు", "te_IN", "Hind Guntur"),
    ("ta", "தமிழ்", "ta_IN", "Mukta Malar"),
    ("kn", "ಕನ್ನಡ", "kn_IN", "Noto Sans Kannada"),
    ("ml", "മലയാളം", "ml_IN", "Noto Sans Malayalam"),
]


def page_url(code):
    return BASE if code == "en" else f"{BASE}{code}/"


def main():
    tpl = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    en = json.loads((ROOT / "i18n" / "en.json").read_text(encoding="utf-8"))
    ver = time.strftime("%Y%m%d%H%M")
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{page_url(c)}">' for c, *_ in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'

    built = []
    for code, native, locale, font in LANGS:
        path = ROOT / "i18n" / f"{code}.json"
        if not path.exists():
            print(f"skip {code}: no translation yet")
            continue
        t = json.loads(path.read_text(encoding="utf-8"))
        missing = set(en) - set(t)
        if missing:
            raise SystemExit(f"{code}: missing keys {sorted(missing)}")
        p = "" if code == "en" else "../"

        def chip_href(c):
            if c == code:
                return "./"
            if code == "en":
                return f"{c}/"
            return "../" if c == "en" else f"../{c}/"

        chips = "".join(
            f'<a class="chip" href="{chip_href(c)}" hreflang="{c}" lang="{c}"'
            + (' aria-current="page"' if c == code else "")
            + f">{n}</a>"
            for c, n, *_ in LANGS
            if (ROOT / "i18n" / f"{c}.json").exists()
        )
        font_link = ""
        script_font = "system-ui"
        if font:
            fam = font.replace(" ", "+")
            font_link = (
                f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}'
                f':wght@400;500;600;700&display=swap">'
            )
            script_font = f"'{font}'"
        vars_ = {
            "lang": code,
            "script": "indic" if font else "latin",
            "scriptFont": script_font,
            "scriptFontLink": font_link,
            "url": page_url(code),
            "base": BASE,
            "locale": locale,
            "alternates": alternates,
            "chips": chips,
            "p": p,
            "home": "./",
            "ver": ver,
        }

        def sub(m):
            key = m.group(1)
            if key.startswith("@"):
                return vars_[key[1:]]
            return html.escape(t[key], quote=True)

        out = re.sub(r"\{\{([@\w.]+)\}\}", sub, tpl)
        left = re.findall(r"\{\{[^}]*\}\}", out)
        if left:
            raise SystemExit(f"{code}: unfilled {left}")
        dest = ROOT / ("index.html" if code == "en" else f"{code}/index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        built.append(code)
    print("built:", " ".join(built))


if __name__ == "__main__":
    main()
