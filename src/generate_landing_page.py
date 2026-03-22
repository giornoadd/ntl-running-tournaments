#!/usr/bin/env python3
"""Generate docs/index.html landing page from tournament markdown sources.

Reads live statistics from results/README.md and generates a modern,
data-driven landing page with the latest standings and highlights.
"""
import os
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
RESULTS_README = os.path.join(PROJECT_ROOT, "results", "README.md")

def get_current_week():
    """Determine the current tournament week based on date."""
    now = datetime.now()
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
    return 13  # fallback


def parse_results_readme():
    """Parse results/README.md for live statistics.
    
    Returns a dict with:
      manda_total, it_total, manda_avg, it_avg, leader, gap,
      top5: [(rank_emoji, name, team, distance), ...],
      monthly: [(month, manda_km, it_km, winner), ...]
    """
    stats = {
        "manda_total": "0.00", "it_total": "0.00",
        "manda_avg": "0.00", "it_avg": "0.00",
        "leader": "💻 IT System", "gap": "0.00",
        "top5": [],
        "monthly": [],
    }
    
    if not os.path.exists(RESULTS_README):
        print(f"⚠️ {RESULTS_README} not found, using fallback values.")
        return stats
    
    with open(RESULTS_README, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse 2026 Tournament team totals
    # | **Total Distance** | 774.78 km | 865.93 km | 💻 **IT System** |
    total_match = re.search(
        r'\|\s*\*\*Total Distance\*\*\s*\|\s*([\d.]+)\s*km\s*\|\s*([\d.]+)\s*km\s*\|',
        content
    )
    if total_match:
        stats["manda_total"] = total_match.group(1)
        stats["it_total"] = total_match.group(2)
    
    # | **Average / Person** | 77.48 km | 86.59 km | 💻 **IT System** |
    avg_match = re.search(
        r'\|\s*\*\*Average / Person\*\*\s*\|\s*([\d.]+)\s*km\s*\|\s*([\d.]+)\s*km\s*\|',
        content
    )
    if avg_match:
        stats["manda_avg"] = avg_match.group(1)
        stats["it_avg"] = avg_match.group(2)
    
    # > 💻 **IT System** leads by **9.12 km/person**
    gap_match = re.search(r'leads by \*\*([\d.]+) km/person\*\*', content)
    if gap_match:
        stats["gap"] = gap_match.group(1)
    
    # Determine leader
    m_avg = float(stats["manda_avg"])
    i_avg = float(stats["it_avg"])
    if m_avg > i_avg:
        stats["leader"] = "🪖 Mandalorian"
    else:
        stats["leader"] = "💻 IT System"
    
    # Parse Top 5 — only from 2026 section (first occurrence)
    # | 🥇 1 | Gio | 🪖 Mandalorian | 419.66 km |
    top5_pattern = re.compile(
        r'\|\s*(🥇\s*\d|🥈\s*\d|🥉\s*\d|🏅\s*\d)\s*\|\s*(\w+)\s*\|\s*(.*?)\s*\|\s*([\d.]+)\s*km\s*\|'
    )
    # Find the first "Top 5" section (2026)
    top5_section = content.split("### 🌟 Top 5 Individual Runners")
    if len(top5_section) > 1:
        first_top5 = top5_section[1].split("###")[0]  # up to next section
        for m in top5_pattern.finditer(first_top5):
            stats["top5"].append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()))
    
    # Parse Monthly Details
    # - **2026-March** — Mandalorian: 334.71 km | IT System: 341.63 km | 💻 IT System
    monthly_pattern = re.compile(
        r'\*\*2026-(\w+)\*\*\s*—\s*Mandalorian:\s*([\d.]+)\s*km\s*\|\s*IT System:\s*([\d.]+)\s*km\s*\|\s*(.*?)$',
        re.MULTILINE
    )
    for m in monthly_pattern.finditer(content):
        stats["monthly"].append((m.group(1), m.group(2), m.group(3), m.group(4).strip()))
    
    return stats


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


