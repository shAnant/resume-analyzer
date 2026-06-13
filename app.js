const express=require("express")
const axios=require("axios")
const upload=require("./config/multer_config");
require("dotenv").config();
const app=express();
const exact_matching=require("./matching_algo/exact_matching");
const normalise=require("./preprocessing/normalise")


app.set("view engine","ejs")

app.use(express.json())
app.use(express.urlencoded({extended:true}))

app.get("/",(req,res)=>{
    res.render("index");
})

app.post("/compare",upload.single("resume"),async function(req,res){
    const role=req.body.role;
    const resume=req.file;
    // console.log({role,resume});

    // const response=await axios.get("https://api.adzuna.com/v1/api/jobs/in/search/1",
    //     {
    //         params:{
                
    //             app_id: process.env.ADZUNA_APP_ID, 
    //             app_key: process.env.ADZUNA_APP_KEY,
    //             what: role,
    //             results_per_page: 2
    //         }
    // })

    // const jobs=response.data.results;
    
    // const jobDescriptions = jobs.map(job => job.description);
    

    const python_response=await axios.post(
    "http://localhost:8000/extract-skills",
    // {
    //     resume: resume,
    //     jobDescriptions: jobDescriptions
    // }
    );

    const {resume_skills,job_skills}=python_response.data;



    const resume_set=new Set(
        resume_skills.map(normalise)
    );

    const {matched,missing}=exact_matching(resume_set,job_skills);
    const matched_percentage=(matched.length/job_skills.length)*100;

    res.json({matched_percentage,matched,missing});
})



app.listen(3000)