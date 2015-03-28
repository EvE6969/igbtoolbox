#!/usr/bin/python

import logging.handlers, os, getopt, sys, signal, importlib, pathlib, json
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import tornado.web
import tornado.httpserver
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import sockjs.tornado
import motor
from igbtoolbox import settings, universe


# list of imported modules (modulename, mod)
_importedModules = []

# tornado scheduler instance
_scheduler = None

# tornado templates registered by modules
_module_templates = []


def __detectModules(dirpath):
    """Detects modules from all subdirectories of provided directory"""
    mdirpath = pathlib.Path(dirpath)
    # find all subdirectories
    emods = [ mdir.name for mdir in mdirpath.iterdir() if mdir.is_dir() ]
    # add valid server python dirs to list
    spaths = []
    for mod in emods:

        # read bower.json and get module type
        isIgbModule = False
        bowerFile = pathlib.Path(mdirpath, mod, "bower.json")
        if bowerFile.is_file():
            with bowerFile.open() as f:
                bj = json.load(f)
                isIgbModule = "igbtoolbox" in bj.get("moduleType", [])

        if not isIgbModule: continue

        logging.debug("Adding module '%s'" % mod)
        # require server directory for python code
        ps = pathlib.Path(mdirpath, mod, "server")
        if not ps.is_dir():
            logging.debug("%s: server directory required in case you want to run python code" % ps)
        else:
            spaths.append((mod, ps))

    # first add all modules python code to path
    for mod, serverpath in spaths:
        sys.path.append(str(serverpath))

    # import web.py from modules
    for mod, serverpath in spaths:
        # find web.py and import as python module (will register all the server side stuff for module)
        for web in serverpath.glob("**/web.py"):
            sp = ".".join(web.relative_to(serverpath).parts)
            sp = sp[:-3] # truncate .py

            _importedModules.append(__importModule(sp))


def __importModule(n):
    """imports a specified module using importlib"""

    try: return (n, importlib.import_module(n))
    except ImportError as e:
      logging.exception(e)
      logging.debug("Python path: %s" % sys.path)
      return (n, None)


def _onHupSignal(sig, func=None):
    logging.debug("Exit handler triggered")

    for n, m in _importedModules:
        if not m: continue
        if hasattr(m, 'onHupSignal'):
            m.onHupSignal()

def _onTermSignal(sig, func=None):
    logging.debug("Exit sigterm handler triggered")

    for n, m in _importedModules:
        if not m: continue
        if hasattr(m, 'onTermSignal'):
            m.onTermSignal()

    tornado.ioloop.IOLoop.instance().stop()

    _scheduler.shutdown()


