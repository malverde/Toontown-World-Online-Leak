from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import lineInfo, Functor
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.level import Level
from otp.level import LevelConstants
from otp.level import Entity
from otp.level import EditMgr
from SpecImports import *
from InGameEditorElements import *
from toontown.cogdominium import CogdoEntityCreator
import string

class InGameEditorEntityBase(InGameEditorElement):
    def __init__(self):
        InGameEditorElement.__init__(self)

    def aTTWibChanged(self, aTTWib, value):
        Entity.Entity.aTTWibChanged(self, aTTWib, value)
        print 'aTTWibChange: %s %s, %s = %s' % (self.level.getEntityType(self.entId),
         self.entId,
         aTTWib,
         repr(value))

    def getTypeName(self):
        return self.level.getEntityType(self.entId)

    def privGetNamePrefix(self):
        return '[%s-%s] ' % (self.getTypeName(), self.entId)

    def privGetEntityName(self):
        return self.level.levelSpec.getEntitySpec(self.entId)['name']

    def getName(self):
        return '%s%s' % (self.privGetNamePrefix(), self.privGetEntityName())

    def setNewName(self, newName):
        prefix = self.privGetNamePrefix()
        if newName[:len(prefix)] == prefix:
            newName = newName[len(prefix):]
        oldName = self.privGetEntityName()
        if oldName != newName:
            self.level.setATTWibEdit(self.entId, 'name', newName)

    def setParentEntId(self, parentEntId):
        self.parentEntId = parentEntId
        self.level.buildEntityTree()

    def setName(self, name):
        self.name = name
        self.level.buildEntityTree()


class InGameEditorEntity(Entity.Entity, InGameEditorEntityBase):

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)

    def id(self):
        return self.entId

    def destroy(self):
        Entity.Entity.destroy(self)


class InGameEditorEditMgr(EditMgr.EditMgr, InGameEditorEntityBase):

    def __init__(self, level, entId):
        EditMgr.EditMgr.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)

    def destroy(self):
        EditMgr.EditMgr.destroy(self)


class ATTWibModifier(Entity.Entity, InGameEditorEntityBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ATTWibModifier')

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)

    def destroy(self):
        Entity.Entity.destroy(self)

    def setValue(self, value):
        if len(self.typeName) == 0:
            ATTWibModifier.notify.warning('no typeName set')
            return
        entTypeReg = self.level.entTypeReg
        if self.typeName not in entTypeReg.getAllTypeNames():
            ATTWibModifier.notify.warning('invalid typeName: %s' % self.typeName)
            return
        typeDesc = entTypeReg.getTypeDesc(self.typeName)
        if len(self.aTTWibName) == 0:
            ATTWibModifier.notify.warning('no aTTWibName set')
            return
        if self.aTTWibName not in typeDesc.getATTWibNames():
            ATTWibModifier.notify.warning('invalid aTTWibName: %s' % self.aTTWibName)
            return
        if len(value) == 0:
            ATTWibModifier.notify.warning('no value set')

        def setATTWib(entId, typeName = self.typeName, aTTWibName = self.aTTWibName, value = eval(value), recursive = self.recursive):
            if typeName == self.level.getEntityType(entId):
                self.level.setATTWibEdit(entId, aTTWibName, value)
            if recursive:
                entity = self.level.getEntity(entId)
                for child in entity.getChildren():
                    setATTWib(child.entId)

        setATTWib(self.parentEntId)


def getInGameEditorEntityCreatorClass(level):
    entCreator = level.createEntityCreator()
    EntCreatorClass = entCreator.__class__

    class InGameEditorEntityCreator(EntCreatorClass):

        def __init__(self, editor):
            EntCreatorClass.__init__(self, editor)
            entTypes = self.entType2Ctor.keys()
            for type in entTypes:
                self.entType2Ctor[type] = InGameEditorEntity

            self.entType2Ctor['editMgr'] = InGameEditorEditMgr
            self.entType2Ctor['aTTWibModifier'] = ATTWibModifier

    return InGameEditorEntityCreator


