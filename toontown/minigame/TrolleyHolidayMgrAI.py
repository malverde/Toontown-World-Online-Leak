from direct.directnotify.DirectNotifyGlobal import *
from toontown.ai import HolidayBaseAI


class TrolleyHolidayMgrAI(HolidayBaseAI.HolidayBaseAI):
    notify = directNotify.newCategory('TrolleyHolidayMgrAI')

    PostName = 'TrolleyHoliday'
    StartStopMsg = 'TrolleyHolidayStartStop'

    def start(self):
        HolidayBaseAI.HolidayBaseAI.start(self)

        bboard.post(TrolleyHolidayMgrAI.PostName, True)
        simbase.air.newsManager.trolleyHolidayStart()
        messenger.send(TrolleyHolidayMgrAI.StartStopMsg)

    def stop(self):
        HolidayBaseAI.HolidayBaseAI.stop(self)

        bboard.remove(TrolleyHolidayMgrAI.PostName)
        simbase.air.newsManager.trolleyHolidayEnd()
        messenger.send(TrolleyHolidayMgrAI.StartStopMsg)
