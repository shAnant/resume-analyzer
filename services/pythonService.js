const axios = require("axios");

async function extractSkills(resume_path, jobDescriptions) {

    const response = await axios.post(
        "http://localhost:8000/extract-skills",
        {
            resume_path,
            jobDescriptions
        }
    );

    return response.data;
}

async function compareSkills(resume_skills, job_skills) {

    const response = await axios.post(
        "http://localhost:8000/compare",
        {
            resume_skills,
            job_skills
        }
    );

    return response.data;
}

module.exports = {
    extractSkills,
    compareSkills
};