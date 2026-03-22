import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useRosterDetail } from '../hooks/useCompetitionData';
import { Badge } from '../components/ui/Badge';
import DOMPurify from 'dompurify';
import { marked } from 'marked';
import { resolveImagePath } from '../../utils/imagePath';

// Intercept markdown links ending in image extensions and render them as actual images
marked.use({
    renderer: {
        link(token) {
            let { href, text, title } = token;

            // Fix Vite Router pathing: Force relative links to resolve properly
            href = resolveImagePath(href);

            if (href.match(/\.(jpg|jpeg|png|gif|webp|JPG|JPEG|PNG)$/)) {
                return `<a href="${href}" target="_blank" rel="noopener noreferrer" title="${title || text}"><img src="${href}" alt="${text}" class="w-16 h-16 object-cover inline-block rounded-lg shadow-sm border border-white/20 mx-1 transition-transform hover:scale-110" loading="lazy" /></a>`;
            }
            // For other links (like .md documents), allow them to be clickable
            return `<a href="${href}" target="_blank" rel="noopener noreferrer" class="text-accent hover:text-white underline underline-offset-2 transition-colors">${text}</a>`;
        }
    }
});

export const RosterDetailPage: React.FC = () => {
    const { nickname } = useParams<{ nickname: string }>();
    const navigate = useNavigate();
    const { member, loading } = useRosterDetail(nickname);
    const [activeTab, setActiveTab] = useState<'readme' | 'plan' | 'statistics' | 'coach' | 'daily'>('readme');
    const [selectedMonth, setSelectedMonth] = useState<string>('all');
    const [selectedDailyDate, setSelectedDailyDate] = useState<string>('');
    const [dailyContent, setDailyContent] = useState<string>('');
    const [dailyLoading, setDailyLoading] = useState(false);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [nickname]);

    // Auto-select the latest daily date when member loads
    useEffect(() => {
        if (member?.daily_dates && member.daily_dates.length > 0) {
            const latest = member.daily_dates[member.daily_dates.length - 1];
            setSelectedDailyDate(latest);
        }
    }, [member]);

    // Fetch daily markdown content when date changes
    useEffect(() => {
        if (!selectedDailyDate || !member) return;
        setDailyLoading(true);

        const nicknameSafe = member.nickname.toLowerCase().replace(/[^a-z0-9_\-\.]/g, '');
        const basePath = import.meta.env.BASE_URL || '/';
        const url = `${basePath}assets_data/member_results/${nicknameSafe}/daily/${selectedDailyDate}.md`;

        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error('Not found');
                return res.text();
            })
            .then(text => {
                setDailyContent(text);
                setDailyLoading(false);
            })
            .catch(() => {
                setDailyContent('*ไม่พบรายงาน Daily Performance สำหรับวันที่เลือก*');
                setDailyLoading(false);
            });
    }, [selectedDailyDate, member]);

    if (loading) return <div className="p-10 text-center text-textMuted">Loading profile...</div>;
    if (!member) return <div className="p-10 text-center text-red-500">Member Not Found</div>;

    const parseMd = (text?: string, monthFilter: string = 'all') => {
        if (!text) return "*No data available*";

        let textToParse = text;

        if (monthFilter !== 'all') {
            const headerSplit = text.split(/---\n/);
            if (headerSplit.length > 1) {
                const headerPart = headerSplit[0];
                const sectionsPart = headerSplit.slice(1).join('---\n');
                const monthRegex = new RegExp(`(## 📅 ${monthFilter}[\\s\\S]*?)(?=## 📅|$)`);
                const match = sectionsPart.match(monthRegex);
                if (match) {
                    textToParse = `${headerPart}---\n\n${match[1]}`;
                } else {
                    textToParse = `${headerPart}---\n\n*No activities found for this month.*`;
                }
            }
        }

        const preprocessedText = textToParse.replace(
            /\[(.*?)\]\((.*?)\)/g,
            (_match, p1, p2) => {
                const encoded = p2.replace(/ /g, "%20").replace(/\(/g, "%28").replace(/\)/g, "%29");
                return `[${p1}](${encoded})`;
            }
        );

        return DOMPurify.sanitize(marked.parse(preprocessedText) as string, { ADD_ATTR: ['target'] });
    };

    // Extract available months from statistics markdown
    const availableMonths: string[] = [];
    if (member.markdown?.statistics) {
        const matches = member.markdown.statistics.matchAll(/## 📅 (20\d{2}-[a-zA-Z]+)/g);
        for (const match of matches) {
            if (!availableMonths.includes(match[1])) {
                availableMonths.push(match[1]);
            }
        }
    }

    const hasCoachAnalysis = !!member.markdown?.coach_analysis;
    const hasDailyReports = (member.daily_dates?.length ?? 0) > 0;
    const isManda = member.team === 'Mandalorian';
    const teamIcon = isManda ? '🪖' : '💻';

    return (
        <div className="fade-in">
            <button
                onClick={() => navigate('/roster')}
                className="mb-6 px-4 py-2 border border-white/10 rounded-lg hover:bg-white/5 transition-colors"
            >
                ⬅️ Back to Roster
            </button>

            <div className="text-center py-6">
                <div className="text-4xl font-heading font-black mb-2">
                    {member.nickname} <span className="text-xl text-textMuted font-normal">({member.thai_name})</span>
                </div>
                <Badge team={member.team} className="text-sm px-4 py-1">
                    {teamIcon} {member.team}
                </Badge>
                <div className="mt-4 text-lg opacity-90">
                    🔥 <strong>{member.total_distance.toFixed(2)} km</strong> run over <strong>{member.active_days}</strong> active days.
                </div>
            </div>

            <div className="flex justify-between items-end border-b border-white/10 pb-2 mb-4 mt-8 flex-wrap gap-4">
                <div className="flex space-x-2 overflow-x-auto">
                    <button
                        onClick={() => setActiveTab('readme')}
                        className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${activeTab === 'readme' ? 'bg-white/10 text-white font-bold' : 'text-textMuted hover:text-white hover:bg-white/5'}`}
                    >
                        👤 Profile README
                    </button>
                    <button
                        onClick={() => setActiveTab('plan')}
                        className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${activeTab === 'plan' ? 'bg-white/10 text-white font-bold' : 'text-textMuted hover:text-white hover:bg-white/5'}`}
                    >
                        📝 Running Plan
                    </button>
                    <button
                        onClick={() => setActiveTab('statistics')}
                        className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${activeTab === 'statistics' ? 'bg-white/10 text-white font-bold' : 'text-textMuted hover:text-white hover:bg-white/5'}`}
                    >
                        📊 Statistics
                    </button>
                    <button
                        onClick={() => setActiveTab('coach')}
                        className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${activeTab === 'coach'
                            ? 'bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 text-emerald-300 font-bold border-b-2 border-emerald-400'
                            : 'text-textMuted hover:text-emerald-300 hover:bg-emerald-500/5'}`}
                    >
                        🏃 Coach Analysis
                    </button>
                    {hasDailyReports && (
                        <button
                            onClick={() => setActiveTab('daily')}
                            className={`px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${activeTab === 'daily'
                                ? 'bg-gradient-to-r from-amber-500/20 to-orange-500/20 text-amber-300 font-bold border-b-2 border-amber-400'
                                : 'text-textMuted hover:text-amber-300 hover:bg-amber-500/5'}`}
                        >
                            🏅 Daily Performance
                        </button>
                    )}
                </div>

                {activeTab === 'statistics' && availableMonths.length > 0 && (
                    <select
                        value={selectedMonth}
                        onChange={(e) => setSelectedMonth(e.target.value)}
                        className="bg-black/40 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-accent"
                    >
                        <option value="all">All Quarters</option>
                        {availableMonths.map(month => (
                            <option key={month} value={month}>{month.replace('-', ' ')}</option>
                        ))}
                    </select>
                )}

                {activeTab === 'daily' && hasDailyReports && (
                    <select
                        value={selectedDailyDate}
                        onChange={(e) => setSelectedDailyDate(e.target.value)}
                        className="bg-black/40 border border-amber-500/30 rounded-lg px-3 py-1.5 text-sm text-amber-200 focus:outline-none focus:border-amber-400"
                    >
                        {[...(member.daily_dates || [])].reverse().map(date => (
                            <option key={date} value={date}>📅 {date}</option>
                        ))}
                    </select>
                )}
            </div>

            <div className="glass-panel p-8 overflow-x-auto markdown-body">
                {activeTab === 'readme' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.readme) }} />}
                {activeTab === 'plan' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.plan) }} />}
                {activeTab === 'statistics' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.statistics, selectedMonth) }} />}
                {activeTab === 'coach' && (
                    hasCoachAnalysis ? (
                        <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.coach_analysis) }} />
                    ) : (
                        <div className="text-center py-16">
                            <div className="text-6xl mb-4">🏃</div>
                            <h3 className="text-xl font-bold text-white/80 mb-2">Coach Analysis Coming Soon</h3>
                            <p className="text-textMuted max-w-md mx-auto">
                                ยังไม่มีข้อมูล Coach Analysis สำหรับสมาชิกท่านนี้ — จะถูกสร้างขึ้นโดยอัตโนมัติหลังจากการวิเคราะห์จาก Running Coach ครั้งถัดไป
                            </p>
                        </div>
                    )
                )}
                {activeTab === 'daily' && (
                    dailyLoading ? (
                        <div className="text-center py-16 text-textMuted">⏳ Loading Daily Report...</div>
                    ) : dailyContent ? (
                        <div dangerouslySetInnerHTML={{ __html: parseMd(dailyContent) }} />
                    ) : (
                        <div className="text-center py-16">
                            <div className="text-6xl mb-4">🏅</div>
                            <h3 className="text-xl font-bold text-white/80 mb-2">No Daily Reports Yet</h3>
                            <p className="text-textMuted max-w-md mx-auto">
                                ยังไม่มีรายงาน Daily Performance สำหรับสมาชิกท่านนี้
                            </p>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};
