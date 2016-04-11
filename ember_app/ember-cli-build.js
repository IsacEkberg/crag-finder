/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    /*sassOptions: {
        includePaths: [
          'vendor/tim/sass'
        ]
      }*/
    // Add options here
  });

  //Vendor JS:
  app.import('vendor/tim/js/bootstrap.min.js');
  app.import('vendor/tim/js/bootstrap-datepicker.js');
  app.import('vendor/tim/js/nouislider.min.js');
  app.import('vendor/tim/js/material.min.js');
  //app.import('vendor/tim/js/material-kit.js');
  //app.import('vendor/tim/js/jquery.min.js');

  app.import('vendor/tim/css/bootstrap.min.css');
  app.import('vendor/tim/css/demo.css');

  app.import('bower_components/font-awesome/css/font-awesome.min.css');
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.woff', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.woff2', {destDir: 'fonts'});
  app.import('bower_components/font-awesome/fonts/fontawesome-webfont.ttf', {destDir: 'fonts'});


  app.import('bower_components/jquery-ui/jquery-ui.js');
  // Use `app.import` to add additional libraries to the generated
  // output files.
  //
  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  return app.toTree();
};
