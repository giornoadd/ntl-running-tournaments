#!/usr/bin/env python3
"""Generate docs/index.html landing page from tournament markdown sources."""
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

def get_current_week():
    """Determine the current tournament week based on date (Mar 11 = Week 11)."""
    now = datetime.now()
    # Week calendar data: (week_num, start_date, end_date)
    weeks = [
        (1, "2026-01-01", "2026-01-03"),
        (2, "2026-01-04", "2026-01-10"),
        (3, "2026-01-11", "2026-01-17"),
        (4, "2026-01-18", "2026-01-24"),
        (5, "2026-01-25", "2026-01-31"),
        (6, "2026-02-01", "2026-02-07"),
        (7, "2026-02-08", "2026-02-14"),
        (8, "2026-02-15", "2026-02-21"),
        (9, "2026-02-22", "2026-02-28"),
        (10, "2026-03-01", "2026-03-07"),
        (11, "2026-03-08", "2026-03-14"),
        (12, "2026-03-15", "2026-03-21"),
        (13, "2026-03-22", "2026-03-28"),
    ]
    for wk, start, end in weeks:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        if s <= now <= e:
            return wk
    return 11  # fallback

def generate_calendar_rows(current_week):
    """Generate HTML table rows for Q1 calendar with current week highlighted."""
    q1_weeks = [
        (1, "1 Jan – 3 Jan", "Thu – Sat", "🎉 Competition Kick-off!"),
        (2, "4 Jan – 10 Jan", "Sun – Sat", ""),
        (3, "11 Jan – 17 Jan", "Sun – Sat", ""),
        (4, "18 Jan – 24 Jan", "Sun – Sat", ""),
        (5, "25 Jan – 31 Jan", "Sun – Sat", "🧧 Chinese New Year"),
        (6, "1 Feb – 7 Feb", "Sun – Sat", ""),
        (7, "8 Feb – 14 Feb", "Sun – Sat", "💕 Valentine's Day"),
        (8, "15 Feb – 21 Feb", "Sun – Sat", ""),
        (9, "22 Feb – 28 Feb", "Sun – Sat", ""),
        (10, "1 Mar – 7 Mar", "Sun – Sat", ""),
        (11, "8 Mar – 14 Mar", "Sun – Sat", ""),
        (12, "15 Mar – 21 Mar", "Sun – Sat", ""),
        (13, "22 Mar – 28 Mar", "Sun – Sat", ""),
        ("—", "29 Mar – 31 Mar", "Sun – Tue", "⚡ Q1 Final Sprint!"),
    ]
    
    rows = []
    for wk, dates, period, notes in q1_weeks:
        is_current = (wk == current_week)
        cls = ' class="current-week"' if is_current else ''
        badge = ' <span class="badge">📍 NOW</span>' if is_current else ''
        rows.append(f'<tr{cls}><td>{wk}</td><td>{dates}</td><td>{period}</td><td>{notes}{badge}</td></tr>')
    return "\n".join(rows)

def generate_quarter_rows():
    """Generate quarter summary rows."""
    return """
    <tr class="current-week"><td>Q1 🟢</td><td>1 Jan – 31 Mar</td><td>13</td><td>In Progress</td></tr>
    <tr><td>Q2 ⬜</td><td>1 Apr – 30 Jun</td><td>13</td><td>Upcoming</td></tr>
    <tr><td>Q3 ⬜</td><td>1 Jul – 30 Sep</td><td>13</td><td>Upcoming</td></tr>
    <tr><td>Q4 ⬜</td><td>1 Oct – 31 Dec</td><td>13</td><td>Upcoming</td></tr>
    """

def main():
    current_week = get_current_week()
    calendar_rows = generate_calendar_rows(current_week)
    quarter_rows = generate_quarter_rows()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Running Competition 2026 — Mandalorian vs IT System</title>
<meta name="description" content="Official tournament hub for the 2026 Running Competition between Mandalorian and IT System teams.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=Outfit:wght@700;900&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0a0e1a;
  --surface: #111827;
  --border: rgba(255,255,255,0.08);
  --text: #e2e8f0;
  --muted: #94a3b8;
  --accent: #22d3ee;
  --manda: #00ff88;
  --it: #00ccff;
  --warning: #fbbf24;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Inter', -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  min-height: 100vh;
}}
.container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}

/* Header */
.hero {{
  text-align: center;
  padding: 3rem 1rem 2rem;
  background: linear-gradient(135deg, rgba(0,255,136,0.05), rgba(0,204,255,0.05));
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
}}
.hero h1 {{
  font-family: 'Outfit', sans-serif;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 900;
  background: linear-gradient(135deg, var(--manda), var(--it));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}}
.hero .subtitle {{
  font-size: 1.1rem;
  color: var(--muted);
}}
.hero .status {{
  display: inline-block;
  margin-top: 1rem;
  padding: 0.4rem 1rem;
  border-radius: 999px;
  background: rgba(0,255,136,0.1);
  border: 1px solid rgba(0,255,136,0.2);
  color: var(--manda);
  font-size: 0.85rem;
  font-weight: 600;
}}

