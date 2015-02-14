define(
  "igbtoolbox/iframe-ui",
  [
  "igbtoolbox/flightjs/define"
  ],

  function(defineComponent) {
    'use strict';

    return defineComponent([], {

      attributes: {
        iframeSrc: 'javascript:""',
        iframeStyle: 'border:0;vertical-align:bottom;',
        iframeWidth: '100%',
        iframeHeight: '100%'
      },

      attached: function() {

        this.$node.append('iframe')
          .attr('frameborder', 0)
          .attr('style', this.iframeStyle)
          .attr('src': this.attr.iframeSrc)
          .attr('width', this.attr.iframeWidth)
          .attr('height', this.attr.iframeHeight);
      }

    });

});