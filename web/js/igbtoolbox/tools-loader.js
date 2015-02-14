
define(
  "igbtoolbox/tools-loader",
  [
  'igbtoolbox/flightjs/define',
  'igbtoolbox/authzsimple/permission-mixin'
  ],
  function(defineComponent, withPermission) {
    'use strict';

    return defineComponent(
      [withPermission],
    {

      attributes: {
        permissions: null, // set by parent
        pilot: null
      },

      attached: function() {

this.withPermission("signatures", function() {
  var pageController = require("igbtoolbox/signatures/page-controller");
  pageController.attachTo("#pageSignature");
});
this.withPermission("signatures", function() {
  var pageController = require("igbtoolbox/signatures/page-controller");
  pageController.attachTo("#pageSignature");
});
var proximityTracker = require("igbtoolbox/spatial/proximity-tracker");
proximityTracker.attachTo(document);


      }

    });
});