import cPickle
import os


class BackupManager:
    def __init__(self, filepath='backups', extension='.bu'):
        self.filepath = filepath
        self.extension = extension
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

    def getFileName(self, category, info):
        filename = '{0}/{1}/{1}'.format(self.filepath, category)
        for i in info:
            filename += '_{0}'.format(i)
        filename += self.extension
        return filename

    def load(self, category, info, default=None):
        filename = self.getFileName(category, info)
        if not os.path.exists(filename):
            return default
        f = open(filename, 'r')
        data = cPickle.load(f)
        f.close()
        return data

    def save(self, category, info, data):
        filepath = '{0}/{1}'.format(self.filepath, category)
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        filename = self.getFileName(category, info)
        f = open(filename, 'w')
        cPickle.dump(data, f)
        f.close()
