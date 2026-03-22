#!/usr/bin/env python3
"""Generate performance-report/personal-performance-report.md for all members.

Follows GIO's report structure:
  performance-report/
  ├── personal-performance-report.md   ← Main comprehensive report
  └── (daily/ folder created but populated by /running-coach per session)

Also creates coach-analysis.md symlink/copy at member root for data pipeline compatibility.
"""
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMBER_RESULTS_DIR = os.path.join(PROJECT_ROOT, "member_results")

FOLDER_MAP = {
    "Manda-1_โจ (GIO)": ("Gio", "โจ", "🪖 Mandalorian", "Mandalorian"),
    "Manda-2_โบ๊ท (Boat)": ("Boat", "โบ๊ท", "🪖 Mandalorian", "Mandalorian"),
    "Manda-3_ต้อ (TORO)": ("Toro", "ต้อ", "🪖 Mandalorian", "Mandalorian"),
    "Manda-4_เอ็ม (EM)": ("Em", "เอ็ม", "🪖 Mandalorian", "Mandalorian"),
    "Manda-5_แซนด์ (SAND)": ("Sand", "แซนด์", "🪖 Mandalorian", "Mandalorian"),
    "Manda-6_เป๊ก (peck)": ("Peck", "เป๊ก", "🪖 Mandalorian", "Mandalorian"),
    "Manda-7_หนึ่ง (Neung)": ("Neung", "หนึ่ง", "🪖 Mandalorian", "Mandalorian"),
    "Manda-8_ฟิวส์ (fuse)": ("Fuse", "ฟิวส์", "🪖 Mandalorian", "Mandalorian"),
    "Manda-9_พี่ฉันท์ (Chan)": ("Chan", "พี่ฉันท์", "🪖 Mandalorian", "Mandalorian"),
    "Manda-10_มอส (Mos)": ("Mos", "มอส", "🪖 Mandalorian", "Mandalorian"),
    "ITSystem-1_Oat (โอ๊ต)": ("Oat", "โอ๊ต", "💻 IT System", "IT System"),
    "ITSystem-2_Game (เกมส์)": ("Game", "เกมส์", "💻 IT System", "IT System"),
    "ITSystem-3_O (โอ)": ("O", "โอ", "💻 IT System", "IT System"),
    "ITSystem-4_Palm (ปาล์ม)": ("Palm", "ปาล์ม", "💻 IT System", "IT System"),
    "ITSystem-5_Oum (อุ้ม)": ("Oum", "อุ้ม", "💻 IT System", "IT System"),
    "ITSystem-6_Jojo (โจโจ้)": ("Jojo", "โจโจ้", "💻 IT System", "IT System"),
    "ITSystem-7_Tae (เต)": ("Tae", "เต", "💻 IT System", "IT System"),
    "ITSystem-8_Boy (บอย)": ("Boy", "บอย", "💻 IT System", "IT System"),
    "ITSystem-9_Ton (ต้น)": ("Ton", "ต้น", "💻 IT System", "IT System"),
    "ITSystem-10_PAN (แพน)": ("PAN", "แพน", "💻 IT System", "IT System"),
}


def parse_pace_to_seconds(pace_str):
    if not pace_str or pace_str.strip() == 'N/A' or pace_str.strip() == '':
        return None
    m = re.search(r'(\d+)[:\'\"](\d+)', pace_str)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None


def seconds_to_pace(secs):
    if secs is None:
        return "N/A"
    return f"{secs // 60}:{secs % 60:02d}/km"


def parse_hr(hr_str):
    if not hr_str or hr_str.strip() == 'N/A':
        return None, None
    m = re.search(r'(\d+)', hr_str)
    avg = int(m.group(1)) if m else None
    m2 = re.search(r'/\s*(\d+)', hr_str)
    mx = int(m2.group(1)) if m2 else None
    return avg, mx


