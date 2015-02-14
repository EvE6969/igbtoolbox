define(
  "igbtoolbox/about-ui",
  [
  "igbtoolbox/flightjs/define",
  "igbtoolbox/portal/nav-events"
  ],

  function(defineComponent, navEvents) {
    'use strict';


    return defineComponent([], {

      attributes: {
        navActivatedEventId: "nav_about_activated"
      },

      attached: function() {
        this._isActivated = false;

        this.trigger(navEvents.NEED_NAV_ITEM, new navEvents.NavItem("About", this.attr.navActivatedEventId));

        this.on(document, navEvents.NAV_ITEM_ACTIVATED, this._activated);
      },

      _activated: function(e, obj) {

        if(obj.eventId == this.attr.navActivatedEventId) {
          this.$node.show();
        } else {
          this.$node.hide();
        }
      }
    });
  }
);