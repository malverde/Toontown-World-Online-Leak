#Embedded file name: toontown.election.SafezoneInvasionGlobals
import random
FirstSuitSpawnPoint = (65.0, -5.0, 4.0, 180.0)
FinaleSuitSpawnPoint = (-138.0, 4.0, 0.5, -90.0)
FinaleSuitDestinations = [(-96.2, -52.3),
 (-36.5, -56.0),
 (7.1, -1.4),
 (27.3, -0.4),
 (36.5, -1.9)]
FinaleSuitName = 'Director of\nAmbush Marketing\nSupervisor\nLevel 50'
FinaleSuitPhrases = ['Apparently our marketing strategies haven\'t exactly appealed to you "Toons".',
 'I suppose you could say that "I\'m the boss."',
 "I'll be needing to speak with your President directly.I'm prepared to close this deal quickly.",
 "Relax, you'll find this is for the best.",
 "At this rate I'll need to liquidate toons from the picture.",
 "I assure you that you'll find no greater offer.",
 "The Chairman won't be happy until you are.",
 "Ah, finally. Just the toon I've been searching for.",
 "I hope you won't pull out of the deal like your predecessor.",
 "Don't worry, he is in safe keeping now."]
FinaleSuitAttackDamage = 10
FinaleSuitAttackDelay = 10
SuitSpawnPoints = [(-59.0, 70.0, 0.0, -149.0),
 (-122.0, -54.0, 0.5, -40.0),
 (-23.7, -83.1, 0.5, 0.0),
 (-116.1, 7.8, 0.0, -90.0),
 (14.0, 83.5, 2.5, 140.0),
 (17.8, -72.4, 2.5, 45.0),
 (10.0, -81.5, 2.5, 45.0),
 (-55.1, -35.0, -3.7, -60.0),
 (-66.7, 87.8, 0.5, -150.0),
 (-91.7, 88.8, -0.7, -140.0),
 (29.7, 139.8, 2.5, -70.0),
 (90.0, 106.0, 2.5, -100.0),
 (-127.5, 56.3, 0.5, 30.0),
 (-104.6, 51.0, 0.02, -30.0),
 (-111.3, -67.0, 0.5, 40.0),
 (135.0, -98.0, 2.5, -130.0),
 (121.6, -52.8, 2.5, 80.0),
 (46.1, -114.8, 2.5, 60.0),
 (-113.6, 20.0, 0.03, 55.0)]
suitLevels = [0,
 1,
 2,
 3,
 4]
sellbotSuits = ['cc',
 'tm',
 'nd',
 'gh',
 'ms',
 'tf',
 'm',
 'mh']
cashbotSuits = ['sc',
 'pp',
 'tw',
 'bc',
 'nc',
 'mb',
 'ls',
 'rb']
lawbotSuitTypes = ['bf',
 'b',
 'dt',
 'ac',
 'bs',
 'sd',
 'le',
 'bw']
bossbotSuits = ['f',
 'p',
 'ym',
 'mm',
 'ds',
 'hh',
 'cr',
 'tbc']

def generateSuits(numberOfSuits, suitLevelRange = [0, 0], suitRange = [0, 0], wantExtraShakers = False):
    suits = [sellbotSuits,
     cashbotSuits,
     lawbotSuitTypes,
     bossbotSuits]
    wave = []
    if wantExtraShakers:
        wave = [ (random.choice(suits)[random.randint(suitRange[0], suitRange[1])], random.randint(suitLevelRange[0], suitLevelRange[1])) for k in range(numberOfSuits) ]
        wave.append(('ms', 4))
        wave.append(('ms', 4))
    else:
        wave = [ (random.choice(suits)[random.randint(suitRange[0], suitRange[1])], random.randint(suitLevelRange[0], suitLevelRange[1])) for k in range(numberOfSuits) ]
    return wave


SuitWaves = [generateSuits(5, [0, 4], [0, 0]),
 generateSuits(7, [2, 3], [0, 0]),
 generateSuits(9, [2, 4], [0, 0]),
 generateSuits(6, [2, 3], [0, 1]),
 generateSuits(7, [2, 2], [0, 1]),
 generateSuits(9, [2, 3], [0, 1]),
 generateSuits(4, [2, 3], [1, 2]),
 generateSuits(6, [2, 2], [2, 2]),
 generateSuits(9, [2, 3], [2, 2]),
 generateSuits(4, [2, 3], [2, 3]),
 generateSuits(6, [2, 2], [3, 3]),
 generateSuits(9, [2, 3], [3, 3]),
 generateSuits(4, [0, 2], [3, 4]),
 generateSuits(6, [2, 4], [4, 4]),
 generateSuits(9, [2, 3], [4, 4]),
 generateSuits(4, [1, 2], [4, 5]),
 generateSuits(6, [1, 4], [5, 5], True),
 generateSuits(8, [2, 3], [5, 5], True),
 generateSuits(4, [0, 2], [5, 6], True),
 generateSuits(6, [1, 2], [6, 6], True),
 generateSuits(8, [2, 3], [6, 6], True),
 generateSuits(8, [1, 3], [6, 7], True),
 generateSuits(8, [1, 4], [7, 7], True),
 generateSuits(8, [2, 4], [7, 7], True),
 generateSuits(8, [1, 3], [6, 7], True),
 generateSuits(10, [1, 4], [7, 7], True),
 generateSuits(10, [2, 4], [7, 7], True)]
SuitWaitWaves = [1,
 4,
 7,
 10,
 13,
 16,
 19,
 22,
 24,
 25]
SuitIntermissionWaves = [2,
 5,
 8,
 11,
 14,
 17,
 20,
 23,
 26]
SuitSkelecogWaves = [24, 25, 26]
WaveBeginningTime = 10
IntermissionTime = 20
StandardSuitDamage = 5
MoveShakerDamageRadius = 3
MoveShakerRadius = 15
MoveShakerStunTime = 5
ToonHealAmount = 3
CogSkyFile = 'phase_3.5/models/props/BR_sky'
InvasionMusicEnter = 'phase_4/audio/bgm/DD_main_temp.ogg'
LeaveToontownCentralAlert = "There isn't anywhere to go! Shops are closed for the election today."
Thanks = "Thank you so much for attending the elections! We'd like to thank you all for supporting us! See you all soon!"
