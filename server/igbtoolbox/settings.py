import os, yaml, logging, shutil
import motor

__settings_path = os.path.join(os.environ['HOME'], ".igbtoolbox.yml")
__settings_template_path = os.path.join(os.path.dirname(__file__), "..", "..", "settings_template.yml")

def __load_settings(fname):
    """Loads settings from yaml file at provided path"""
    if os.path.isfile(fname):
      logging.debug('Loading yaml settings file: %s' % fname)
      with open(fname, 'r') as fd:
        return list(yaml.load_all(fd))
    else:

      logging.debug("Settings not found at %s, copying template %s -> %s" % (fname, __settings_template_path, fname))
      shutil.copyfile(__settings_template_path, fname)
      return __load_settings(fname)


__settings = {}

MONGODB_DATABASE_DOMAIN = None
MONGODB_DATABASE_EVEKILL = None
MONGODB_DATABASE_GLOBAL = None

DEBUG = None

def load_settings():
    global __settings
    __settings = __load_settings(__settings_path)

    global MONGODB_DATABASE_DOMAIN
    global MONGODB_DATABASE_EVEKILL
    global MONGODB_DATABASE_GLOBAL
    MONGODB_DATABASE_DOMAIN = get_settings("mongodb")["db_domain"]
    MONGODB_DATABASE_EVEKILL = get_settings("mongodb")["db_evekill"]
    MONGODB_DATABASE_GLOBAL = get_settings("mongodb")["db_global"]

    global DEBUG
    DEBUG = get_settings("server").get("debug", False)

    logging.debug("Loaded settings: %s" % __settings)

def get_settings(configKey):
    """Returns settings for a given key found at top level of yml file, e.g. 'access'"""
    for section in __settings:
        for k in section.keys():
            if k == configKey: return section[k]


def get_mongodb_client(db=None):
    """Returns MongoDB driver client for configured server"""
    cl = motor.MotorClient(get_settings("mongodb")["host"], get_settings("mongodb")["port"])
    if db: return cl[db]
    else: return cl
