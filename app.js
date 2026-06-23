const express=require("express")
const axios=require("axios")
const upload=require("./config/multer-config");
const app=express();
const path=require("path")
const cookieParser = require("cookie-parser");
const isloggedin=require("./middlewares/isLoggedIn")
const {generateUser,loginUser,logoutUser}=require("./controllers/authController")
const {fetchJobs}=require("./services/adzunaAPI");
const { extractSkills, compareSkills } = require("./services/pythonService");
const session=require("express-session")
const flash=require("connect-flash")
require("dotenv").config();

app.use(session({
    secret:"resume-analyzer-secret",
    resave:false,
    saveUninitialized:false
    })
);

app.use(flash());
app.use(cookieParser())
app.use(express.static(path.join(__dirname,"public")));
app.set("view engine","ejs")
app.use(express.json())
app.use(express.urlencoded({extended:true}))


app.get("/",(req,res)=>{
    res.render("auth");
})

app.post("/create",generateUser)
app.post("/login",loginUser)
app.post("/logout",logoutUser)

app.get("/home",(req,res)=>{
    const result = req.session.analysisResult || {};

    res.render("index", {
        resume_skills: result.resume_skills || null,
        technicalSkills: result.technicalSkills || null,
        final_output: result.final_output || null
    });
})

app.post("/compare",isloggedin,upload.single("resume"),async function(req,res){

    //  role entered by the user
    const role=req.body.role;
    const resume_path=req.file.path;

    // saving the resume inside the database
    req.user.resume=resume_path
    await req.user.save();

    //  calling the adzuna API to get diff jobs.
    const jobs=await fetchJobs(role);
    const jobDescriptions = jobs.map(job => job.description);
    //  it'll have the job description only


     try {

        //  calling the python service to extract the skills from resume,job description
        const { resume_skills, job_skills } =await extractSkills(resume_path,jobDescriptions);

        const technicalSkills = Object.keys(
            job_skills.technical_skills
        );


        //  after extraction again calling the python service to give the final score
        const final_output=await compareSkills(resume_skills,technicalSkills);

        req.session.analysisResult = {
            resume_skills,
            technicalSkills,
            final_output
        };

        res.redirect("/home");

    } catch(err) {

        return res.status(500).send("Python service error");
    }
   
    
})

app.listen(3000)