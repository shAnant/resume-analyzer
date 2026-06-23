const jwt=require("jsonwebtoken")
const user=require("../models/user-model")
const cookieParser = require("cookie-parser");
const express=require("express")

const app=express();
app.use(cookieParser());
module.exports=async function(req,res,next){
    if(!req.cookies.token){
        req.flash("error","you need to login first");
        return res.redirect("/");
    }
    try{
        let decoded=jwt.verify(req.cookies.token,process.env.JWT_KEY);
        // decoded will have both the fields i.e {email,pass}

        let curr_user=await user.findOne({email:decoded.email}).select("-pass")
        //this will deselect the pass field

        req.user=curr_user;
        next();
    }
    catch(err){
        req.flash("error","some error occurs.");
        res.redirect("/");
    }
}