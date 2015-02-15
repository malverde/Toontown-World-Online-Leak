########################## THE TOON LAND PROJECT ##########################
# Filename: PicnicBasket.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the picnic tables in Funny Farm, as well as some
# client to client communications.
####

from toontown.safezone.PicnicBasket import PicnicBasket

class PicnicBasket(PicnicBasket):

    def enter(self):
        self.fsm.enterInitialState()
        if base.localAvatar.hp > 0:
            self.fsm.request('requestBoard')
            messenger.send('enterPicnicTableOK_%d_%d' % (self.tableNumber, self.seatNumber))
        else:
            self.fsm.request('trolleyHFA')