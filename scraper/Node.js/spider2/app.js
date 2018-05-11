var express = require('express');
var app = express();
const cheerio = require('cheerio')


app.get('/', function(req, res){
    var request = require('request');
    request('http://www.jikexueyuan.com', function (error, response, body) {
      if(!error && response.statusCode==200 ) {
        // console.log(body); // Print the HTML for the Google homepage.
          $ = cheerio.load(body); // Get the Dom obj

          res.json (
              {
                  'Class Name' : $('.aside-allCategory .bd li').length
              }
          )


    }});

});

app.listen(3000);