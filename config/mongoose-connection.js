const mg=require("mongoose")
const dbgr=require("debug")("development:mongoose")
const config=require("config");
mg
.connect(`${config.get("MONGODB_URI")}/resume_analyzer`)
.then(function(){
    dbgr("succeeded")
})
.catch(function(err){
    dbgr(err)
})

module.exports=mg.connection;