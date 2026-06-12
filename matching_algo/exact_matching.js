const normalise = require("../preprocessing/normalise");

module.exports=function(resume_set,job_skills){

    const matched=[];
    const missing=[];

    for(const skill of job_skills){
        const normalise_skill=normalise(skill)
        if(resume_set.has(normalise_skill)){

            matched.push(normalise_skill);

        }
        else{

            missing.push(normalise_skill);

        }

    }

    return {matched,missing};
}