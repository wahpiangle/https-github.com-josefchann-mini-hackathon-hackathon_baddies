import { ReloadIcon } from '@radix-ui/react-icons';
import React, { useContext } from 'react'
import { Button } from './ui/button';
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
    ChartConfig,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"
import { resultOutput, UploadFileContextType } from '@/@types/uploadFile';
import { UploadFileContext } from '@/context/uploadFileContext';

export default function ResultsMultipleJd({ data, resetMutation }: {
    data: resultOutput[],
    resetMutation: () => void
}) {
    const chartConfig = {
        education: {
            label: "Education",
            color: "#4285F4",
        },
        workExperience: {
            label: "Work Experience",
            color: "#34A853",
        },
        technicalSkill: {
            label: "Technical Skill",
            color: "#FBBC05",
        },
        softSkill: {
            label: "Soft Skill",
            color: "#EA4335",
        },
    } satisfies ChartConfig
    const { uploadFileData, setUploadFileData } = useContext(UploadFileContext) as UploadFileContextType;
    return (
        <div className="flex items-center justify-center h-full flex-col gap-2">
            <h1>
                Multiple Job Descriptions with single CV for {uploadFileData.files[0].name}
            </h1>
            <div className='flex gap-4'>
                <ChartContainer config={chartConfig} className='min-h-[500px] min-w-[1000px]'>
                    <BarChart accessibilityLayer data={data} className='border border-white'>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="job_description"
                            tickMargin={10}
                        />
                        <ChartTooltip
                            content={<ChartTooltipContent indicator="dashed" />}
                        />
                        <YAxis
                            domain={[0, 100]}
                        />
                        <ChartLegend content={<ChartLegendContent />} />
                        <Bar dataKey="education" fill={chartConfig.education.color} radius={4} />
                        <Bar dataKey="workExperience" fill={chartConfig.workExperience.color} radius={4} />
                        <Bar dataKey="technicalSkill" fill={chartConfig.technicalSkill.color} radius={4} />
                        <Bar dataKey="softSkill" fill={chartConfig.softSkill.color} radius={4} />
                    </BarChart>
                </ChartContainer>
            </div>

            <Button onClick={() => {
                resetMutation()
            }}>
                <ReloadIcon className="mr-2" />
                Upload again
            </Button>
        </div>
    )
}
