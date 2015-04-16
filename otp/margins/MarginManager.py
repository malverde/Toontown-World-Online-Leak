# Embedded file name: otp\margins\MarginManager.py
from pandac.PandaModules import *
from MarginCell import MarginCell
import random

class MarginManager(PandaNode):

    def __init__(self):
        PandaNode.__init__(self, 'margins')
        self.cells = set()
        self.visiblePopups = set()

    def addGridCell(self, x, y, a2d):
        nodePath = NodePath.anyPath(self)
        a2d.reparentTo(nodePath)
        cell = MarginCell(self)
        cell.reparentTo(a2d)
        cell.setScale(0.2)
        cell.setPos(x, 0, y)
        cell.setAvailable(True)
        cell.setPythonTag('MarginCell', cell)
        self.cells.add(cell)
        self.reorganize()
        return cell

    def setCellAvailable(self, cell, available):
        cell = cell.getPythonTag('MarginCell')
        cell.setAvailable(available)
        self.reorganize()

    def addVisiblePopup(self, popup):
        self.visiblePopups.add(popup)
        self.reorganize()

    def removeVisiblePopup(self, popup):
        if popup not in self.visiblePopups:
            return
        self.visiblePopups.remove(popup)
        self.reorganize()

    def reorganize(self):
        activeCells = [ cell for cell in self.cells if cell.isAvailable() ]
        popups = list(self.visiblePopups)
        popups.sort(key=lambda x: -x.getPriority())
        popups = popups[:len(activeCells)]
        freeCells = []
        for cell in activeCells:
            if not cell.hasContent():
                freeCells.append(cell)
            elif cell.getContent() in popups:
                popups.remove(cell.getContent())
            else:
                cell.setContent(None)
                freeCells.append(cell)

        raise len(freeCells) >= len(popups) or AssertionError
        for popup in popups:
            if popup._lastCell in freeCells and popup._lastCell.isFree():
                popup._lastCell.setContent(popup)
                freeCells.remove(popup._lastCell)
            else:
                cell = random.choice(freeCells)
                cell.setContent(popup)
                freeCells.remove(cell)

        return