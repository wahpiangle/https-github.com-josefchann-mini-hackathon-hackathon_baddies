"use client";
import { UploadFileContextType, UploadFileData } from "@/@types/uploadFile";
import React from "react";

export const UploadFileContext = React.createContext<UploadFileContextType | null>(null);

export const UploadFileProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [uploadFileData, setUploadFileData] = React.useState<UploadFileData>({
        files: [],
        jobDescription: [],
        importance: {
            softSkill: 10,
            technicalSkill: 10,
            workExperience: 10,
            education: 10,
        },
    });
    return (
        <UploadFileContext.Provider value={{ uploadFileData, setUploadFileData }}>
            {children}
        </UploadFileContext.Provider>
    )
};

