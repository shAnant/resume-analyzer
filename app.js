const express=require("express")
const axios=require("axios")
const upload=require("./config/multer_config");
require("dotenv").config();
const app=express();


app.set("view engine","ejs")

app.use(express.json())
app.use(express.urlencoded({extended:true}))

app.get("/",(req,res)=>{
    res.render("index");
})

app.post("/compare",upload.single("resume"),async function(req,res){

    //  role entered by the user
    const role=req.body.role;
    const resume_path=req.file.path;
    // console.log({role,resume});


    //  calling the adzuna API to get diff jobs.
    const response=await axios.get("https://api.adzuna.com/v1/api/jobs/in/search/1",
        {
            params:{
                
                app_id: process.env.ADZUNA_APP_ID, 
                app_key: process.env.ADZUNA_APP_KEY,
                what: role,
                results_per_page: 2
            }
    })

    const jobs=response.data.results;
    

    //  it'll have the job description only
    const jobDescriptions = jobs.map(job => job.description);
    
    
     try {

        //  calling the python service to extract the skills from resume,job description
        const python_response = await axios.post(
            "http://localhost:8000/extract-skills",
            {
                resume_path,
                jobDescriptions
            }
        );


        const { resume_skills, job_skills } = python_response.data;


        //  after extraction again calling the python service to give the final score
        const python_response2=await axios.post(
            "http://localhost:8000/compare",
                {
                    resume_skills,
                    job_skills
                }
        )
        res.send(python_response2.data)

    } catch(err) {
        console.log("Error:", err.message);
        console.log("Response:", err.response?.data);
        return res.status(500).send("Python service error");
    }
   
    
})

app.listen(3000)