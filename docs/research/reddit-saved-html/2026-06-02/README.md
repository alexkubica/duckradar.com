# Reddit Saved HTML Captures

Date moved into repo: 2026-06-02

These are operator-supplied saved Reddit thread pages used for DuckRadar market research.

Only the top-level `.html` files are tracked. Browser-created `_files` asset folders were left out because the local importer reads the HTML captures directly and the asset bundles add hundreds of megabytes of CSS, JavaScript, images, and CAPTCHA resources that are not needed for research reproducibility.

Import command:

```bash
while IFS= read -r -d '' file; do
  python3 scripts/signals/collect.py --db data/signals.sqlite --group seo --import-reddit-html "$file"
done < <(find docs/research/reddit-saved-html/2026-06-02 -maxdepth 1 -type f \( -iname '*.html' -o -iname '*.htm' \) -print0)
```
