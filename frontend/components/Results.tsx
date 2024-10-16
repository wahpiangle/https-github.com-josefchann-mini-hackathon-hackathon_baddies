import { ReloadIcon } from '@radix-ui/react-icons';
import React from 'react'
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
import { resultOutput } from '@/@types/uploadFile';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';

export default function Results({ data, resetMutation }: {
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

    return (
        <div className="flex items-center justify-center h-full flex-col gap-2">
            <h1>
                Single Job Description with multiple CVs
            </h1>
            <div className='flex'>
                <ChartContainer config={chartConfig} className='min-h-[400px] min-w-[1000px]'>
                    <BarChart accessibilityLayer data={data}>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="cv"
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
                <div>
                    <h1 className="underline text-xl mb-4">Ranking of CV Uploaded based on job description</h1>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="text-left">Rank</TableHead>
                                <TableHead className="text-left">CV</TableHead>
                                <TableHead className="text-left">Total Score</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data
                                .sort((a, b) => b.totalScore - a.totalScore)
                                .map((cv, index) => (
                                    <TableRow key={cv.cv}>
                                        <TableCell>{index + 1}</TableCell>
                                        <TableCell>{cv.cv}</TableCell>
                                        <TableCell className="text-gray-500">
                                            {parseFloat(cv.totalScore.toFixed(2))}
                                        </TableCell>
                                    </TableRow>
                                ))}
                        </TableBody>
                    </Table>
                </div>
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
