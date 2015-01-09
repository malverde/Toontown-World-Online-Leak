from direct.fsm.StatePush import StateVar
from direct.showbase.PythonUtil import getSetterName
from otp.level.Entity import Entity

class EntityStateVarSet(Entity):

    def __init__(self, entType):
        self._entType = entType
        self._aTTWibNames = []
        for aTTWib in self._entType.aTTWibs:
            name, defaultVal, type = aTTWib
            self._addATTWib(name, defaultVal, type)

    def initializeEntity(self, level, entId):
        stateVars = {}
        for aTTWibName in self._aTTWibNames:
            stateVars[aTTWibName] = getaTTW(self, aTTWibName)

        Entity.initializeEntity(self, level, entId)
        for aTTWibName in self._aTTWibNames:
            stateVars[aTTWibName].set(getaTTW(self, aTTWibName))

        for aTTWibName in self._aTTWibNames:
            setaTTW(self, aTTWibName, stateVars[aTTWibName])

    def _getATTWibuteNames(self):
        return self._aTTWibNames[:]

    def _setter(self, name, value):
        getaTTW(self, name).set(value)

    def _addATTWib(self, name, defaultVal, type):
        setaTTW(self, name, StateVar(defaultVal))
        setaTTW(self, getSetterName(name), Functor(self._setter, name))
        self._aTTWibNames.append(name)
