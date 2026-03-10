import { useState, useEffect } from 'react';
import type { Member, DailySummary, CompetitionData } from '../../domain/models/types';
import { CompetitionService } from '../../application/services/CompetitionService';

const service = new CompetitionService();

export function useCompetitionData() {
    const [data, setData] = useState<CompetitionData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        service.getDashboardData()
            .then(d => {
                setData(d);
                setLoading(false);
            })
            .catch(e => {
                setError(e);
                setLoading(false);
            });
    }, []);

    return { data, loading, error };
}

export function useRosterDetail(nickname: string | undefined) {
    const [member, setMember] = useState<Member | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!nickname) return;
        setLoading(true);
        service.getRosterDetails(nickname)
            .then(m => {
                setMember(m || null);
                setLoading(false);
            });
    }, [nickname]);

    return { member, loading };
}

export function useHistory(monthFilter: string = 'all') {
    const [activities, setActivities] = useState<DailySummary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        service.getHistory(monthFilter)
            .then(items => {
                setActivities(items);
                setLoading(false);
            });
    }, [monthFilter]);

    return { activities, loading };
}
