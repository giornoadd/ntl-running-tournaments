import type { ICompetitionRepository, CompetitionData, Member, DailySummary } from '../../domain/models/types';
import { StaticCompetitionRepository } from '../../infrastructure/repositories/StaticCompetitionRepository';

export class CompetitionService {
    private repository: ICompetitionRepository;

    constructor(repository?: ICompetitionRepository) {
        // Dependency Injection default
        this.repository = repository || new StaticCompetitionRepository();
    }

    async getDashboardData(): Promise<CompetitionData> {
        return await this.repository.getCompetitionData();
    }

    async getRosterDetails(nickname: string): Promise<Member | undefined> {
        return await this.repository.getMemberByNickname(nickname);
    }

    async getHistory(month: string = 'all'): Promise<DailySummary[]> {
        return await this.repository.getActivitiesByMonth(month);
    }
}
