import re
import os
import subprocess
import docx
from embedder import convertToVector, produceSimilarityResult
from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    
    # Debugging: Show raw file path
    print(f"File path: '{pdf_path}'")
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    
    # Get file name and extension
    file_name, file_extension = os.path.splitext(pdf_path.strip())
    
    # Debugging: Show extracted file name and extension
    print(f"File name: {file_name}")
    print(f"File extension: '{file_extension}'")
    
    if not file_extension:
        print("File extension is empty or invalid.")
        return
    
    text = ''
    
    if file_extension == '.pdf':
        text = extract_text(pdf_path).strip()
                
    elif file_extension == '.docx':
        print("Processing DOCX file...")  # Debugging
        doc = docx.Document(pdf_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Only PDF and DOCX are supported.")
    
    #  Clean up the text:
    cleaned_text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single one
    # cleaned_text = re.sub(r'(?<![.!?])\n(?![.!?])', ' ', cleaned_text)  # Remove newlines splitting sentences
    cleaned_text = re.sub(r'[|•●]', '\n', cleaned_text)  # Replace '•', '●', and '|' with new lines
    
    return cleaned_text

# Step 2: Analyze CV and organize into sections using Ollama
def analyze_cv_with_ollama(cv_text):
    prompt = f"""

    Organize the following CV into 4 clear sections:
    - Education
    - Work Experience
    - Technical Skills
    - Soft Skills

    Take the following CV and simplify detailed phrases or technical descriptions into more general terms. For example, if the CV says 'Applied Object-Oriented Programming principles to create structured architectures,' simplify that to 'Object-Oriented Programming.' Similarly, if it says 'Led the frontend team in designing the UI,' simplify that to 'Frontend design leadership.' Maintain the same structure of the CV but replace detailed or technical phrases with simpler, more generalized terms. Under the Work Experience section, you should calculate the number of experience years based on their oldest work experience year, and display this number. It should also be written without any + for the content. For example,
    **Work Experience**

    2 years work experience
    * Marketing and Communications Intern, Blueskeye AI (Nottingham, UK) (July 2024 – Aug 2024)
    Frontend design leadership
    Project management
    SEO and digital marketing knowledge

    * Software Engineering Intern, NHS Nottingham University Hospitals (Nottingham, UK) (Nov 2023 – May 2024)
    Led frontend team in designing UI
    Applied Object-Oriented Programming principles
    Utilized multiple testing libraries for backend and frontend testing

    * Software Engineering Intern, VaazMe (Kuala Lumpur, Malaysia) (Sept 2022 – June 2023)
    Developed proficiency in Software Development Lifecycle using Scrum methodology
    Contributed to modern tech stack with Spring Boot and React.js

    
    Also, under the Technical Skills and Soft Skills section should just be the skills separated like commas. For example, 
    **Technical Skills**

    HTML, CSS, JavaScript, Python, Java, C, React.js, Spring Boot, Flutter
    Here's the CV:

    {cv_text}

    """
    
    command = ['ollama', 'run', 'llama3.1', prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    
    return result.stdout

def extract_sections(text):
    # Regular expression to match section titles (text surrounded by two asterisks)
    section_pattern = r'\*\*(.*?)\*\*'

    # Split the text into sections based on the section titles
    sections = re.split(section_pattern, text)

    # Dictionary to store section titles and their corresponding content
    organized_sections = {}

    # Loop through the sections list.
    # Sections with even indexes (0, 2, 4...) are content, odd indexes (1, 3, 5...) are section titles.
    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        section_content = sections[i + 1].strip() if i + 1 < len(sections) else ''

        # Replace consecutive newlines with a single newline
        section_content = re.sub(r'\n\s*\n', '\n', section_content)

        # Replace bullet points, tabs, and plus signs with commas
        section_content = section_content.replace(' * ', ',').replace('\t', ',').replace(' + ', '')
        
        # Replace the Unicode en dash with a regular dash
        section_content = section_content.replace('\u2013', '-')

        section_content = section_content.replace('---', "")
        
        # Replace newlines with spaces and remove any extra spaces
        section_content = section_content.replace('\n', ' ').replace('  ', ' ').strip()

        # Ensure there are no trailing commas
        section_content = section_content.strip(', ')

        # Add the cleaned-up section to the dictionary
        organized_sections[section_title] = section_content

    # Convert the dictionary to a JSON object
    # json_object = json.dumps(organized_sections, indent=4)

    return organized_sections

def analyse_job_description_ollama(cv_text):
    prompt = f"""

    Organize the following job description into only 4 clear sections:
    - Education
    - Work Experience
    - Technical Skills
    - Soft Skills

    Take the following Job Description and simplify detailed phrases or technical descriptions into more general terms. For example, if the Job Description says 'Applied Object-Oriented Programming principles to create structured architectures,' simplify that to 'Object-Oriented Programming.' Similarly, if it says 'Led the frontend team in designing the UI,' simplify that to 'Frontend design leadership.' Maintain the same structure of the Job Description but replace detailed or technical phrases with simpler, more generalized terms. Under the Work Experience section, you should display the number of experience years that the job description requires. If there is no information, then write ---. Same for the Education section, if there is no information, write ---. For example,

    **Work Experience**

    2 years work experience

    and if there are no work experience requirements, write --- like below:
    
    **Work Experience**

    ---

    
    Also, under the Technical Skills and Soft Skills section should just be the skills separated like commas. For example, 
    **Technical Skills**

    HTML, CSS, JavaScript, Python, Java, C, React.js, Spring Boot, Flutter
    Here's the CV:

    {cv_text}

    """
    
    command = ['ollama', 'run', 'llama3.1', prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    
    return result.stdout

# Function to compare each section of the CV and job description
def compare_sections(cv_data, job_description_data):
    scores = {}

    # Compare each section individually
    for section in cv_data:
        if section in job_description_data:  # Ensure both have the same sections
            cv_text = cv_data[section]
            job_desc_text = job_description_data[section]

            cv_text_vector = convertToVector(cv_text)
            job_desc_text_vector = convertToVector(job_desc_text)

            score = produceSimilarityResult(cv_text_vector, job_desc_text_vector)
            scores[section] = score

    return scores

def calculateFinalScore(educationScore, workExperienceScore, technicalSkillsScore, softSkillsScore, 
                        educationWeight, workExperienceWeight, technicalSkillsWeight, softSkillsWeight):
    # Normalize the weights so that the total sum of weights is 1
    total_weight = educationWeight + workExperienceWeight + technicalSkillsWeight + softSkillsWeight
    
    if total_weight == 0:
        return 0  # To prevent division by zero if all weights are zero

    # Calculate weighted scores
    weighted_education = (educationScore * educationWeight) / total_weight
    weighted_work_experience = (workExperienceScore * workExperienceWeight) / total_weight
    weighted_technical_skills = (technicalSkillsScore * technicalSkillsWeight) / total_weight
    weighted_soft_skills = (softSkillsScore * softSkillsWeight) / total_weight

    # Sum the weighted scores
    total_score = weighted_education + weighted_work_experience + weighted_technical_skills + weighted_soft_skills

    # Normalize to a 100-point scale
    final_score = total_score

    return final_score

sampleJobDescription = """
Personal Attributes & Experience

Proficient in JavaScript, Typescript, React + Hooks, NodeJs, HTML5 and SASS/CSS
Experience with Redux/Context or similar state management libraries
Experience with Jest, Cypress and React Testing Library or similar tools/frameworks
Knowledge of UX/UI design
Proficient in Git source control
Knowledge of Linting and formatting tools
Prior experience working in an Agile Environment
Strong analytical and problem-solving skills, with an affinity for logically and structurally breaking down complex problems
Good communication skills, both verbal and written, with the ability to work well with different stakeholders

"""

# Example usage:
# pdf_path = '/Users/nigelseah/Desktop/hackathon-prep/sampleCVs/Nigel Resume.pdf'
# pdf_path = '../sampleCVs/Mary - Account Specialist - Resume.pdf'
# pdf_path = '../sampleCVs/CV_XYZ.pdf'

# # 1. Extract text from the PDF
# raw_text = extract_text_from_pdf(pdf_path)
# print(raw_text)

# filtered = initial_extraction(raw_text)
# print(filtered)

# # 2. Analyze the CV and organize into sections using Ollama
# cv_analysis = analyze_cv_with_ollama(raw_text)
# cv_analysis = analyze_cv_with_gpt4(raw_text)
# print(cv_analysis)

# 3. Analyse job description
# job_analysis = analyse_job_description_ollama(sampleJobDescription)
# job_analysis = analyse_job_description_gpt4o(sampleJobDescription)
# print(job_analysis)

# 4. Extract sections from the analyzed job description and CV
# cv_sections = extract_sections(cv_analysis)
# print(cv_sections)
# cv_sections = extract_sections(cv_analysis)
# print(cv_sections)
# job_sections = extract_sections(job_analysis)
# # print(job_sections)

# # 5. Embed the CV and job description sections into a JSON object
# # Get similarity scores for each section
# section_scores = compare_sections(cv_sections, job_sections)
# # 5. Embed the CV and job description sections into a JSON object
# # Get similarity scores for each section
# section_scores = compare_sections(cv_sections, job_sections)

# # Print the section-wise scores
# for section, score in section_scores.items():
#     print(f"{section} similarity score: {score}")
# # Print the section-wise scores
# for section, score in section_scores.items():
#     print(f"{section} similarity score: {score}")

# # 6. Calculate the final score
# educationWeight = 0.1
# workExperienceWeight = 0.4
# technicalSkillsWeight = 0.3
# softSkillsWeight = 0.2

# educationScore = section_scores.get("Education", 0)
# workExperienceScore = section_scores.get("Work Experience", 0)
# technicalSkillsScore = section_scores.get("Technical Skills", 0)
# softSkillsScore = section_scores.get("Soft Skills", 0)

# final_score = calculateFinalScore(educationScore, workExperienceScore, technicalSkillsScore, softSkillsScore,
#                                     educationWeight, workExperienceWeight, technicalSkillsWeight, softSkillsWeight)

# print(f"Final score: {final_score}")