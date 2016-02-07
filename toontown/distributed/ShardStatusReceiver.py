class ShardStatusReceiver:
    def __init__(self, air):
        self.air = air

        self.shards = {}

        # Accept the shardStatus event:
        self.air.accept('shardStatus', self.handleShardStatus)

        self.air.sendNetEvent('queryShardStatus')

    def handleShardStatus(self, channel, status):
        self.shards.setdefault(channel, {}).update(status)

    def getShards(self):
        return self.shards
