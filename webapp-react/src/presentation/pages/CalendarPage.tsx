import React from 'react';
import { Card } from '../components/ui/Card';
import { StaticCompetitionRepository } from '../../infrastructure/repositories/StaticCompetitionRepository';

interface WeekData {
    week: number | string;
    dates: string;
    period: string;
    notes: string;
}

const getCurrentWeek = (): number => {
    const now = new Date();
    const weeks: [number, string, string][] = [
        [1, '2026-01-01', '2026-01-03'],
        [2, '2026-01-04', '2026-01-10'],
        [3, '2026-01-11', '2026-01-17'],
        [4, '2026-01-18', '2026-01-24'],
        [5, '2026-01-25', '2026-01-31'],
        [6, '2026-02-01', '2026-02-07'],
        [7, '2026-02-08', '2026-02-14'],
        [8, '2026-02-15', '2026-02-21'],
        [9, '2026-02-22', '2026-02-28'],
        [10, '2026-03-01', '2026-03-07'],
        [11, '2026-03-08', '2026-03-14'],
        [12, '2026-03-15', '2026-03-21'],
        [13, '2026-03-22', '2026-03-28'],
    ];
    for (const [wk, start, end] of weeks) {
        const s = new Date(start + 'T00:00:00');
        const e = new Date(end + 'T23:59:59');
        if (now >= s && now <= e) return wk;
    }
    return 11;
};

// Week date ranges for Q1 2026
const Q1_WEEKS: { week: number; start: string; end: string; label: string }[] = [
    { week: 1, start: '2026-01-01', end: '2026-01-03', label: '1–3 Jan' },
    { week: 2, start: '2026-01-04', end: '2026-01-10', label: '4–10 Jan' },
    { week: 3, start: '2026-01-11', end: '2026-01-17', label: '11–17 Jan' },
    { week: 4, start: '2026-01-18', end: '2026-01-24', label: '18–24 Jan' },
    { week: 5, start: '2026-01-25', end: '2026-01-31', label: '25–31 Jan' },
    { week: 6, start: '2026-02-01', end: '2026-02-07', label: '1–7 Feb' },
    { week: 7, start: '2026-02-08', end: '2026-02-14', label: '8–14 Feb' },
    { week: 8, start: '2026-02-15', end: '2026-02-21', label: '15–21 Feb' },
    { week: 9, start: '2026-02-22', end: '2026-02-28', label: '22–28 Feb' },
    { week: 10, start: '2026-03-01', end: '2026-03-07', label: '1–7 Mar' },
    { week: 11, start: '2026-03-08', end: '2026-03-14', label: '8–14 Mar' },
    { week: 12, start: '2026-03-15', end: '2026-03-21', label: '15–21 Mar' },
    { week: 13, start: '2026-03-22', end: '2026-03-28', label: '22–28 Mar' },
];

interface GapData {
    week: number;
    dates: string;
    manda: number;
    it: number;
    gap: number; // IT - Manda (positive = IT leads)
}

function computeWeeklyGap(activities: { date: string; mando_accum: number; it_accum: number }[]): GapData[] {
    const result: GapData[] = [];
    for (const wk of Q1_WEEKS) {
        // Find all activities within this week's date range
        const weekActivities = activities.filter(a => a.date >= wk.start && a.date <= wk.end);
        if (weekActivities.length === 0) continue;
        // Sort by date descending to get the latest (highest accumulate)
        weekActivities.sort((a, b) => b.date.localeCompare(a.date));
        const latest = weekActivities[0];
        result.push({
            week: wk.week,
            dates: wk.label,
            manda: latest.mando_accum,
            it: latest.it_accum,
            gap: latest.it_accum - latest.mando_accum,
        });
    }
    return result;
}

