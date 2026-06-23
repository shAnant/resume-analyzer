from fastapi import FastAPI
from pydantic import BaseModel 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from python_modules.resumeParser import extract_text, extract_skil
from matching_model.ontology_matching import ontology_match
from matching_model.exact_matching import exact_match
from matching_model.semantic_matching import semantic_match
from python_modules.job_skills_extrtact import job_skills_and_frequency


app = FastAPI()


class CompareRequest(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]   

model=SentenceTransformer('all-MiniLM-L6-v2')

class SkillRequest(BaseModel):
    resume_path: str
    jobDescriptions: list[str]   



#This is the function for skill extraction from resume,job description. 
@app.post("/extract-skills")
async def extract_skills(data: SkillRequest):


    resume_skills = extract_skil(extract_text(data.resume_path))
    job_skills = job_skills_and_frequency(jobDescription=data.jobDescriptions)

    
    return {
        #resume_skills :- datatype :- list, example : ['python', 'machine learning']
        
        "resume_skills": resume_skills,
        "job_skills": job_skills 

        #job_skills :- datatype :- JSON, example : {'technical_skills'{'skill_1' : 3, 'skill_2' : 2}}
    }







#This is the comparison function .It'll give the score of the resume woth respect to diff job skills.
@app.post("/compare") 
async def  compare(data: CompareRequest):
    resume_skills=data.resume_skills
    job_skills=data.job_skills


    # ----------Exact Matching-----------
    exact_matched, exact_missing = exact_match(
        resume_skills,
        job_skills
    )



    # ----------Ontology Matching----------
    ontology_matched, ontology_missing = ontology_match(
        resume_skills,
        exact_missing
    )



    # ----------Semantic Matching----------
    semantic_matched, semantic_missing = semantic_match(
        resume_skills,
        ontology_missing
    )


    # -----------Final_score--------------
    hybrid_score=(len(exact_matched)+len(ontology_matched)+len(semantic_matched))/len(job_skills)*100;

    
    return {
        "exact_matches": exact_matched,
        "ontology_matches": ontology_matched,
        "semantic_matches": semantic_matched,
        "overall_score": hybrid_score,
        "missing": semantic_missing
    }




