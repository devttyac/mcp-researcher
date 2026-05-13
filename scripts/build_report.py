#!/usr/bin/env python3
"""
MCP Researcher report builder.
Reads a structured JSON data file and fills the appropriate HTML template.
The model writes small JSON; this script generates all HTML — nothing large
ever flows through the model response stream.

Usage:
  python3 build_report.py <data.json> <output.html>

JSON schema: see SKILL.md Step 5 — Generate Report.
"""

import json
import math
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "references"


def score_class(score):
    if score >= 80:
        return "score-green"
    if score >= 60:
        return "score-amber"
    if score >= 40:
        return "score-orange"
    return "score-red"


def fmt_stars(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def build_digest(data, template):
    servers = data["servers"]
    top = servers[0] if servers else {}
    stats = data.get("stats", {})

    chips_html = "".join(
        f'<span class="chip">{c["icon"]} {c["text"]}</span>'
        for c in data.get("top_chips", [])
    )

    ideas_html = "".join(
        f'<div class="idea-item"><div class="idea-title">{i["title"]}</div>'
        f'<div class="idea-body">{i["body"]}</div></div>\n'
        for i in data.get("ideas", [])
    )

    servers_json = json.dumps([
        {
            "name": s["name"], "url": s["url"], "cat": s.get("cat", ""),
            "score": s["score"], "stars": s["stars"], "commit": s["commit"],
            "lang": s.get("lang", ""), "src": s.get("src", ""),
            "desc": s.get("desc", ""), "abandoned": s.get("abandoned", False),
        }
        for s in servers
    ])

    time_series = data.get("time_series", [])
    avg_score = stats.get("avg_score", 0)
    peak_stars = stats.get("peak_stars", 0)

    replacements = {
        "DATE": data["date"],
        "DAY_OF_WEEK": data.get("day_of_week", ""),
        "SERVER_COUNT": str(len(servers)),
        "SOURCING_NOTE": data.get("sourcing_note", ""),
        "TOP_SCORE": str(top.get("score", 0)),
        "TOP_SCORE_CLASS": score_class(top.get("score", 0)),
        "TOP_NAME": top.get("name", ""),
        "TOP_URL": top.get("url", ""),
        "TOP_CAT": top.get("cat", ""),
        "TOP_DESC": top.get("desc", ""),
        "TOP_CHIPS": chips_html,
        "STAT_SERVERS": str(len(servers)),
        "STAT_AVG_SCORE": f"{avg_score:.1f}",
        "STAT_ABANDONMENT": f"{stats.get('abandonment_pct', 0)}%",
        "STAT_SOURCES": str(stats.get("sources_count", 0)),
        "STAT_GTE40": str(stats.get("gte40_count", 0)),
        "STAT_PEAK_STARS": fmt_stars(peak_stars),
        "IDEAS_HTML": ideas_html,
        "SERVERS_JSON": servers_json,
        "TIME_LABELS_JSON": json.dumps([t["label"] for t in time_series]),
        "TIME_VALS_JSON": json.dumps([t["count"] for t in time_series]),
    }

    for key, val in replacements.items():
        template = template.replace("{{" + key + "}}", val)
    return template


def build_deep_dive(data, template):
    servers = data["servers"]
    stats = data.get("stats", {})

    cards_html = ""
    for card in data.get("top_cards", []):
        s = card.get("stats", {})
        tools_html = "".join(
            f'<span class="tool-chip">{t}</span>' for t in card.get("tools", [])
        )
        examples_text = " ".join(card.get("examples", []))
        cards_html += f"""<div class="dd-card">
  <div class="dd-card-hdr">
    <div class="dd-score">
      <span class="num score-badge {score_class(card['score'])}">{card['score']}</span>
      <span class="denom">/100</span>
    </div>
    <div>
      <div class="dd-name"><a href="{card['url']}" target="_blank">{card['name']}</a></div>
      <div class="dd-meta">{card.get('meta', '')}</div>
    </div>
  </div>
  <div class="dd-desc">{card.get('desc', '')}</div>
  <div class="dd-stats">
    <span><strong>{s.get('stars', 0):,}</strong> stars</span>
    <span><strong>{s.get('forks', 0)}</strong> forks</span>
    <span><strong>{s.get('commit', '')}</strong> last commit</span>
    <span><strong>{s.get('installs', 0):,}</strong> installs</span>
    <span><strong>{s.get('contributors', 0)}</strong> contributors</span>
  </div>
  <div class="dd-section">
    <div class="dd-lbl">Tools Exposed</div>
    <div class="tools-list">{tools_html}</div>
  </div>
  <div class="dd-section">
    <div class="dd-lbl">Usage Examples</div>
    <div class="dd-body">{examples_text}</div>
  </div>
  <div class="pros-cons">
    <div class="pros"><h4>Strengths</h4><div class="dd-body">{card.get('pros', '')}</div></div>
    <div class="cons"><h4>Limitations</h4><div class="dd-body">{card.get('cons', '')}</div></div>
  </div>
</div>\n"""

    impl_html = "".join(
        f'<div class="combo"><div class="combo-title">{i["title"]}</div>'
        f'<div class="combo-desc">{i["desc"]}</div></div>\n'
        for i in data.get("impl_map", [])
    )

    servers_json = json.dumps([
        {
            "name": s["name"], "url": s["url"], "subcat": s.get("subcat", ""),
            "score": s["score"], "stars": s["stars"], "commit": s["commit"],
            "installs": s.get("installs", 0), "complexity": s.get("complexity", ""),
            "lang": s.get("lang", ""), "src": s.get("src", 0),
            "desc": s.get("desc", ""), "abandoned": s.get("abandoned", False),
        }
        for s in servers
    ])

    avg_score = stats.get("avg_score", 0)

    replacements = {
        "DATE": data["date"],
        "CATEGORY": data.get("category", ""),
        "SERVER_COUNT": str(len(servers)),
        "SOURCING_NOTE": data.get("sourcing_note", ""),
        "EXEC_SUMMARY": data.get("exec_summary", ""),
        "STAT_TOTAL": str(len(servers)),
        "STAT_AVG_SCORE": f"{avg_score:.1f}",
        "STAT_ABANDONMENT": str(stats.get("abandonment_pct", 0)),
        "STAT_MEDIAN_STARS": str(stats.get("median_stars", 0)),
        "STAT_MEDIAN_DAYS": str(stats.get("median_days", 0)),
        "STAT_SOURCES": str(stats.get("sources_count", 0)),
        "DEEP_DIVE_CARDS_HTML": cards_html,
        "IMPL_MAP_HTML": impl_html,
        "RECOMMENDATION_HTML": data.get("recommendation", ""),
        "SERVERS_JSON": servers_json,
        "SUBCATS_JSON": json.dumps(data.get("subcats", [])),
    }

    for key, val in replacements.items():
        template = template.replace("{{" + key + "}}", val)
    return template


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <data.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    data_path, output_path = sys.argv[1], sys.argv[2]

    with open(data_path) as f:
        data = json.load(f)

    mode = data["mode"]
    template_name = "digest-template.html" if mode == "digest" else "deep-dive-template.html"

    with open(TEMPLATES_DIR / template_name) as f:
        template = f.read()

    output = build_digest(data, template) if mode == "digest" else build_deep_dive(data, template)

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
