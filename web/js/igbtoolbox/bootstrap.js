
define(
  function(require) {
    'use strict';

    bootstrap();

    /**
     * Global entry function trigged by window load event.
     */
    function bootstrap() {

      var $ = require("jquery");

      $.ajax('/api/account/capabilities').done(function(resp) {

        if(resp['data'] === undefined) {
          throw new Error('Could not get capabilities');
          return;
        }

        // create pilot object from response
        var perm = {};
        if(resp['data']['capabilities']) {
          perm = resp['data']['capabilities'];
        }

        var Pilot = require("igbtoolbox/igb/pilot");

        var pilot = null;
        if(resp['data']['pilot']) {
          pilot = new Pilot(resp['data']['pilot'], perm);
        }

        // user agent is IGB?
        var igb = resp['data']['igb'] === true;

        // logged in?
        var isLoggedIn = false;

        // global xhr headers
        if (typeof eveintel == 'undefined') { eveintel = {}; }
        eveintel.EI_OVERRIDE_HEADERS = { };

        if(pilot) {
          var authUser = pilot.authUser;
          if(authUser) {
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_CHARID'] = pilot.characterId;
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_CHARNAME'] = pilot.characterName;
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_CORPID'] = pilot.corpId;
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_CORPNAME'] = pilot.corpName;
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_ALLIANCEID'] = pilot.allianceId;
            eveintel.EI_OVERRIDE_HEADERS['EVE_RUNAS_ALLIANCENAME'] = pilot.allianceName;
            if(!igb) {
              eveintel.EI_OVERRIDE_HEADERS['EVE_SHIPTYPEID'] = 670;
            }
          }

          isLoggedIn = authUser != undefined;
        }

        // send xhrf cookie with each ajax request
        function getCookie(name) {
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
        }

        var xsrf = getCookie("_xsrf");
        if(xsrf) {
          eveintel.EI_OVERRIDE_HEADERS['X-XSRFToken'] = xsrf;
        }

        //eveintel.singleton = {};

        if(pilot) {
          _gaq.push(['_trackEvent', 'Access', 'Alliance', pilot.allianceName]);
          _gaq.push(['_trackEvent', 'Access', 'Corp', pilot.corpName]);
        }

        var permAttrs = {permissions: perm, loggedIn: isLoggedIn, igb: igb};

        if(igb) {
          // ping toggle button
          //var pingUI = require("igbtoolbox/ping-ui");
          //pingUI.attachTo('m_ping');

          // create ping sender with pilot
          var pingSender = require("igbtoolbox/igb/ping-sender");
          pingSender.attachTo(document, {pingPilot: pilot, pingEnable: true});
        }

        // global notification widgets
        var errorUI = require("igbtoolbox/portal/error-ui");
        errorUI.attachTo('#m_errors');

        var messagesUI = require("igbtoolbox/portal/messages-ui");
        messagesUI.attachTo('#m_messages');

        // nav controller handle requests from modules to add items to primary navigation
        var navUI = require("igbtoolbox/portal/nav-ui");
        navUI.attachTo('#m_navbar');

        // sockjs connection
        var messagebus = require("igbtoolbox/messagebus/messagebus");
        messagebus.attachTo(document, {messageBusPilot: pilot});

        // trust notification
        if(igb) {
          var trustmanagerUI = require("igbtoolbox/trustmanager-ui");
          trustmanagerUI.attachTo('#m_trustmanager', {pilot: pilot});
        }

        // constantly update timestamp durations
        var timestampsUI = require("igbtoolbox/portal/timestamps-ui");
        timestampsUI.attachTo(document);

        // trigger event for all module specific bootstrap functions
        var bootstrapEvents = require("igbtoolbox/bootstrap-events");
        $(document).triggerHandler(bootstrapEvents.PILOT_RECEIVED, pilot);

        var toolsLoader = require("igbtoolbox/tools-loader");
        toolsLoader.attachTo(document, {permissions: perm, pilot: pilot});

        // about page controller - should be last page
        var aboutUI = require("igbtoolbox/about-ui");
        aboutUI.attachTo('#pageAbout');

      });

    };

  }
);
