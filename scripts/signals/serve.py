#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.signals.config import DEFAULT_DB_PATH, SOURCE_GROUPS
from scripts.signals.db import SignalsDB


SIGNAL_TYPES = [
    "pain",
    "lead_source",
    "idea",
    "competitor",
    "workflow",
    "tool_pricing",
    "ai_search",
    "agency_reporting",
    "sales_outreach",
    "unknown",
]

ENTRY_TYPES = ["post", "comment", "rss_entry", "external_export"]
RESULT_LIMITS = [200, 500, 1000, 2500, 5000]


class SignalsHandler(BaseHTTPRequestHandler):
    db: SignalsDB

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.render_index(parse_qs(parsed.query))
            return
        if parsed.path == "/entry":
            self.render_entry(parse_qs(parsed.query))
            return
        if parsed.path == "/runs":
            self.render_runs()
            return
        self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/tag":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)
        entry_id = int(first(form, "id") or "0")
        tags = [tag.strip() for tag in (first(form, "tags") or "").split(",") if tag.strip()]
        self.db.set_entry_tags(entry_id, tags)
        self.redirect(f"/entry?id={entry_id}")

    def render_index(self, query: dict[str, list[str]]) -> None:
        search = first(query, "q")
        source_group = first(query, "group")
        community = first(query, "community")
        signal_type = first(query, "signal_type")
        entry_type = first(query, "entry_type")
        result_limit = parse_result_limit(query)
        rows = self.db.search_entries(
            search,
            source_group=source_group or None,
            community=community or None,
            signal_type=signal_type or None,
            entry_type=entry_type or None,
            limit=result_limit,
        )
        communities = self.db.list_communities()
        content = f"""
        <section class="toolbar">
          <form method="get" action="/" class="search-form">
            <input type="search" name="q" value="{esc(search)}" placeholder="Search cached signals">
            {select("group", source_group, ["", *SOURCE_GROUPS.keys()])}
            {select("community", community, ["", *communities])}
            {select("signal_type", signal_type, ["", *SIGNAL_TYPES])}
            {select("entry_type", entry_type, ["", *ENTRY_TYPES])}
            {select("limit", str(result_limit), [str(limit) for limit in RESULT_LIMITS])}
            <button type="submit">Search</button>
            <a class="button secondary" href="/runs">Runs</a>
          </form>
        </section>
        <section class="result-meta">{len(rows)} results shown, limit {result_limit}</section>
        <section class="results">
          {''.join(result_row(row, self.db.get_entry_tags(row["id"])) for row in rows) or '<p class="empty">No cached signals match this search.</p>'}
        </section>
        """
        self.respond(page("Signals", content))

    def render_entry(self, query: dict[str, list[str]]) -> None:
        entry_id = int(first(query, "id") or "0")
        row = self.db.get_entry(entry_id)
        if not row:
            self.send_error(404)
            return
        tags = self.db.get_entry_tags(entry_id)
        evidence = evidence_note(row)
        content = f"""
        <nav class="subnav"><a href="/">Search</a> <a href="/runs">Runs</a></nav>
        <article class="detail">
          <div class="eyebrow">{esc(row['source_group'])} / {esc(row['community'])} / {esc(row['signal_type'])}</div>
          <div class="badges">{evidence_badges_html(row)}</div>
          <h1>{esc(row['title'])}</h1>
          <div class="meta">
            <span>{esc(row['created_at'])}</span>
            <span>{esc(row['author_username'])}</span>
            <span>{esc(row['entry_type'])}</span>
          </div>
          <p class="source"><a href="{esc(row['url'])}">{esc(row['url'])}</a></p>
          <pre class="body">{esc(row['body'])}</pre>
          <form method="post" action="/tag" class="tag-form">
            <input type="hidden" name="id" value="{entry_id}">
            <label>Tags</label>
            <input name="tags" value="{esc(', '.join(tags))}" placeholder="idea, pain, lead_source">
            <button type="submit">Save Tags</button>
          </form>
          <section class="evidence">
            <h2>Evidence Note</h2>
            <textarea id="evidence-note" readonly>{esc(evidence)}</textarea>
            <button type="button" onclick="navigator.clipboard.writeText(document.getElementById('evidence-note').value)">Copy</button>
          </section>
          <details>
            <summary>Raw JSON</summary>
            <pre class="body">{esc(str(row['raw_json']))}</pre>
          </details>
        </article>
        """
        self.respond(page(row["title"], content))

    def render_runs(self) -> None:
        rows = self.db.list_runs(limit=100)
        body = "".join(
            f"""
            <tr>
              <td>{run['id']}</td>
              <td>{esc(run['finished_at'])}</td>
              <td>{esc(run['source_group'])}</td>
              <td>{esc(run['source'])}</td>
              <td><span class="status {esc(run['status'])}">{esc(run['status'])}</span></td>
              <td>{run['entries_inserted']}/{run['entries_seen']}</td>
              <td>{esc(run['message'])}</td>
            </tr>
            """
            for run in rows
        )
        content = f"""
        <nav class="subnav"><a href="/">Search</a></nav>
        <table class="runs">
          <thead>
            <tr><th>ID</th><th>Finished</th><th>Group</th><th>Source</th><th>Status</th><th>Inserted/Seen</th><th>Message</th></tr>
          </thead>
          <tbody>{body}</tbody>
        </table>
        """
        self.respond(page("Runs", content))

    def redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def respond(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def first(query: dict[str, list[str]], key: str) -> str:
    values = query.get(key) or [""]
    return values[0]


def parse_result_limit(query: dict[str, list[str]]) -> int:
    raw_limit = first(query, "limit")
    if not raw_limit:
        return 1000
    try:
        limit = int(raw_limit)
    except ValueError:
        return 1000
    return limit if limit in RESULT_LIMITS else 1000


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def select(name: str, current: str, options: list[str]) -> str:
    html_options = []
    label = {
        "group": "All groups",
        "community": "All communities",
        "signal_type": "All signals",
        "entry_type": "All types",
        "limit": "Limit",
    }[name]
    for option in options:
        text = option or label
        selected = " selected" if option == current else ""
        html_options.append(f'<option value="{esc(option)}"{selected}>{esc(text)}</option>')
    return f'<select name="{name}">{"".join(html_options)}</select>'


def result_row(row: dict[str, object], tags: list[str]) -> str:
    tag_html = " ".join(f'<span class="tag">{esc(tag)}</span>' for tag in tags)
    badge_html = evidence_badges_html(row)
    params = urlencode({"id": row["id"]})
    snippet = str(row.get("body") or "")[:280]
    return f"""
    <article class="result">
      <div class="result-head">
        <a href="/entry?{params}">{esc(row['title'])}</a>
        <span>{esc(row['community'])}</span>
      </div>
      <div class="meta">
        <span>{esc(row['created_at'])}</span>
        <span>{esc(row['author_username'])}</span>
        <span>{esc(row['signal_type'])}</span>
        <span>{esc(row['entry_type'])}</span>
      </div>
      <div class="badges">{badge_html}</div>
      <p>{esc(snippet)}</p>
      <div class="tags">{tag_html}</div>
    </article>
    """


def evidence_badges_html(row: dict[str, object]) -> str:
    return " ".join(f'<span class="badge">{esc(label)}</span>' for label in evidence_labels(row))


def evidence_labels(row: dict[str, object]) -> list[str]:
    source = str(row.get("source") or "")
    raw_json = row.get("raw_json")
    raw = raw_json if isinstance(raw_json, dict) else {}
    labels: list[str] = []

    if source == "reddit_html" or raw.get("capture_format") == "reddit_saved_html":
        labels.append("saved HTML")
    elif source == "reddit_rss":
        labels.append("RSS cache")
    elif source:
        labels.append(source)

    if raw.get("evidence_type") == "manual_paste":
        labels.append("manual capture")
    if raw.get("visible_comments_only"):
        labels.append("visible comments")
    return labels


def evidence_note(row: dict[str, object]) -> str:
    return (
        f"- {row['community']}, {row['created_at']}: "
        f"\"{row['title']}\" {row['url']}"
    )


def page(title: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} - DuckRadar Signals</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --panel: #ffffff;
      --text: #1f2723;
      --muted: #65706a;
      --line: #d8ddd8;
      --accent: #136f63;
      --warn: #9b4a17;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 14px;
      line-height: 1.45;
    }}
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 20px;
      border-bottom: 1px solid var(--line);
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 1;
    }}
    header h1 {{ margin: 0; font-size: 18px; font-weight: 650; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 18px 20px 40px; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .toolbar {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
    }}
    .search-form {{
      display: grid;
      grid-template-columns: minmax(220px, 1fr) repeat(4, minmax(130px, 170px)) auto auto;
      gap: 8px;
      align-items: center;
    }}
    input, select, button, .button {{
      min-height: 36px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 10px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }}
    button, .button {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
    }}
    .button.secondary {{ background: #fff; color: var(--accent); }}
    .result-meta {{ margin: 14px 0 8px; color: var(--muted); }}
    .results {{ display: grid; gap: 10px; }}
    .result, .detail, .runs {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .result {{ padding: 12px; }}
    .result-head {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
      font-weight: 650;
    }}
    .result-head span, .meta, .eyebrow {{ color: var(--muted); font-size: 12px; }}
    .meta {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 6px; }}
    .result p {{ margin: 8px 0 0; }}
    .tags {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }}
    .tag, .badge {{
      border: 1px solid var(--line);
      background: #eef4f0;
      color: #285247;
      border-radius: 999px;
      padding: 2px 8px;
      font-size: 12px;
    }}
    .badges {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }}
    .badge {{ background: #fff7e8; color: #6c3d0b; border-color: #e7c47e; }}
    .subnav {{ margin-bottom: 12px; display: flex; gap: 12px; }}
    .detail {{ padding: 18px; }}
    .detail h1 {{ margin: 4px 0 8px; font-size: 24px; letter-spacing: 0; }}
    .source {{ overflow-wrap: anywhere; }}
    .body {{
      white-space: pre-wrap;
      background: #f1f3ef;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 12px;
      overflow-x: auto;
    }}
    .tag-form {{
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 8px;
      align-items: center;
      margin: 16px 0;
    }}
    .evidence textarea {{
      width: 100%;
      min-height: 90px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      font: inherit;
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 9px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    .status.aborted, .status.failed {{ color: var(--warn); font-weight: 650; }}
    .status.success {{ color: var(--accent); font-weight: 650; }}
    .empty {{ color: var(--muted); }}
    @media (max-width: 900px) {{
      .search-form {{ grid-template-columns: 1fr 1fr; }}
      .tag-form {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>DuckRadar Signals</h1>
    <div>Local cache</div>
  </header>
  <main>{content}</main>
</body>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the local DuckRadar signals browser.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    db = SignalsDB(Path(args.db))
    db.init_schema()
    SignalsHandler.db = db
    server = ThreadingHTTPServer((args.host, args.port), SignalsHandler)
    print(f"Serving DuckRadar Signals at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
