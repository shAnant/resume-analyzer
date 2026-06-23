
const jwt=require("jsonwebtoken")
const bcrypt=require("bcrypt")
const user=require("../models/user-model")
const generateToken=require("../utils/generateToken")
const express=require("express")
const router=express();

router.use(express.json());
router.use(express.urlencoded({extended:true}))

module.exports.generateUser=async function(req,res){
    try{
                let {fullname,email,pass}=req.body;
                
                let curr_user=await user.findOne({email});
                if(curr_user) return res.send(curr_user)

                bcrypt.genSalt(10,function(err,salt){
                    bcrypt.hash(pass,salt,async function(err,hash){
                        let createdUser=await user.create({
                            fullname,
                            email,
                            pass:hash
                        })
                        let token=generateToken(createdUser);
                        res.cookie("token",token).redirect("/home");
                    })
                })            
            }
            catch(err){
                res.redirect("/");
            }
}

module.exports.loginUser=async function(req,res){
    let {email,pass}=req.body;
    let curr_user=await user.findOne({email:email});

    if(!curr_user) {
        req.flash("error","create user first.")
        return res.redirect("/");
    }

    bcrypt.compare(pass,curr_user.pass,function(err,result){
        try{
            if(!result) return res.send("something is wrong");
            

            let token=generateToken(curr_user);

            res.cookie("token",token).redirect("/home");
        }
        catch(err){
            res.send("someting is wrong check")
        }
    })

}

module.exports.logoutUser=function(req,res){
    res.cookie("token","").redirect("/");
}