# Sell Front proposal for brands

The brand proposal as a web page, in ten languages: English, Hindi, Marathi, Gujarati, Punjabi, Bengali, Telugu, Tamil, Kannada and Malayalam.

Live: https://alokverma2004.github.io/sellfront-proposal/ (each language also has its own link, e.g. `/te/` for Telugu).

## Change the text

1. Edit the words in `i18n/en.json`, and the same key in each other language file.
2. Run `python3 src/build.py`. It rebuilds `index.html` and every `<language>/index.html`.
3. Commit and push. GitHub Pages updates in about a minute.

The layout is `src/template.html`; the look is `assets/site.css`.
