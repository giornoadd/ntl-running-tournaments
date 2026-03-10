import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCompetitionData } from '../hooks/useCompetitionData';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const RosterPage: React.FC = () => {
    const { data, loading } = useCompetitionData();
    const navigate = useNavigate();
    const [filter, setFilter] = useState<'all' | 'Mandalorian' | 'IT System'>('all');

    if (loading || !data) return <div className="text-center p-10 text-textMuted">Loading Roster...</div>;

    const filteredRoster = data.roster.filter(r => filter === 'all' || r.team === filter);

    return (
        <div className="fade-in">
            {/* Filter Bar */}
            <div className="flex flex-wrap gap-2 mb-8 bg-black/40 backdrop-blur-md p-2 rounded-xl inline-flex border border-white/5">
                <button onClick={() => setFilter('all')} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'all' ? 'bg-accent text-white shadow-lg' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>
                    All Members
                </button>
                <button onClick={() => setFilter('Mandalorian')} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'Mandalorian' ? 'bg-manda text-black shadow-lg shadow-manda/20' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>
                    🪖 Mandalorian
                </button>
                <button onClick={() => setFilter('IT System')} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'IT System' ? 'bg-it text-black shadow-lg shadow-it/20' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>
                    💻 IT System
                </button>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredRoster.map(r => {
                    const isManda = r.team === 'Mandalorian';
                    return (
                        <Card key={r.nickname} onClick={() => navigate(`/roster/${encodeURIComponent(r.nickname)}`)} className={`flex flex-col h-full border-t-4 ${isManda ? 'border-t-manda' : 'border-t-it'}`}>
                            <div className="flex justify-between items-start w-full">
                                <div>
                                    <div className="text-xl font-semibold">{r.nickname}</div>
                                    <div className="text-sm text-textMuted">{r.thai_name}</div>
                                </div>
                                <Badge team={r.team}>{isManda ? '🪖' : '💻'}</Badge>
                            </div>

                            <div className="grid grid-cols-2 w-full mt-4 text-sm">
                                <div>📝 Active: <strong className="text-textMain">{r.active_days} d</strong></div>
                                <div className="text-right">🏃 Dist: <strong className="text-accent">{r.total_distance.toFixed(2)} km</strong></div>
                            </div>

                            {r.stats_details?.longest_run_dist && (
                                <div className="text-xs text-textMuted mt-4 opacity-80">
                                    🏅 Longest: {r.stats_details.longest_run_dist} km
                                </div>
                            )}

                            {r.recent_images?.length > 0 && (
                                <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
                                    {r.recent_images.slice(0, 4).map((img, i) => {
                                        const cleanImg = img.startsWith('../member_results/') ? img.replace('../member_results/', '/member_results/') : img;
                                        return (
                                            <img key={i} src={cleanImg} alt="Run evidence" className="w-[40px] h-[40px] rounded-lg object-cover border border-white/10" />
                                        )
                                    })}
                                </div>
                            )}
                        </Card>
                    );
                })}
            </div>
        </div>
    );
};
