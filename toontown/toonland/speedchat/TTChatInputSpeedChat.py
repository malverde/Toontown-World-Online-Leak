########################## THE TOON LAND PROJECT ##########################
# Filename: TTChatInputSpeedChat.py
# Created by: Cody/Fd Green Cat Fd (February 11th, 2013)
####
# Description:
#
# Modifies the Speed Chat globals to contain some of our custom messages.
####

from otp.speedchat import SCStaticTextTerminal
from toontown.chat import TTChatInputSpeedChat

SCStaticTextTerminal.SpeedChatStaticText[31051] = 'Let\'s go to Funny Farm!'
scStructure = TTChatInputSpeedChat.scStructure[7][1]
scStructure = (scStructure[:9] + [31051] + scStructure[9:])
TTChatInputSpeedChat.scStructure[7][1] = scStructure