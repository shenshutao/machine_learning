var webdriverio = require('webdriverio');

var options = {
    desiredCapabilities: {
        browserName: 'firefox'
    }
};

webdriverio
    .remote(options)
    .init()
    .url('https://github.com/shenshutao')
    .getTitle().then(function (title) {
    console.log('Title was: ' + title);
}).end();