const q1Weeks: WeekData[] = [
    { week: 1, dates: '1 Jan – 3 Jan', period: 'Thu – Sat', notes: '🎉 Competition Kick-off!' },
    { week: 2, dates: '4 Jan – 10 Jan', period: 'Sun – Sat', notes: '' },
    { week: 3, dates: '11 Jan – 17 Jan', period: 'Sun – Sat', notes: '' },
    { week: 4, dates: '18 Jan – 24 Jan', period: 'Sun – Sat', notes: '' },
    { week: 5, dates: '25 Jan – 31 Jan', period: 'Sun – Sat', notes: '🧧 Chinese New Year' },
    { week: 6, dates: '1 Feb – 7 Feb', period: 'Sun – Sat', notes: '' },
    { week: 7, dates: '8 Feb – 14 Feb', period: 'Sun – Sat', notes: '💕 Valentine\'s Day' },
    { week: 8, dates: '15 Feb – 21 Feb', period: 'Sun – Sat', notes: '' },
    { week: 9, dates: '22 Feb – 28 Feb', period: 'Sun – Sat', notes: '' },
    { week: 10, dates: '1 Mar – 7 Mar', period: 'Sun – Sat', notes: '' },
    { week: 11, dates: '8 Mar – 14 Mar', period: 'Sun – Sat', notes: '' },
    { week: 12, dates: '15 Mar – 21 Mar', period: 'Sun – Sat', notes: '' },
    { week: 13, dates: '22 Mar – 28 Mar', period: 'Sun – Sat', notes: '' },
];

const q2Weeks: WeekData[] = [
    { week: 14, dates: '1 Apr – 4 Apr', period: 'Wed – Sat', notes: '🔄 Q2 Starts!' },
    { week: 15, dates: '5 Apr – 11 Apr', period: 'Sun – Sat', notes: 'Chakri Memorial Day' },
    { week: 16, dates: '12 Apr – 18 Apr', period: 'Sun – Sat', notes: '🌊 Songkran Festival' },
    { week: 17, dates: '19 Apr – 25 Apr', period: 'Sun – Sat', notes: '' },
    { week: 18, dates: '26 Apr – 2 May', period: 'Sun – Sat', notes: 'Labour Day' },
    { week: 19, dates: '3 May – 9 May', period: 'Sun – Sat', notes: '👑 Coronation Day' },
    { week: 20, dates: '10 May – 16 May', period: 'Sun – Sat', notes: 'Visakha Bucha' },
    { week: 21, dates: '17 May – 23 May', period: 'Sun – Sat', notes: '' },
    { week: 22, dates: '24 May – 30 May', period: 'Sun – Sat', notes: '' },
    { week: 23, dates: '31 May – 6 Jun', period: 'Sun – Sat', notes: '' },
    { week: 24, dates: '7 Jun – 13 Jun', period: 'Sun – Sat', notes: '' },
    { week: 25, dates: '14 Jun – 20 Jun', period: 'Sun – Sat', notes: '' },
    { week: 26, dates: '21 Jun – 27 Jun', period: 'Sun – Sat', notes: '' },
];

const q3Weeks: WeekData[] = [
    { week: 27, dates: '1 Jul – 4 Jul', period: 'Wed – Sat', notes: '🔄 Q3 Starts!' },
    { week: 28, dates: '5 Jul – 11 Jul', period: 'Sun – Sat', notes: 'Asahna Bucha' },
    { week: 29, dates: '12 Jul – 18 Jul', period: 'Sun – Sat', notes: '' },
    { week: 30, dates: '19 Jul – 25 Jul', period: 'Sun – Sat', notes: '' },
    { week: 31, dates: '26 Jul – 1 Aug', period: 'Sun – Sat', notes: '👑 King\'s Birthday' },
    { week: 32, dates: '2 Aug – 8 Aug', period: 'Sun – Sat', notes: '' },
    { week: 33, dates: '9 Aug – 15 Aug', period: 'Sun – Sat', notes: '👑 Queen Mother\'s Birthday' },
    { week: 34, dates: '16 Aug – 22 Aug', period: 'Sun – Sat', notes: '' },
    { week: 35, dates: '23 Aug – 29 Aug', period: 'Sun – Sat', notes: '' },
    { week: 36, dates: '30 Aug – 5 Sep', period: 'Sun – Sat', notes: '' },
    { week: 37, dates: '6 Sep – 12 Sep', period: 'Sun – Sat', notes: '' },
    { week: 38, dates: '13 Sep – 19 Sep', period: 'Sun – Sat', notes: '' },
    { week: 39, dates: '20 Sep – 26 Sep', period: 'Sun – Sat', notes: '' },
];

