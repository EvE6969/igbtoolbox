define(
  "igbtoolbox/trustmanager-ui",
  [
  "jquery",
  "igbtoolbox/flightjs/define",
  "igbtoolbox/igb/ping-mixin",
  "igbtoolbox/igb/ping-events"
  ],

  function($, defineComponent, withPilot, pingEvents) {
    'use strict';


    return defineComponent(
      [withPilot],
      {

        attributes: {
          trustBtnSelector: ".btn-trustme"
        },

        attached: function() {

          this.onPilotChanged(this._checkPilot);

          this._checkPilot(null, this.getPilot());

          this.on(this.$node.find(this.attr.trustBtnSelector), 'click', this._requestTrust);

          this.$node.hide();
        },

        _checkPilot: function(e, pilot) {
          if(!pilot || !pilot.trusted) {
            console.debug("Trust flag not set for page, showing trust module");
            this.$node.show();
          } else {
            console.debug("Trust flag set");
            this.$node.hide();
          }
        },

        _requestTrust: function() {
          CCPEVE['requestTrust']('http://' + window.location.host);
          window.setTimeout("window.location.reload()", 10000);
          _gaq.push(['_trackEvent', 'Access', 'Trust Requested']);
        }

      }
    );

  }
);