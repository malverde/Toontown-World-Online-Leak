#Embedded file name: toontown.parties.GlobalPartyManagerUD
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from PartyGlobals import *
from datetime import datetime, timedelta
from panda3d.core import *

class GlobalPartyManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('GlobalPartyManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.debug('GPMUD generated')
        self.senders2Mgrs = {}
        self.host2PartyId = {}
        self.id2Party = {}
        self.party2PubInfo = {}
        self.tempSlots = {}
        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        startTime = datetime.strptime('2014-01-20 11:50:00', PARTY_TIME_FORMAT)
        endTime = datetime.strptime('2014-01-20 12:20:00', PARTY_TIME_FORMAT)
        self.partyAllocator = UniqueIdAllocator(0, 100000000)
        config = getConfigShowbase()
        self.wantInstantParties = config.GetBool('want-instant-parties', 0)
        self.runAtNextInterval()

    def _makeAIMsg(self, field, values, recipient):
        return self.air.dclassesByName['DistributedPartyManagerUD'].getFieldByName(field).aiFormatUpdate(recipient, recipient, simbase.air.ourChannel, values)

    def sendToAI(self, field, values, sender = None):
        if not sender:
            sender = self.air.getAvatarIdFromSender()
        dg = self._makeAIMsg(field, values, self.senders2Mgrs.get(sender, sender + 8))
        self.air.send(dg)

    def _makeAvMsg(self, field, values, recipient):
        return self.air.dclassesByName['DistributedToonUD'].getFieldByName(field).aiFormatUpdate(recipient, recipient, simbase.air.ourChannel, values)

    def sendToAv(self, avId, field, values):
        dg = self._makeAvMsg(field, values, avId)
        self.air.send(dg)

    def runAtNextInterval(self):
        now = datetime.now()
        howLongUntilAFive = 60 - now.second + 60 * (4 - now.minute % 5)
        taskMgr.doMethodLater(howLongUntilAFive, self.__checkPartyStarts, 'GlobalPartyManager_checkStarts')

    def canPartyStart(self, party):
        now = datetime.now()
        delta = timedelta(minutes=15)
        endStartable = party['start'] + delta
        if self.wantInstantParties:
            return True
        else:
            return party['start'] < now

    def isTooLate(self, party):
        now = datetime.now()
        delta = timedelta(minutes=15)
        endStartable = party['start'] + delta
        return endStartable > now

    def __checkPartyStarts(self, task):
        now = datetime.now()
        for partyId in self.id2Party:
            party = self.id2Party[partyId]
            hostId = party['hostId']
            if self.canPartyStart(party) and party['status'] == PartyStatus.Pending:
                party['status'] = PartyStatus.CanStart
                self.sendToAv(hostId, 'setHostedParties', [[self._formatParty(party)]])
                self.sendToAv(hostId, 'setPartyCanStart', [partyId])
            elif self.isTooLate(party):
                party['status'] = PartyStatus.NeverStarted
                self.sendToAv(hostId, 'setHostedParties', [[self._formatParty(party)]])

        self.runAtNextInterval()

    def _formatParty(self, partyDict):
        start = partyDict['start']
        end = partyDict['end']
        return [partyDict['partyId'],
         partyDict['hostId'],
         start.year,
         start.month,
         start.day,
         start.hour,
         start.minute,
         end.year,
         end.month,
         end.day,
         end.hour,
         end.minute,
         partyDict['isPrivate'],
         partyDict['inviteTheme'],
         partyDict['activities'],
         partyDict['decorations'],
         partyDict.get('status', PartyStatus.Pending)]

    def avatarJoined(self, avId):
        partyId = self.host2PartyId.get(avId, None)
        if partyId:
            party = self.id2Party.get(partyId, None)
            if not party:
                return
            self.sendToAv(avId, 'setHostedParties', [[self._formatParty(party)]])
            if partyId not in self.party2PubInfo and self.canPartyStart(party):
                self.sendToAv(avId, 'setPartyCanStart', [partyId])

    def __updatePartyInfo(self, partyId):
        party = self.party2PubInfo[partyId]
        for sender in self.senders2Mgrs.keys():
            actIds = []
            for activity in self.id2Party[partyId]['activities']:
                actIds.append(activity[0])

            minLeft = int((PARTY_DURATION - (datetime.now() - party['started']).seconds) / 60)
            self.sendToAI('updateToPublicPartyInfoUdToAllAi', [party['shardId'],
             party['zoneId'],
             partyId,
             self.id2Party[partyId]['hostId'],
             party['numGuests'],
             party['maxGuests'],
             party['hostName'],
             actIds,
             minLeft], sender=sender)

    def __updatePartyCount(self, partyId):
        for sender in self.senders2Mgrs.keys():
            self.sendToAI('updateToPublicPartyCountUdToAllAi', [self.party2PubInfo[partyId]['numGuests'], partyId], sender=sender)

    def partyHasStarted(self, partyId, shardId, zoneId, hostName):
        self.party2PubInfo[partyId] = {'partyId': partyId,
         'shardId': shardId,
         'zoneId': zoneId,
         'hostName': hostName,
         'numGuests': 0,
         'maxGuests': MaxToonsAtAParty,
         'started': datetime.now()}
        self.__updatePartyInfo(partyId)
        if partyId not in self.id2Party:
            self.notify.warning("Didn't find details for starting Party ID %s hosted by %s" % (partyId, hostName))
            return
        self.id2Party[partyId]['status'] = PartyStatus.Started
        party = self.id2Party.get(partyId, None)
        self.sendToAv(party['hostId'], 'setHostedParties', [[self._formatParty(party)]])

    def partyDone(self, partyId):
        del self.party2PubInfo[partyId]
        self.id2Party[partyId]['status'] = PartyStatus.Finished
        party = self.id2Party.get(partyId, None)
        self.sendToAv(party['hostId'], 'setHostedParties', [[self._formatParty(party)]])
        del self.id2Party[partyId]
        self.air.writeServerEvent('party-done', '%s')

    def toonJoinedParty(self, partyId, avId):
        if avId in self.tempSlots:
            del self.tempSlots[avId]
            return
        self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] += 1
        self.__updatePartyCount(partyId)

    def toonLeftParty(self, partyId, avId):
        self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] -= 1
        self.__updatePartyCount(partyId)

    def partyManagerAIHello(self, channel):
        self.notify.info('AI with base channel %s, will send replies to DPM %s' % (simbase.air.getAvatarIdFromSender(), channel))
        self.senders2Mgrs[simbase.air.getAvatarIdFromSender()] = channel
        self.sendToAI('partyManagerUdStartingUp', [])
        self.air.addPostRemove(self._makeAIMsg('partyManagerUdLost', [], channel))

    def addParty(self, avId, partyId, start, end, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.notify.info('Start Time: %s' % start)
        startTime = datetime.strptime(start, PARTY_TIME_FORMAT)
        endTime = datetime.strptime(end, PARTY_TIME_FORMAT)
        self.notify.info('Start Year: %s' % startTime.year)
        if avId in self.host2PartyId:
            self.sendToAI('addPartyResponseUdToAi', [partyId, AddPartyErrorCode.TooManyHostedParties, self._formatParty(self.id2Party[partyId])])
        self.id2Party[partyId] = {'partyId': partyId,
         'hostId': avId,
         'start': startTime,
         'end': endTime,
         'isPrivate': isPrivate,
         'inviteTheme': inviteTheme,
         'activities': activities,
         'decorations': decorations,
         'inviteeIds': inviteeIds,
         'status': PartyStatus.Pending}
        self.host2PartyId[avId] = partyId
        self.sendToAI('addPartyResponseUdToAi', [partyId, AddPartyErrorCode.AllOk, self._formatParty(self.id2Party[partyId])])
        if self.wantInstantParties:
            taskMgr.remove('GlobalPartyManager_checkStarts')
            taskMgr.doMethodLater(15, self.__checkPartyStarts, 'GlobalPartyManager_checkStarts')

    def queryParty(self, hostId):
        if hostId in self.host2PartyId:
            party = self.id2Party[self.host2PartyId[hostId]]
            self.sendToAI('partyInfoOfHostResponseUdToAi', [self._formatParty(party), party.get('inviteeIds', [])])
            return
        self.notify.warning("Query failed, Av %s isn't hosting anything!" % hostId)

    def requestPartySlot(self, partyId, avId, gateId):
        if partyId not in self.party2PubInfo:
            recipient = self.GetPuppetConnectionChannel(avId)
            sender = simbase.air.getAvatarIdFromSender()
            dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('partyRequestDenied').aiFormatUpdate(gateId, recipient, sender, [PartyGateDenialReasons.Unavailable])
            self.air.send(dg)
            return
        party = self.party2PubInfo[partyId]
        if party['numGuests'] >= party['maxGuests']:
            recipient = self.GetPuppetConnectionChannel(avId)
            sender = simbase.air.getAvatarIdFromSender()
            dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('partyRequestDenied').aiFormatUpdate(gateId, recipient, sender, [PartyGateDenialReasons.Full])
            self.air.send(dg)
            return
        party['numGuests'] += 1
        self.__updatePartyCount(partyId)
        self.tempSlots[avId] = partyId
        taskMgr.doMethodLater(60, self._removeTempSlot, 'partyManagerTempSlot%d' % avId, extraArgs=[avId])
        actIds = []
        for activity in self.id2Party[partyId]['activities']:
            actIds.append(activity[0])

        info = [party['shardId'],
         party['zoneId'],
         party['numGuests'],
         party['hostName'],
         actIds,
         0]
        hostId = self.id2Party[party['partyId']]['hostId']
        recipient = self.GetPuppetConnectionChannel(avId)
        sender = simbase.air.getAvatarIdFromSender()
        dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('setParty').aiFormatUpdate(gateId, recipient, sender, [info, hostId])
        self.air.send(dg)

    def _removeTempSlot(self, avId):
        partyId = self.tempSlots.get(avId)
        if partyId:
            del self.tempSlots[avId]
            self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] -= 1
            self.__updatePartyCount(partyId)

    def allocIds(self, numIds):
        ids = []
        while len(ids) < numIds:
            ids.append(self.partyAllocator.allocate())

        self.sendToAI('receiveId', ids)
