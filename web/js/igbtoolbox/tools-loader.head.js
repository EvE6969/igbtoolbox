
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
