from pandac import PandaModules as PM
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import list2dict, uniqueElements
import string
import LevelConstants
import types
if __dev__:
    import os

class LevelSpec:
    notify = DirectNotifyGlobal.directNotify.newCategory('LevelSpec')
    SystemEntIds = (LevelConstants.UberZoneEntId, LevelConstants.LevelMgrEntId, LevelConstants.EditMgrEntId)

    def __init__(self, spec = None, scenario = 0):
        newSpec = 0
        if type(spec) is types.ModuleType:
            if __dev__:
                reload(spec)
            self.specDict = spec.levelSpec
            if __dev__:
                self.setFilename(spec.__file__)
        elif type(spec) is types.DictType:
            self.specDict = spec
        elif spec is None:
            if __dev__:
                newSpec = 1
                self.specDict = {'globalEntities': {},
                 'scenarios': [{}]}
        self.entId2specDict = {}
        self.entId2specDict.update(list2dict(self.getGlobalEntIds(), value=self.privGetGlobalEntityDict()))
        for i in range(self.getNumScenarios()):
            self.entId2specDict.update(list2dict(self.getScenarioEntIds(i), value=self.privGetScenarioEntityDict(i)))

        self.setScenario(scenario)
        if __dev__:
            if newSpec:
                import EntityTypes
                import EntityTypeRegistry
                etr = EntityTypeRegistry.EntityTypeRegistry(EntityTypes)
                self.setEntityTypeReg(etr)
                entId = LevelConstants.UberZoneEntId
                self.insertEntity(entId, 'zone')
                self.doSetATTWib(entId, 'name', 'UberZone')
                entId = LevelConstants.LevelMgrEntId
                self.insertEntity(entId, 'levelMgr')
                self.doSetATTWib(entId, 'name', 'LevelMgr')
                entId = LevelConstants.EditMgrEntId
                self.insertEntity(entId, 'editMgr')
                self.doSetATTWib(entId, 'name', 'EditMgr')
        return

    def destroy(self):
        del self.specDict
        del self.entId2specDict
        del self.scenario
        if hasaTTW(self, 'level'):
            del self.level
        if hasaTTW(self, 'entTypeReg'):
            del self.entTypeReg

    def getNumScenarios(self):
        return len(self.specDict['scenarios'])

    def setScenario(self, scenario):
        self.scenario = scenario

    def getScenario(self):
        return self.scenario

    def getGlobalEntIds(self):
        return self.privGetGlobalEntityDict().keys()

    def getScenarioEntIds(self, scenario = None):
        if scenario is None:
            scenario = self.scenario
        return self.privGetScenarioEntityDict(scenario).keys()

    def getAllEntIds(self):
        return self.getGlobalEntIds() + self.getScenarioEntIds()

    def getAllEntIdsFromAllScenarios(self):
        entIds = self.getGlobalEntIds()
        for scenario in xrange(self.getNumScenarios()):
            entIds.extend(self.getScenarioEntIds(scenario))

        return entIds

    def getEntitySpec(self, entId):
        specDict = self.entId2specDict[entId]
        return specDict[entId]

    def getCopyOfSpec(self, spec):
        specCopy = {}
        exec 'from %s import *' % self.getSpecImportsModuleName()
        for key in spec.keys():
            specCopy[key] = eval(repr(spec[key]))

        return specCopy

    def getEntitySpecCopy(self, entId):
        specDict = self.entId2specDict[entId]
        return self.getCopyOfSpec(specDict[entId])

    def getEntityType(self, entId):
        return self.getEntitySpec(entId)['type']

    def getEntityZoneEntId(self, entId):
        spec = self.getEntitySpec(entId)
        type = spec['type']
        if type == 'zone':
            return entId
        return self.getEntityZoneEntId(spec['parentEntId'])

    def getEntType2ids(self, entIds):
        entType2ids = {}
        for entId in entIds:
            type = self.getEntityType(entId)
            entType2ids.setdefault(type, [])
            entType2ids[type].append(entId)

        return entType2ids

    def privGetGlobalEntityDict(self):
        return self.specDict['globalEntities']

    def privGetScenarioEntityDict(self, scenario):
        return self.specDict['scenarios'][scenario]

    def printZones(self):
        allIds = self.getAllEntIds()
        type2id = self.getEntType2ids(allIds)
        zoneIds = type2id['zone']
        if 0 in zoneIds:
            zoneIds.remove(0)
        zoneIds.sort()
        for zoneNum in zoneIds:
            spec = self.getEntitySpec(zoneNum)
            print 'zone %s: %s' % (zoneNum, spec['name'])

    if __dev__:

        def setLevel(self, level):
            self.level = level

        def hasLevel(self):
            return hasaTTW(self, 'level')

        def setEntityTypeReg(self, entTypeReg):
            self.entTypeReg = entTypeReg
            for entId in self.getAllEntIds():
                spec = self.getEntitySpec(entId)
                type = self.getEntityType(entId)
                typeDesc = self.entTypeReg.getTypeDesc(type)
                aTTWibDescDict = typeDesc.getATTWibDescDict()
                for aTTWibName, desc in aTTWibDescDict.iteritems():
                    if aTTWibName not in spec:
                        spec[aTTWibName] = desc.getDefaultValue()

            self.checkSpecIntegrity()

        def hasEntityTypeReg(self):
            return hasaTTW(self, 'entTypeReg')

        def setFilename(self, filename):
            self.filename = filename

        def doSetATTWib(self, entId, aTTWib, value):
            specDict = self.entId2specDict[entId]
            specDict[entId][aTTWib] = value

        def setATTWibChange(self, entId, aTTWib, value, username):
            LevelSpec.notify.info('setATTWibChange(%s): %s, %s = %s' % (username,
             entId,
             aTTWib,
             repr(value)))
            self.doSetATTWib(entId, aTTWib, value)
            if self.hasLevel():
                self.level.handleATTWibChange(entId, aTTWib, value, username)

        def insertEntity(self, entId, entType, parentEntId = 'unspecified'):
            LevelSpec.notify.info('inserting entity %s (%s)' % (entId, entType))
            globalEnts = self.privGetGlobalEntityDict()
            self.entId2specDict[entId] = globalEnts
            globalEnts[entId] = {}
            spec = globalEnts[entId]
            aTTWibDescs = self.entTypeReg.getTypeDesc(entType).getATTWibDescDict()
            for name, desc in aTTWibDescs.items():
                spec[name] = desc.getDefaultValue()

            spec['type'] = entType
            if parentEntId != 'unspecified':
                spec['parentEntId'] = parentEntId
            if self.hasLevel():
                self.level.handleEntityInsert(entId)
            else:
                LevelSpec.notify.warning('no level to be notified of insertion')

        def removeEntity(self, entId):
            LevelSpec.notify.info('removing entity %s' % entId)
            if self.hasLevel():
                self.level.handleEntityRemove(entId)
            else:
                LevelSpec.notify.warning('no level to be notified of removal')
            dict = self.entId2specDict[entId]
            del dict[entId]
            del self.entId2specDict[entId]

        def removeZoneReferences(self, removedZoneNums):
            type2ids = self.getEntType2ids(self.getAllEntIdsFromAllScenarios())
            for type in type2ids:
                typeDesc = self.entTypeReg.getTypeDesc(type)
                visZoneListATTWibs = typeDesc.getATTWibsOfType('visZoneList')
                if len(visZoneListATTWibs) > 0:
                    for entId in type2ids[type]:
                        spec = self.getEntitySpec(entId)
                        for aTTWibName in visZoneListATTWibs:
                            for zoneNum in removedZoneNums:
                                while zoneNum in spec[aTTWibName]:
                                    spec[aTTWibName].remove(zoneNum)

        def getSpecImportsModuleName(self):
            return 'toontown.coghq.SpecImports'

        def getFilename(self):
            return self.filename

        def privGetBackupFilename(self, filename):
            return '%s.bak' % filename

        def saveToDisk(self, filename = None, makeBackup = 1):
            if filename is None:
                filename = self.filename
                if filename.endswith('.pyc'):
                    filename = filename.replace('.pyc', '.py')
            if makeBackup and self.privFileExists(filename):
                try:
                    backupFilename = self.privGetBackupFilename(filename)
                    self.privRemoveFile(backupFilename)
                    os.rename(filename, backupFilename)
                except OSError, e:
                    LevelSpec.notify.warning('error during backup: %s' % str(e))

            LevelSpec.notify.info("writing to '%s'" % filename)
            self.privRemoveFile(filename)
            self.privSaveToDisk(filename)
            return

        def privSaveToDisk(self, filename):
            retval = 1
            f = file(filename, 'wb')
            try:
                f.write(self.getPrettyString())
            except IOError:
                retval = 0

            f.close()
            return retval

        def privFileExists(self, filename):
            try:
                os.stat(filename)
                return 1
            except OSError:
                return 0

        def privRemoveFile(self, filename):
            try:
                os.remove(filename)
                return 1
            except OSError:
                return 0

        def getPrettyString(self):
            import pprint
            tabWidth = 4
            tab = ' ' * tabWidth
            globalEntitiesName = 'GlobalEntities'
            scenarioEntitiesName = 'Scenario%s'
            topLevelName = 'levelSpec'

            def getPrettyEntityDictStr(name, dict, tabs = 0):

                def t(n):
                    return (tabs + n) * tab

                def sortList(lst, firstElements = []):
                    elements = list(lst)
                    result = []
                    for el in firstElements:
                        if el in elements:
                            result.append(el)
                            elements.remove(el)

                    elements.sort()
                    result.extend(elements)
                    return result

                firstTypes = ('levelMgr', 'editMgr', 'zone')
                firstATTWibs = ('type', 'name', 'comment', 'parentEntId', 'pos', 'x', 'y', 'z', 'hpr', 'h', 'p', 'r', 'scale', 'sx', 'sy', 'sz', 'color', 'model')
                str = t(0) + '%s = {\n' % name
                entIds = dict.keys()
                entType2ids = self.getEntType2ids(entIds)
                types = sortList(entType2ids.keys(), firstTypes)
                for type in types:
                    str += t(1) + '# %s\n' % type.upper()
                    entIds = entType2ids[type]
                    entIds.sort()
                    for entId in entIds:
                        str += t(1) + '%s: {\n' % entId
                        spec = dict[entId]
                        aTTWibs = sortList(spec.keys(), firstATTWibs)
                        for aTTWib in aTTWibs:
                            str += t(2) + "'%s': %s,\n" % (aTTWib, repr(spec[aTTWib]))

                        str += t(2) + '}, # end entity %s\n' % entId

                str += t(1) + '}\n'
                return str

            def getPrettyTopLevelDictStr(tabs = 0):

                def t(n):
                    return (tabs + n) * tab

                str = t(0) + '%s = {\n' % topLevelName
                str += t(1) + "'globalEntities': %s,\n" % globalEntitiesName
                str += t(1) + "'scenarios': [\n"
                for i in range(self.getNumScenarios()):
                    str += t(2) + '%s,\n' % (scenarioEntitiesName % i)

                str += t(2) + '],\n'
                str += t(1) + '}\n'
                return str

            str = 'from %s import *\n' % self.getSpecImportsModuleName()
            str += '\n'
            str += getPrettyEntityDictStr('GlobalEntities', self.privGetGlobalEntityDict())
            str += '\n'
            numScenarios = self.getNumScenarios()
            for i in range(numScenarios):
                str += getPrettyEntityDictStr('Scenario%s' % i, self.privGetScenarioEntityDict(i))
                str += '\n'

            str += getPrettyTopLevelDictStr()
            self.testPrettyString(prettyString=str)
            return str

        def _recurKeyTest(self, dict1, dict2):
            s = ''
            errorCount = 0
            if set(dict1.keys()) != set(dict2.keys()):
                return 0
            for key in dict1:
                if type(dict1[key]) == type({}) and type(dict2[key]) == type({}):
                    if not self._recurKeyTest(dict1[key], dict2[key]):
                        return 0
                else:
                    strd1 = repr(dict1[key])
                    strd2 = repr(dict2[key])
                    if strd1 != strd2:
                        s += '\nBAD VALUE(%s): %s != %s\n' % (key, strd1, strd2)
                        errorCount += 1

            print s
            if errorCount == 0:
                return 1
            else:
                return 0

        def testPrettyString(self, prettyString = None):
            if prettyString is None:
                prettyString = self.getPrettyString()
            exec prettyString
            if self._recurKeyTest(levelSpec, self.specDict):
                return 1
            return

        def checkSpecIntegrity(self):
            entIds = self.getGlobalEntIds()
            entIds = list2dict(entIds)
            for i in range(self.getNumScenarios()):
                for id in self.getScenarioEntIds(i):
                    entIds[id] = None

            if self.entTypeReg is not None:
                allEntIds = entIds
                for entId in allEntIds:
                    spec = self.getEntitySpec(entId)
                    entType = spec['type']
                    typeDesc = self.entTypeReg.getTypeDesc(entType)
                    aTTWibNames = typeDesc.getATTWibNames()
                    aTTWibDescs = typeDesc.getATTWibDescDict()
                    for aTTWib in spec.keys():
                        if aTTWib not in aTTWibNames:
                            LevelSpec.notify.warning("entId %s (%s): unknown aTTWib '%s', omitting" % (entId, spec['type'], aTTWib))
                            del spec[aTTWib]

                    for aTTWibName in aTTWibNames:
                        if not spec.has_key(aTTWibName):
                            LevelSpec.notify.warning("entId %s (%s): missing aTTWib '%s'" % (entId, spec['type'], aTTWibName))

            return

        def stringHash(self):
            h = PM.HashVal()
            h.hashString(repr(self))
            return h.asHex()

        def __hash__(self):
            return hash(repr(self))

        def __str__(self):
            return 'LevelSpec'

        def __repr__(self):
            return 'LevelSpec(%s, scenario=%s)' % (repeatableRepr(self.specDict), repeatableRepr(self.scenario))
