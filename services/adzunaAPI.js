const axios = require("axios");

async function fetchJobs(role) {
    const response = await axios.get(
        "https://api.adzuna.com/v1/api/jobs/in/search/1",
        {
            params: {
                app_id: process.env.ADZUNA_APP_ID,
                app_key: process.env.ADZUNA_APP_KEY,
                what: role,
                results_per_page: 2
            }
        }
    );

    return response.data.results;
}

module.exports = { fetchJobs };