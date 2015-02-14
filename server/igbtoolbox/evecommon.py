import logging, os, platform
import tornado.web
import bson
from authn_simple import access
from igbtoolbox import settings
from igbtoolbox.model import Pilot


try:
    import simplejson
except ImportError:
    import json as simplejson



#===============================================================================
# Basic functionality and classes used across modules.
#===============================================================================


class AbstractPage(tornado.web.RequestHandler):
    """Abstract base class with some convinience methods"""


    # database accessors

    @property
    def _eve_db(self):
      return self.settings['db_global']

    @property
    def _domain_db(self):
      return self.settings['db_domain']

    @property
    def _kill_db(self):
      return self.settings['db_kill']


    def _send_json_response(self, retValue=None, errMsg=None):
        """Provides json encoded response document"""

        ret = {}
        if retValue != None: ret['data'] = retValue
        if errMsg != None: ret['error'] = errMsg

        #self.set_header("Content-Type", "text/plain")
        self.set_header("Content-Type", "application/json")

        #self.write(tornado.escape.json_encode(ret))
        self.write(simplejson.dumps(ret, cls=EnhancedEncoder))
        self.finish()


    def _send_plain_response(self, retValue=None, errMsg=None):
        """Sends plain text, unencoded response document"""

        self.set_header("Content-Type", "text/plain")

        s = ''
        if errMsg: s = errMsg
        elif retValue: s = retValue

        self.write(s)
        self.finish()


    @property
    def _pilot(self):
        """Provides a cached instance of the current value by calling get_pilot"""

        if not hasattr(self, '__pilot'):
            self.__pilot = self.get_pilot(self.request)
        return self.__pilot

    @staticmethod
    def get_pilot(request, pilot=None):
        """Gets instance of current pilot"""

        ret = pilot or Pilot(request)
        ret.allowed = access.is_pilot_allowed(ret)
        agent = request.headers.get('User-Agent')
        ret.igb = agent and agent.find('EVE-IGB') != -1
        return ret



class EnhancedEncoder(simplejson.JSONEncoder):
    """Handles some special objects during encoding"""

    def default(self, obj):

        if hasattr(obj, 'isoformat'):
            # encode datetime instance as iso string
            return obj.isoformat()
        if hasattr(obj, 'to_json_dict'):
            # use special method for custom models
            return obj.to_json_dict()
        elif type(obj) == bson.ObjectId:
            return None
        else:
            return simplejson.JSONEncoder.default(self, obj)
