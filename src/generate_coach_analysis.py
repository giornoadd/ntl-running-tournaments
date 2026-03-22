#!/usr/bin/env python3
"""Generate coach-analysis.md for all members from their personal-statistics.md data."""
import os
import re
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMBER_RESULTS_DIR = os.path.join(PROJECT_ROOT, "member_results")

FOLDER_MAP = {
    "Manda-1_โจ (GIO)": ("Gio", "โจ", "🪖 Mandalorian"),
    "Manda-2_โบ๊ท (Boat)": ("Boat", "โบ๊ท", "🪖 Mandalorian"),
    "Manda-3_ต้อ (TORO)": ("Toro", "ต้อ", "🪖 Mandalorian"),
    "Manda-4_เอ็ม (EM)": ("Em", "เอ็ม", "🪖 Mandalorian"),
    "Manda-5_แซนด์ (SAND)": ("Sand", "แซนด์", "🪖 Mandalorian"),
    "Manda-6_เป๊ก (peck)": ("Peck", "เป๊ก", "🪖 Mandalorian"),
    "Manda-7_หนึ่ง (Neung)": ("Neung", "หนึ่ง", "🪖 Mandalorian"),
    "Manda-8_ฟิวส์ (fuse)": ("Fuse", "ฟิวส์", "🪖 Mandalorian"),
    "Manda-9_พี่ฉันท์ (Chan)": ("Chan", "พี่ฉันท์", "🪖 Mandalorian"),
    "Manda-10_มอส (Mos)": ("Mos", "มอส", "🪖 Mandalorian"),
    "ITSystem-1_Oat (โอ๊ต)": ("Oat", "โอ๊ต", "💻 IT System"),
    "ITSystem-2_Game (เกมส์)": ("Game", "เกมส์", "💻 IT System"),
    "ITSystem-3_O (โอ)": ("O", "โอ", "💻 IT System"),
    "ITSystem-4_Palm (ปาล์ม)": ("Palm", "ปาล์ม", "💻 IT System"),
    "ITSystem-5_Oum (อุ้ม)": ("Oum", "อุ้ม", "💻 IT System"),
    "ITSystem-6_Jojo (โจโจ้)": ("Jojo", "โจโจ้", "💻 IT System"),
    "ITSystem-7_Tae (เต)": ("Tae", "เต", "💻 IT System"),
    "ITSystem-8_Boy (บอย)": ("Boy", "บอย", "💻 IT System"),
    "ITSystem-9_Ton (ต้น)": ("Ton", "ต้น", "💻 IT System"),
    "ITSystem-10_PAN (แพน)": ("PAN", "แพน", "💻 IT System"),
}

def parse_pace_to_seconds(pace_str):
    """Convert pace string like '7:01/km' or '7'01\"/km' to total seconds."""
    if not pace_str or pace_str == 'N/A':
        return None
    m = re.search(r'(\d+)[:\'](\d+)', pace_str)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None

def seconds_to_pace(secs):
    """Convert seconds to pace string."""
    if secs is None:
        return "N/A"
    return f"{secs // 60}:{secs % 60:02d}/km"

def parse_stats(folder_path):
    """Parse personal-statistics.md and return structured data."""
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
            time_val = cols[4]
            pace_val = cols[5] if len(cols) > 5 else ''
            hr_val = cols[6] if len(cols) > 6 else 'N/A'
            
            pace_secs = parse_pace_to_seconds(pace_val)
            is_walk = 'walk' in activity.lower()
            
            sessions.append({
                'date': date_val,
                'activity': activity,
                'distance': dist,
                'time': time_val,
                'pace_str': pace_val,
                'pace_secs': pace_secs,
                'hr': hr_val,
                'is_walk': is_walk,
            })
    return sessions

def get_month_label(date_str):
    """Get month label from date string."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%b")
    except ValueError:
        return "Unknown"

def generate_coach_analysis(nickname, thai_name, team, sessions):
    """Generate coach-analysis.md content from session data."""
    
    if not sessions:
        return f"""# 🏃 Coach Analysis — {nickname} ({thai_name})

> วิเคราะห์พัฒนาการจาก Running Coach | อัพเดตล่าสุด: {datetime.now().strftime('%Y-%m-%d')}

---

## 📊 ยังไม่มีข้อมูลกิจกรรม

ยังไม่พบข้อมูลการวิ่ง/เดินสำหรับ {nickname} — เมื่อมีกิจกรรมแรก Coach Analysis จะถูกสร้างขึ้นอัตโนมัติ

> 💪 **พร้อมเมื่อไหร่ ออกมาวิ่ง/เดินกันเลยครับ! ทีม {team} รอคุณอยู่!**

