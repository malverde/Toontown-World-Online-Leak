########################## THE TOON LAND PROJECT ##########################
# Filename: FFStreet.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm street module.
####

from toontown.town import Street

class FFStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [requestStatus])

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)