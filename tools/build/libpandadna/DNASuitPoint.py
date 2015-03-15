class DNASuitPoint:
    COMPONENT_CODE = 20
    STREET_POINT = 0
    FRONT_DOOR_POINT = 1
    SIDE_DOOR_POINT = 2
    COGHQ_IN_POINT = 3
    COGHQ_OUT_POINT = 4

    def __init__(self, index, pointType, pos, landmarkBuildingIndex=-1):
        self.index = index
        self.pointType = pointType
        self.pos = pos
        self.graphId = 0
        self.landmarkBuildingIndex = landmarkBuildingIndex

    def __str__(self):
        pointType = self.getPointType()
        if pointType == DNASuitPoint.STREET_POINT:
            pointTypeStr = 'STREET_POINT'
        elif pointType == DNASuitPoint.FRONT_DOOR_POINT:
            pointTypeStr = 'FRONT_DOOR_POINT'
        elif pointType == DNASuitPoint.SIDE_DOOR_POINT:
            pointTypeStr = 'SIDE_DOOR_POINT'
        elif pointType == DNASuitPoint.COGHQ_IN_POINT:
            pointTypeStr = 'COGHQ_IN_POINT'
        elif pointType == DNASuitPoint.COGHQ_OUT_POINT:
            pointTypeStr = 'COGHQ_OUT_POINT'
        else:
            pointTypeStr = '**invalid**'
        return 'DNASuitPoint index: %d, pointType: %s, pos: %s' % (
            self.getIndex(), pointTypeStr, self.getPos())

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def getGraphId(self):
        return self.graphId

    def getLandmarkBuildingIndex(self):
        return self.landmarkBuildingIndex

    def getPos(self):
        return self.pos

    def isTerminal(self):
        return self.pointType <= 2

    def setGraphId(self, id):
        self.graphId = id

    def setLandmarkBuildingIndex(self, index):
        self.landmarkBuildingIndex = index

    def setPointType(self, pointType):
        if isinstance(pointType, int):
            if type == DNASuitPoint.STREET_POINT:
                self.pointType = DNASuitPoint.STREET_POINT
            elif type == DNASuitPoint.FRONT_DOOR_POINT:
                self.pointType = DNASuitPoint.FRONT_DOOR_POINT
            elif pointType == DNASuitPoint.SIDE_DOOR_POINT:
                self.pointType = DNASuitPoint.SIDE_DOOR_POINT
            elif pointType == DNASuitPoint.COGHQ_IN_POINT:
                self.pointType = DNASuitPoint.COGHQ_IN_POINT
            elif pointType == DNASuitPoint.COGHQ_OUT_POINT:
                self.pointType = DNASuitPoint.COGHQ_OUT_POINT
            else:
                raise TypeError('%i is not a valid DNASuitPointType' % pointType)
        elif isinstance(pointType, str):
            if type == 'STREET_POINT':
                self.pointType = DNASuitPoint.STREET_POINT
            elif type == 'FRONT_DOOR_POINT':
                self.pointType = DNASuitPoint.FRONT_DOOR_POINT
            elif pointType == 'SIDE_DOOR_POINT':
                self.pointType = DNASuitPoint.SIDE_DOOR_POINT
            elif pointType == 'COGHQ_IN_POINT':
                self.pointType = DNASuitPoint.COGHQ_IN_POINT
            elif pointType == 'COGHQ_OUT_POINT':
                self.pointType = DNASuitPoint.COGHQ_OUT_POINT
            else:
                raise TypeError('%s is not a valid DNASuitPointType' % pointType)

    def getPointType(self):
        return self.pointType

    def setPos(self, pos):
        self.pos = pos
