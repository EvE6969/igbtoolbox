import datetime
from igbtoolbox import universe



class Pilot:

    def __init__(self, request, headers=None):
        hd = headers or request.headers
        self.systemId = int(hd.get('EVE_SOLARSYSTEMID', 0))
        self.systemName = universe.getSystemNameById(self.systemId)
        self.trusted = hd.get('EVE_TRUSTED')
        self.trusted = self.trusted == 'Yes'
        self.stationId = hd.get('EVE_STATIONID')
        if self.stationId: self.stationId = int(self.stationId)

        self.charIdCurrent = hd.get('EVE_CHARID')
        self.charId = hd.get('EVE_RUNAS_CHARID')
        if not self.charId: self.charId = self.charIdCurrent
        if self.charId: self.charId = int(self.charId)
        if self.charIdCurrent: self.charIdCurrent = int(self.charIdCurrent)

        self.charNameCurrent = hd.get('EVE_CHARNAME')
        self.charName = hd.get('EVE_RUNAS_CHARNAME')
        if not self.charName: self.charName = self.charNameCurrent

        self.corpIdCurrent = hd.get('EVE_CORPID')
        self.corpId = hd.get('EVE_RUNAS_CORPID')
        if not self.corpId: self.corpId = self.corpIdCurrent
        if self.corpId: self.corpId = int(self.corpId)
        if self.corpIdCurrent: self.corpIdCurrent = int(self.corpIdCurrent)

        self.corpNameCurrent = hd.get('EVE_CORPNAME')
        self.corpName = hd.get('EVE_RUNAS_CORPNAME')
        if not self.corpName: self.corpName = self.corpNameCurrent

        self.allianceIdCurrent = hd.get('EVE_ALLIANCEID')
        self.allianceId = hd.get('EVE_RUNAS_ALLIANCEID')
        if not self.allianceId: self.allianceId = self.allianceIdCurrent
        if self.allianceId == 'null': self.allianceId = None
        if self.allianceId: self.allianceId = int(self.allianceId)
        if self.allianceIdCurrent == 'null': self.allianceIdCurrent = None
        if self.allianceIdCurrent: self.allianceIdCurrent = int(self.allianceIdCurrent)

        self.allianceNameCurrent = hd.get('EVE_ALLIANCENAME', '')
        self.allianceName = hd.get('EVE_RUNAS_ALLIANCENAME')
        if not self.allianceName: self.allianceName = self.allianceNameCurrent

        self.shipId = hd.get('EVE_SHIPTYPEID')
        if self.shipId: self.shipId = int(self.shipId)
        else: self.shipId = 670 # igb bug or just pod killed and in station
        self.ship = universe.getShipNameById(self.shipId)

        self.authUser = None
        self.igb = None

        # dict that can be used for extra data in external modules
        self.extra = {}

    def to_json_dict(self):

        return { 'systemName': self.systemName, 'systemId': self.systemId,
               'regionName': universe.getRegionBySystemName(self.systemName), 'trusted': self.trusted,
               'stationId':  self.stationId, 'igb': self.igb, 'shipId': self.shipId, 'authUser': self.authUser,
               'charName': self.charName, 'charId': self.charId,
               'corpName': self.corpName, 'allianceName': self.allianceName,
               'corpId': self.corpId, 'allianceId': self.allianceId,
               'charNameCurrent': self.charNameCurrent, 'charIdCurrent': self.charIdCurrent,
               'corpNameCurrent': self.corpNameCurrent, 'allianceNameCurrent': self.allianceNameCurrent,
               'corpIdCurrent': self.corpIdCurrent, 'allianceIdCurrent': self.allianceIdCurrent,
               'extra': self.extra
               }

    def __repr__(self):
      return str(self.to_json_dict())
