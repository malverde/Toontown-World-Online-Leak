from datetime import datetime, timedelta
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedObject
import time

from toontown.parties.ToontownTimeZone import ToontownTimeZone, UTC


class ToontownTimeManager(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('ToontownTimeManager')
    ClockFormat = '%I:%M:%S %p'
    formatStr = '%Y-%m-%d %H:%M:%S'

    def __init__(self, serverTimeAtLogin=0, clientTimeAtLogin=0,
                 realTimeAtLogin=0):
        self.serverTimeZone = ToontownTimeZone()
        self.updateLoginTimes(serverTimeAtLogin, clientTimeAtLogin,
                              realTimeAtLogin)

    def updateLoginTimes(self, serverTimeAtLogin, clientTimeAtLogin,
                         realTimeAtLogin):
        self.serverTimeAtLogin = serverTimeAtLogin
        self.clientTimeAtLogin = clientTimeAtLogin
        self.realTimeAtLogin = realTimeAtLogin

        self.serverDateTime = datetime.fromtimestamp(
            self.serverTimeAtLogin, self.serverTimeZone)

    def getCurServerDateTime(self):
        secondsPassed = globalClock.getRealTime() - self.realTimeAtLogin
        dt = self.serverDateTime + timedelta(seconds=secondsPassed)
        return dt.astimezone(self.serverTimeZone)

    def convertStrToToontownTime(self, dateStr):
        try:
            timeStruct = time.strptime(dateStr, self.formatStr)
            return datetime.fromtimestamp(time.mktime(timeStruct), self.serverTimeZone)
        except:
            self.notify.warning('error parsing date string: "%s"' % dateStr)

    def convertUtcStrToToontownTime(self, dateStr):
        try:
            timeStruct = time.strptime(dateStr, self.formatStr)
            dtUtc = datetime(timeStruct[:6], UTC)
            return dtUtc.astimezone(self.serverTimeZone)
        except:
            self.notify.warning('error parsing date string: "%s"' % dateStr)
