from otp.chat.WhiteList import WhiteList
from toontown.toonbase import TTLocalizer
from toontown.chat import WhiteListData


class TTWhiteList(WhiteList):
    notify = directNotify.newCategory('TTWhiteList')

    def __init__(self):
        WhiteList.__init__(self, WhiteListData.WHITELIST)

        self.defaultWord = TTLocalizer.ChatGarblerDefault[0]
