export interface ResearchAssistant {
    user: number;
    research_goal: string;
    research_objective: string;
    research_parameters: string;
    report_format: string;
    uploaded_file?: string;
}

export class Platform {
    user: number = 0;
    finance: boolean = false;
    healthcare: boolean = false;
    technology: boolean = false;
    refresh_frequency: string = "";
}

export interface TrendingHeadline {
    trending_headlines: TrendingHeadlineItem[]
}

export interface TrendingHeadlineItem {
    title: string;
    url: string;
    image_url:string;
}