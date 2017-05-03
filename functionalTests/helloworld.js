module.exports = {
  'Hello World Test' : function (browser) {
    browser
      .url('http://localhost:5000/helloworld')
      .waitForElementVisible('body', 1000)
      .assert.containsText('body', 'Hello World')
      .end();
  }
};