def generate_standings_card(stats):
    """Generate the Live Standings HTML card from parsed stats."""
    # Top 5 rows
    top5_rows = ""
    for rank_emoji, name, team, distance in stats["top5"]:
        team_color = "var(--manda)" if "Mandalorian" in team else "var(--it)"
        team_icon = "🪖" if "Mandalorian" in team else "💻"
        top5_rows += f'<tr><td>{rank_emoji}</td><td><b>{name}</b></td><td><span style="color:{team_color}">{team_icon}</span></td><td style="text-align:right">{distance} km</td></tr>\n'
    
    # Monthly rows
    monthly_rows = ""
    for month, manda_km, it_km, winner in stats["monthly"]:
        monthly_rows += f'<tr><td>{month}</td><td style="color:var(--manda)">{manda_km} km</td><td style="color:var(--it)">{it_km} km</td><td>{winner}</td></tr>\n'

    # Determine leader color
    leader = stats["leader"]
    leader_color = "var(--manda)" if "Mandalorian" in leader else "var(--it)"
    
    return f"""
  <div class="card standings-card">
    <h2>⚔️ Live Standings — Q1 2026</h2>
    <div class="team-battle">
      <div class="team-row">
        <div class="team-block manda-block">
          <div class="team-label">🪖 Mandalorian</div>
          <div class="team-distance">{stats['manda_total']} km</div>
          <div class="team-avg">avg {stats['manda_avg']} km/person</div>
        </div>
        <div class="vs-divider">VS</div>
        <div class="team-block it-block">
          <div class="team-label">💻 IT System</div>
          <div class="team-distance">{stats['it_total']} km</div>
          <div class="team-avg">avg {stats['it_avg']} km/person</div>
        </div>
      </div>
      <div class="gap-indicator">
        <span style="color:{leader_color};font-weight:800">{leader}</span> leads by 
        <span style="color:var(--accent);font-size:1.3em;font-weight:900">{stats['gap']} km/person</span>
      </div>
    </div>
    
    <h3 style="margin-top:1.5rem;margin-bottom:0.8rem;font-size:1rem;color:var(--accent)">🌟 Top 5 Individual</h3>
    <table>
      <thead><tr><th>Rank</th><th>Name</th><th>Team</th><th style="text-align:right">Distance</th></tr></thead>
      <tbody>{top5_rows}</tbody>
    </table>
    
    <h3 style="margin-top:1.5rem;margin-bottom:0.8rem;font-size:1rem;color:var(--accent)">📅 Monthly Breakdown</h3>
    <table>
      <thead><tr><th>Month</th><th>🪖 Manda</th><th>💻 IT</th><th>Winner</th></tr></thead>
      <tbody>{monthly_rows}</tbody>
    </table>
  </div>
"""


def generate_highlight_card(stats):
    """Generate the 100km Milestone highlight card using latest data."""
    # Calculate combined total
    combined = float(stats["manda_total"]) + float(stats["it_total"])
    
    return f"""
  <!-- 🏆 Q1 100 KM Milestone Highlight -->
  <div class="card highlight-card">
    <h2>🏆🔥 100 KM CLUB — สัปดาห์สุดท้ายของ Q1!</h2>
    <div class="infographic-content">
      <p class="impact-text">
        ผ่านมา 3 เดือนเต็ม! จาก 20 นักรบ... มีเพียง <b style="color:var(--warning);font-size:1.3em">5 คน</b> ที่ฝ่าด่านนรก 100 กิโลเมตรสะสมได้สำเร็จ! 🏅
      </p>
      
      <div class="milestone-table">
        <table>
          <thead>
            <tr><th>Rank</th><th>Runner</th><th>Team</th><th style="text-align:right">Distance</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr class="milestone-row gold"><td>👑</td><td><b>GIO</b></td><td><span style="color:var(--manda)">🪖 Manda</span></td><td style="text-align:right"><b>{stats['top5'][0][3]} km</b></td><td>🌟🌟🌟🌟 LEGENDARY</td></tr>
            <tr class="milestone-row silver"><td>🥈</td><td><b>Jojo</b></td><td><span style="color:var(--it)">💻 IT</span></td><td style="text-align:right"><b>{stats['top5'][1][3]} km</b></td><td>🌟🌟🌟 ELITE</td></tr>
            <tr class="milestone-row bronze"><td>🥉</td><td><b>Boy</b></td><td><span style="color:var(--it)">💻 IT</span></td><td style="text-align:right"><b>{stats['top5'][2][3]} km</b></td><td>🌟🌟 CHAMPION</td></tr>
            <tr class="milestone-row"><td>🏅</td><td><b>O</b></td><td><span style="color:var(--it)">💻 IT</span></td><td style="text-align:right"><b>{stats['top5'][3][3]} km</b></td><td>🌟 HERO</td></tr>
            <tr class="milestone-row"><td>🏅</td><td><b>Sand</b></td><td><span style="color:var(--manda)">🪖 Manda</span></td><td style="text-align:right"><b>{stats['top5'][4][3]} km</b></td><td>🌟 HERO</td></tr>
          </tbody>
        </table>
      </div>
      
      <div class="fun-stats">
        <div class="fun-stat-item">🏃 ระยะรวมทั้ง 20 คน = <b style="color:var(--accent)">{combined:,.2f} km</b></div>
        <div class="fun-stat-item">👟 คนที่ผ่าน 100km = <b style="color:var(--warning)">5 จาก 20 คน</b> (25%)</div>
        <div class="fun-stat-item">📅 เหลืออีก <b style="color:var(--warning)">9 วัน</b> จบ Q1!</div>
        <div class="fun-stat-item">💬 <i>ทุกก้าวมีค่า! เดิน 2 กม. ก็นับ!</i> 🔥</div>
      </div>
      
      <img src="img/q1-100km-milestone.png" alt="100 KM Club — Q1 2026" style="width:100%; border-radius:12px; margin-top:1.5rem; border: 1px solid var(--border); box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
      <div style="text-align: center;">
        <a href="html/index.html" class="pulse-btn">📊 ดู Dashboard เต็มรูปแบบ →</a>
      </div>
    </div>
  </div>
"""


