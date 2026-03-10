import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useRosterDetail } from '../hooks/useCompetitionData';
import { Badge } from '../components/ui/Badge';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

// Intercept markdown links ending in image extensions and render them as actual images
marked.use({
    renderer: {
        link(token) {
            let { href, text, title } = token;

            // Fix Vite Router pathing: Force relative links pointing to member_results to resolve from the absolute root
            if (href.startsWith('../member_results/')) {
                href = href.replace('../member_results/', '/member_results/');
            }

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

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [nickname]);

    if (loading) return <div className="p-10 text-center text-textMuted">Loading profile...</div>;
    if (!member) return <div className="p-10 text-center text-red-500">Member Not Found</div>;

    const parseMd = (text?: string) => {
        if (!text) return "*No data available*";
        // ADD_ATTR: ['target'] is necessary so DOMPurify doesn't strip target="_blank"
        return DOMPurify.sanitize(marked.parse(text) as string, { ADD_ATTR: ['target'] });
    };

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

            <div className="flex space-x-2 mt-8 mb-4 border-b border-white/10 pb-2 overflow-x-auto">
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

            <div className="glass-panel p-8 overflow-x-auto markdown-body">
                {activeTab === 'readme' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.readme) }} />}
                {activeTab === 'plan' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.plan) }} />}
                {activeTab === 'statistics' && <div dangerouslySetInnerHTML={{ __html: parseMd(member.markdown?.statistics) }} />}
            </div>
        </div>
    );
};
