import type { CompetitionData, ICompetitionRepository, Member, DailySummary } from '../../domain/models/types';

// Declare the global variable injected by data.js
declare global {
    interface Window {
        COMPETITION_DATA?: CompetitionData;
    }
}

export class StaticCompetitionRepository implements ICompetitionRepository {

    async getCompetitionData(): Promise<CompetitionData> {
        // In a real app, this would be a fetch() call.
        // Here, we wait for the globally injected COMPETITION_DATA from data.js
        return new Promise((resolve, reject) => {
            if (window.COMPETITION_DATA) {
                resolve(window.COMPETITION_DATA);
            } else {
                // Poll briefly in case scripts loaded out of order
                let retries = 0;
                const interval = setInterval(() => {
                    if (window.COMPETITION_DATA) {
                        clearInterval(interval);
                        resolve(window.COMPETITION_DATA);
                    }
                    retries++;
                    if (retries > 10) {
                        clearInterval(interval);
                        reject(new Error("COMPETITION_DATA not found. Make sure data.js is loaded."));
                    }
                }, 100);
            }
        });
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
