########################## THE TOON LAND PROJECT ##########################
# Filename: __init__.py
# Created by: Cody/Fd Green Cat Fd (February 1st, 2013)
####
# Description:
#
# Initializes the Toon Land objects.
####

import toontown
from toontown.toonbase import ToontownGlobals
from toontown.distributed import PlayGame
from direct.fsm import StateData, ClassicFSM, State
from toontown.hood import ToonHood

StreetNames = {6100:('to', 'in', 'Nutty Place'),
               PlaygroundGlobals.FUNNY_FARM:('to the', 'in the', 'Playground'),
               PlaygroundGlobals.FUNNY_FARM + 100:('to', 'in', 'Barking Boulevard')}

toontown.town.OZTownLoader = OZTownLoader
toontown.town.OZStreet = OZStreet

toontown.hood.FFHood = FFHood
toontown.safezone.FFPlayground = FFPlayground
toontown.safezone.FFSafeZoneLoader = FFSafeZoneLoader
toontown.town.FFTownLoader = FFTownLoader
toontown.town.FFStreet = FFStreet
ToontownGlobals.hoodNameMap[PlaygroundGlobals.FUNNY_FARM] = ('to', 'in', 'Funny Farm')
ToontownGlobals.hoodCountMap[PlaygroundGlobals.FUNNY_FARM] = 2
ToontownGlobals.safeZoneCountMap[PlaygroundGlobals.FUNNY_FARM] = 500
ToontownGlobals.townCountMap[PlaygroundGlobals.FUNNY_FARM] = 40
ToontownGlobals.phaseMap[PlaygroundGlobals.FUNNY_FARM] = 8
PlayGame.PlayGame.Hood2ClassDict[PlaygroundGlobals.FUNNY_FARM] = FFHood.FFHood
PlayGame.PlayGame.Hood2StateDict[PlaygroundGlobals.FUNNY_FARM] = 'FFHood'
base.cr.hoodMgr.hoodId2Name[19000] = 'ff'
base.cr.hoodMgr.hoodName2Id['ff'] = 19000
base.cr.hoodMgr.dropPoints[19000] = ([-23.645, 44.332, 10.026, -70.338, 0, 0],
                                     [35.903, -8.8, 10.026, -342.535, 0, 0],
                                     [70.208, 53.846, 10.026, -197.012, 0, 0],
                                     [-53.355, 25.654, 10.026, -158.932, 0, 0],
                                     [-90.708, -50.178, 10.026, -100.268, 0, 0],
                                     [-68.551, -92.413, 10.026, -58.459, 0, 0],
                                     [6.114, -63.672, 10.026, 4.756, 0, 0],
                                     [76.510, -25.626, 10.026, 34.8, 0, 0],
                                     [121.028, 47.339, 10.026, 106.151, 0, 0],
                                     [-94.343, 51.996, 10.026, 183.670, 0, 0])

def enterFFHood(self, requestStatus):
    self.accept(self.hoodDoneEvent, self.handleHoodDone)
    self.hood.enter(requestStatus)

PlayGame.PlayGame.enterFFHood = enterFFHood

def exitFFHood(self):
    self._destroyHood()

PlayGame.PlayGame.exitFFHood = exitFFHood

playGame = base.cr.playGame
playGame.fsm = ClassicFSM.ClassicFSM('PlayGame', [State.State('start', playGame.enterStart, playGame.exitStart, ['quietZone']),
 State.State('quietZone', playGame.enterQuietZone, playGame.exitQuietZone, ['TTHood', 'DDHood', 'BRHood', 'MMHood',
 'DGHood', 'DLHood', 'GSHood', 'OZHood', 'GZHood', 'FFHood', 'SellbotHQ', 'CashbotHQ', 'LawbotHQ', 'BossbotHQ',
 'TutorialHood', 'EstateHood', 'PartyHood']),
 State.State('TTHood', playGame.enterTTHood, playGame.exitTTHood, ['quietZone']),
 State.State('DDHood', playGame.enterDDHood, playGame.exitDDHood, ['quietZone']),
 State.State('BRHood', playGame.enterBRHood, playGame.exitBRHood, ['quietZone']),
 State.State('MMHood', playGame.enterMMHood, playGame.exitMMHood, ['quietZone']),
 State.State('DGHood', playGame.enterDGHood, playGame.exitDGHood, ['quietZone']),
 State.State('DLHood', playGame.enterDLHood, playGame.exitDLHood, ['quietZone']),
 State.State('GSHood', playGame.enterGSHood, playGame.exitGSHood, ['quietZone']),
 State.State('OZHood', playGame.enterOZHood, playGame.exitOZHood, ['quietZone']),
 State.State('GZHood', playGame.enterGZHood, playGame.exitGZHood, ['quietZone']),
 State.State('FFHood', playGame.enterFFHood, playGame.exitFFHood, ['quietZone']),
 State.State('BossbotHQ', playGame.enterBossbotHQ, playGame.exitBossbotHQ, ['quietZone']),
 State.State('SellbotHQ', playGame.enterSellbotHQ, playGame.exitSellbotHQ, ['quietZone']),
 State.State('CashbotHQ', playGame.enterCashbotHQ, playGame.exitCashbotHQ, ['quietZone']),
 State.State('LawbotHQ', playGame.enterLawbotHQ, playGame.exitLawbotHQ, ['quietZone']),
 State.State('TutorialHood', playGame.enterTutorialHood, playGame.exitTutorialHood, ['quietZone']),
 State.State('EstateHood', playGame.enterEstateHood, playGame.exitEstateHood, ['quietZone']),
 State.State('PartyHood', playGame.enterPartyHood, playGame.exitPartyHood, ['quietZone'])], 'start', 'start')
playGame.fsm.enterInitialState()
playGame.parentFSM.getStateNamed('playGame').addChild(playGame.fsm)

ToonHood.StreetNames.update(StreetNames)