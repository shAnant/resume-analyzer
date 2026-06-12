module.exports=function normalize(skill){
    
    return skill
        .toLowerCase()
        .replace(/[^\w\s]/g, "")
        .trim();
}