def main():
    current_week = get_current_week()
    calendar_rows = generate_calendar_rows(current_week)
    quarter_rows = generate_quarter_rows()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Parse live statistics from results/README.md
    stats = parse_results_readme()
    standings_card = generate_standings_card(stats)
    highlight_card = generate_highlight_card(stats)

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

/* Standings Card */
.standings-card {{
  border-color: rgba(0,255,136,0.2);
  background: linear-gradient(135deg, var(--surface), rgba(0,255,136,0.03));
}}
.team-row {{
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}}
.team-block {{
  flex: 1;
  text-align: center;
  padding: 1.2rem;
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
}}
.manda-block {{ border-color: rgba(0,255,136,0.2); }}
.it-block {{ border-color: rgba(0,204,255,0.2); }}
.team-label {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 0.3rem; font-weight: 600; }}
.team-distance {{ font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; }}
.manda-block .team-distance {{ color: var(--manda); }}
.it-block .team-distance {{ color: var(--it); }}
.team-avg {{ font-size: 0.8rem; color: var(--muted); margin-top: 0.2rem; }}
.vs-divider {{
  font-family: 'Outfit', sans-serif;
  font-size: 1.2rem;
  font-weight: 900;
  color: var(--warning);
  flex-shrink: 0;
}}
.gap-indicator {{
  text-align: center;
  padding: 0.6rem;
  font-size: 0.95rem;
  color: var(--text);
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

/* Infographic Highlight Card */
.highlight-card {{
  border-color: var(--warning);
  background: linear-gradient(135deg, rgba(17, 24, 39, 1), rgba(251, 191, 36, 0.06));
  position: relative;
  overflow: hidden;
}}
.highlight-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--warning), var(--accent));
}}
.impact-text {{
  font-size: 1.1rem;
  color: #fff;
  line-height: 1.6;
}}
.milestone-table {{
  margin: 1.5rem 0;
}}
.milestone-row td {{
  padding: 0.5rem 0.75rem;
}}
.milestone-row.gold {{ background: rgba(251,191,36,0.08); }}
.milestone-row.silver {{ background: rgba(192,192,192,0.06); }}
.milestone-row.bronze {{ background: rgba(205,127,50,0.06); }}
.fun-stats {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(255,255,255,0.02);
  border-radius: 12px;
}}
.fun-stat-item {{
  font-size: 0.9rem;
  padding: 0.4rem;
}}
.pulse-btn {{
  display: inline-block;
  margin-top: 1.5rem;
  padding: 0.8rem 1.5rem;
  background: var(--accent);
  color: #000;
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  border-radius: 999px;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.2s;
  box-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
}}
.pulse-btn:hover {{
  transform: scale(1.05) translateY(-2px);
  box-shadow: 0 0 25px rgba(0, 204, 255, 0.6);
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
  .team-row {{ flex-direction: column; }}
  .vs-divider {{ margin: 0.5rem 0; }}
  .fun-stats {{ grid-template-columns: 1fr; }}
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
  <a href="/ntl-running-tournaments/html/index.html" class="cta-card">
    <div class="cta-title">📊 Open Live Dashboard →</div>
    <div class="cta-sub">Real-time standings, team stats, roster profiles & activity history</div>
  </a>

  <!-- ⚔️ Live Standings (from results/README.md) -->
  {standings_card}

  <!-- 🏆 100km Milestone Highlight -->
  {highlight_card}

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
    print(f"   📊 Stats: Manda {stats['manda_total']} km | IT {stats['it_total']} km | Gap {stats['gap']} km/person")


if __name__ == '__main__':
    main()
