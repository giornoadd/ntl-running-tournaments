import React from 'react';
import { useCompetitionData } from '../hooks/useCompetitionData';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Table, TableRow, TableCell } from '../components/ui/Table';

export const StandingsPage: React.FC = () => {
    const { data, loading, error } = useCompetitionData();

    if (loading) return <div className="text-center p-10 text-textMuted">Loading Standings...</div>;
    if (error || !data) return <div className="text-center p-10 text-red-500">Error Loading Data</div>;

    const mandoDist = data.teams["Mandalorian"].total_distance;
    const itDist = data.teams["IT System"].total_distance;
    const totalDist = mandoDist + itDist;
    const mandoPct = totalDist > 0 ? (mandoDist / totalDist) * 100 : 50;
    const itPct = totalDist > 0 ? (itDist / totalDist) * 100 : 50;
    const leadingTeam = mandoDist >= itDist ? "Mandalorian" : "IT System";

    const top5 = [...data.roster].sort((a, b) => b.total_distance - a.total_distance).slice(0, 5);

    return (
        <div className="flex flex-col gap-8 fade-in">
            {/* Team Battle Head to Head */}
            <Card>
                <h2 className="text-xl font-heading mb-6">🏆 Current Leaders: <span className="text-accent">{leadingTeam}</span></h2>
                <div className="flex justify-between items-end mb-2 px-2">
                    <div className="text-left">
                        <div className="text-3xl font-black text-manda">{mandoDist.toFixed(2)} <span className="text-lg font-normal">km</span></div>
                        <div className="text-sm text-textMuted">🪖 Mandalorian</div>
                    </div>
                    <div className="text-right">
                        <div className="text-3xl font-black text-it">{itDist.toFixed(2)} <span className="text-lg font-normal">km</span></div>
                        <div className="text-sm text-textMuted">💻 IT System</div>
                    </div>
                </div>

                <div className="w-full h-8 bg-black/40 rounded-full flex overflow-hidden border border-white/10 relative">
                    <div className="h-full bg-manda/20 transition-all duration-1000 flex items-center px-4" style={{ width: `${mandoPct}%`, boxShadow: '0 0 20px rgba(0,255,136,0.3) inset' }}></div>
                    <div className="h-full bg-it/20 transition-all duration-1000 flex items-center px-4 justify-end" style={{ width: `${itPct}%`, boxShadow: '0 0 20px rgba(0,204,255,0.3) inset' }}></div>
                    <div className="absolute top-0 bottom-0 left-1/2 w-0.5 bg-white/20 z-10"></div>
                </div>
            </Card>

            {/* Top 5 Runners */}
            <Card>
                <h2 className="text-xl font-heading mb-4">⭐ Top 5 Ranked Players</h2>
                <Table headers={["Rank", "Runner", "Team", "Distance", "Active"]}>
                    {top5.map((r, i) => (
                        <TableRow key={r.nickname}>
                            <TableCell className="font-bold">{i === 0 ? '🥇 1' : i === 1 ? '🥈 2' : i === 2 ? '🥉 3' : i + 1}</TableCell>
                            <TableCell>
                                <strong>{r.nickname}</strong> <span className="opacity-50 text-sm">({r.thai_name})</span>
                            </TableCell>
                            <TableCell><Badge team={r.team}>{r.team}</Badge></TableCell>
                            <TableCell>{r.total_distance.toFixed(2)} km</TableCell>
                            <TableCell>{r.active_days} d</TableCell>
                        </TableRow>
                    ))}
                </Table>
            </Card>
        </div>
    );
};
