from fastapi import FastAPI
from pydantic import BaseModel 
from python_modules.resumeParser import extract_text, extract_skills
from python_modules.job_skills_extrtact import job_skills_and_frequency


app = FastAPI()

class ResumeRequest(BaseModel):
    resume_path : str
    jobDescription: list[str]

@app.post("/extract-skills")
async def extract_skills(data : ResumeRequest):
    
    resume_skills = extract_skills(extract_text(data.resume_path))
    
    job_skills = job_skills_and_frequency(jobDescription=data.jobDescription)

    # print(data)

    return {
        "resume_skills": resume_skills, #resume_skills :- datatype :- list, example : ['python', 'machine learning']
        "job_skills": job_skills  #job_skills :- datatype :- JSON, example : {'technical_skills'{'skill_1' : 3, 'skill_2' : 2}}
    }
    
    