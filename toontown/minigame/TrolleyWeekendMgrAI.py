from direct.directnotify.DirectNotifyGlobal import *
from toontown.ai import HolidayBaseAI


class TrolleyWeekendMgrAI(HolidayBaseAI.HolidayBaseAI):
    notify = directNotify.newCategory('TrolleyWeekendMgrAI')

    PostName = 'TrolleyWeekend'
    StartStopMsg = 'TrolleyWeekendStartStop'

    def start(self):
        HolidayBaseAI.HolidayBaseAI.start(self)

        bboard.post(TrolleyWeekendMgrAI.PostName, True)
        simbase.air.newsManager.trolleyWeekendStart()
        messenger.send(TrolleyWeekendMgrAI.StartStopMsg)


    def stop(self):
        HolidayBaseAI.HolidayBaseAI.stop(self)

        bboard.remove(TrolleyWeekendMgrAI.PostName)
        simbase.air.newsManager.trolleyWeekendEnd()
        messenger.send(TrolleyWeekendMgrAI.StartStopMsg)
