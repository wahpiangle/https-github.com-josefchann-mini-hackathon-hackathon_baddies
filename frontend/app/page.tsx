'use client';
import { resultOutput, UploadFileContextType } from "@/@types/uploadFile";
import FileUploadCard from "@/components/FileUploadCard";
import JobDescriptionUploadCard from "@/components/JobDescriptionUploadCard";
import Results from "@/components/Results";
import ResultsMultipleJd from "@/components/ResultsMultipleJd";
import { Button } from "@/components/ui/button"
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { UploadFileContext } from "@/context/uploadFileContext";
import { uploadFile } from "@/hooks/fileUploadHook";
import { useToast } from "@/hooks/use-toast";
import { useMutation } from "@tanstack/react-query";
import { useContext } from "react";

export default function Home() {
  const { uploadFileData, setUploadFileData } = useContext(UploadFileContext) as UploadFileContextType;
  const { toast } = useToast();
  const mutation = useMutation({
    mutationFn: uploadFile,
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
      });
    },
  });


  if (mutation.isPending) {
    return (
      <div className="flex items-center justify-center h-full">
        <LoadingSpinner className="text-white" />
      </div>
    );
  }

  if (mutation.data && !mutation.isError) {
    const data = mutation.data as resultOutput[];
    return (
      (uploadFileData.jobDescription.length === 1
        ?
        <Results data={data} resetMutation={mutation.reset} />
        :
        <ResultsMultipleJd data={data} resetMutation={mutation.reset} />
      )
    );
  };

  const handleUpload = () => {
    if (uploadFileData.files.length === 0 || uploadFileData.jobDescription.length === 0) {
      toast({
        title: "Error",
        description: "Please upload files",
        variant: "destructive",
      });
      return;
    }
    mutation.mutate(uploadFileData);
  };


  return (
    <>
      <div className="flex justify-between w-full gap-8">
        <JobDescriptionUploadCard />
        <FileUploadCard />
      </div>
      <Button onClick={handleUpload}>
        Upload
      </Button>
    </>
  );
}
