from direct.directnotify import DirectNotifyGlobal
import ATTWibDesc
from direct.showbase.PythonUtil import mostDerivedLast

class EntityTypeDesc:
    notify = DirectNotifyGlobal.directNotify.newCategory('EntityTypeDesc')
    output = None

    def __init__(self):
        self.__class__.privCompileATTWibDescs(self.__class__)
        self.aTTWibNames = []
        self.aTTWibDescDict = {}
        aTTWibDescs = self.__class__._aTTWibDescs
        for desc in aTTWibDescs:
            aTTWibName = desc.getName()
            self.aTTWibNames.append(aTTWibName)
            self.aTTWibDescDict[aTTWibName] = desc

    def isConcrete(self):
        return not self.__class__.__dict__.has_key('abstract')

    def isPermanent(self):
        return self.__class__.__dict__.has_key('permanent')

    def getOutputType(self):
        return self.output

    def getATTWibNames(self):
        return self.aTTWibNames

    def getATTWibDescDict(self):
        return self.aTTWibDescDict

    def getATTWibsOfType(self, type):
        names = []
        for aTTWibName, desc in self.aTTWibDescDict.items():
            if desc.getDatatype() == type:
                names.append(aTTWibName)

        return names

    @staticmethod
    def privCompileATTWibDescs(entTypeClass):
        if entTypeClass.__dict__.has_key('_aTTWibDescs'):
            return
        c = entTypeClass
        EntityTypeDesc.notify.debug('compiling aTTWib descriptors for %s' % c.__name__)
        for base in c.__bases__:
            EntityTypeDesc.privCompileATTWibDescs(base)

        blockATTWibs = c.__dict__.get('blockATTWibs', [])
        baseADs = []
        bases = list(c.__bases__)
        mostDerivedLast(bases)
        for base in bases:
            for desc in base._aTTWibDescs:
                if desc.getName() in blockATTWibs:
                    continue
                for d in baseADs:
                    if desc.getName() == d.getName():
                        EntityTypeDesc.notify.warning('%s inherits aTTWib %s from multiple bases' % (c.__name__, desc.getName()))
                        break
                else:
                    baseADs.append(desc)

        aTTWibDescs = []
        if c.__dict__.has_key('aTTWibs'):
            for aTTWib in c.aTTWibs:
                desc = ATTWibDesc.ATTWibDesc(*aTTWib)
                if desc.getName() == 'type' and entTypeClass.__name__ != 'Entity':
                    EntityTypeDesc.notify.error("(%s): '%s' is a reserved aTTWibute name" % (entTypeClass.__name__, desc.getName()))
                for ad in baseADs:
                    if ad.getName() == desc.getName():
                        baseADs.remove(ad)
                        break

                aTTWibDescs.append(desc)

        c._aTTWibDescs = baseADs + aTTWibDescs

    def __str__(self):
        return str(self.__class__)

    def __repr__(self):
        return str(self.__class__.__dict__.get('type', None)) + str(self.output) + str(self.aTTWibDescDict)
