class InteractableAI:
    def __init__(self):
        self.customerId = None

    def isOccupied(self):
        return self.customerId is not None

    def occupy(self, customerId):
        if self.isOccupied():
            return False
        self.customerId = customerId
        return True

    def verifyCustomer(self, customerId):
        return self.customerId == customerId

    def releaseCustomer(self):
        self.customerId = None

    def getCustomerId(self):
        return self.customerId