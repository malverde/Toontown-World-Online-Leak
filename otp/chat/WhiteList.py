from bisect import bisect_left


class WhiteList:
    def __init__(self, words):
        self.words = words
        self.numWords = len(self.words)

    def cleanText(self, text):
        text = text.strip('.,?!')
        return text.lower()

    def isWord(self, text):
        return self.cleanText(text) in self.words

    def isPrefix(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)

        if i == self.numWords:
            return False

        return self.words[i].startswith(text)
