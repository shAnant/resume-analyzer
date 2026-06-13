from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
)

def job_skills_and_frequency(jobDescription : list[str]):
    combined_job_descriptions = "\n\n".join(jobDescription)
    model = "gemini-2.5-flash"
    messages = f"""
                                            Analyze all the job descriptions.

                        Extract:
                        1. Technical skills only
                        2. Count how many job descriptions mention each skill

                        Rules:
                        - Merge equivalent skills
                        Example:
                            GCP -> Google Cloud Platform
                            ML -> Machine Learning
                        - Ignore soft skills
                        - Ignore company names
                        - Ignore job titles
                        - Return ONLY valid JSON
                        - Do not use markdown
                        - Do not wrap the response in ```json

                        The JSON MUST follow this exact schema:
                        
                                                    {{
                            "technical_skills": {{
                                "Machine Learning": 44,
                                "Artificial Intelligence": 24,
                                
                            }}
                            }}
                            Job Descriptions:
                    {combined_job_descriptions}
                """
    response = client.models.generate_content(
        model=model, contents=messages
    )
    try:
        cleaned = response.text.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

        data = json.loads(cleaned)

        return data

    except json.JSONDecodeError as e:
        return e
    
# jobDescription = ["OPPORTUNITY IS FOR IMMEDIATE JOINERS ONLY Job Title: Lead Analyst \u2013 Machine Learning Forecasting Job Locatio n: Noida Job Typ e: Full-Ti me Role Overview Seeking an experienc ed Assistant Manager \u2013 Machine Learning Forecast ing to lead advanced predictive modeling initiatives and drive strategic insights for business planning. This role requires strong expertise in statistical modeling, machine learning algorithms, and data engineering, combined with leadership skills to manage projects and men\u2026", "Job Title: Azure AI Engineer Location: Noida (Sector-132) Experience: 3 Years (Preferred immediate joiners) Job Description: We are seeking a talented and experienced Azure AI Engineer to join our innovative team. The ideal candidate will have a strong background in artificial intelligence, machine learning, and cloud computing, with expertise in implementing AI solutions on the Azure platform. You will play a key role in designing, developing, and deploying AI-driven applications to drive busi\u2026","About Turing: Based in San Francisco, California, Turing is the world\u2019s leading research accelerator for frontier AI labs and a trusted partner for global enterprises deploying advanced AI systems. Turing supports customers in two ways: first, by accelerating frontier research with high-quality data, advanced training pipelines, plus top AI researchers who specialize in coding, reasoning, STEM, multilinguality, multimodality, and agents; and second, by applying that expertise to help enterprise\u2026", "Data Architect-AI/ML Those who share our core belief of 'Every Day is Game Day' We bring our best selves to work each day to realize our mission of enriching the world through the power of digital commerce and financial services. ROLE PURPOSE We are looking for a highly skilled and motivated Data Architect-AI/ML with 10-15 years of experience to join our growing team. You will work with large payment datasets to uncover actionable insights, build predictive models, and contribute to strategic d\u2026","HCLTech is hiring Gen AI Engineer with GCP experience || Hyderabad/Bangalore/Noida/Chennai Summary: Overall Experience: 5 to 9 yrs CTC Range: 11 to 14 LPA Mandatory Skills: Gen AI, AI/ML, GCP, Big Query, Python. Location : Bangalore/Chennai/Noida/Hyderabad Notice Period : Immediate/30 days/60 days Job Summary Experience in designing & implementing solution in mentioned areas: Strong experience in developing AI/ML models on Google Cloud Platform Core Skills : TensorFl"]
    

# print(job_skills_and_frequency(jobDescription=jobDescription))