/* Dashboard CTA */
.cta-card {{
  display: block;
  text-align: center;
  padding: 1.5rem 2rem;
  margin: 2rem 0;
  background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(0,204,255,0.08));
  border: 1px solid var(--border);
  border-radius: 16px;
  text-decoration: none;
  transition: all 0.3s ease;
}}
.cta-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,204,255,0.15);
  border-color: var(--accent);
}}
.cta-card .cta-title {{
  font-family: 'Outfit', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 0.25rem;
}}
.cta-card .cta-sub {{
  font-size: 0.9rem;
  color: var(--muted);
}}

/* Cards */
.card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
}}
.card h2 {{
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}}

/* Rules */
.rules-grid {{ display: grid; gap: 1rem; }}
.rule-item {{
  padding: 1rem 1.25rem;
  background: rgba(255,255,255,0.02);
  border-radius: 12px;
  border-left: 3px solid var(--accent);
}}
.rule-item h3 {{
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: var(--accent);
}}
.rule-item p, .rule-item ul {{
  font-size: 0.9rem;
  color: var(--muted);
}}
.rule-item ul {{ padding-left: 1.2rem; }}
.rule-item li {{ margin-bottom: 0.2rem; }}
.warning-box {{
  padding: 0.75rem 1rem;
  border-radius: 10px;
  background: rgba(251,191,36,0.08);
  border: 1px solid rgba(251,191,36,0.15);
  color: var(--warning);
  font-size: 0.85rem;
  margin-top: 0.5rem;
}}

/* Tables */
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}}
th {{
  text-align: left;
  padding: 0.6rem 0.75rem;
  color: var(--muted);
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border);
}}
td {{
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}}
tr:hover {{ background: rgba(255,255,255,0.02); }}
.current-week {{
  background: rgba(0,255,136,0.06) !important;
  border-left: 3px solid var(--manda);
}}
.current-week td {{ color: var(--manda); font-weight: 600; }}
.badge {{
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  background: var(--manda);
  color: #000;
  margin-left: 0.4rem;
  vertical-align: middle;
}}

/* Footer */
.footer {{
  text-align: center;
  padding: 2rem 0;
  color: var(--muted);
  font-size: 0.8rem;
  border-top: 1px solid var(--border);
  margin-top: 2rem;
}}

@media (max-width: 640px) {{
  .container {{ padding: 1rem; }}
  .card {{ padding: 1.25rem; }}
  th, td {{ padding: 0.4rem 0.5rem; font-size: 0.8rem; }}
}}
</style>
</head>
<body>

<div class="hero">
  <h1>🏃 Running Competition 2026</h1>
  <div class="subtitle">Mandalorian vs IT System — Quarterly Team Challenge</div>
  <div class="status">🟢 Q1 Active — Week {current_week}</div>
</div>

<div class="container">

  <!-- Dashboard Link -->
  <a href="/ntl-running-tournaments/docs/html/index.html" class="cta-card">
    <div class="cta-title">📊 Open Live Dashboard →</div>
    <div class="cta-sub">Real-time standings, team stats, roster profiles & activity history</div>
  </a>

  <!-- Tournament Rules -->
  <div class="card">
    <h2>📋 Tournament Rules</h2>
    <div class="rules-grid">
      <div class="rule-item">
        <h3>🏃 Accepted Activities</h3>
        <ul>
          <li>✅ Outdoor Run (min 1.0 km)</li>
          <li>✅ Treadmill Run (min 1.0 km)</li>
          <li>✅ Walk (min 2.0 km)</li>
        </ul>
      </div>
      <div class="rule-item">
        <h3>🏆 Team Scoring (Average Distance)</h3>
        <p>Team Average = Total Team Distance ÷ 10 members. Every member matters!</p>
      </div>
      <div class="rule-item">
        <h3>⭐ Individual Competition</h3>
        <p>Highest accumulated distance wins. Top 5 recognized per quarter.</p>
      </div>
      <div class="rule-item">
        <h3>📸 Submission Rules</h3>
        <p>Submit evidence screenshots via LINE within 24 hours. Must include distance, time, and GPS route.</p>
        <div class="warning-box">⚠️ Duplicate submissions, data tampering, and micro-activities are strictly prohibited.</div>
      </div>
      <div class="rule-item">
        <h3>🎁 Rewards &amp; Penalties</h3>
        <ul>
          <li>🥇 Winning team receives special reward</li>
          <li>😂 Losing team sponsors lunch + funny costume day</li>
          <li>🏅 Top 5 individuals receive individual awards</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Tournament Calendar -->
  <div class="card">
    <h2>📅 Q1 Calendar (Jan – Mar 2026)</h2>
    <table>
      <thead>
        <tr><th>Week</th><th>Dates</th><th>Period</th><th>Notes</th></tr>
      </thead>
      <tbody>
        {calendar_rows}
      </tbody>
    </table>
  </div>

  <!-- Quarter Summary -->
  <div class="card">
    <h2>📊 Yearly Quarter Overview</h2>
    <table>
      <thead>
        <tr><th>Quarter</th><th>Period</th><th>Weeks</th><th>Status</th></tr>
      </thead>
      <tbody>
        {quarter_rows}
      </tbody>
    </table>
  </div>

  <div class="footer">
    Running Competition 2026 · Mandalorian vs IT System · Auto-generated on {now_str}
  </div>

</div>
</body>
</html>"""

    output_path = os.path.join(DOCS_DIR, "index.html")
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Generated {output_path} successfully.")

if __name__ == '__main__':
    main()
