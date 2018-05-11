var connect = require('connect')
var http = require('http')


var app = connect();

function doFirst(request, response, next) {
    console.log("Bacon")
    next()
}

function doSecond(request, response, next ) {
    console.log("Hot dog")
    next()
}

app.use(doFirst)
app.use(doSecond)

function profile (request, response) {
    console.log("User request profile")
    response.end()
}
function forum (request, response) {
    console.log("User request forum")
}



app.use("/profile", profile)
app.use("/forum", forum)

http.createServer(app).listen(8888)
console.log("Server is now running...")