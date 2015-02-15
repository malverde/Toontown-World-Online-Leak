########################## THE TOON LAND PROJECT ##########################
# Filename: TTSendBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the client to client communication. The networking source files
# are the only files that may stray from the programming standard.
####

from random import randrange
from toontown.toon.LocalToon import globalClockDelta

class TTSendBuffer:

    FormatMessage = 'a=%d;b=%d;c=\'%s\';d=%s;e=%s'

    def __init__(self):
        self.queued_messages    = []
        self.networking_objects = {}
        self.temporary_objects  = []

    def generateClientHeader(self):
        client_header = 'x\x8c'
        for iteration in range(4):
            client_header += chr(randrange(256))
        return client_header

    def sendMessage(self, id, name, args=[], send_to_id=None, has_persistence=False, reciever=None):
        if has_persistence == True:
            self.queued_messages.append((id, name, args, send_to_id))
        message = self.generateClientHeader()
        time_stamp = globalClockDelta.getRealNetworkTime()
        formatMessage = self.FormatMessage
        if reciever:
            formatMessage += ';f=' + str(reciever)
        message += HackerCrypt.encrypt(formatMessage % (time_stamp, id, name, args, send_to_id))
        base.localAvatar.d_setParent(message)

TTSendBuffer = TTSendBuffer()