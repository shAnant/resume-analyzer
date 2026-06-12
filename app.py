from fastapi import FastAPI

app = FastAPI()

@app.post("/extract-skills")
async def extract_skills():

    # print(data)

    return {
        "resume_skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "nodejs"
        ],
        "job_skills": [
            "Python",
            "Docker",
            "AWS",
            "Node.js"
        ]
    }