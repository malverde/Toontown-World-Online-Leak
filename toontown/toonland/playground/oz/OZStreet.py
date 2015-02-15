########################## THE TOON LAND PROJECT ##########################
# Filename: OZStreet.py
# Created by: Cody/Fd Green Cat Fd (February 10th, 2013)
####
# Description:
#
# The Outdoor Zone street module.
####

from toontown.town import Street

class OZStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [requestStatus])

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)