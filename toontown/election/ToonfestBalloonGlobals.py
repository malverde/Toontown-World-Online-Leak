#Embedded file name: toontown.election.ToonfestBalloonGlobals
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from pandac.PandaModules import *
from random import choice
BalloonBasePosition = [274, -263, 25]
BalloonScale = 1.2
SlappySpeech1 = ['Heeeeellllllooooo!',
 'Despite my serendipitous exclamation, I must inform you that I am actually quite terrified!',
 "Balloon rides aren't really my forte. I'm all about TTW.",
 'Preferably I would not be up here.',
 'You know, I did not want to be up here.',
 "It was all Flippys idea!",
 'He wanted some fun in our town!',
 "Thats how I got up here up here in the balloon.",
 "That's the last time I fall asleep in a toon council meeting",
 "Teleport to a friend or go to acorn acres to get down!"]
SlappySpeech2 = ['Another balloon ride. Just what my day needed!',
 'That was complete sarcasm, too. I actually have a mortal fear of heights.',
 "I've been living my nightmares all day today!",
 "I must say though, this ride isn't so bad yet. At least I'm not alone!",
 'You can see a lot from up here, actually. The mine, the mountains -- is that... A castle?',
 'Flippy really is going all out with these construction projects.',
 "I can't say I like the color scheme though.",
 "Wowee, this is great! I'm actually pretty excited to head--",
 "Hang on - you're getting off here? No, you can't just leave me all the way up here!",
 "Teleport to a friend or go to acorn acres to get down! Don't mind me, I'll just float here panicking!"]
SlappySpeech3 = ['Need a lift?',
 "I actually wouldn't recommend it.",
 'Say, do you know how many Toons go sad from balloon crashes each year?',
 "One. There's actually only been one and he didn't really go sad from a crash.",
 'He worked with balloons though. So that counts.',
 "I've happened to notice that you haven't asked me to take you back down to the ground yet!",
 "I mean seriously, I'm telling you straightforward: We're not going to survive this ride.",
 "Listen, I didn't want to do this, but we're too high. This is just too high. For your own safety I'm taking us back--",
 "Oh we're here. You know, that was just as bad as anticipated, and now I get to relive it all again. Hooray!",
 "Teleport to a friend or go to acorn acres to get down!"]
SlappySpeech5 = ['No, no! Blargghh, not another one!',
 "I don't mean to offend very much -- I'm just not a fan of rides.",
 '...or balloons...',
 '...or...heights...',
 'AHH! -- Sorry, just looked down.',
 "I didn't really volunteer for the job you see, it's just that...",
 'We was in a meeting',
 'I fell asleep and when I woke up all the best jobs were gone.',
 "Oh boy, we're here. Looks like I get to go back down.",
 "Teleport to a friend or go to acorn acres to get down!"]
SlappySpeechChoices = [SlappySpeech1,
 SlappySpeech2,
 SlappySpeech3,
 SlappySpeech5]
SlappySpeeches = choice(SlappySpeechChoices)
NumBalloonPaths = 1

def generateFlightPaths(balloon):
    flightPaths = []
    flightPaths.append(Sequence(Wait(0.5), balloon.balloon.posHprInterval(1.5, Point3(232, -262, 27), (0, 2, 2)), balloon.balloon.posHprInterval(1.5, Point3(170, -252, 32), (0, -2, -2)), balloon.balloon.posHprInterval(8.0, Point3(178, -189, 37), (0, 0, 0)), balloon.balloon.posHprInterval(6.5, Point3(241, -146, 45), (5, 2, 2)), balloon.balloon.posHprInterval(11.0, Point3(259, -95, 67), (180, -2, -2)), balloon.balloon.posHprInterval(5.5, Point3(252, -100, 95), (175, -4, 0)), balloon.balloon.posHprInterval(10.0, Point3(204, -125, 110), (0, 2, -2)), balloon.balloon.posHprInterval(4.5, Point3(182, -141, 140), (-2, -2, 2)), balloon.balloon.posHprInterval(21.5, Point3(198, -141, 175), (-70, 0, 0)), balloon.balloon.posHprInterval(15.0, Point3(196, -141, 205), (-25, 0, 0))))
    return flightPaths


def generateToonFlightPaths(balloon):
    toonFlightPaths = []
    toonFlightPaths.append(Sequence(Wait(0.5), base.localAvatar.posInterval(1.5, Point3(232, -262, 27)), base.localAvatar.posInterval(1.5, Point3(170, -252, 32)), base.localAvatar.posInterval(8.0, Point3(178, -189, 37)), base.localAvatar.posInterval(6.5, Point3(241, -146, 45)), base.localAvatar.posInterval(11.0, Point3(259, -95, 67)), base.localAvatar.posInterval(5.5, Point3(252, -100, 95)), base.localAvatar.posInterval(10.0, Point3(204, -125, 110)), base.localAvatar.posInterval(4.5, Point3(182, -141, 140)), base.localAvatar.posInterval(21.5, Point3(198, -141, 175)), base.localAvatar.posInterval(15.0, Point3(196, -141, 205))))
    return toonFlightPaths


def generateSpeechSequence(balloon):
    speechSequence = Sequence(Func(balloon.alec.setChatAbsolute, SlappySpeeches[0], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[1], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[2], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[3], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[4], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[5], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[6], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[7], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[8], CFSpeech | CFTimeout), Wait(9.5), Func(balloon.alec.setChatAbsolute, SlappySpeeches[9], CFSpeech | CFTimeout))
    return speechSequence