class DistributedInGameEditor(DistributedObject.DistributedObject, Level.Level, InGameEditorElement):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInGameEditor')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        Level.Level.__init__(self)
        InGameEditorElement.__init__(self)
        self.editorInitialized = 0
        self.specModified = 0
        self.undoStack = []
        self.redoStack = []
        self.entCreateHandlerQ = []
        self.entitiesWeCreated = []
        self.nodePathId2EntId = {}

    def generate(self):
        self.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)
        base.inGameEditor = self

    def setEditorAvId(self, editorAvId):
        self.editorAvId = editorAvId

    def setEditUsername(self, editUsername):
        self.editUsername = editUsername

    def getEditUsername(self):
        return self.editUsername

    def setLevelDoId(self, levelDoId):
        self.levelDoId = levelDoId
        self.level = base.cr.doId2do[self.levelDoId]

    def getLevelDoId(self):
        return self.levelDoId

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)
        if self.editorIsLocalToon():
            from otp.level import EditorGlobals
            EditorGlobals.assertReadyToEdit()
            self.notify.debug('requesting an up-to-date copy of the level spec')
            self.sendUpdate('requestCurrentLevelSpec')

    def setSpecSenderDoId(self, doId):
        DistributedInGameEditor.notify.debug('setSpecSenderDoId: %s' % doId)
        blobSender = base.cr.doId2do[doId]

        def setSpecBlob(specBlob, blobSender = blobSender, self = self):
            blobSender.sendAck()
            from otp.level.LevelSpec import LevelSpec
            curSpec = eval(specBlob)
            self.gotCurrentSpec(curSpec)

        if blobSender.isComplete():
            setSpecBlob(blobSender.getBlob())
        else:
            evtName = self.uniqueName('specDone')
            blobSender.setDoneEvent(evtName)
            self.acceptOnce(evtName, setSpecBlob)

    def gotCurrentSpec(self, curSpec):
        self.entTypeReg = self.level.getEntityTypeReg()
        curSpec.setEntityTypeReg(self.entTypeReg)
        self.axis = loader.loadModel('models/misc/xyzAxis')
        self.axis.setColorOff()
        self.axis.setColorScale(1, 1, 1, 1, 1)
        self.initializeLevel(self.doId, curSpec, curSpec.getScenario())
        entCreator = self.level.createEntityCreator()
        self.entTypes = entCreator.getEntityTypes()
        self.selectedEntity = None
        base.startTk()
        import InGameEditor
        doneEvent = self.uniqueName('editorDone')
        saveAsEvent = self.uniqueName('saveSpec')
        requestSaveEvent = self.uniqueName('requestSpecSave')
        undoEvent = self.uniqueName('undoEvent')
        redoEvent = self.uniqueName('redoEvent')
        wireframeEvent = self.uniqueName('wireframeEvent')
        oobeEvent = self.uniqueName('oobeEvent')
        csEvent = self.uniqueName('csEvent')
        runEvent = self.uniqueName('runEvent')
        texEvent = self.uniqueName('texEvent')
        self.editor = InGameEditor.InGameEditor(level=self, doneEvent=doneEvent, requestSaveEvent=requestSaveEvent, saveAsEvent=saveAsEvent, undoEvent=undoEvent, redoEvent=redoEvent, wireframeEvent=wireframeEvent, oobeEvent=oobeEvent, csEvent=csEvent, runEvent=runEvent, texEvent=texEvent)
        self.acceptOnce(doneEvent, self.doneEditing)
        self.accept(saveAsEvent, self.saveSpec)
        self.accept(requestSaveEvent, self.requestSpecSave)
        self.accept(undoEvent, self.doUndo)
        self.accept(redoEvent, self.doRedo)
        self.accept(wireframeEvent, self.doWireframe)
        self.accept(oobeEvent, self.doOobe)
        self.accept(csEvent, self.doCs)
        self.accept(runEvent, self.doRun)
        self.accept(texEvent, self.doTex)
        self.accept(self.editor.getEventMsgName('Select'), self.handleEntitySelect)
        self.accept(self.editor.getEventMsgName('Flash'), self.handleEntitySelect)
        self.editorInitialized = 1
        self.buildEntityTree()
        return

    def editorIsLocalToon(self):
        return self.editorAvId == base.localAvatar.doId

    def createEntityCreator(self):
        return getInGameEditorEntityCreatorClass(self.level)(self)

    def doneEditing(self):
        self.notify.debug('doneEditing')
        if self.specModified:
            if self.editor.askYesNo('Save the spec on the AI?'):
                self.requestSpecSave()
        self.sendUpdate('setFinished')

    def disable(self):
        self.notify.debug('disable')
        if self.editorInitialized and self.editorIsLocalToon():
            self.axis.removeNode()
            del self.axis
            if hasaTTW(self, 'entTypeReg'):
                del self.entTypeReg
            self.editorInitialized = 0
            Level.Level.destroyLevel(self)
            if hasaTTW(self, 'editor'):
                self.editor.quit()
                del self.editor
        DistributedObject.DistributedObject.disable(self)
        self.ignoreAll()

    def getEntInstance(self, entId):
        return self.level.getEntity(entId)

    def getEntInstanceNP(self, entId):
        entity = self.getEntInstance(entId)
        if entity is None:
            return
        if isinstance(entity, NodePath):
            return entity
        if hasaTTW(entity, 'getNodePath'):
            return entity.getNodePath()
        return

    def getEntInstanceNPCopy(self, entId):
        np = self.getEntInstanceNP(entId)
        if np is None:
            return np
        stashNodeGroups = []
        searches = ('**/+ActorNode', '**/+Character')
        for search in searches:
            stashNodeGroups.append(np.findAllMatches(search))

        for group in stashNodeGroups:
            if not group.isEmpty():
                group.stash()

        par = np.getParent()
        copy = np.copyTo(par)
        for group in stashNodeGroups:
            if not group.isEmpty():
                group.unstash()

        return copy

    def saveSpec(self, filename):
        return self.levelSpec.saveToDisk(filename)

    def setEntityParent(self, entity, parent):
        parent.addChild(entity)
        entity._parentEntity = parent

    def insertEntityIntoTree(self, entId):
        ent = self.getEntity(entId)
        if entId == LevelConstants.UberZoneEntId:
            self.setEntityParent(ent, self)
            return
        parentEnt = self.getEntity(ent.parentEntId)
        if parentEnt is not None:
            self.setEntityParent(ent, parentEnt)
            return
        self.setEntityParent(ent, self.uberZoneEntity)
        return

    def buildEntityTree(self):
        self.setChildren([])
        entIds = self.entities.keys()
        entIds.sort()
        for entId in entIds:
            ent = self.getEntity(entId)
            ent.setChildren([])

        for entId in entIds:
            self.insertEntityIntoTree(entId)

        self.editor.refreshExplorer()

    def onEntityCreate(self, entId):
        DistributedInGameEditor.notify.debug('onEntityCreate %s' % entId)
        Level.Level.onEntityCreate(self, entId)
        entityNP = self.getEntInstanceNP(entId)
        if entityNP:
            self.nodePathId2EntId[entityNP.id()] = entId
        if not self.editorInitialized:
            return
        self.insertEntityIntoTree(entId)
        self.editor.refreshExplorer()
        if entId == self.entitiesWeCreated[0]:
            self.entitiesWeCreated = self.entitiesWeCreated[1:]
            self.editor.selectEntity(entId)

    def onEntityDestroy(self, entId):
        DistributedInGameEditor.notify.debug('onEntityDestroy %s' % entId)
        ent = self.getEntity(entId)
        if self.editorInitialized:
            entityNP = self.getEntInstanceNP(entId)
            if entityNP in self.nodePathId2EntId:
                del self.nodePathId2EntId[entityNP.id()]
            if ent is self.selectedEntity:
                self.editor.clearATTWibEditPane()
                self.selectedEntity = None
            ent._parentEntity.removeChild(ent)
            del ent._parentEntity
            self.editor.refreshExplorer()
        Level.Level.onEntityDestroy(self, entId)
        return

    def handleEntitySelect(self, entity):
        self.selectedEntity = entity
        if hasaTTW(self, 'identifyIval'):
            self.identifyIval.finish()
        if entity is self:
            self.editor.clearATTWibEditPane()
        else:
            entityNP = self.getEntInstanceNP(entity.entId)
            if entityNP is not None:
                dur = float(0.5)
                oColor = entityNP.getColorScale()
                flashIval = Sequence(Func(Functor(entityNP.setColorScale, 1, 0, 0, 1)), WaitInterval(dur / 3), Func(Functor(entityNP.setColorScale, 0, 1, 0, 1)), WaitInterval(dur / 3), Func(Functor(entityNP.setColorScale, 0, 0, 1, 1)), WaitInterval(dur / 3), Func(Functor(entityNP.setColorScale, oColor[0], oColor[1], oColor[2], oColor[3])))
                boundIval = Sequence(Func(entityNP.showBounds), WaitInterval(dur * 0.5), Func(entityNP.hideBounds))
                entCp = self.getEntInstanceNPCopy(entity.entId)
                entCp.setRenderModeWireframe()
                entCp.setTextureOff(1)
                wireIval = Sequence(Func(Functor(entCp.setColor, 1, 0, 0, 1, 1)), WaitInterval(dur / 3), Func(Functor(entCp.setColor, 0, 1, 0, 1, 1)), WaitInterval(dur / 3), Func(Functor(entCp.setColor, 0, 0, 1, 1, 1)), WaitInterval(dur / 3), Func(entCp.removeNode))
                self.identifyIval = Parallel(flashIval, boundIval, wireIval)

                def putAxis(self = self, entityNP = entityNP):
                    self.axis.reparentTo(entityNP)
                    self.axis.setPos(0, 0, 0)
                    self.axis.setHpr(0, 0, 0)

                def takeAxis(self = self):
                    self.axis.reparentTo(hidden)

                self.identifyIval = Sequence(Func(putAxis), Parallel(self.identifyIval, WaitInterval(1000.5)), Func(takeAxis))
                self.identifyIval.start()
            self.editor.updateATTWibEditPane(entity.entId, self.levelSpec, self.entTypeReg)
            entType = self.getEntityType(entity.entId)
            menu = self.editor.menuBar.component('Entity-menu')
            index = menu.index('Remove Selected Entity')
            if entType in self.entTypeReg.getPermanentTypeNames():
                menu.entryconfigure(index, state='disabled')
            else:
                menu.entryconfigure(index, state='normal')
        return

    def privSendATTWibEdit(self, entId, aTTWib, value):
        self.specModified = 1
        valueStr = repr(value)
        self.notify.debug("sending edit: %s: '%s' = %s" % (entId, aTTWib, valueStr))
        self.sendUpdate('setEdit', [entId,
         aTTWib,
         valueStr,
         self.editUsername])

    def privExecActionList(self, actions):
        for action in actions:
            if callable(action):
                action()
            else:
                entId, aTTWib, value = action
                self.privSendATTWibEdit(entId, aTTWib, value)

    def setUndoableATTWibEdit(self, old2new, new2old):
        self.redoStack = []
        self.undoStack.append((new2old, old2new))
        self.privExecActionList(old2new)

    def setATTWibEdit(self, entId, aTTWib, value, canUndo = 1):
        oldValue = eval(repr(self.levelSpec.getEntitySpec(entId)[aTTWib]))
        new2old = [(entId, aTTWib, oldValue)]
        old2new = [(entId, aTTWib, value)]
        self.setUndoableATTWibEdit(old2new, new2old)
        if not canUndo:
            self.undoStack = []

    def doUndo(self):
        if len(self.undoStack) == 0:
            self.editor.showWarning('Nothing left to undo')
            return
        undo = self.undoStack.pop()
        self.redoStack.append(undo)
        new2old, old2new = undo
        self.privExecActionList(new2old)

    def doRedo(self):
        if len(self.redoStack) == 0:
            self.editor.showWarning('Nothing to redo')
            return
        redo = self.redoStack.pop()
        self.undoStack.append(redo)
        new2old, old2new = redo
        self.privExecActionList(old2new)

    def doWireframe(self):
        messenger.send('magicWord', ['~wire'])

    def doOobe(self):
        messenger.send('magicWord', ['~oobe'])

    def doCs(self):
        messenger.send('magicWord', ['~cs'])

    def doRun(self):
        messenger.send('magicWord', ['~run'])

    def doTex(self):
        messenger.send('magicWord', ['~tex'])

    def insertEntity(self, entType, parentEntId = None, callback = None):
        if parentEntId is None:
            try:
                parentEntId = self.selectedEntity.entId
            except ATTWibuteError:
                self.editor.showWarning('Please select a valid parent entity first.', 'error')
                return

        removeAction = (self.editMgrEntity.entId, 'removeEntity', {'entId': 'REPLACEME'})
        new2old = [removeAction]

        def setNewEntityId(entId, self = self, action = removeAction, callback = callback):
            action[2]['entId'] = entId
            if callback:
                callback(entId)

        def setEntCreateHandler(self = self, handler = setNewEntityId):
            self.entCreateHandlerQ.append(handler)

        old2new = [setEntCreateHandler, (self.editMgrEntity.entId, 'requestNewEntity', {'entType': entType,
           'parentEntId': parentEntId,
           'username': self.editUsername})]
        self.setUndoableATTWibEdit(old2new, new2old)
        return

    def setEntityCreatorUsername(self, entId, editUsername):
        Level.Level.setEntityCreatorUsername(self, entId, editUsername)
        if editUsername == self.getEditUsername():
            print 'entity %s about to be created; we requested it' % entId
            callback = self.entCreateHandlerQ[0]
            del self.entCreateHandlerQ[:1]
            callback(entId)
            self.entitiesWeCreated.append(entId)

    def removeSelectedEntity(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity to be removed first.', 'error')
            return -1

        if self.getEntity(selectedEntId).getNumChildren() > 0:
            self.editor.showWarning('Remove children first.')
            return -1
        self.doRemoveEntity(selectedEntId)

    def removeSelectedEntityTree(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity to be removed first.', 'error')
            return -1

        def removeEntity(entId):
            entity = self.getEntity(entId)
            for child in entity.getChildren():
                removeEntity(child.entId)

            self.doRemoveEntity(entId)

        removeEntity(selectedEntId)

    def doRemoveEntity(self, entId):
        parentEntId = self.getEntity(entId)._parentEntity.entId
        entType = self.getEntityType(entId)
        if entType in self.entTypeReg.getPermanentTypeNames():
            self.editor.showWarning("Cannot remove entities of type '%s'" % entType)
            return
        removeAction = (self.editMgrEntity.entId, 'removeEntity', {'entId': entId})
        old2new = [removeAction]
        oldATTWibs = []
        spec = self.levelSpec.getEntitySpecCopy(entId)
        del spec['type']
        for aTTWib, value in spec.items():
            oldATTWibs.append((aTTWib, value))

        def setNewEntityId(entId, self = self, removeAction = removeAction, oldATTWibs = oldATTWibs):
            removeAction[2]['entId'] = entId
            for aTTWib, value in spec.items():
                self.privSendATTWibEdit(entId, aTTWib, value)

        def setEntCreateHandler(self = self, handler = setNewEntityId):
            self.entCreateHandlerQ.append(handler)

        new2old = [setEntCreateHandler, (self.editMgrEntity.entId, 'requestNewEntity', {'entType': self.getEntityType(entId),
           'parentEntId': parentEntId,
           'username': self.editUsername})]
        self.setUndoableATTWibEdit(old2new, new2old)

    def makeCopyOfEntName(self, name):
        prefix = 'copy of '
        suffix = ' (%s)'
        oldName = name
        if len(oldName) <= len(prefix):
            newName = prefix + oldName
        elif oldName[:len(prefix)] != prefix:
            newName = prefix + oldName
        else:
            hasSuffix = True
            copyNum = 2
            if oldName[-1] != ')':
                hasSuffix = False
            if hasSuffix and oldName[-2] in string.digits:
                i = len(oldName) - 2
                numString = ''
                while oldName[i] in string.digits:
                    numString = oldName[i] + numString
                    i -= 1

                if oldName[i] != '(':
                    hasSuffix = False
                else:
                    i -= 1
                    if oldName[i] != ' ':
                        hasSuffix = False
                    else:
                        print 'numString: %s' % numString
                        copyNum = int(numString) + 1
            if hasSuffix:
                newName = oldName[:i] + suffix % copyNum
            else:
                newName = oldName + suffix % copyNum
        return newName

    def duplicateSelectedEntity(self):
        try:
            selectedEntId = self.selectedEntity.entId
            parentEntId = self.selectedEntity._parentEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity to be removed first.', 'error')
            return

        if self.selectedEntity.getNumChildren() > 0:
            self.editor.showTodo('Cannot duplicate entity with children.')
            return
        removeAction = (self.editMgrEntity.entId, 'removeEntity', {'entId': selectedEntId})
        new2old = [removeAction]
        copyATTWibs = self.levelSpec.getEntitySpecCopy(selectedEntId)
        copyATTWibs['comment'] = ''
        copyATTWibs['name'] = self.makeCopyOfEntName(copyATTWibs['name'])
        typeDesc = self.entTypeReg.getTypeDesc(copyATTWibs['type'])
        aTTWibDescs = typeDesc.getATTWibDescDict()
        for aTTWibName, aTTWibDesc in aTTWibDescs.items():
            if aTTWibDesc.getDatatype() == 'const':
                del copyATTWibs[aTTWibName]

        def setNewEntityId(entId, self = self, removeAction = removeAction, copyATTWibs = copyATTWibs):
            removeAction[2]['entId'] = entId
            for aTTWibName, value in copyATTWibs.items():
                self.privSendATTWibEdit(entId, aTTWibName, value)

        def setEntCreateHandler(self = self, handler = setNewEntityId):
            self.entCreateHandlerQ.append(handler)

        old2new = [setEntCreateHandler, (self.editMgrEntity.entId, 'requestNewEntity', {'entType': self.getEntityType(selectedEntId),
           'parentEntId': parentEntId,
           'username': self.editUsername})]
        self.setUndoableATTWibEdit(old2new, new2old)

    def specPrePickle(self, spec):
        for aTTWibName, value in spec.items():
            spec[aTTWibName] = repr(value)

        return spec

    def specPostUnpickle(self, spec):
        for aTTWibName, value in spec.items():
            spec[aTTWibName] = eval(value)

        return spec

    def handleImportEntities(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity first.', 'error')
            return

        import tkFileDialog
        filename = tkFileDialog.askopenfilename(parent=self.editor.parent, defaultextension='.egroup', filetypes=[('Entity Group', '.egroup'), ('All Files', '*')])
        if len(filename) == 0:
            return
        try:
            import pickle
            f = open(filename, 'r')
            eTree = pickle.load(f)
            eGroup = pickle.load(f)
            for entId, spec in eGroup.items():
                eGroup[entId] = self.specPostUnpickle(spec)

        except:
            self.editor.showWarning("Error importing entity group from '%s'." % filename, 'error')
            return

        oldEntId2new = {}

        def addEntities(treeEntry, parentEntId, eGroup = eGroup):
            for entId, children in treeEntry.items():
                spec = eGroup[entId]
                entType = spec['type']
                del spec['type']
                del spec['parentEntId']
                typeDesc = self.entTypeReg.getTypeDesc(entType)
                for aTTWibName, aTTWibDesc in typeDesc.getATTWibDescDict().items():
                    if aTTWibDesc.getDatatype() == 'const':
                        if aTTWibName in spec:
                            del spec[aTTWibName]

                def handleEntityInsertComplete(newEntId, oldEntId = entId, oldEntId2new = oldEntId2new, spec = spec, treeEntry = treeEntry, addEntities = addEntities):
                    oldEntId2new[oldEntId] = newEntId

                    def assignATTWibs(entId = newEntId, oldEntId = oldEntId, spec = spec, treeEntry = treeEntry):
                        for aTTWibName in spec:
                            self.setATTWibEdit(entId, aTTWibName, spec[aTTWibName])

                        addEntities(treeEntry[oldEntId], newEntId)

                    self.acceptOnce(self.getEntityCreateEvent(newEntId), assignATTWibs)

                self.insertEntity(entType, parentEntId=parentEntId, callback=handleEntityInsertComplete)

        addEntities(eTree, selectedEntId)

    def handleExportEntity(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity first.', 'error')
            return

        import tkFileDialog
        filename = tkFileDialog.asksaveasfilename(parent=self.editor.parent, defaultextension='.egroup', filetypes=[('Entity Group', '.egroup'), ('All Files', '*')])
        if len(filename) == 0:
            return
        eTree = {selectedEntId: {}}
        eGroup = {}
        eGroup[selectedEntId] = self.levelSpec.getEntitySpecCopy(selectedEntId)
        for entId, spec in eGroup.items():
            eGroup[entId] = self.specPrePickle(spec)

        try:
            import pickle
            f = open(filename, 'w')
            pickle.dump(eTree, f)
            pickle.dump(eGroup, f)
        except:
            self.editor.showWarning("Error exporting entity group to '%s'." % filename, 'error')
            return

    def handleExportEntityTree(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity first.', 'error')
            return

        import tkFileDialog
        filename = tkFileDialog.asksaveasfilename(parent=self.editor.parent, defaultextension='.egroup', filetypes=[('Entity Group', '.egroup'), ('All Files', '*')])
        if len(filename) == 0:
            return
        eTree = {}
        eGroup = {}

        def addEntity(entId, treeEntry):
            treeEntry[entId] = {}
            eGroup[entId] = self.levelSpec.getEntitySpecCopy(entId)
            entity = self.getEntity(entId)
            for child in entity.getChildren():
                addEntity(child.entId, treeEntry[entId])

        addEntity(selectedEntId, eTree)
        for entId, spec in eGroup.items():
            eGroup[entId] = self.specPrePickle(spec)

        try:
            import pickle
            f = open(filename, 'w')
            pickle.dump(eTree, f)
            pickle.dump(eGroup, f)
        except:
            self.editor.showWarning("Error exporting entity group to '%s'." % filename, 'error')
            return

    def moveAvToSelected(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except ATTWibuteError:
            self.editor.showWarning('Please select a valid entity first.', 'error')
            return

        entNp = self.getEntInstanceNP(selectedEntId)
        if entNp is None:
            zoneEntId = self.levelSpec.getEntityZoneEntId(selectedEntId)
            entNp = self.getEntInstanceNP(zoneEntId)
        base.localAvatar.setPos(entNp, 0, 0, 0)
        base.localAvatar.setHpr(entNp, 0, 0, 0)
        zoneNum = self.getEntityZoneEntId(selectedEntId)
        self.level.enterZone(zoneNum)
        return

    def requestSpecSave(self):
        self.privSendATTWibEdit(LevelConstants.EditMgrEntId, 'requestSave', None)
        self.specModified = 0
        return

    def setATTWibChange(self, entId, aTTWib, valueStr, username):
        if username == self.editUsername:
            print 'we got our own edit back!'
        value = eval(valueStr)
        self.levelSpec.setATTWibChange(entId, aTTWib, value, username)

    def getTypeName(self):
        return 'Level'
