<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedDeliveryManager(DistributedObject):
    neverDisable = 1

    def sendHello(self, message):
        self.sendUpdate('hello', [message])

    def rejectHello(self, message):
        print 'rejected', message

    def helloResponse(self, message):
        print 'accepted', message

    def sendAck(self):
        self.sendUpdate('requestAck', [])

    def returnAck(self):
        messenger.send('DeliveryManagerAck')

    def test(self):
        print 'Distributed Delviery Manager Stub Test'
<<<<<<< HEAD
=======
from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedDeliveryManager(DistributedObject):
    neverDisable = 1

    def sendHello(self, message):
        self.sendUpdate('hello', [message])

    def rejectHello(self, message):
        print 'rejected', message

    def helloResponse(self, message):
        print 'accepted', message

    def sendAck(self):
        self.sendUpdate('requestAck', [])

    def returnAck(self):
        messenger.send('DeliveryManagerAck')

    def test(self):
        print 'Distributed Delviery Manager Stub Test'
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
