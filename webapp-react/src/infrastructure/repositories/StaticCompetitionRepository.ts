import type { CompetitionData, ICompetitionRepository, Member, DailySummary } from '../../domain/models/types';

// Declare the global variable injected by data.js
declare global {
    interface Window {
        COMPETITION_DATA?: CompetitionData;
    }
}

export class StaticCompetitionRepository implements ICompetitionRepository {

    async getCompetitionData(): Promise<CompetitionData> {
        // Fetch data.json dynamically at runtime from the public directory.
        // Vite will route this from base URL.
        const basePath = import.meta.env.BASE_URL || '/';
        const dataUrl = `${basePath.endsWith('/') ? basePath : basePath + '/'}data.json`;
        
        try {
            const response = await fetch(dataUrl);
            if (!response.ok) {
                throw new Error(`Failed to fetch data.json: ${response.statusText}`);
            }
            const data: CompetitionData = await response.json();
            return data;
        } catch (error) {
            console.error("Error fetching competition data:", error);
            throw error;
        }
    }

    async getMemberByNickname(nickname: string): Promise<Member | undefined> {
        const data = await this.getCompetitionData();
        return data.roster.find(m => m.nickname.toLowerCase() === nickname.toLowerCase());
    }

    async getActivitiesByMonth(monthFilter: string): Promise<DailySummary[]> {
        const data = await this.getCompetitionData();
        if (monthFilter === 'all') {
            return data.activities;
        } else if (monthFilter === 'Q1') {
            return data.activities.filter(a =>
                a.month.includes('Jan') ||
                a.month.includes('Feb') ||
                a.month.includes('Mar')
            );
        }
        return data.activities.filter(a => a.month === monthFilter);
    }
}
