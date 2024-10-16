export interface UploadFileData {
    files: File[];
    jobDescription: File[];
    importance: Importance;
}

export type UploadFileContextType = {
    uploadFileData: UploadFileData;
    setUploadFileData: (uploadFileData: UploadFileData) => void;
}

export interface Importance {
    softSkill: number;
    technicalSkill: number;
    workExperience: number;
    education: number;
}

export interface resultOutput {
    education: number;
    workExperience: number;
    technicalSkill: number;
    softSkill: number;
    totalScore: number;
    cv: string;
    job_description: string;
}