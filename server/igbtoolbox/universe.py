
from igbtoolbox.universedump.systems import *
from igbtoolbox.universedump.sec import *
from igbtoolbox.universedump.ships import *

# TODO: move code to SDE module

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

def getShipById(i):
    return SHIPS_BY_ID.get(i)
