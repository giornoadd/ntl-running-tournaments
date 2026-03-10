import React, { useState, useEffect, useRef } from 'react';
import { useHistory } from '../hooks/useCompetitionData';
import { Card } from '../components/ui/Card';
import { Table, TableRow, TableCell } from '../components/ui/Table';

export const HistoryPage: React.FC = () => {
    const [filter, setFilter] = useState('all');
    const { activities, loading } = useHistory(filter);
    const [displayCount, setDisplayCount] = useState(20);
    const observer = useRef<IntersectionObserver | null>(null);

    const loadMoreRef = React.useCallback((node: HTMLDivElement | null) => {
        if (loading) return;
        if (observer.current) observer.current.disconnect();
        observer.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && activities.length > displayCount) {
                setDisplayCount(prev => prev + 20);
            }
        });
        if (node) observer.current.observe(node);
    }, [loading, activities.length, displayCount]);

    useEffect(() => {
        setDisplayCount(20); // Reset pagination on filter change
    }, [filter]);

    if (loading) return <div className="p-10 text-center text-textMuted">Loading History...</div>;

    const visibleActivities = activities.slice(0, displayCount);

    return (
        <div className="fade-in">
            <div className="flex flex-wrap gap-2 mb-8 bg-black/40 backdrop-blur-md p-2 rounded-xl inline-flex border border-white/5">
                <button onClick={() => setFilter('all')} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'all' ? 'bg-accent text-white shadow-lg' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>All Quarters</button>
                <button onClick={() => setFilter('Q1')} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'Q1' ? 'bg-accent text-white shadow-lg' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>Q1</button>
                {/* Dynamically extract unique months */}
                {Array.from(new Set(activities.map(a => a.month))).map(month => (
                    <button key={month} onClick={() => setFilter(month)} className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === month ? 'bg-accent text-white shadow-lg' : 'text-textMuted hover:text-white hover:bg-white/5'}`}>
                        {month}
                    </button>
                ))}
            </div>

            <div className="timeline-container relative pl-0 md:pl-8 border-l-0 md:border-l-2 border-white/10 flex flex-col gap-10">
                {visibleActivities.map((day, idx) => (
                    <Card key={idx} className="relative !p-0 overflow-hidden">
                        <div className="absolute top-4 -left-[42px] w-5 h-5 rounded-full bg-accent border-4 border-background hidden md:block"></div>

                        <div className="bg-white/5 p-4 border-b border-white/10 flex justify-between items-center">
                            <h3 className="text-xl font-heading font-black">{day.date}</h3>
                            <span className="text-sm text-textMuted bg-black/40 px-3 py-1 rounded-full">{day.runners_list.length} Activities</span>
                        </div>

                        <div className="p-6">
                            <div className="grid grid-cols-2 gap-4 mb-6">
                                <div className="bg-mandaBg border border-manda/20 p-4 rounded-xl text-center">
                                    <div className="text-sm text-manda/80 mb-1">Mandalorian Daily</div>
                                    <div className="text-2xl font-bold text-manda">+{day.mando_daily.toFixed(2)} <span className="text-sm font-normal">km</span></div>
                                </div>
                                <div className="bg-itBg border border-it/20 p-4 rounded-xl text-center">
                                    <div className="text-sm text-it/80 mb-1">IT System Daily</div>
                                    <div className="text-2xl font-bold text-it">+{day.it_daily.toFixed(2)} <span className="text-sm font-normal">km</span></div>
                                </div>
                            </div>

                            <Table headers={["Runner", "Activity", "Distance", "Images"]}>
                                {day.runners_list.map((run, rIdx) => (
                                    <TableRow key={rIdx}>
                                        <TableCell>
                                            <strong>{run.name}</strong>
                                            <div className="text-xs text-textMuted mt-1">{run.team === 'Mandalorian' ? '🪖 Manda' : '💻 IT System'}</div>
                                        </TableCell>
                                        <TableCell>{run.distance.toFixed(2)} km</TableCell>
                                        <TableCell>
                                            <span className="bg-white/10 px-2 py-1 rounded text-xs">{run.activity || 'Run'}</span>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-2">
                                                {run.images?.slice(0, 3).map((img, i) => {
                                                    const cleanImg = img.startsWith('../member_results/') ? img.replace('../member_results/', '/member_results/') : img;
                                                    return (
                                                        <img key={i} src={cleanImg} className="w-8 h-8 rounded object-cover border border-white/20" alt="run" />
                                                    )
                                                })}
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </Table>

                            {/* Cumulative Teams */}
                            <div className="mt-6 flex justify-between text-sm text-textMuted px-2 py-3 bg-white/5 rounded-lg border border-white/10">
                                <div>Total: Manda <strong className="text-white">{day.mando_accum.toFixed(2)} km</strong></div>
                                <div>Total: IT <strong className="text-white">{day.it_accum.toFixed(2)} km</strong></div>
                            </div>
                        </div>
                    </Card>
                ))}

                {displayCount < activities.length && (
                    <div ref={loadMoreRef} className="py-8 text-center text-textMuted">
                        Loading more activities...
                    </div>
                )}
            </div>
        </div>
    );
};
