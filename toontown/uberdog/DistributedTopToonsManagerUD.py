# CLEANUP IMPORTS

from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.DistributedObjectUD import *
from direct.showbase.DirectObject import *
from toontown.toon.ToonDNA import ToonDNA, getSpeciesName
import TopToonsGlobals
import time, cPickle, random
import datetime, json
import urllib
import urllib2
import hashlib

def getCurrentMonth():
    dt = datetime.date.today()
    month = dt.month
    year = dt.year
    return year * 100 + month

def getPrevMonth():
    current = getCurrentMonth()
    year, month = divmod(current, 100)
    month -= 1
    if not month:
        month = 12
        year -= 1

    return year * 100 + month

def getNextMonth():
    current = getCurrentMonth()
    year, month = divmod(current, 100)
    month += 1
    if month > 12:
        month = 1
        year += 1

    return year * 100 + month

def timeToNextMonth():
    now = datetime.datetime.now()
    year, month = divmod(getNextMonth(), 100)
    return (datetime.datetime(year, month, 1) - now).total_seconds()

def getEmptySiteToonsColl(month):
    coll = {}

    start = TopToonsGlobals._CAT_BEGIN
    end = TopToonsGlobals._CAT_END
    while start <= end:
        coll[str(start)] = {}
        start *= 2

    coll['month'] = month
    return coll

class SiteUploadFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiteUploadFSM')
    URL = config.GetString('toptoons-api-endpoint', 'http://toontownworldonline.com/api/toptoons/post/') # TODO:

    def __init__(self, mgr, data):
        FSM.__init__(self, 'SiteUploadFSM')

        self.mgr = mgr
        self.data = {}
        self.month = data.pop('month')
        for category, avs in data.items():
            self.data[int(category)] = sorted(avs.items(), key=lambda x: -x[1])

        self.__cat = TopToonsGlobals._CAT_BEGIN
        self.__responses = {}
        self.__cache = {}
        self.__waiting = {}
        self.__dataToSend = {}
        self.__failures = -1

        self.demand('QueryAvatars')

    def enterQueryAvatars(self):
        avs = self.data[self.__cat]
        cutoff = self.__failures
        if cutoff == -1:
            cutoff = 5
        selected, remaining = avs[:cutoff], avs[cutoff:]
        self.data[self.__cat] = remaining

        self.__waiting = {int(x[0]): x[1] for x in selected}
        avIds = self.__waiting.keys()
        for avId in avIds:
            if avId in self.__cache:
                self.__responses[avId] = (self.__cache[avId][0], self.__waiting.pop(avId))

        self.__failures = 0
        for avId in self.__waiting:
            def response(x, y, avId=avId):
                self.__handleToon(avId, x, y)

            self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, avId, response)

        if not self.__waiting:
            self.demand('SortResults')

    def __handleToon(self, avId, dclass, fields):
        if avId not in self.__waiting:
            return

        if dclass != self.mgr.air.dclassesByName['DistributedToonUD']:
            self.__failures += 1
            self.notify.warning('%d query failed!' % avId)
            del self.__waiting[avId]
            if not self.__waiting:
                self.demand('QueryAvatars')
            return

        name = fields['setName'][0]
        hp = fields['setMaxHp'][0]

        dna = ToonDNA(fields['setDNAString'][0])
        species = getSpeciesName(dna.head)
        color = dna.headColor

        if species == 'pig':
            dna = 'pig'

        else:
            if species == 'cat' and color == 26:
                dna = 'blackcat'

            else:
                if color > 23:
                    color = 0

                dna = '%s_%s_%d' % (species, dna.head[1:], color)

        self.__responses[avId] = ((name, dna, hp), self.__waiting.pop(avId))

        if not self.__waiting:
            self.demand('QueryAvatars')

    def enterSortResults(self):
        responses = sorted(self.__responses.values(), key=lambda x: -x[-1])
        self.__dataToSend[self.__cat] = responses
        self.__cache.update(self.__responses)
        self.__failures = -1
        self.__responses = {}
        self.__cat *= 2
        if self.__cat * 2 == TopToonsGlobals._CAT_END:
            self.demand('Upload')
            return

        self.demand('QueryAvatars')

    def enterUpload(self):
        self.__dataToSend['month'] = self.month

        (success, error), res = self.post(self.URL, self.__dataToSend)
        print (success, error), res

    def post(self, url, data):
        headers = {'User-Agent' : 'TTUberAgent'}

        innerData = json.dumps(data)
        hmac = hashlib.sha512(innerData + self.mgr.air.getApiKey()).hexdigest() # XXX PROVIDE THE KEY HERE

        data = 'data=%s' % urllib.quote(innerData)
        data += '&hmac=%s' % urllib.quote(hmac)

        success = True
        error = None
        res = {}

        try:
            req = urllib2.Request(url, data, headers)
            res = json.loads(urllib2.urlopen(req).read())
            success = res['success']
            error = res.get('error')

        except Exception as e:
            if hasattr(e, 'read'):
                with open('../e.html', 'wb') as f:
                    f.write(e.read())

            success = False
            error = str(e)

        return (success, error), res

class DistributedTopToonsManagerUD(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTopToonsManagerUD')

    def __init__(self, air):
        self.air = air

        self.__curMonth = getCurrentMonth()
        coll = None
        # if self.air.dbConn:
        #     coll = self.air.db.Toons.find_one({'month': self.__curMonth})
        #     if not coll:
        #         lastMonthColl = self.air.db.Toons.find_one({'month': getPrevMonth()})
        #         if lastMonthColl:
        #             self.__uploadLastMonth(lastMonthColl)

        if not coll:
            coll = getEmptySiteToonsColl(self.__curMonth)

        self.__topToonsData = coll
        self.__topToonsData.pop('_id', None)

        self.accept('topToonsManager-AI-score-site', self.__topToonsScore)
        self.waitForNextMonth()

    def __uploadLastMonth(self, data):
        self.notify.info('Sending last month result to site...')
        SiteUploadFSM(self, data)

    def waitForNextMonth(self):
        def _nm(task):
            self.__uploadLastMonth(self.__topToonsData)

            self.__curMonth = getCurrentMonth()
            self.__topToonsData = getEmptySiteToonsColl(self.__curMonth)

            self.waitForNextMonth()

            return task.done

        taskMgr.doMethodLater(timeToNextMonth() + 1, _nm, 'DistributedTopToonsManagerUD-nextMonth')

    def saveSite(self):
        """if self.air.dbConn:
            self.air.dbConn.Toons.update({'month': self.__curMonth}, {'$set': self.__topToonsData}, upsert=True)"""
    def __topToonsScore(self, avId, categories, score):
        def _add(cat):
            cd = self.__topToonsData[str(cat)]
            cd[str(avId)] = cd.get(str(avId), 0) + score

        start = TopToonsGlobals._CAT_BEGIN
        end = TopToonsGlobals._CAT_END
        while start <= end:
            if categories & start:
                _add(start)

            start *= 2

        self.saveSite()