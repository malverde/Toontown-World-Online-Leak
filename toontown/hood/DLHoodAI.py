from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedResistanceEmoteMgrAI
from toontown.ai import DistributedWinterCarolingTargetAI
import datetime


class DLHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland

    def createZone(self):
        SZHoodAI.createZone(self)
        self.resistanceEmoteManager = DistributedResistanceEmoteMgrAI.DistributedResistanceEmoteMgrAI(self.air)
        self.resistanceEmoteManager.generateWithRequired(9720)

        self.spawnObjects()
        
        day = str(datetime.datetime.now().strftime("%d"))
        
        if str(datetime.datetime.now().strftime("%m")) == "12" and day == "14" or day == "15" or day == "16" or day == "17" or day == "18" or day == "19" or day == "20" or day == "21" or day == "22" or day == "23" or day == "24" or day == "25" or day == "26" or day == "27" or "28" or day == "29" or day == "30" or day == "31":
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(9720)
            
        elif str(datetime.datetime.now().strftime("%m")) == "01" and day == "02" or day == "03" or day == "04":
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(9720)
            
        elif str(datetime.datetime.now().strftime("%m")) == "10" and day ==  "21" or day == "22" or day == "23" or day == "25" or day == "26" or day == "27" or day == "28" or day == "29" or day == "30" or day == "31":
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(9619)
            
        elif str(datetime.datetime.now().strftime("%m")) == "11" and day ==  "01":
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(9619)
