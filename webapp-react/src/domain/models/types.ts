export interface RunnerImage {
    url: string;
}

export interface Activity {
    name: string;
    distance: number;
    team: string;
    activity?: string;
    images: string[];
}

export interface DailySummary {
    date: string;
    month: string;
    runners_list: Activity[];
    mando_daily: number;
    it_daily: number;
    mando_accum: number;
    it_accum: number;
    mando_avg: number;
    it_avg: number;
}

export interface MemberStats {
    "Total Distance"?: string;
    "Active Days"?: string;
    "Average / Session"?: string;
    "Best Session"?: string;
    "Best Pace"?: string | null;
    "Longest Run"?: string | null;
    best_pace?: number;
    longest_run_dist?: number;
}

export interface MemberMarkdown {
    readme: string;
    statistics: string;
    plan: string;
    coach_analysis: string;
}

export interface Member {
    nickname: string;
    thai_name: string;
    team: 'Mandalorian' | 'IT System';
    total_distance: number;
    active_days: number;
    image_count: number;
    recent_images: string[];
    stats_details: MemberStats;
    markdown: MemberMarkdown;
    daily_dates?: string[];
}

export interface TeamStats {
    name: string;
    total_distance: number;
    members: number;
    active_members: number;
    avg_distance: number;
}

export interface CompetitionData {
    last_updated: string;
    teams: {
        "Mandalorian": TeamStats;
        "IT System": TeamStats;
    };
    roster: Member[];
    activities: DailySummary[];
}

export interface ICompetitionRepository {
    getCompetitionData(): Promise<CompetitionData>;
    getMemberByNickname(nickname: string): Promise<Member | undefined>;
    getActivitiesByMonth(monthFilter: string): Promise<DailySummary[]>;
}
