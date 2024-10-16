from fastapi import FastAPI, File, Query, UploadFile
from spellingChecker import check_multiple_texts_concurrently
from pdfScrapper import calculateFinalScore, extract_text_from_pdf, analyze_cv_with_ollama, extract_sections, analyse_job_description_ollama, compare_sections
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to handle Job Description analysis
def jd_analyzer(jd):
    print("Running Job Description analysis...", flush=True)
    job_desc = analyse_job_description_ollama(jd)
    return job_desc

# Function to handle CV analysis
def cv_analyzer(text):
    print("Running CV analysis...", flush=True)
    ollama_analysis = analyze_cv_with_ollama(text)
    return ollama_analysis

# Function to extract text from a PDF
def extract_text(pdf_path):
    print("Extracting text from PDF...", flush=True)
    extracted_text = extract_text_from_pdf(pdf_path)
    return extracted_text

# Function to spell check extracted text
def spell_check(text):
    print("Checking spelling...", flush=True)
    checked_spelling = check_multiple_texts_concurrently([text])
    return checked_spelling

@app.post("/analyze-cv/")
async def analyze_cv(
    cv_files: list[UploadFile] = File(...),
    jd_file: UploadFile = File(...),
    educationWeight: float = Query(1.0),  # Default value is 1.0
    workExperienceWeight: float = Query(1.0),
    softSkillsWeight: float = Query(1.0),
    technicalSkillsWeight: float = Query(1.0)
):
    results = []
    # Step 1: Extract text from the Job Description file
    jd_path = f"./temp_jd_{jd_file.filename}"

    # Save the JD file temporarily
    with open(jd_path, "wb") as temp_file:
        temp_file.write(await jd_file.read())

    # Extract text from the JD file
    jd_extracted_text = extract_text(jd_path)

    # Run Job Description analysis
    jd_analysis_results = jd_analyzer(jd_extracted_text)

    # Extracting Job Description sections
    jd_sections = extract_sections(jd_analysis_results)

    for file in cv_files:
        # Step 2: Save each uploaded CV file temporarily
        cv_path = f"./temp_cv_{file.filename}"
        with open(cv_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Step 3: Extract text from the CV
        extracted_text = extract_text(cv_path)

        # Step 4: Perform spell check on the extracted text
        spelling_results = spell_check(extracted_text)

        # Step 5: Run CV analysis on the extracted text
        cv_analysis_results = cv_analyzer(extracted_text)

        # Step 6: Extracting CV sections
        cv_sections = extract_sections(cv_analysis_results)

        # Step 7: Comparing Sections
        scores = compare_sections(cv_sections, jd_sections)

        print(scores)

        educationScore = scores.get("Education", 0)
        workExperienceScore = scores.get("Work Experience", 0)
        technicalSkillsScore = scores.get("Technical Skills", 0)
        softSkillsScore = scores.get("Soft Skills", 0)

        totalScore = calculateFinalScore(educationScore, workExperienceScore, technicalSkillsScore, softSkillsScore, educationWeight, workExperienceWeight, technicalSkillsWeight, softSkillsWeight)

        # Collect the results for this file in the new format
        results.append({
            "cv": file.filename,
            "education": scores.get("Education", 0),
            "workExperience": scores.get("Work Experience", 0),
            "technicalSkill": scores.get("Technical Skills", 0),
            "softSkill": scores.get("Soft Skills", 0),
            "totalScore": totalScore
        })

        # Clean up the temporary CV file after processing
        os.remove(cv_path)

    # Clean up the temporary JD file after processing
    os.remove(jd_path)

    # Return the results for all files as a JSON response
    return results

@app.post("/analyze-jds/")
async def analyze_jds(
    jd_files: list[UploadFile] = File(...),
    cv_file: UploadFile = File(...)
):
    results = []

    # Step 1: Save and extract text from the CV file
    cv_path = f"./temp_cv_{cv_file.filename}"
    with open(cv_path, "wb") as temp_file:
        temp_file.write(await cv_file.read())

    # Extract text from the CV file
    extracted_text = extract_text(cv_path)

    # Step 2: Perform spell check on the extracted text
    spelling_results = spell_check(extracted_text)

    # Step 3: Run CV analysis on the extracted text
    cv_analysis_results = cv_analyzer(extracted_text)

    # Step 4: Extracting CV sections
    cv_sections = extract_sections(cv_analysis_results)

    for jd_file in jd_files:
        # Step 5: Save each uploaded JD file temporarily
        jd_path = f"./temp_jd_{jd_file.filename}"
        with open(jd_path, "wb") as temp_file:
            temp_file.write(await jd_file.read())

        # Step 6: Extract text from the JD
        jd_extracted_text = extract_text(jd_path)

        # Step 7: Run Job Description analysis
        jd_analysis_results = jd_analyzer(jd_extracted_text)

        # Step 8: Extracting Job Description sections
        jd_sections = extract_sections(jd_analysis_results)

        # Step 9: Comparing Sections
        scores = compare_sections(cv_sections, jd_sections)

        print(scores)

        # Collect the results for this JD in the new format
        results.append({
            "job_description": jd_file.filename,
            "education": scores.get("Education", 0),
            "workExperience": scores.get("Work Experience", 0),
            "technicalSkill": scores.get("Technical Skills", 0),
            "softSkill": scores.get("Soft Skills", 0)
        })

        # Clean up the temporary JD file after processing
        os.remove(jd_path)

    # Clean up the temporary CV file after processing
    os.remove(cv_path)

    # Return the results for all Job Descriptions as a JSON response
    return results

# Entry point to run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)