[🏠 กลับหน้าหลัก (Profile)](README.md)
"""
    
    total_dist = sum(s['distance'] for s in sessions)
    run_sessions = [s for s in sessions if not s['is_walk']]
    walk_sessions = [s for s in sessions if s['is_walk']]
    run_dist = sum(s['distance'] for s in run_sessions)
    walk_dist = sum(s['distance'] for s in walk_sessions)
    
    # Monthly breakdown
    monthly = defaultdict(lambda: {'sessions': 0, 'distance': 0.0, 'paces': [], 'best_dist': 0.0, 'runs': 0, 'walks': 0})
    for s in sessions:
        month = get_month_label(s['date'])
        monthly[month]['sessions'] += 1
        monthly[month]['distance'] += s['distance']
        if s['pace_secs']:
            monthly[month]['paces'].append(s['pace_secs'])
        if s['distance'] > monthly[month]['best_dist']:
            monthly[month]['best_dist'] = s['distance']
        if s['is_walk']:
            monthly[month]['walks'] += 1
        else:
            monthly[month]['runs'] += 1
    
    sorted_months = sorted(monthly.keys())
    
    # Best pace and longest run
    paces = [s['pace_secs'] for s in sessions if s['pace_secs']]
    best_pace_secs = min(paces) if paces else None
    best_pace_session = None
    longest_run = max(sessions, key=lambda s: s['distance'])
    for s in sessions:
        if s['pace_secs'] == best_pace_secs:
            best_pace_session = s
            break
    
    # First and last dates
    first_date = sessions[0]['date']
    last_date = sessions[-1]['date']
    
    # Unique active days
    active_days = len(set(s['date'] for s in sessions))
    
    # Avg distance
    avg_dist = total_dist / len(sessions) if sessions else 0
    
    # Determine primary activity type
    is_primarily_walker = len(walk_sessions) > len(run_sessions)
    activity_icon = "🚶" if is_primarily_walker else "🏃"
    activity_label = "Walker" if is_primarily_walker else "Runner"
    
    # Calculate improvements
    if len(sorted_months) >= 2:
        first_month = sorted_months[0]
        last_month = sorted_months[-1]
        fm = monthly[first_month]
        lm = monthly[last_month]
        dist_change = ((lm['distance'] / max(fm['distance'], 0.01)) - 1) * 100
        avg_first = fm['distance'] / max(fm['sessions'], 1)
        avg_last = lm['distance'] / max(lm['sessions'], 1)
        avg_change = ((avg_last / max(avg_first, 0.01)) - 1) * 100
    else:
        dist_change = 0
        avg_change = 0
    
    # Achievement badges
    badges = []
    badges.append(('🎯', 'First Activity', f'ก้าวแรกสู่สนาม', first_date))
    
    if total_dist >= 100:
        badges.append(('💯', '100K Club', f'ระยะรวมทะลุ 100 km!', last_date))
    elif total_dist >= 50:
        badges.append(('🔥', '50K Club', f'ระยะรวมทะลุ 50 km!', last_date))
    
    if longest_run['distance'] >= 10:
        badges.append(('🏔️', '10K Club', f'ทะลุ 10km ครั้งแรก ({longest_run["distance"]:.2f} km)', longest_run['date']))
    elif longest_run['distance'] >= 7:
        badges.append(('📈', '7K Milestone', f'ทะลุ 7km ({longest_run["distance"]:.2f} km)', longest_run['date']))
    elif longest_run['distance'] >= 5:
        badges.append(('📈', '5K Milestone', f'ทะลุ 5km ({longest_run["distance"]:.2f} km)', longest_run['date']))
    
    if active_days >= 20:
        badges.append(('🗓️', 'Consistency King', f'วิ่ง/เดิน {active_days} วัน!', last_date))
    elif active_days >= 10:
        badges.append(('🗓️', 'Consistency Star', f'วิ่ง/เดิน {active_days} วัน', last_date))
    
    if len(sessions) >= 20:
        badges.append(('🔥', 'Session Master', f'{len(sessions)} sessions สะสม!', last_date))
    
    # Build the markdown
    lines = []
    lines.append(f"# {activity_icon} Coach Analysis — {nickname} ({thai_name})")
    lines.append(f"")
    lines.append(f"> วิเคราะห์พัฒนาการจาก Running Coach | {team} | อัพเดตล่าสุด: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Performance Journey
    lines.append(f"## 📊 Performance Journey (เส้นทางพัฒนาการ)")
    lines.append(f"")
    lines.append(f"| Metric | " + " | ".join([f"🗓️ {m}" for m in sorted_months]) + " | 📈 Trend |")
    lines.append(f"|:---|" + "|".join([":---:" for _ in sorted_months]) + "|:---:|")
    
    # Sessions row
    sess_vals = [str(monthly[m]['sessions']) for m in sorted_months]
    if len(sorted_months) >= 2:
        s_first = monthly[sorted_months[0]]['sessions']
        s_last = monthly[sorted_months[-1]]['sessions']
        trend = "📈" if s_last > s_first else ("➡️" if s_last == s_first else "📉")
    else:
        trend = "—"
    lines.append(f"| **Sessions** | " + " | ".join(sess_vals) + f" | {trend} |")
    
    # Total Distance row
    dist_vals = [f"{monthly[m]['distance']:.1f} km" for m in sorted_months]
    if len(sorted_months) >= 2:
        trend = f"📈 +{dist_change:.0f}%" if dist_change > 0 else ("➡️" if dist_change == 0 else f"📉 {dist_change:.0f}%")
    else:
        trend = "—"
    lines.append(f"| **Total Distance** | " + " | ".join(dist_vals) + f" | {trend} |")
    
    # Avg per Session row
    avg_vals = [f"{monthly[m]['distance']/max(monthly[m]['sessions'],1):.2f} km" for m in sorted_months]
    if len(sorted_months) >= 2:
        trend = f"📈 +{avg_change:.0f}%" if avg_change > 0 else ("➡️" if avg_change == 0 else f"📉")
    else:
        trend = "—"
    lines.append(f"| **Avg / Session** | " + " | ".join(avg_vals) + f" | {trend} |")
    
    # Best Run row
    best_vals = [f"{monthly[m]['best_dist']:.2f} km" for m in sorted_months]
    lines.append(f"| **Best Activity** | " + " | ".join(best_vals) + f" | {'🔥' if len(sorted_months)>=2 and monthly[sorted_months[-1]]['best_dist'] > monthly[sorted_months[0]]['best_dist'] else '➡️'} |")
    
    lines.append(f"")
    
    # Insight
    if dist_change > 0:
        lines.append(f"> 💡 **Insight:** ระยะทางเพิ่มขึ้น **{dist_change:.0f}%** จากเดือนแรก — แสดงถึงพัฒนาการที่ชัดเจน!")
    elif len(sessions) > 0:
        lines.append(f"> 💡 **Insight:** รักษาความสม่ำเสมอได้ดี — ออกกำลังกายมาแล้ว {len(sessions)} ครั้ง รวม {total_dist:.2f} km")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Achievement Badges
    lines.append(f"## 🏆 Achievement Badges")
    lines.append(f"")
    lines.append(f"| Badge | Description | Date Earned |")
    lines.append(f"|:---:|:---|:---:|")
    for icon, name, desc, date in badges:
        lines.append(f"| {icon} | **{name}** — {desc} | {date} |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Key Stats
    lines.append(f"## 📈 Key Statistics (สถิติสำคัญ)")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|:---|:---|")
    lines.append(f"| **ระยะทางรวม** | 🔥 **{total_dist:.2f} km**{f' (Run {run_dist:.1f} + Walk {walk_dist:.1f})' if walk_sessions and run_sessions else ''} |")
    lines.append(f"| **จำนวน Sessions** | 📋 {len(sessions)} ครั้ง{f' (Run {len(run_sessions)} + Walk {len(walk_sessions)})' if walk_sessions and run_sessions else ''} |")
    lines.append(f"| **Active Days** | 📅 {active_days} วัน |")
    lines.append(f"| **Avg / Session** | 📏 {avg_dist:.2f} km |")
    lines.append(f"| **Best Distance** | 🏆 {longest_run['distance']:.2f} km — {longest_run['activity']} ({longest_run['date']}) |")
    if best_pace_session:
        lines.append(f"| **Best Pace** | ⚡ {seconds_to_pace(best_pace_secs)} — {best_pace_session['activity']} ({best_pace_session['date']}) |")
    lines.append(f"| **First Active** | 🗓️ {first_date} |")
    lines.append(f"| **Last Active** | 🗓️ {last_date} |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Distance Progression
    lines.append(f"## 📏 Distance Progression (พัฒนาการระยะทาง)")
    lines.append(f"")
    max_dist_month = max(monthly[m]['distance'] for m in sorted_months) if sorted_months else 1
    for m in sorted_months:
        d = monthly[m]['distance']
        bar_len = int((d / max(max_dist_month, 0.01)) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        lines.append(f"```")
        lines.append(f"{m}:  {bar}  {d:.1f} km ({monthly[m]['sessions']} sessions)")
        lines.append(f"```")
    lines.append(f"")
    
    # PR Timeline
    lines.append(f"### ⚡ Personal Records Timeline")
    lines.append(f"")
    lines.append(f"| Date | Milestone | Distance |")
    lines.append(f"|:---|:---|:---:|")
    lines.append(f"| {first_date} | First Activity | {sessions[0]['distance']:.2f} km |")
    
    # Track running distance PRs
    current_best = 0
    for s in sessions:
        if s['distance'] > current_best:
            current_best = s['distance']
            if s != sessions[0]:
                lines.append(f"| {s['date']} | New PB! 🏆 | {s['distance']:.2f} km |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Coach Recommendations
    lines.append(f"## 💡 Coach's Recommendations (คำแนะนำจากโค้ช)")
    lines.append(f"")
    
    lines.append(f"### 🟢 สิ่งที่ทำได้ดี")
    if active_days >= 10:
        lines.append(f"1. **ความสม่ำเสมอ** — ออกกำลังกายมาแล้ว {active_days} วัน ถือว่ามีวินัยดีมาก!")
    if dist_change > 20:
        lines.append(f"1. **ระยะทางพัฒนา** — เพิ่มขึ้น {dist_change:.0f}% จากเดือนแรก")
    if longest_run['distance'] >= 5:
        lines.append(f"1. **ระยะทางสูงสุด** — ทำได้ {longest_run['distance']:.2f} km ถือว่าดีมาก!")
    if len(sessions) >= 5:
        lines.append(f"1. **ต่อเนื่อง** — สะสมมาแล้ว {len(sessions)} sessions ไม่ทิ้งนิสัย")
    lines.append(f"")
    
    lines.append(f"### 🟡 จุดที่ควรพัฒนา")
    if is_primarily_walker:
        lines.append(f"1. **ลองเพิ่มช่วงวิ่งเบาๆ** — สลับเดิน-วิ่ง (Walk-Run) เพื่อสร้างฐาน")
    if active_days < 10 and len(sessions) > 0:
        lines.append(f"1. **เพิ่มความถี่** — ปัจจุบันเฉลี่ย ~{len(sessions)/max(((datetime.strptime(last_date,'%Y-%m-%d')-datetime.strptime(first_date,'%Y-%m-%d')).days/7), 1):.1f} ครั้ง/สัปดาห์ พยายามเพิ่มเป็น 3 ครั้ง/สัปดาห์")
    if longest_run['distance'] < 5 and not is_primarily_walker:
        lines.append(f"1. **ค่อยๆ เพิ่มระยะ** — ตั้งเป้า 5 km เป็น milestone ถัดไป")
    elif longest_run['distance'] < 10 and not is_primarily_walker:
        lines.append(f"1. **ค่อยๆ เพิ่มระยะ Long Run** — เพิ่มไม่เกิน 10% ต่อสัปดาห์")
    lines.append(f"1. **อย่าลืมวันพัก** — ร่างกายสร้างความแข็งแรงในช่วงพัก ไม่ใช่ตอนออกกำลังกาย")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Generated by Running Coach AI | {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append(f"")
    lines.append(f"[🏠 กลับหน้าหลัก (Profile)](README.md) | [📊 ดูสถิติทั้งหมด (Statistics)](personal-statistics.md)")
    
    # Add plan link if exists
    plan_path = os.path.join(os.path.dirname(os.path.join(MEMBER_RESULTS_DIR, "dummy")), "running-plan.md")
    lines.append(f"")
    
    return "\n".join(lines)


def main():
    generated = 0
    skipped = 0
    
    for folder_name, (nickname, thai_name, team) in FOLDER_MAP.items():
        folder_path = os.path.join(MEMBER_RESULTS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            print(f"  ⚠️ Folder not found: {folder_name}")
            continue
        
        # Skip Boy — already has a hand-crafted coach-analysis.md
        if nickname == "Boy":
            print(f"  ⏭️ {nickname:8s} | Skipped (already has coach-analysis.md)")
            skipped += 1
            continue
        
        # Skip GIO — already has performance-report/
        if nickname == "Gio":
            # Create a coach-analysis.md that references the performance-report/
            sessions = parse_stats(folder_path)
            if sessions:
                content = generate_coach_analysis(nickname, thai_name, team, sessions)
            else:
                content = generate_coach_analysis(nickname, thai_name, team, [])
            out_path = os.path.join(folder_path, "coach-analysis.md")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {nickname:8s} | {len(sessions):3d} sessions | {sum(s['distance'] for s in sessions):8.2f} km | {out_path}")
            generated += 1
            continue
        
        sessions = parse_stats(folder_path)
        content = generate_coach_analysis(nickname, thai_name, team, sessions)
        
        out_path = os.path.join(folder_path, "coach-analysis.md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        dist = sum(s['distance'] for s in sessions)
        print(f"  ✅ {nickname:8s} | {len(sessions):3d} sessions | {dist:8.2f} km | {out_path}")
        generated += 1
    
    print(f"\n🎉 Generated {generated} coach-analysis.md files ({skipped} skipped)")


if __name__ == '__main__':
    main()
