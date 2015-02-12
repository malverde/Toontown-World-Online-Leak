from pandac.PandaModules import NodePath

from toontown.shtiker.CogMenuBar import CogMenuBar


class CogMenu(NodePath):
    def __init__(self):
        NodePath.__init__(self, 'CogMenu')

        self.sellbotBar = CogMenuBar(self, 's')
        self.cashbotBar = CogMenuBar(self, 'm')
        self.lawbotBar = CogMenuBar(self, 'l')
        self.bossbotBar = CogMenuBar(self, 'c')

        self.sellbotBar.setX(-0.502)
        self.lawbotBar.setX(0.502)
        self.bossbotBar.setX(1)

    def update(self):
        self.sellbotBar.update()
        self.cashbotBar.update()
        self.lawbotBar.update()
        self.bossbotBar.update()

    def cleanup(self):
        self.sellbotBar.cleanup()
        self.cashbotBar.cleanup()
        self.lawbotBar.cleanup()
        self.bossbotBar.cleanup()
        self.removeNode()