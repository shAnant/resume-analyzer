const mongoose=require("mongoose")

mongoose.connect("mongodb://127.0.0.1:27017/resume-analyzer")

const userSchema=new mongoose.Schema({
    fullname:{
        type:String,
        required:true
    },
    email:{
        type:String,
        required:true
    },
    pass:{
        type:String,
        required:true
    },
    resume:{
        type:String,
        default:null
    }
})

module.exports=mongoose.model("user",userSchema)