const q4Weeks: WeekData[] = [
    { week: 40, dates: '1 Oct – 3 Oct', period: 'Thu – Sat', notes: '🔄 Q4 Starts!' },
    { week: 41, dates: '4 Oct – 10 Oct', period: 'Sun – Sat', notes: '' },
    { week: 42, dates: '11 Oct – 17 Oct', period: 'Sun – Sat', notes: 'King Bhumibol Memorial' },
    { week: 43, dates: '18 Oct – 24 Oct', period: 'Sun – Sat', notes: 'Chulalongkorn Day' },
    { week: 44, dates: '25 Oct – 31 Oct', period: 'Sun – Sat', notes: '🎃 Halloween' },
    { week: 45, dates: '1 Nov – 7 Nov', period: 'Sun – Sat', notes: '' },
    { week: 46, dates: '8 Nov – 14 Nov', period: 'Sun – Sat', notes: '🪷 Loy Krathong' },
    { week: 47, dates: '15 Nov – 21 Nov', period: 'Sun – Sat', notes: '' },
    { week: 48, dates: '22 Nov – 28 Nov', period: 'Sun – Sat', notes: '' },
    { week: 49, dates: '29 Nov – 5 Dec', period: 'Sun – Sat', notes: '👑 King Bhumibol Birthday' },
    { week: 50, dates: '6 Dec – 12 Dec', period: 'Sun – Sat', notes: 'Constitution Day' },
    { week: 51, dates: '13 Dec – 19 Dec', period: 'Sun – Sat', notes: '' },
    { week: 52, dates: '20 Dec – 26 Dec', period: 'Sun – Sat', notes: '🎄 Christmas' },
];

interface QuarterInfo {
    label: string;
    status: string;
    statusColor: string;
    period: string;
    weeks: WeekData[];
}

const quarters: QuarterInfo[] = [
    { label: 'Q1', status: '🟢 Active', statusColor: 'text-green-400', period: 'January – March', weeks: q1Weeks },
    { label: 'Q2', status: '⬜ Upcoming', statusColor: 'text-textMuted', period: 'April – June', weeks: q2Weeks },
    { label: 'Q3', status: '⬜ Upcoming', statusColor: 'text-textMuted', period: 'July – September', weeks: q3Weeks },
    { label: 'Q4', status: '⬜ Upcoming', statusColor: 'text-textMuted', period: 'October – December', weeks: q4Weeks },
];

