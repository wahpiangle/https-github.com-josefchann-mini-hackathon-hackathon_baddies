import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import FileUpload from "./ui/FileUpload"
import { useContext } from "react";
import { UploadFileContextType } from "@/@types/uploadFile";
import { UploadFileContext } from "@/context/uploadFileContext";

export default function FileUploadCard(
) {
    const { uploadFileData, setUploadFileData } = useContext(UploadFileContext) as UploadFileContextType;
    const setFiles = (files: File[]) => {
        setUploadFileData({ ...uploadFileData, files })
    }
    const handleFilesUploaded = (files: File[]) => {
        setUploadFileData({
            ...uploadFileData,
            files
        })
    }
    return (
        <Card className="flex-1">
            <CardHeader>
                <CardTitle>Upload your CV(s) here</CardTitle>
                <CardDescription></CardDescription>
            </CardHeader>
            <CardContent>
                <FileUpload
                    onFilesUploaded={handleFilesUploaded}
                    uploadMode={
                        uploadFileData.jobDescription &&
                            uploadFileData.jobDescription.length > 1 ? "single" : "multi"
                    }
                    files={uploadFileData.files}
                    setFiles={setFiles}
                    defaultText="Upload the CV(s) here"
                />
            </CardContent>
            <CardFooter>
                <p></p>
            </CardFooter>
        </Card>
    )
}
