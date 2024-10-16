import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Importance, UploadFileContextType } from "@/@types/uploadFile"
import FileUpload from "./ui/FileUpload"
import { useContext } from "react"
import { UploadFileContext } from "@/context/uploadFileContext"

const JobDescriptionUploadCard = (
) => {
    const { uploadFileData, setUploadFileData } = useContext(UploadFileContext) as UploadFileContextType;
    const handleSliderChange = (value: number, key: string) => {
        setImportance({
            ...uploadFileData.importance,
            [key]: value
        })
    }
    const handleJobDescriptionUploaded = (files: File[]) => {
        setJobDescription(files)
    }
    const setImportance = (importance: Importance) => setUploadFileData({ ...uploadFileData, importance })
    const setJobDescription = (jobDescription: File[]) => {
        setUploadFileData({
            ...uploadFileData,
            jobDescription
        })
    }

    return (
        <Card className="flex-1">
            <CardHeader>
                <CardTitle>Enter the job description here</CardTitle>
                <CardDescription></CardDescription>
            </CardHeader>
            <CardContent className="flex gap-2 flex-col">
                <FileUpload
                    onFilesUploaded={handleJobDescriptionUploaded}
                    uploadMode={
                        uploadFileData.files &&
                            uploadFileData.files.length > 1 ? "single" : "multi"
                    }
                    files={uploadFileData.jobDescription}
                    setFiles={setJobDescription}
                    defaultText="Upload the Job Description files here"
                />
                {
                    !(uploadFileData.jobDescription.length > 1) && (
                        <>
                            <p className="my-2">Rate the importance of the following:</p>
                            {Object.entries(uploadFileData.importance).map(([key, importanceValue]) => (
                                <div key={key}>
                                    <Label className="capitalize">
                                        {key.replace(/([A-Z])/g, ' $1').trim()} {importanceValue}
                                    </Label>
                                    <Slider
                                        defaultValue={[importanceValue]}
                                        max={10}
                                        step={1}
                                        id={key}
                                        onValueChange={(value) => handleSliderChange(value[0], key)}
                                    />
                                </div>
                            ))}
                        </>
                    )
                }
            </CardContent>
            <CardFooter>
                <p></p>
            </CardFooter>
        </Card>
    )
}

export default JobDescriptionUploadCard