def usage():
    print("""
Starts EVE toolbox server

Options:
   --port              Port number
   --module            Modules directory
   --debug             Run in debug mode
""")


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [ "port=", "modules=", "help", "debug"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)


    port = None
    modulesdir = None
    debug = None

    for o, a in opts:

        if o == "--help":
            usage()
            sys.exit()

        elif o == "--port":
            port = a

        elif o == "--modules":
            modulesdir = a

        elif o == "--debug":
            debug = True

    # load settings once and periodically afterwards
    settings.load_settings()
    if debug != None: settings.DEBUG = True
    if settings.DEBUG: logging.debug("Server running in debug mode")
    cfgServer = settings.get_settings('server')

    # port number if not specified
    if port == None: port = cfgServer.get('port', 8080)

    # write pid file
    fd = open('/var/tmp/tornado-%s.pid' % port, "w")
    fd.write(str(os.getpid()))
    fd.close()

    # init logging
    logging.getLogger().setLevel(logging.DEBUG)
    if not settings.DEBUG:
        logging.getLogger().addHandler(logging.handlers.SysLogHandler('/dev/log', logging.handlers.SysLogHandler.LOG_LOCAL6))

    # disable asyncio spam
    logging.getLogger('asyncio').setLevel(logging.INFO)

    # load modules
    if not modulesdir:
        logging.warn("No modules directory specified using --modules")
    else:
        __detectModules(modulesdir)

    # register shutdown hooks
    signal.signal(signal.SIGHUP, _onHupSignal)
    signal.signal(signal.SIGTERM, _onTermSignal)

    # create and install asyncio main event loop
    # http://www.tornadoweb.org/en/stable/asyncio.html#tornado.platform.asyncio.AsyncIOMainLoop
    AsyncIOMainLoop().install()

    # advanced python scheduler for reoccuring tasks as defined by modules
    _scheduler = AsyncIOScheduler() #TornadoScheduler()

    # reload settings periodically
    _scheduler.add_job(settings.load_settings, 'interval', minutes=5)

    # add eve user and url of your application here
    import eveapi
    if 'in_game_owner' in cfgServer:
        eveapi.set_user_agent('Host: %s; Admin-EVE-Character: %s' % ('dev-local', cfgServer['in_game_owner']))

    # init universe data from SDE
    asyncio.get_event_loop().run_until_complete(universe.initCaches())

    # only import at this point to make sure all required modules have already been loaded
    from igbtoolbox import pages

    # default routes
    urls = []

    if settings.DEBUG:
        urls.append((r"/static/bower_components/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), '..', '..', 'bower_components')}))

    urls.extend([
            (r"/static/common/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), '..', '..', 'web')}),
            ('/', pages.MainPage)
            ])


    # read routes from imported modules and call modules init function
    for n, m in _importedModules:
        if not m:
            logging.error("Could not load module %s" % n)
            continue
        if hasattr(m, 'routes'):
            for r in m.routes():
                logging.debug("Registering URL %s for %s" % (r[0], r[1]))
                urls.append(r)

        if hasattr(m, 'tornado_templates'):
            for r in m.tornado_templates():
                # adjust path for modules directory
                r = os.path.join('..', r)
                logging.debug("Registering template %s for %s" % (r, n))
                _module_templates.append(r)

        if hasattr(m, 'schedule'):
            m.schedule(_scheduler)

        if hasattr(m, 'onStartup'):
            m.onStartup()


    # start scheduler
    _scheduler.start()

    # create tornado application
    app_settings = {
        #"static_path": os.path.join(os.path.dirname(__file__), '..', 'web'),
        'template_path': os.path.join(os.path.dirname(__file__), '..', '..', 'tornado-templates'),
        'module_templates': _module_templates,
        "login_url": "/login",
        "xsrf_cookies": False,
        "debug": settings.DEBUG,
        # mongodb db clients
        "db_domain": settings.get_mongodb_client(settings.MONGODB_DATABASE_DOMAIN),
        "db_global": settings.get_mongodb_client(settings.MONGODB_DATABASE_GLOBAL),
        "db_kill": settings.get_mongodb_client(settings.MONGODB_DATABASE_EVEKILL)
    }

    cookieSecret = cfgServer.get('cookie_secret')
    if cookieSecret:
        logging.debug("Secure cookies enabled")
        app_settings["xsrf_cookies"] = True
        app_settings["cookie_secret"] = cookieSecret


    # sockjs global message bus shared by all clients
    try:
        from messagebus import messaging_sockjs
        sockRouter = sockjs.tornado.SockJSRouter(messaging_sockjs.MessageBusConnection, r'/bus/(?:[^/.]+)')
        application = tornado.web.Application(urls + sockRouter.urls, **app_settings)
    except ImportError as e:
      logging.debug("Could not import messagebus module, feature will not be available")


    # If your log is full of "WARNING: Connection closed by the client", pass no_keep_alive as True to HTTPServer constructor:
    # https://github.com/mrjoes/sockjs-tornado
    # server = tornado.httpserver.HTTPServer(application) # , no_keep_alive=True)
    # server.bind(int(port))
    # server.start(1)  # Forks multiple sub-processes
    application.listen(int(port))

    # start tornado event loop
    try:
        #tornado.ioloop.IOLoop.instance().start()
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        _onTermSignal(None)
