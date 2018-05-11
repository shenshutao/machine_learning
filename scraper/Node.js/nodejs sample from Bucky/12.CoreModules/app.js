var fs = require('fs')
fs.writeFileSync("corn.txt", "Corn is good")

console.log(fs.readFileSync("corn.txt").toString());

var path = require('path')
var websiteName = "./Desktop/Bucky//website/index.html"
var websiteAbout = "./Desktop/Bucky/website/../website/about.html"

console.log(path.normalize(websiteName))
console.log(path.normalize(websiteAbout))
console.log(path.dirname(websiteName))
console.log(path.basename(websiteName))
console.log(path.extname(websiteName))



setInterval(function () {
    console.log('Hello')
}, 2000)


console.log(__dirname)
console.log(__filename)