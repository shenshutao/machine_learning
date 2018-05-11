var request = require('request');
const cheerio = require('cheerio')
var fs = require('fs')

// path = require('path')
// certFile = path.resolve(__dirname, 'ssl/LFSolutions.crt')

var request = request.defaults({jar: true})

var options = {
    url: 'https://107.170.168.107/users/sign_in',
    // cert: fs.readFileSync(certFile),
    rejectUnauthorized: false
};

// request.get(options, function (error, response, body) {
//     if (error) {
//         console.log("Error: ", error.message)
//     } else if (!error && response.statusCode == 200) {
//         $ = cheerio.load(body); // load the page
//
//         console.log($('input[name="authenticity_token"]').val());
//         console.log($('input[name="utf8"]').val());
//         console.log($('input[name="commit"]').val());
//         console.log($('#new_user').attr('action'));
//
//         var authTokenVal = $('input[name="authenticity_token"]').val();
//         var utf8Val = $('input[name="utf8"]').val();
//         var commitVal = $('input[name="commit"]').val();
//
//         var actionVal = $('#new_user').attr('action');
//
//         var username = 'shutao@sofeene.com.sg';
//         var password = 'shutao123';


// request.post('https://107.170.168.107' + actionVal,
//     {
//         rejectUnauthorized: false, form: {
//         'utf8': utf8Val, 'authenticity_token': authTokenVal,
//         'user[email]': username, 'user[password]': password, 'user[remember_me]': '0', 'commit': 'Sign in'
//     }
//     },
//     function optionalCallback(err, httpResponse, body) {
//         if (err) {
//             return console.error('Error:', err);
//         }
//         console.log('Body: ', body);
//         var cookie = httpResponse.headers['set-cookie'];
//         // var cookie = cookie.toString().split(";").indexOf(1);
//         console.log(cookie)

require('request').debug = true
request.get('https://107.170.168.107/indents?commit=Search&page=2&q%5Bbuyer_name_cont%5D=&q%5Bcreater_id_eq%5D=&q%5Bindent_date_gteq%5D=01-01-2012&q%5Bindent_date_lteq%5D=31-12-2012&q%5Bindent_no_cont%5D=&q%5Bproduct_category_id_eq%5D=&q%5Brequester_id_eq%5D=&q%5Bsalesman_office_id_eq%5D=&q%5Bstatus_eq%5D=&q%5Bsupplier_code_cont%5D=&q%5Bsupplier_name_cont%5D=&q%5Buser_id_eq%5D=&utf8=%E2%9C%93', {
    rejectUnauthorized: false,
    header: {
        Host: '107.170.168.107',
        Connection: 'keep-alive',
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        Accept: 'image/webp,image/apng,image/*,*/*;q=0.8',
        Referer: 'https://107.170.168.107/indents?commit=Search&page=2&q%5Bbuyer_name_cont%5D=&q%5Bcreater_id_eq%5D=&q%5Bindent_date_gteq%5D=01-01-2012&q%5Bindent_date_lteq%5D=31-12-2012&q%5Bindent_no_cont%5D=&q%5Bproduct_category_id_eq%5D=&q%5Brequester_id_eq%5D=&q%5Bsalesman_office_id_eq%5D=&q%5Bstatus_eq%5D=&q%5Bsupplier_code_cont%5D=&q%5Bsupplier_name_cont%5D=&q%5Buser_id_eq%5D=&utf8=%E2%9C%93',
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        Cookie: '_sofeene_app_session=BAh7CEkiD3Nlc3Npb25faWQGOgZFRkkiJWNiNGU4YTYwYWFjZTUxYjdiZGM3NzE4ZTlhMGZlNTdhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMW5HYmtmdlBNV25rNDAzQmRDdHFjWXpLTUVOMEhMU2E4WWl1WWhNWStDZ0k9BjsARkkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsISSIJVXNlcgY7AEZbBmlHSSIiJDJhJDEwJElVQmhDTE81Qkc5N0JBSUNPV2NNL2UGOwBU--c440c98c08b4da53c9fcc6344a22532de067b125'
    }
}, function (error, response, body) {
    if (error) {
        console.log("Error: ", error.message)
    } else if (!error && response.statusCode == 200) {
        $ = cheerio.load(body); // load the page
        console.log('Body: ', body);
    }
});
// Cookie:_sofeene_app_session=BAh7CEkiD3Nlc3Npb25faWQGOgZFRkkiJWNiNGU4YTYwYWFjZTUxYjdiZGM3NzE4ZTlhMGZlNTdhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMW5HYmtmdlBNV25rNDAzQmRDdHFjWXpLTUVOMEhMU2E4WWl1WWhNWStDZ0k9BjsARkkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsISSIJVXNlcgY7AEZbBmlHSSIiJDJhJDEwJElVQmhDTE81Qkc5N0JBSUNPV2NNL2UGOwBU--c440c98c08b4da53c9fcc6344a22532de067b125
// Host:107.170.168.107
// Referer:https://107.170.168.107/indents?commit=Search&page=2&q%5Bbuyer_name_cont%5D=&q%5Bcreater_id_eq%5D=&q%5Bindent_date_gteq%5D=01-01-2012&q%5Bindent_date_lteq%5D=31-12-2012&q%5Bindent_no_cont%5D=&q%5Bproduct_category_id_eq%5D=&q%5Brequester_id_eq%5D=&q%5Bsalesman_office_id_eq%5D=&q%5Bstatus_eq%5D=&q%5Bsupplier_code_cont%5D=&q%5Bsupplier_name_cont%5D=&q%5Buser_id_eq%5D=&utf8=%E2%9C%93
//     User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36