from direct.fsm.StatePush import FunctionCall
from otp.level.EntityStateVarSet import EntityStateVarSet
from otp.level.LevelSpec import LevelSpec

class CogdoLevelGameBase:

    def getLevelSpec(self):
        return LevelSpec(self.getSpec())

    if __dev__:

        def startHandleEdits(self):
            fcs = []
            Consts = self.getConsts()
            for item in Consts.__dict__.itervalues():
                if isinstance(item, EntityStateVarSet):
                    for aTTWibName in item._getATTWibuteNames():
                        handler = getaTTW(self, '_handle%sChanged' % aTTWibName, None)
                        if handler:
                            stateVar = getaTTW(item, aTTWibName)
                            fcs.append(FunctionCall(handler, stateVar))

            self._functionCalls = fcs
            return

        def stopHandleEdits(self):
            if __dev__:
                for fc in self._functionCalls:
                    fc.destroy()

                self._functionCalls = None
            return

        def getEntityTypeReg(self):
            import CogdoEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(CogdoEntityTypes)
            return typeReg
