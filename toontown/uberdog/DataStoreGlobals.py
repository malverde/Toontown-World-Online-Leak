<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from toontown.uberdog.ScavengerHuntDataStore import *
from toontown.uberdog.DataStore import *
SH = 1
GEN = 2
TYPES = {SH: (ScavengerHuntDataStore,),
 GEN: (DataStore,)}

def getStoreClass(type):
    storeClass = TYPES.get(type, None)
    if storeClass:
        return storeClass[0]
    return
<<<<<<< HEAD
=======
from toontown.uberdog.ScavengerHuntDataStore import *
from toontown.uberdog.DataStore import *
SH = 1
GEN = 2
TYPES = {SH: (ScavengerHuntDataStore,),
 GEN: (DataStore,)}

def getStoreClass(type):
    storeClass = TYPES.get(type, None)
    if storeClass:
        return storeClass[0]
    return
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
