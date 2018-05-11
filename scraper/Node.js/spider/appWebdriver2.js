var webdriverio = require('webdriverio');
var describe = require('describe');

var options = {
    desiredCapabilities: {
        browserName: 'firefox',
        acceptInsecureCerts: true,
        // "moz:firefoxOptions": {"binary": "/home/ato/src/gecko/obj-x86_64-pc-linux-gnu/dist/bin/firefox",
        "log": {"level": "debug"}
    }
};

describe('webdriver.io page', function() {
    it('should have the right title', function () {
        // browser.set
        console.log('1');
        browser.remote(options);
        browser.url('https://107.170.168.107/users/sign_in');
        console.log('2');
        var title = browser.getTitle();
        console.log('3');
        assert.equal(title, 'WebdriverIO - WebDriver bindings for Node.js');
    });
});