import logging
import asyncio
from igbtoolbox.universedump.systems import *
from igbtoolbox.universedump.sec import *
import tornado.gen
from igbtoolbox import settings


_SHIP_NAMES_BY_ID = {}
_SHIP_GROUPS = {}


@asyncio.coroutine
def initCaches():
    global _SHIP_NAMES_BY_ID
    global _SHIP_GROUPS

    cp = yield from settings.get_sde_pool()
    with (yield from cp.cursor()) as cur:

        logging.debug("Initializing universe data caches from SDE")

        # build ship ID <> ship group mappings
        yield from cur.execute("""
            select i."typeID", g."groupName" from "invTypes" i
            join "invGroups" g on i."groupID" = g."groupID"
            where g."categoryID" = 6""") # 6 = ships

        res = yield from cur.fetchall()
        for r in res:
            _SHIP_GROUPS[r[0]] = r[1]


        yield from cur.execute("""
            select i."typeID", i."typeName" from "invTypes" i
            join "invGroups" g on i."groupID" = g."groupID"
            where g."categoryID" = 6""") # 6 = ships

        res = yield from cur.fetchall()
        for r in res:
            _SHIP_NAMES_BY_ID[r[0]] = r[1]

    logging.debug("Finished initializing caches from SDE")


def getSystemIdByName(name):
    return SYSTEMS_NAME_2_ID.get(name)

def getSystemNameById(i):
    for k, v in SYSTEMS_NAME_2_ID.items():
        if v == i:
            return k

def getSystemSecById(i):
    return SYSTEMS_ID_2_SEC[i]

def getSystemTrueSecById(i):
    return SYSTEMS_ID_2_TRUESEC[i]

def getSystemNamesByRegion(region):

    ret = []
    for k, v in SYSTEMS_NAME_2_REGION.items():
        if v == region:
            ret.append(k)
    return ret

def getRegionBySystemName(name):
    return SYSTEMS_NAME_2_REGION.get(name)




def getShipNamesByIds(*args):
    sids = map(int, args)
    return [ _SHIP_NAMES_BY_ID[shipId] for shipId in sids if shipId in _SHIP_NAMES_BY_ID ]

def getShipNameById(id):
    return _SHIP_NAMES_BY_ID.get(int(id))

def getGroupsByShipIds(*args):
    sids = map(int, args)
    return [ _SHIP_GROUPS[shipId] for shipId in sids if shipId in _SHIP_GROUPS ]

def getGroupByShipId(id):
    return _SHIP_GROUPS.get(int(id))


@tornado.gen.coroutine
def getAsyncConstellationBySystemName(system):
    res = yield from __get_sde_result_by_id("""
        select "constellationName" from "mapSolarSystems" s
        join "mapConstellations" c on s."constellationID" = c."constellationID"
        where s."solarSystemName" = %s""", (system,))
    return res

def __get_sde_result_by_id(query, param):
    cp = yield from settings.get_sde_pool()
    with (yield from cp.cursor()) as cur:
        yield from cur.execute(query, param)
        res = yield from cur.fetchone()
        if res: return res[0]
        else: return None
