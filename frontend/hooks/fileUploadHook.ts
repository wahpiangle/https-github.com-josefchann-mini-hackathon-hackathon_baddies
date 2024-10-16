import { UploadFileData } from "@/@types/uploadFile";

export const uploadFile = async (uploadFileData: UploadFileData) => {
    const formData = new FormData();
    const multipleCVs = uploadFileData.files.length > 1 && uploadFileData.jobDescription.length === 1;
    if (multipleCVs) {
        uploadFileData.files.forEach((file) => {
            formData.append('cv_files', file);
        });
        uploadFileData.jobDescription.forEach((jobDescription) => {
            formData.append('jd_file', jobDescription);
        });
        formData.append('educationWeight', uploadFileData.importance.education.toString());
        formData.append('workExperienceWeight', uploadFileData.importance.workExperience.toString());
        formData.append('softSkillsWeight', uploadFileData.importance.softSkill.toString());
        formData.append('technicalSkillsWeight', uploadFileData.importance.technicalSkill.toString());

    } else {
        uploadFileData.files.forEach((file) => {
            formData.append('cv_file', file);
        });
        uploadFileData.jobDescription.forEach((jobDescription) => {
            formData.append('jd_files', jobDescription);
        });
        formData.append('educationWeight', uploadFileData.importance.education.toString());
        formData.append('workExperienceWeight', uploadFileData.importance.workExperience.toString());
        formData.append('softSkillsWeight', uploadFileData.importance.softSkill.toString());
        formData.append('technicalSkillsWeight', uploadFileData.importance.technicalSkill.toString());
    }

    const res = await fetch(
        uploadFileData.files.length > 1 && uploadFileData.jobDescription.length === 1
            ? "http://127.0.0.1:8000/analyze-cv/"
            : "http://127.0.0.1:8000/analyze-jds/", {
        method: 'POST',
        body: formData,
    });
    return await res.json();
};