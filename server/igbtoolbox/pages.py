import os, logging
import tornado.web
import tornado.auth
from igbtoolbox import evecommon, settings
from authn_simple.access import pilot_allowed



class MainPage(evecommon.AbstractPage):
    """Main page for IGB toolbox (single page app)"""

    def get(self):

        logging.debug('Headers: %s' % self.request.headers)

        agent = self.request.headers.get('User-Agent')
        isigb = agent and agent.find('EVE-IGB') != -1

        cfgServer = settings.get_settings('server')
        ga = cfgServer.get('ga-account')

        self.render("main.html", debug=settings.DEBUG, igb=isigb, ei_pilot=self._pilot,
            ei_module_templates=self.application.settings['module_templates'], ga_account=ga)


