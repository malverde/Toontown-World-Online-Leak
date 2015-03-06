import simplejson
import os


class BackupManager:
    def __init__(self, filepath='backups', extension='.json'):
        self.filepath = filepath
        self.extension = extension

    def getFileName(self, category, info):
        filename = os.path.join(self.filepath, category) + '/'
        for i in info:
            filename += str(i) + '_'
        return filename[:-1] + self.extension

    def load(self, category, info, default=None):
        filename = self.getFileName(category, info)
        if not os.path.exists(filename):
            return default
        with open(filename, 'r') as f:
            return simplejson.load(f)

    def save(self, category, info, data):
        filepath = os.path.join(self.filepath, category)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = self.getFileName(category, info)
        with open(filename, 'w') as f:
            simplejson.dump(data, f)