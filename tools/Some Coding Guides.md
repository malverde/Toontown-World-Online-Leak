NEW NPCS:

* Go to TTLocalizerEnglish.py
* CTRL + F and type in NPCToonNames
* Click Find Next
* number = ID for NPC and it is a important thing to remember
* Use any ID Number not currently used and type in the info for your new toon
* Go to NPCToons.py
* Find NPCToonDict
* Game will still find data, even when it's in a random spot in NPCToonDict

DNA Data Example:

1014: (-1,
lnames[1014],
('csl',
'l',
'l',
'm',
27,
27,
27,
27,
0,
0,
0,
0,
0,
0),
'm',
0,
NPC_REGULAR),

Explanation of DNA:

1014: // ID of the toon
(-1, // Zone ID of the NPC in the game. -1 is the number to use if you don't want it to show up anywhere
lnames[1014], // ID of the toon again, to get it's name
('dss', // Head type. First letter is species, second two are style
'l', // Torso type
'm', // Leg type
'm', // Gender. M = Boy, F = Girl
27, // Arm color 0 - 27
27, // Glove color. 0 - 27
27, // Leg color 0 - 27
27, // Head color 0 - 27
0, // Shirt ID
0, // Shirt coloring. 0 - 27
0, // Sleeve ID
0, // Sleeve coloring. 0 - 27 
0, // Shorts ID
0), // Shorts coloring. 0 - 27
'm', // Gender again. Make sure it is the same as above.
0, // Used in a building. 0 = No, 1 = Yes.
NPC_REGULAR) // This is the type of NPC so the game knows where it's used. Regular is shopkeepers and other.

How to Guide for DNA:

For the various lists of all head types, torso types, leg types, shirt IDs, short IDs, and sleeve IDs.

Species:
d = dog
c = cat
h = horse
m = mouse
r = rabbit
f = duck
p = monkey
b = bear
s = pig

Head types: (First letter = Species, Second letter = Head, Third letter = mouth) (l = large, s = small)
dls
dss
dsl
dll
cls
css
csl
cll
hls
hss
hsl
hll
mls
ms s
rls
rss
rsl
rll
fls
fss
fsl
fll
pls
pss
psl
pll
bls
bss
bsl
bll
sls
sss
ssl
sll

Torso types: (First letter = tallness, Second letter = wideness) (l = large, m = medium, s = small, d = fat)
ss
ms
ls
sd
md
ld
s
m
l

Leg types: (l = large, m = medium, s = small, d = fat)
s
m
l

* Save and do not close yet
* Find HQnpcFriends

Example:

1014: (ToontownBattleGlobals.DROP_TRACK,
0,
255,
5),

Walkthrough:

1014: // ID of the toon
(ToontownBattleGlobals.DROP_TRACK, // Gag track to use
0, // Gag level to use
255, // Damage from gag
5), // Star rating of SOS card


New ToonTasks:

There are two files to edit: TTLocalizerEnglish.py (in toontown.toonbase) and Quests.py (in toontown.quest)

TTLocalizerEnglish.py:

Here you need to edit/add the dialogue for the NPC chat. Here's an example of mine:

Code:
 13003: {GREETING: '',
         LEAVING: '',
         QUEST: 'Hello, there. A replica of Acorn Acres has been created right next to Acorn Acres. It is top secret, only available to the highest toons. I see you have reached 137 laff. Congratulations. Now, you must prove your worth. Go defeat 2000 cogs.',
         INCOMPLETE_PROGRESS: 'You still have some cogs left to bust!',
         COMPLETE: 'Congratulations! You are now permitted to enter the Secret City.'}}
GREETING and LEAVING are not required. QUEST is what the NPC says to you when you visit them. INCOMPLETE_PROGRESS is what the NPC says if you return to them without completing the task. COMPLETE is what the NPC says when you return a completed task.

Quests.py:

There are 3 things to edit here. First, you need to make sure there is a tier alloted to your spot. Second, you need to put in the actual coding for the task that includes the type of task, the NPC you visit for it, the rewards, and ties it to the dialogue you entered in TTLocalizerEnglish. Third up is the rewards system.

1. Tiers

Tiers are the spots that your tasks allocate. If you want to just edit a task or add on to a task, you can skip this step.

Code:
TT_TIER = 0
DD_TIER = 4
DG_TIER = 7
MM_TIER = 8
BR_TIER = 11
DL_TIER = 14
LAWBOT_HQ_TIER = 18
BOSSBOT_HQ_TIER = 32
SC_TIER = 49
ELDER_TIER = 100
If you want to add a new set of tasks to appear after Bossbot HQ, you need to move Elder Tier (the looping final set of tasks that is just for fun) up to slot 100 until you know how many tiers your tasks will encompass. (Bossbot HQ's tasks take up 17 slots, 32-48.) Then name your tier and have it equal 49, like so:

Code:
MYTIER_TIER = 49

2. Task information

For reference, here is the coding for my tasks.

Code:
    13000: (SC_TIER, Start, (VisitQuest,), Any, 2003, NA, 13001, TTLocalizer.QuestDialogDict[13000]),
    13001: (SC_TIER, Start, (LaffQuest,), Any, 2003, NA, 13002, TTLocalizer.QuestDialogDict[13001]),
    13002: (SC_TIER, Start, (VisitQuest,), Any, 2001, NA, 13003, TTLocalizer.QuestDialogDict[13002]),
    13003: (SC_TIER, Start, (CogQuest, Anywhere, 2000, Any), Any, 2001, 102, NA, TTLocalizer.QuestDialogDict[13003]) }
You need to put this information in for your tasks.

Color coded task 13003 with information:

(SC_TIER, Start, (CogQuest, Anywhere, 2000, Any), Any, 2001, 102, NA, TTLocalizer.QuestDialogDict[13003])

SC_TIER: This is the tier of your task. See step 1.
Start: Start or Obsolete. Start is active, obsolote means it won't appear.
CogQuest: Type of task. There are many types of tasks. CogQuest tasks are for defeating certain numbers of cogs.
Anywhere: Where the cogs need to be.
2000: How many cogs you need to defeat.
Any: What type of cog they need to be.
**NOTE** Most task types do not need these extra bits, but most cog type tasks do.
Any: I am not totally sure about this, but I believe this is the NPC ID that you can start the task with.
2001: This is the NPC ID of the toon you return to or visit when finishing a task.
102: This is the reward ID. See line 4539 of Quests.py
NA: This is the taskID that you move to when you're done with this one. This is how LOM links up his tasks of doom.
TTLocalizer.QuestDialogDict[13003]): This is just the task ID (it should be the same in both files) and it ties the dialogue to the task.

3. Rewards

The final thing is adding a reward. From line 4859 to line 4910 are the reward IDs of all the tasks. You need to add the reward ID to the tier of your edit, or add it into the tier that you created. Here's my rewards tier:

Code:
SC_TIER: (102,),
If the reward ID is already there, you needn't worry!


New Cog Phrases:

* Go to TTLocalizerEnglish.py 
* Find SuitAttackTaunts
* Go through each Suit Attack Name and add new phrases that match the attack
* When adding new Cog Phrases, remember to quote the phrase with ' ' or "" , and have a comma at the end of the line for the new phrase.
* Remember to close up the bracket for the Suit Attack name, so the source code won't crash.
