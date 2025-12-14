export enum ConferenceStatus {
    IDEES = "Idées",
    CONTACTE = "Contacté",
    PLANIFIE = "Planifié",
    BLOQUE = "Bloqué",
    FEEDBACK = "Feedback",
    TERMINE = "Terminé"
}

export enum ConferenceLevel {
    EASY = "easy",
    MID = "mid",
    EXPERT = "expert"
}

export interface Conference {
    id?: number;
    title: string;
    status: ConferenceStatus;
    assignee?: string;
    date?: string;
    link_doc?: string;
    address?: string;
    level?: ConferenceLevel;
}
