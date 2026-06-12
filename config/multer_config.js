const multer=require("multer")
const path=require("path")
const crypto=require("crypto")




const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './public/pdfs')
  },
  // file contain all the data about the file
  filename: function (req, file, cb) {  
    crypto.randomBytes(12,function(err,byte){
        const fn=byte.toString("hex")+path.extname(file.originalname);
        cb(null, fn);
    })
    
  }
})



module.exports = multer({ storage: storage })