def parse_cadence(cad_str):
    if not cad_str or cad_str.strip() == 'N/A':
        return None
    m = re.search(r'(\d+)\s*spm', cad_str)
    return int(m.group(1)) if m else None


def parse_stats(folder_path):
    stats_path = os.path.join(folder_path, "personal-statistics.md")
    if not os.path.isfile(stats_path):
        return []
    sessions = []
    with open(stats_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|'):
                continue
            cols = [c.strip() for c in line.split('|')]
            if len(cols) < 6:
                continue
            date_val = cols[1]
            if not re.match(r'\d{4}-\d{2}-\d{2}', date_val):
                continue
            activity = cols[2]
            dist_match = re.search(r'([\d.]+)\s*km', cols[3])
            dist = float(dist_match.group(1)) if dist_match else 0.0
            time_val = cols[4] if len(cols) > 4 else ''
            pace_val = cols[5] if len(cols) > 5 else ''
            hr_val = cols[6] if len(cols) > 6 else 'N/A'
            cadence_val = cols[8] if len(cols) > 8 else 'N/A'
            pace_secs = parse_pace_to_seconds(pace_val)
            hr_avg, hr_max = parse_hr(hr_val)
            cadence = parse_cadence(cadence_val)
            is_walk = 'walk' in activity.lower()
            sessions.append({
                'date': date_val, 'activity': activity, 'distance': dist,
                'time': time_val, 'pace_str': pace_val, 'pace_secs': pace_secs,
                'hr_avg': hr_avg, 'hr_max': hr_max, 'cadence': cadence,
                'is_walk': is_walk,
            })
    return sessions


def get_month_key(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%b")
    except ValueError:
        return "Unknown"


def get_week_key(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"Wk {dt.isocalendar()[1]}"
    except ValueError:
        return "Unknown"


def classify_fitness(sessions):
    run_sessions = [s for s in sessions if not s['is_walk']]
    if not run_sessions:
        return "🟢 Walker", "Walker"
    max_dist = max(s['distance'] for s in run_sessions)
    paces = [s['pace_secs'] for s in run_sessions if s['pace_secs']]
    best_pace = min(paces) if paces else 999
    if max_dist >= 8 and best_pace < 420:  # < 7:00/km
        return "🔴 Advanced", "Advanced"
    elif max_dist >= 4 and best_pace < 540:  # < 9:00/km
        return "🟠 Intermediate", "Intermediate"
    elif max_dist >= 1:
        return "🟡 Beginner", "Beginner"
    return "🟢 Walker", "Walker"


def generate_report(nickname, thai_name, team_icon, team_name, sessions):
    today = datetime.now().strftime('%Y-%m-%d')

    if not sessions:
        return f"""# 📋 Personal Performance Report — {nickname} ({thai_name})
📅 อัพเดต: **{today}**
🏋️ Team: **{team_icon}**

*จัดทำโดย: Running Coach AI · {today}*

---

## 📊 ยังไม่มีข้อมูลกิจกรรม

ยังไม่พบข้อมูลการวิ่ง/เดินสำหรับ {nickname} — เมื่อมีกิจกรรมแรก Performance Report จะถูกสร้างขึ้นอัตโนมัติ

> 💪 **พร้อมเมื่อไหร่ ออกมาวิ่ง/เดินกันเลย! ทีม {team_icon} รอคุณอยู่!**

---

*📊 Auto-generated on {today} by Running Coach AI*

[🏠 Profile](../README.md) | [📊 Statistics](../personal-statistics.md)
"""

    # ── Core metrics ──
    total_dist = sum(s['distance'] for s in sessions)
    run_sessions = [s for s in sessions if not s['is_walk']]
    walk_sessions = [s for s in sessions if s['is_walk']]
    run_dist = sum(s['distance'] for s in run_sessions)
    walk_dist = sum(s['distance'] for s in walk_sessions)
    active_days = len(set(s['date'] for s in sessions))
    first_date = sessions[0]['date']
    last_date = sessions[-1]['date']
    first_dt = datetime.strptime(first_date, "%Y-%m-%d")
    last_dt = datetime.strptime(last_date, "%Y-%m-%d")
    span_days = max((last_dt - first_dt).days, 1)
    sessions_per_week = len(sessions) / max(span_days / 7, 1)
    is_walker = len(walk_sessions) > len(run_sessions)
    fitness_label, fitness_level = classify_fitness(sessions)

    # Paces & bests
    paces = [s['pace_secs'] for s in sessions if s['pace_secs']]
    best_pace_secs = min(paces) if paces else None
    best_pace_session = next((s for s in sessions if s['pace_secs'] == best_pace_secs), None) if best_pace_secs else None
    longest = max(sessions, key=lambda s: s['distance'])
    avg_dist = total_dist / len(sessions)

    # HR data
    hr_sessions = [s for s in sessions if s['hr_avg']]
    avg_hr = sum(s['hr_avg'] for s in hr_sessions) / len(hr_sessions) if hr_sessions else None

    # Cadence data
    cad_sessions = [s for s in sessions if s['cadence']]
    avg_cad = sum(s['cadence'] for s in cad_sessions) / len(cad_sessions) if cad_sessions else None

    # ── Monthly breakdown ──
    monthly = defaultdict(lambda: {'sessions': 0, 'distance': 0.0, 'paces': [], 'best_dist': 0.0,
                                    'runs': 0, 'walks': 0, 'hrs': [], 'cadences': []})
    for s in sessions:
        m = get_month_key(s['date'])
        monthly[m]['sessions'] += 1
        monthly[m]['distance'] += s['distance']
        if s['pace_secs']:
            monthly[m]['paces'].append(s['pace_secs'])
        if s['distance'] > monthly[m]['best_dist']:
            monthly[m]['best_dist'] = s['distance']
        if s['is_walk']:
            monthly[m]['walks'] += 1
        else:
            monthly[m]['runs'] += 1
        if s['hr_avg']:
            monthly[m]['hrs'].append(s['hr_avg'])
        if s['cadence']:
            monthly[m]['cadences'].append(s['cadence'])
    sorted_months = sorted(monthly.keys())

    # ── Weekly breakdown ──
    weekly = defaultdict(lambda: {'sessions': 0, 'distance': 0.0})
    for s in sessions:
        w = get_week_key(s['date'])
        weekly[w]['sessions'] += 1
        weekly[w]['distance'] += s['distance']

    # ── Changes ──
    if len(sorted_months) >= 2:
        fm, lm = monthly[sorted_months[0]], monthly[sorted_months[-1]]
        dist_pct = ((lm['distance'] / max(fm['distance'], 0.01)) - 1) * 100
        avg_first = fm['distance'] / max(fm['sessions'], 1)
        avg_last = lm['distance'] / max(lm['sessions'], 1)
        avg_pct = ((avg_last / max(avg_first, 0.01)) - 1) * 100
    else:
        dist_pct = avg_pct = 0

    # ── Build Achievement Badges ──
    badges = []
    badges.append(('🎯', 'First Activity', f'ก้าวแรกสู่สนาม', first_date))
    if total_dist >= 200:
        badges.append(('🏆', '200K Club', f'ระยะรวมทะลุ 200 km! ({total_dist:.0f} km)', last_date))
    elif total_dist >= 100:
        badges.append(('💯', '100K Club', f'ระยะรวมทะลุ 100 km! ({total_dist:.0f} km)', last_date))
    elif total_dist >= 50:
        badges.append(('🔥', '50K Club', f'ระยะรวมทะลุ 50 km!', last_date))
    if longest['distance'] >= 10:
        badges.append(('🏔️', '10K Club', f'ทะลุ 10km ({longest["distance"]:.2f} km)', longest['date']))
    elif longest['distance'] >= 7:
        badges.append(('📈', '7K Milestone', f'ทะลุ 7km ({longest["distance"]:.2f} km)', longest['date']))
    elif longest['distance'] >= 5:
        badges.append(('📈', '5K Milestone', f'ทะลุ 5km ({longest["distance"]:.2f} km)', longest['date']))
    if best_pace_secs and best_pace_secs < 480:  # < 8:00/km
        badges.append(('⚡', 'Pace Crusher', f'Best Pace {seconds_to_pace(best_pace_secs)}', best_pace_session['date'] if best_pace_session else last_date))
    if active_days >= 20:
        badges.append(('🗓️', 'Consistency King', f'ออกกำลังกาย {active_days} วัน!', last_date))
    elif active_days >= 10:
        badges.append(('🗓️', 'Consistency Star', f'ออกกำลังกาย {active_days} วัน', last_date))
    if len(sessions) >= 30:
        badges.append(('🔥', 'Session Master', f'{len(sessions)} sessions สะสม!', last_date))
    elif len(sessions) >= 10:
        badges.append(('💪', 'Dedicated Runner', f'{len(sessions)} sessions สะสม', last_date))
    # Double-day check
    date_counts = defaultdict(int)
    for s in sessions:
        date_counts[s['date']] += 1
    double_days = [d for d, c in date_counts.items() if c >= 2]
    if double_days:
        badges.append(('💪', 'Double Day Hero', f'{len(double_days)} วันที่ออกกำลัง 2+ ครั้ง', double_days[-1]))

    # ── PR Timeline ──
    prs = []
    current_best_dist = 0
    current_best_pace = 9999
    for s in sessions:
        if s['distance'] > current_best_dist:
            current_best_dist = s['distance']
            prs.append(('🏆 Distance PB', s['date'], f'{s["distance"]:.2f} km', s['activity']))
        if s['pace_secs'] and s['pace_secs'] < current_best_pace:
            current_best_pace = s['pace_secs']
            prs.append(('⚡ Pace PB', s['date'], seconds_to_pace(s['pace_secs']), s['activity']))

    # ════════════════════════════════════════════════════════════
    # BUILD REPORT
    # ════════════════════════════════════════════════════════════
    L = []

    # ── Header ──
    L.append(f"# 📋 Personal Performance Report — {nickname} ({thai_name})")
    L.append(f"📅 ช่วง: **{first_date} — {last_date}** ({span_days} วัน)")
    L.append(f"🏋️ Fitness Level: **{fitness_label}**")
    L.append(f"🏁 Team: **{team_icon}**")
    L.append(f"")
    L.append(f"*จัดทำโดย: Running Coach AI · วันที่ {today}*")
    L.append(f"")
    L.append(f"---")
    L.append(f"")

    # ══════════ 1. Personal Stats Card ══════════
    L.append(f"## 👤 Personal Stats Card")
    L.append(f"")
    L.append(f"| เมตริก | ค่า |")
    L.append(f"|:---|:---|")
    if run_sessions and walk_sessions:
        L.append(f"| **ระยะทางรวม** | 🔥 **{total_dist:.2f} km** (Running {run_dist:.1f} + Walk {walk_dist:.1f}) |")
        L.append(f"| **เซสซั่นทั้งหมด** | 📋 {len(sessions)} ครั้ง (Running {len(run_sessions)} + Walk {len(walk_sessions)}) |")
    else:
        L.append(f"| **ระยะทางรวม** | 🔥 **{total_dist:.2f} km** |")
        L.append(f"| **เซสซั่นทั้งหมด** | 📋 {len(sessions)} ครั้ง |")
    L.append(f"| **วันที่ออกกำลังกาย** | 📅 {active_days}/{span_days} วัน ({active_days/span_days*100:.1f}%) |")
    L.append(f"| **ความถี่** | 📊 ~{sessions_per_week:.1f} เซสซั่น/สัปดาห์ |")
    if best_pace_session:
        L.append(f"| **Best Pace** | ⚡ **{seconds_to_pace(best_pace_secs)}** — {best_pace_session['activity']} ({best_pace_session['date']}) |")
    L.append(f"| **Longest Activity** | 🏅 {longest['distance']:.2f} km — {longest['activity']} ({longest['date']}) |")
    L.append(f"| **Avg / Session** | 📏 {avg_dist:.2f} km |")
    if avg_hr:
        L.append(f"| **Avg HR** | ❤️ {avg_hr:.0f} bpm |")
    if avg_cad:
        L.append(f"| **Avg Cadence** | 🦶 {avg_cad:.0f} spm |")
    L.append(f"")

    # ── Achievement Badges ──
    L.append(f"### 🏅 Achievement Badges")
    L.append(f"")
    L.append(f"| Badge | Achievement | Date |")
    L.append(f"|:---|:---|:---|")
    for icon, name, desc, date in badges:
        L.append(f"| {icon} **{name}** | {desc} | {date} |")
    L.append(f"")
    L.append(f"---")
    L.append(f"")

    # ══════════ 2. Distance & Pace Evolution ══════════
    L.append(f"## ⚡ Distance & Pace Evolution")
    L.append(f"")

    # Monthly progression table
    L.append(f"### 📏 Monthly Progression")
    L.append(f"")
    L.append(f"| Month | Sessions | Total Distance | Avg/Session | Best Activity | {'Avg Pace' if paces else ''} |")
    L.append(f"|:---|:---:|:---:|:---:|:---:|{':---:|' if paces else ''}")
    for mk in sorted_months:
        md = monthly[mk]
        avg_s = md['distance'] / max(md['sessions'], 1)
        avg_pace_m = seconds_to_pace(int(sum(md['paces']) / len(md['paces']))) if md['paces'] else '—'
        pace_col = f" {avg_pace_m} |" if paces else ""
        L.append(f"| **{mk}** | {md['sessions']} | {md['distance']:.1f} km | {avg_s:.2f} km | {md['best_dist']:.2f} km |{pace_col}")
    L.append(f"")

    # Distance progression bar chart
    L.append(f"### 📊 Distance Build-up")
    L.append(f"")
    max_dist_month = max(monthly[m]['distance'] for m in sorted_months) if sorted_months else 1
    for mk in sorted_months:
        d = monthly[mk]['distance']
        bar_len = int((d / max(max_dist_month, 0.01)) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        L.append(f"```")
        L.append(f"{mk}:  {bar}  {d:.1f} km ({monthly[mk]['sessions']} sessions)")
        L.append(f"```")
    L.append(f"")

    # Overall volume change
    if len(sorted_months) >= 2:
        first_m = monthly[sorted_months[0]]
        last_m = monthly[sorted_months[-1]]
        L.append(f"> 📈 **Volume {'เพิ่มจาก' if dist_pct > 0 else 'เปลี่ยนจาก'} {first_m['distance']:.1f} → {last_m['distance']:.1f} km/เดือน ({'+' if dist_pct > 0 else ''}{dist_pct:.0f}%)**")
    L.append(f"")

    # Pace evolution (if available)
    if paces:
        L.append(f"### 🏃 Pace Journey")
        L.append(f"")
        L.append(f"| ช่วง | Avg Pace | Best Pace | แนวโน้ม |")
        L.append(f"|:---|:---|:---|:---:|")
        for mk in sorted_months:
            md = monthly[mk]
            if md['paces']:
                avg_p = seconds_to_pace(int(sum(md['paces']) / len(md['paces'])))
                best_p = seconds_to_pace(min(md['paces']))
                if mk == sorted_months[0]:
                    trend = "— Baseline"
                else:
                    prev_paces = monthly[sorted_months[sorted_months.index(mk)-1]].get('paces', [])
                    if prev_paces and min(md['paces']) < min(prev_paces):
                        trend = "📈 เร็วขึ้น"
                    else:
                        trend = "➡️ คงที่"
                L.append(f"| {mk} | {avg_p} | {best_p} | {trend} |")
        L.append(f"")
        if best_pace_secs:
            first_paces = monthly[sorted_months[0]]['paces']
            if first_paces:
                orig_avg = sum(first_paces) / len(first_paces)
                improvement = ((orig_avg - best_pace_secs) / orig_avg) * 100
                if improvement > 0:
                    L.append(f"> ⚡ **Pace Improvement: {improvement:.0f}% เร็วขึ้นจากเริ่มต้น!**")
                    L.append(f"")
    L.append(f"---")
    L.append(f"")

    # ══════════ 3. Heart Rate & Cadence (if available) ══════════
    if hr_sessions or cad_sessions:
        L.append(f"## ❤️ Heart Rate & Cadence Development")
        L.append(f"")

        if hr_sessions:
            L.append(f"### ❤️ Heart Rate Trend")
            L.append(f"")
            L.append(f"| ช่วง | Avg HR | จำนวน Sessions | สัญญาณ |")
            L.append(f"|:---|:---|:---:|:---:|")
            for mk in sorted_months:
                md = monthly[mk]
                if md['hrs']:
                    avg_h = sum(md['hrs']) / len(md['hrs'])
                    prev_idx = sorted_months.index(mk) - 1
                    if prev_idx >= 0 and monthly[sorted_months[prev_idx]]['hrs']:
                        prev_h = sum(monthly[sorted_months[prev_idx]]['hrs']) / len(monthly[sorted_months[prev_idx]]['hrs'])
                        if avg_h < prev_h - 3:
                            signal = "📉 HR ลดลง (ดี!)"
                        elif avg_h > prev_h + 3:
                            signal = "📈 HR เพิ่ม"
                        else:
                            signal = "➡️ คงที่"
                    else:
                        signal = "— Baseline"
                    L.append(f"| {mk} | ❤️ {avg_h:.0f} bpm | {len(md['hrs'])} | {signal} |")
            L.append(f"")

        if cad_sessions:
            L.append(f"### 🦶 Cadence Trend")
            L.append(f"")
            L.append(f"| ช่วง | Avg Cadence | จำนวน Sessions | เป้าหมาย |")
            L.append(f"|:---|:---|:---:|:---:|")
            for mk in sorted_months:
                md = monthly[mk]
                if md['cadences']:
                    avg_c = sum(md['cadences']) / len(md['cadences'])
                    target = "160-180 spm" if not is_walker else "—"
                    L.append(f"| {mk} | 🦶 {avg_c:.0f} spm | {len(md['cadences'])} | {target} |")
            L.append(f"")

        L.append(f"---")
        L.append(f"")

    # ══════════ 4. Personal Records Timeline ══════════
    L.append(f"## 🏅 Personal Records Timeline")
    L.append(f"")
    L.append(f"| Date | Record | Value | Activity |")
    L.append(f"|:---|:---|:---:|:---|")
    for pr_type, pr_date, pr_val, pr_act in prs:
        L.append(f"| {pr_date} | {pr_type} | **{pr_val}** | {pr_act} |")
    L.append(f"")
    L.append(f"---")
    L.append(f"")

    # ══════════ 5. Weekly Session Log ══════════
    L.append(f"## 📅 Recent Sessions (Last 10)")
    L.append(f"")
    recent = sessions[-10:]
    L.append(f"| Date | Activity | Distance | Pace | {'HR |' if hr_sessions else ''}")
    L.append(f"|:---|:---|:---:|:---:|{':---:|' if hr_sessions else ''}")
    for s in recent:
        hr_col = f" {s['hr_avg']} bpm |" if s['hr_avg'] and hr_sessions else (" N/A |" if hr_sessions else "")
        pace_col = seconds_to_pace(s['pace_secs']) if s['pace_secs'] else s.get('pace_str', '—')
        L.append(f"| {s['date']} | {s['activity']} | {s['distance']:.2f} km | {pace_col} |{hr_col}")
    L.append(f"")
    L.append(f"---")
    L.append(f"")

    # ══════════ 6. Coach's Recommendations ══════════
    L.append(f"## 🔮 คำแนะนำจากโค้ช (Coach's Recommendations)")
    L.append(f"")

    L.append(f"### ✅ สิ่งที่ทำได้ดีแล้ว — รักษาไว้!")
    L.append(f"")
    strengths = []
    if active_days >= 10:
        strengths.append(f"💪 **วินัยสม่ำเสมอ** — ออกกำลังกายมาแล้ว {active_days} วัน ({sessions_per_week:.1f} ครั้ง/สัปดาห์)")
    if dist_pct > 20:
        strengths.append(f"📈 **Volume เพิ่มขึ้น {dist_pct:.0f}%** — ทำเวลาเพิ่มระยะอย่างเป็นระบบ")
    if longest['distance'] >= 5:
        strengths.append(f"🏅 **ระยะทางสูงสุด {longest['distance']:.2f} km** — {longest['activity']}")
    if best_pace_secs and best_pace_secs < 600:
        strengths.append(f"⚡ **Best Pace {seconds_to_pace(best_pace_secs)}** — แสดงถึง Aerobic Fitness ที่ดี")
    if len(sessions) >= 5:
        strengths.append(f"🔥 **{len(sessions)} sessions สะสม** — ไม่ทิ้งกิจวัตร")
    if not strengths:
        strengths.append(f"🎯 **เริ่มต้นดีแล้ว!** — การก้าวแรกคือสิ่งที่ยากที่สุด คุณทำได้แล้ว!")
    for i, s in enumerate(strengths, 1):
        L.append(f"{i}. {s}")
    L.append(f"")

    L.append(f"### ⚠️ จุดที่ต้องปรับปรุง")
    L.append(f"")
    improvements = []
    if is_walker and run_sessions:
        improvements.append(f"🏃 **ลองเพิ่มช่วงวิ่ง** — สลับเดิน-วิ่ง (Walk-Run) เพื่อสร้าง Aerobic Base")
    elif is_walker:
        improvements.append(f"🏃 **ลองเริ่มวิ่งเบาๆ** — เริ่มจาก Walk-Run 1 นาทีวิ่ง / 2 นาทีเดิน")
    if sessions_per_week < 2.5 and len(sessions) > 3:
        improvements.append(f"📊 **เพิ่มความถี่** — ปัจจุบัน {sessions_per_week:.1f} ครั้ง/สัปดาห์ ตั้งเป้า 3 ครั้ง/สัปดาห์")
    if longest['distance'] < 5 and not is_walker:
        improvements.append(f"📏 **ค่อยๆ เพิ่มระยะ** — ตั้งเป้า 5 km เป็น milestone ถัดไป (เพิ่มไม่เกิน 10%/สัปดาห์)")
    elif longest['distance'] < 10 and not is_walker:
        improvements.append(f"📏 **ขยายระยะ Long Run** — ค่อยๆ เพิ่มจาก {longest['distance']:.1f} km เป้าถัดไป {min(longest['distance']*1.15, 10):.0f} km")
    if hr_sessions and avg_hr and avg_hr > 155:
        improvements.append(f"❤️ **คุม Easy Run ให้ช้าลง** — HR เฉลี่ย {avg_hr:.0f} bpm สูงเกินไป ลดเพซจน \"พูดคุยได้ไม่หอบ\"")
    improvements.append(f"🧘 **อย่าลืมวันพัก** — ร่างกายสร้างความแข็งแรงในช่วงพัก ไม่ใช่ตอนออกกำลังกาย")
    for i, s in enumerate(improvements, 1):
        L.append(f"{i}. {s}")
    L.append(f"")

    # Next milestone
    L.append(f"### 🎯 เป้าหมายถัดไป")
    L.append(f"")
    if total_dist < 50:
        L.append(f"| Milestone | Target | ปัจจุบัน | Progress |")
        L.append(f"|:---|:---:|:---:|:---:|")
        L.append(f"| 🔥 50K Club | 50 km | {total_dist:.1f} km | {'█' * int(total_dist/50*10)}{'░' * (10-int(total_dist/50*10))} {total_dist/50*100:.0f}% |")
    elif total_dist < 100:
        L.append(f"| Milestone | Target | ปัจจุบัน | Progress |")
        L.append(f"|:---|:---:|:---:|:---:|")
        L.append(f"| 💯 100K Club | 100 km | {total_dist:.1f} km | {'█' * int(total_dist/100*10)}{'░' * (10-int(total_dist/100*10))} {total_dist/100*100:.0f}% |")
    elif total_dist < 200:
        L.append(f"| Milestone | Target | ปัจจุบัน | Progress |")
        L.append(f"|:---|:---:|:---:|:---:|")
        L.append(f"| 🏆 200K Club | 200 km | {total_dist:.1f} km | {'█' * int(total_dist/200*10)}{'░' * (10-int(total_dist/200*10))} {total_dist/200*100:.0f}% |")
    else:
        L.append(f"| Milestone | Target | ปัจจุบัน | Progress |")
        L.append(f"|:---|:---:|:---:|:---:|")
        L.append(f"| 🏆 500K Club | 500 km | {total_dist:.1f} km | {'█' * min(int(total_dist/500*10),10)}{'░' * max(10-int(total_dist/500*10),0)} {total_dist/500*100:.0f}% |")
    L.append(f"")

    L.append(f"---")
    L.append(f"")
    L.append(f"> 🏆 **สรุป: {nickname} มีระยะรวม {total_dist:.2f} km จาก {len(sessions)} sessions ใน {span_days} วัน — {'ถ้ารักษาวินัยนี้ไว้ จะพัฒนาได้อีกมาก!' if active_days >= 5 else 'ออกมาวิ่ง/เดินต่อเนื่องอีกนะ!'}** {'🔥✌️' if total_dist > 50 else '💪'}")
    L.append(f"")
    L.append(f"---")
    L.append(f"")
    L.append(f"*📊 Auto-generated on {today} by Running Coach AI*")
    L.append(f"")
    L.append(f"[🔙 สถิติการวิ่ง](../personal-statistics.md) | [🏃🏻‍♂️ แผนฝึกซ้อม](../running-plan.md) | [🏠 Profile](../README.md)")
    L.append(f"")

    return "\n".join(L)


def main():
    generated = 0
    today = datetime.now().strftime('%Y-%m-%d')

    for folder_name, (nickname, thai_name, team_icon, team_name) in FOLDER_MAP.items():
        folder_path = os.path.join(MEMBER_RESULTS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            print(f"  ⚠️ Folder not found: {folder_name}")
            continue

        sessions = parse_stats(folder_path)

        # Create performance-report/ directory
        report_dir = os.path.join(folder_path, "performance-report")
        os.makedirs(report_dir, exist_ok=True)

        # Create daily/ subdirectory
        daily_dir = os.path.join(report_dir, "daily")
        os.makedirs(daily_dir, exist_ok=True)

        # Generate main report
        content = generate_report(nickname, thai_name, team_icon, team_name, sessions)

        # Write to performance-report/personal-performance-report.md
        report_path = os.path.join(report_dir, "personal-performance-report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Also write to coach-analysis.md at member root (for data pipeline compatibility)
        coach_path = os.path.join(folder_path, "coach-analysis.md")
        with open(coach_path, 'w', encoding='utf-8') as f:
            f.write(content)

        dist = sum(s['distance'] for s in sessions)
        print(f"  ✅ {nickname:8s} | {len(sessions):3d} sessions | {dist:8.2f} km | {report_path}")
        generated += 1

    print(f"\n🎉 Generated {generated} performance reports")


if __name__ == '__main__':
    main()
