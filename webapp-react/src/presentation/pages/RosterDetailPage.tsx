import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useRosterDetail } from '../hooks/useCompetitionData';
import { Badge } from '../components/ui/Badge';
import DOMPurify from 'dompurify';

/**
 * Fetch a pre-rendered HTML file from assets_data/members/{nickname}/{file}.html
 * and return just the <body> inner HTML (stripping the wrapper document).
 */
async function fetchHtmlContent(nickname: string, file: string): Promise<string> {
    const basePath = import.meta.env.BASE_URL || '/';
    const base = basePath.endsWith('/') ? basePath : basePath + '/';
    const nicknameSafe = nickname.toLowerCase().replace(/[^a-z0-9_\-\.]/g, '');
    const url = `${base}assets_data/members/${nicknameSafe}/${file}.html`;

    try {
        const response = await fetch(url);
        if (!response.ok) return '';
        const html = await response.text();

        // Extract just the <body> content (skip the wrapper HTML/head/style)
        const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
        return bodyMatch ? bodyMatch[1] : html;
    } catch {
        return '';
    }
}

export const RosterDetailPage: React.FC = () => {
    const { nickname } = useParams<{ nickname: string }>();
    const navigate = useNavigate();
    const { member, loading } = useRosterDetail(nickname);
    const [activeTab, setActiveTab] = useState<'readme' | 'plan' | 'statistics'>('readme');
    const [selectedMonth, setSelectedMonth] = useState<string>('all');

    // HTML content state for each tab
    const [htmlContent, setHtmlContent] = useState<{ readme: string; plan: string; statistics: string }>({
        readme: '', plan: '', statistics: ''
    });
    const [htmlLoading, setHtmlLoading] = useState(true);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [nickname]);

    // Fetch all three HTML files when nickname changes
    useEffect(() => {
        if (!nickname) return;
        setHtmlLoading(true);
        Promise.all([
            fetchHtmlContent(nickname, 'README'),
            fetchHtmlContent(nickname, 'running-plan'),
            fetchHtmlContent(nickname, 'personal-statistics'),
        ]).then(([readme, plan, statistics]) => {
            setHtmlContent({ readme, plan, statistics });
            setHtmlLoading(false);
        });
    }, [nickname]);

    // Extract available months from statistics HTML headings
    const availableMonths: string[] = [];
    if (htmlContent.statistics) {
        const matches = htmlContent.statistics.matchAll(/id="[^"]*"[^>]*>📅\s*(20\d{2}-[a-zA-Z]+)/g);
        for (const match of matches) {
            if (!availableMonths.includes(match[1])) {
                availableMonths.push(match[1]);
            }
        }
    }

    // Filter statistics HTML by month if needed
    const getFilteredStatistics = useCallback((): string => {
        if (!htmlContent.statistics) return '<p><em>No data available</em></p>';
        if (selectedMonth === 'all') return htmlContent.statistics;

        // Find the section for the selected month by splitting on <h2> headings
        const parser = new DOMParser();
        const doc = parser.parseFromString(`<div>${htmlContent.statistics}</div>`, 'text/html');
        const headings = doc.querySelectorAll('h2');

        let targetHeading: Element | null = null;
        for (const h of headings) {
            if (h.textContent?.includes(selectedMonth)) {
                targetHeading = h;
                break;
            }
        }

        if (!targetHeading) {
            return '<p><em>No activities found for this month.</em></p>';
        }

        // Collect all elements before this heading (profile/summary info)
        const allElements: Element[] = [];
        const container = doc.body.firstElementChild;
        if (!container) return htmlContent.statistics;

        let foundHeader = false;
        const headerParts: string[] = [];
        const monthParts: string[] = [];

        for (const child of container.children) {
            if (child === targetHeading) {
                foundHeader = true;
                monthParts.push(child.outerHTML);
                continue;
            }
            if (foundHeader) {
                // Stop at the next h2
                if (child.tagName === 'H2') break;
                monthParts.push(child.outerHTML);
            } else {
                // Everything before the first h2 with 📅 is header content
                if (child.tagName === 'H2' && child.textContent?.includes('📅')) {
                    // Skip other month sections before our target
                    continue;
                }
                headerParts.push(child.outerHTML);
            }
        }

        return headerParts.join('\n') + '\n' + monthParts.join('\n');
    }, [htmlContent.statistics, selectedMonth]);

    const sanitize = (html: string) => {
        if (!html) return '<p><em>No data available</em></p>';
        return DOMPurify.sanitize(html, { ADD_ATTR: ['target'] });
    };

    if (loading || htmlLoading) return <div className="p-10 text-center text-textMuted">Loading profile...</div>;
    if (!member) return <div className="p-10 text-center text-red-500">Member Not Found</div>;

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
                {activeTab === 'readme' && <div dangerouslySetInnerHTML={{ __html: sanitize(htmlContent.readme) }} />}
                {activeTab === 'plan' && <div dangerouslySetInnerHTML={{ __html: sanitize(htmlContent.plan) }} />}
                {activeTab === 'statistics' && <div dangerouslySetInnerHTML={{ __html: sanitize(getFilteredStatistics()) }} />}
            </div>
        </div>
    );
};
