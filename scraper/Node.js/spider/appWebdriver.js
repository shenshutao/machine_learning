var webdriverio = require('webdriverio');

var options = {
    desiredCapabilities: {
        browserName: 'firefox',
        acceptInsecureCerts: true,
        // "moz:firefoxOptions": {"binary": "/home/ato/src/gecko/obj-x86_64-pc-linux-gnu/dist/bin/firefox",
        "log": {"level": "info"}
    }
};
webdriverio
    .remote(options)
    .init()
    .url('https://107.170.168.107/users/sign_in')

    .setValue('#user_email', 'shutao@sofeene.com.sg')

    .setValue('#user_password', 'shutao123')
    .click(name = "commit")
    .getTitle().then(function (title) {
    console.log('Title was: ' + title);
}).end();