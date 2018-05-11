var request = require('request');
const cheerio = require('cheerio')


request('https://github.com/shenshutao', function (error, response, body) {
    if (!error && response.statusCode == 200) {
        $ = cheerio.load(body); // load the page

        $('.repo').each(function () {
            console.log($(this).text());
        });
    }
});