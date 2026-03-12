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
            return false; // fallback to default renderer
        }
    }
});

export const RosterDetailPage: React.FC = () => {
    const { nickname } = useParams<{ nickname: string }>();
    const navigate = useNavigate();
    // In actual implementation we use decodeURIComponent depending on how router passes it, but router handles it mostly.
    const { member, loading } = useRosterDetail(nickname);
    const [activeTab, setActiveTab] = useState<'readme' | 'plan' | 'statistics'>('readme');
    const [selectedMonth, setSelectedMonth] = useState<string>('all');

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [nickname]);

    if (loading) return <div className="p-10 text-center text-textMuted">Loading profile...</div>;
    if (!member) return <div className="p-10 text-center text-red-500">Member Not Found</div>;

    const parseMd = (text?: string, monthFilter: string = 'all') => {
        if (!text) return "*No data available*";

        let textToParse = text;

        if (monthFilter !== 'all') {
            // Keep the initial headers and profile info, but filter the activity months
            const headerSplit = text.split(/---\n/);
            if (headerSplit.length > 1) {
                const headerPart = headerSplit[0];
                const sectionsPart = headerSplit.slice(1).join('---\n');

                // Extract just the selected month section
                const monthRegex = new RegExp(`(## 📅 ${monthFilter}[\\s\\S]*?)(?=## 📅|$)`);
                const match = sectionsPart.match(monthRegex);

                if (match) {
                    textToParse = `${headerPart}---\n\n${match[1]}`;
                } else {
                    textToParse = `${headerPart}---\n\n*No activities found for this month.*`;
                }
            }
        }

        // Fix markdown links with unescaped spaces or parentheses that break the parser
        // specifically targeting any markdown links containing spaces or parens in the URL
        const preprocessedText = textToParse.replace(
            /\[(.*?)\]\((.*?)\)/g,
            (_match, p1, p2) => {
                const encoded = p2.replace(/ /g, "%20").replace(/\(/g, "%28").replace(/\)/g, "%29");
                return `[${p1}](${encoded})`;
            }
        );

        // ADD_ATTR: ['target'] is necessary so DOMPurify doesn't strip target="_blank"
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
            </div>

            <div className="glass-panel p-8 overflow-x-auto markdown-body">
                {activeTab === 'readme' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.readme) }} />}
                {activeTab === 'plan' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.plan) }} />}
                {activeTab === 'statistics' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.statistics, selectedMonth) }} />}
            </div>
        </div>
    );
};