const WeekTable: React.FC<{ weeks: WeekData[]; currentWeek: number; gapData?: GapData[] }> = ({ weeks, currentWeek, gapData }) => {
    const gapMap = new Map<number, GapData>();
    if (gapData) {
        for (const g of gapData) gapMap.set(g.week, g);
    }
    const showGap = gapData && gapData.length > 0;

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
                <thead>
                    <tr className="border-b border-white/10 text-textMuted uppercase text-xs">
                        <th className="pb-3 px-3 font-medium w-16">Week</th>
                        <th className="pb-3 px-3 font-medium">Dates</th>
                        <th className="pb-3 px-3 font-medium hidden sm:table-cell">Period</th>
                        {showGap && <th className="pb-3 px-3 font-medium text-right">Avg Gap/Person</th>}
                        <th className="pb-3 px-3 font-medium">Notes</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                    {weeks.map((w) => {
                        const isCurrent = w.week === currentWeek;
                        const weekNum = typeof w.week === 'number' ? w.week : parseInt(String(w.week));
                        const gap = gapMap.get(weekNum);
                        const avgGap = gap ? gap.gap / 10 : null;

                        return (
                            <tr
                                key={String(w.week)}
                                className={`transition-colors ${isCurrent
                                    ? 'bg-accent/10 border-l-4 border-l-accent'
                                    : 'hover:bg-white/5'
                                    }`}
                            >
                                <td className={`py-3 px-3 font-bold ${isCurrent ? 'text-accent' : ''}`}>
                                    {w.week}
                                </td>
                                <td className={`py-3 px-3 ${isCurrent ? 'text-accent font-semibold' : ''}`}>
                                    {w.dates}
                                </td>
                                <td className={`py-3 px-3 hidden sm:table-cell ${isCurrent ? 'text-accent' : 'text-textMuted'}`}>
                                    {w.period}
                                </td>
                                {showGap && (
                                    <td className="py-3 px-3 text-right">
                                        {avgGap !== null ? (
                                            <span className={`font-semibold text-xs px-2 py-0.5 rounded-full ${avgGap > 0 ? 'bg-red-400/15 text-red-400' : 'bg-green-400/15 text-green-400'}`}>
                                                {avgGap > 0 ? '+' : ''}{avgGap.toFixed(1)} km
                                            </span>
                                        ) : (
                                            <span className="text-textMuted text-xs">—</span>
                                        )}
                                    </td>
                                )}
                                <td className="py-3 px-3">
                                    {w.notes}
                                    {isCurrent && (
                                        <span className="ml-2 inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-accent text-black">
                                            📍 NOW
                                        </span>
                                    )}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

const AccGapCard: React.FC<{ currentWeek: number; gapData: GapData[] }> = ({ currentWeek, gapData }) => {
    if (gapData.length === 0) return null;

    const maxAbsGap = Math.max(...gapData.map(d => Math.abs(d.gap)));
    const peakGap = Math.max(...gapData.map(d => d.gap));
    const peakWeek = gapData.find(d => d.gap === peakGap);
    const latestGap = gapData[gapData.length - 1];
    const gapReduced = peakGap - latestGap.gap;
    const isClosing = gapData.length >= 2 && gapData[gapData.length - 1].gap < gapData[gapData.length - 2].gap;
    const existingWeeks = new Set(gapData.map(d => d.week));
    const futureWeeks = Q1_WEEKS.filter(w => !existingWeeks.has(w.week)).map(w => w.week);

    return (
        <Card>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-5 gap-3">
                <h2 className="text-lg font-heading">📈 ACC-GAP: Weekly Gap Tracker</h2>
                <div className="flex gap-3 text-xs">
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded-full bg-green-500 inline-block" /> 🪖 Manda leads
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded-full bg-red-400 inline-block" /> 💻 IT leads
                    </span>
                </div>
            </div>

            {/* Visual Bar Chart */}
            <div className="space-y-1.5 mb-6">
                {gapData.map((d) => {
                    const pct = (Math.abs(d.gap) / maxAbsGap) * 100;
                    const isITLead = d.gap > 0;
                    const isCurrent = d.week === currentWeek;
                    const isPeak = d.gap === peakGap;

                    return (
                        <div key={d.week} className={`flex items-center gap-2 py-1 px-2 rounded-lg transition-colors ${isCurrent ? 'bg-accent/10 border border-accent/20' : 'hover:bg-white/5'}`}>
                            <div className="w-8 text-xs font-bold text-right shrink-0">
                                W{d.week}
                            </div>

                            {/* Left side (Manda leads) */}
                            <div className="flex-1 flex justify-end">
                                {!isITLead && (
                                    <div
                                        className="h-5 rounded-l-full bg-gradient-to-r from-green-600 to-green-400 transition-all duration-500"
                                        style={{ width: `${pct}%`, minWidth: '4px' }}
                                    />
                                )}
                            </div>

                            {/* Center line */}
                            <div className="w-px h-6 bg-white/20 shrink-0" />

                            {/* Right side (IT leads) */}
                            <div className="flex-1">
                                {isITLead && (
                                    <div
                                        className="h-5 rounded-r-full bg-gradient-to-r from-red-400 to-red-600 transition-all duration-500"
                                        style={{ width: `${pct}%`, minWidth: '4px' }}
                                    />
                                )}
                            </div>

                            <div className="w-20 text-xs text-right shrink-0">
                                <span className={`font-semibold ${isITLead ? 'text-red-400' : 'text-green-400'}`}>
                                    {isITLead ? '+' : ''}{d.gap.toFixed(1)}
                                </span>
                                {isPeak && <span className="ml-1 text-[9px] text-red-300">PEAK</span>}
                                {isCurrent && <span className="ml-1 text-[9px] text-accent">NOW</span>}
                            </div>
                        </div>
                    );
                })}

                {/* Future weeks */}
                {futureWeeks.map(w => (
                    <div key={w} className="flex items-center gap-2 py-1 px-2 opacity-30">
                        <div className="w-8 text-xs font-bold text-right shrink-0">W{w}</div>
                        <div className="flex-1 flex justify-end" />
                        <div className="w-px h-6 bg-white/20 shrink-0" />
                        <div className="flex-1" />
                        <div className="w-20 text-xs text-right shrink-0 text-textMuted">⏳</div>
                    </div>
                ))}
            </div>

            {/* Summary Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
                <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-xl font-black text-red-400">+{peakGap.toFixed(1)}</div>
                    <div className="text-[10px] text-textMuted mt-1">Peak Gap (W{peakWeek?.week})</div>
                </div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-xl font-black text-accent">+{latestGap.gap.toFixed(1)}</div>
                    <div className="text-[10px] text-textMuted mt-1">Current Gap (W{latestGap.week})</div>
                </div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-xl font-black text-green-400">−{gapReduced.toFixed(1)}</div>
                    <div className="text-[10px] text-textMuted mt-1">Gap Reduced</div>
                </div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-xl font-black">{isClosing ? '📉📉' : '📈'}</div>
                    <div className="text-[10px] text-textMuted mt-1">Trend: {isClosing ? 'Closing' : 'Widening'}</div>
                </div>
            </div>

            <div className="text-center text-sm text-textMuted">
                Gap = IT System accumulated − Mandalorian accumulated (km) · Data from data.json
            </div>
        </Card>
    );
};

export const CalendarPage: React.FC = () => {
    const currentWeek = getCurrentWeek();
    const [expandedQ, setExpandedQ] = React.useState<string>('Q1');
    const [gapData, setGapData] = React.useState<GapData[]>([]);

    React.useEffect(() => {
        const repo = new StaticCompetitionRepository();
        repo.getCompetitionData().then(data => {
            const computed = computeWeeklyGap(data.activities);
            setGapData(computed);
        }).catch(err => console.error('Failed to load gap data:', err));
    }, []);

    return (
        <div className="flex flex-col gap-6 fade-in">
            {/* Current Week Highlight */}
            <Card>
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                        <h2 className="text-xl font-heading">📅 Tournament Calendar 2026</h2>
                        <p className="text-textMuted text-sm mt-1">
                            Week 1 begins Thursday, 1 January 2026. Each week runs Thursday → Wednesday.
                        </p>
                    </div>
                    <div className="px-4 py-2 rounded-full bg-accent/10 border border-accent/20 text-accent text-sm font-semibold whitespace-nowrap">
                        📍 Week {currentWeek} — Q{Math.ceil(currentWeek / 13)}
                    </div>
                </div>
            </Card>

            {/* Quarter Tabs */}
            <div className="flex flex-wrap gap-2">
                {quarters.map((q) => (
                    <button
                        key={q.label}
                        onClick={() => setExpandedQ(q.label)}
                        className={`px-5 py-2.5 rounded-xl font-semibold transition-all text-sm ${expandedQ === q.label
                            ? 'bg-accent text-black shadow-lg shadow-accent/20'
                            : 'bg-white/5 text-textMuted hover:bg-white/10 hover:text-white border border-white/5'
                            }`}
                    >
                        {q.label} <span className="ml-1 opacity-70">{q.status.split(' ')[0]}</span>
                    </button>
                ))}
            </div>

            {/* Active Quarter */}
            {quarters.filter(q => q.label === expandedQ).map((q) => (
                <Card key={q.label}>
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-lg font-heading">
                            🏆 {q.label} — {q.period}
                        </h2>
                        <span className={`text-sm font-semibold ${q.statusColor}`}>{q.status}</span>
                    </div>
                    <WeekTable weeks={q.weeks} currentWeek={currentWeek} gapData={q.label === 'Q1' ? gapData : undefined} />
                </Card>
            ))}

            {/* ACC-GAP: Accumulated Gap */}
            {expandedQ === 'Q1' && <AccGapCard currentWeek={currentWeek} gapData={gapData} />}

            {/* Year Summary */}
            <Card>
                <h2 className="text-lg font-heading mb-4">📊 Yearly Overview</h2>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    {quarters.map((q) => (
                        <button
                            key={q.label}
                            onClick={() => setExpandedQ(q.label)}
                            className={`p-4 rounded-xl border transition-all text-center cursor-pointer ${expandedQ === q.label
                                ? 'border-accent bg-accent/10'
                                : 'border-white/10 bg-white/3 hover:border-white/20'
                                }`}
                        >
                            <div className="text-2xl font-black mb-1">{q.label}</div>
                            <div className="text-xs text-textMuted">{q.period}</div>
                            <div className={`text-xs mt-2 font-semibold ${q.statusColor}`}>{q.status}</div>
                        </button>
                    ))}
                </div>
                <div className="text-center text-textMuted text-sm mt-4">
                    Total: 52 Weeks · 365 Days · 4 Quarters
                </div>
            </Card>
        </div>
    );
};
