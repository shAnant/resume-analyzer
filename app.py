from fastapi import FastAPI
from pydantic import BaseModel 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from python_modules.resume_parser import extract_text, extract_skills
from python_modules.job_skills_extrtact import job_skills_and_frequency


app = FastAPI()


class CompareRequest(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]   

model=SentenceTransformer('all-MiniLM-L6-v2')

class SkillRequest(BaseModel):
    resume_path: str
    jobDescriptions: list[str]   



#This is the function for skill extraction from resume,job description. Currently returning the mannual output.
@app.post("/extract-skills")
async def extract_skills(data: SkillRequest):

    #enter your code here and return the output in similar way

    resume_skills = extract_skills(extract_text(data.resume_path))
    
    job_skills = job_skills_and_frequency(jobDescription=data.jobDescription)

    # print(data)

    return {
        "resume_skills": resume_skills, #resume_skills :- datatype :- list, example : ['python', 'machine learning']
        "job_skills": job_skills  #job_skills :- datatype :- JSON, example : {'technical_skills'{'skill_1' : 3, 'skill_2' : 2}}
    }





#This is the comparison function .It'll give the score of the resume woth respect to diff job skills.
#ontology model is still left, will do next
@app.post("/compare") 
async def  compare(data: CompareRequest):
    resume_skills=data.resume_skills
    job_skills=data.job_skills

    exact_matched = []
    exact_missing = []

    threshold = 0.75

    resume_set = set(resume_skills)

    # Exact Matching
    for job_skill in job_skills:

        if job_skill in resume_set:

            exact_matched.append({
                "skill": job_skill
            })

        else:

            exact_missing.append(job_skill)

    exact_score=(len(exact_matched)/len(job_skills))*100;



    
    # Semantic Matching
    semantic_matched=[]
    semantic_missing = []

    resume_embeddings = {
        skill: model.encode(skill)
        for skill in resume_skills
    }

    for job_skill in exact_missing:

        job_embedding = model.encode(job_skill)

        best_score = -1
        best_skill = None

        for resume_skill, resume_embedding in resume_embeddings.items():

            semantic_score = cosine_similarity(
                [job_embedding],
                [resume_embedding]
            )[0][0]

            if semantic_score > best_score:
                best_score = semantic_score
                best_skill = resume_skill

        if best_score >= threshold:

            semantic_matched.append({
                "job_skill": job_skill,
                "resume_skill": best_skill,
                "score": round(float(best_score), 4)
            })

        else:

            semantic_missing.append(job_skill)

    semantic_score=len(semantic_matched)/len(job_skills)*100;
    hybrid_score=semantic_score+exact_score;

    
    return {
        "exact_matches": exact_matched,
        "exact_score": exact_score,

        "semantic_matches": semantic_matched,
        "semantic_score": semantic_score,

        "combined_score": hybrid_score,

        "missing": semantic_missing
    }




