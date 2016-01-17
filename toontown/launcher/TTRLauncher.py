from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from otp.launcher.LauncherBase import LauncherBase
import os
import sys
import time
import httplib, urllib, json
import shutil
import hashlib

class LogAndOutput:
	def __init__(self, orig, log):
		self.orig = orig
		self.log = log

	def write(self, str):
		self.log.write(str)
		self.log.flush()
		self.orig.write(str)
		self.orig.flush()

	def flush(self):
		self.log.flush()
		self.orig.flush()

class TTRLauncher(LauncherBase):
	notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDummyLauncher')


	def __init__(self):
		username = self.getPlayToken()
		password = raw_input('Password:   ')
		passwordencode = urllib.quote_plus(password)
		print passwordencode
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		print ("Sending username/password to server...")
		connection = httplib.HTTPConnection("www.toontownworldonline.com")
		connection.request("GET", "/api/login/login.php?username="+ username + "&password=" + passwordencode)
		response = connection.getresponse()

		data = response.read()
		# turn json into pythonic format
		formattedData = json.loads(data)
		if formattedData.get("success", True):
			# we now have a login, we can log in now.
			print("Success! Starting the game...")
			connection.close()
		elif formattedData.get("banned"): # We are banned RIP
			print("Sorry, you are banned from TTW!") # Lets be nice
			connection.close() # Close connection TO our API
			sys.exit() # And kill them so they cant log in
		else:
			# can't log in, probably because of invalid password
			print("Unable to log into the game. Reason: " + formattedData.get("reason", {}))
			connection.close()
			sys.exit()
			
		self.http = HTTPClient()

		self.logPrefix = 'ttw-'

		ltime = 1 and time.localtime()
		logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,  ltime[1], ltime[2],
												   ltime[3], ltime[4], ltime[5])

		
		if not os.path.exists('logs/'):
			os.mkdir('logs/')
			self.notify.info('Made new directory to save logs.')
		
		logfile = os.path.join('logs', self.logPrefix + logSuffix + '.log')

		log = open(logfile, 'a')
		logOut = LogAndOutput(sys.stdout, log)
		logErr = LogAndOutput(sys.stderr, log)
		sys.stdout = logOut
		sys.stderr = logErr

	def getPlayToken(self):
		return self.getValue('TTR_PLAYCOOKIE')

	def getGameServer(self):
		return self.getValue('TTR_GAMESERVER')

	def setPandaErrorCode(self, code):
		pass

	def getGame2Done(self):
		return True

	def getLogFileName(self):
		return 'toontown'

	def getValue(self, key, default = None):
		return os.environ.get(key, default)

	def setValue(self, key, value):
		os.environ[key] = str(value)

	def getVerifyFiles(self):
		return config.GetInt('launcher-verify', 0)

	def getTestServerFlag(self):
		return self.getValue('IS_TEST_SERVER', 0)

	def isDownloadComplete(self):
		return 1

	def isTestServer(self):
		return 0

	def getPhaseComplete(self, phase):
		print (phase)
		print "Checking for file patches!"
		patchmanifestRaw = urllib.urlopen("http://toontownworldonline.com/api/patcher.json").read()
		patchmanifest = json.loads(patchmanifestRaw)
		newFileComp = urllib.URLopener()
		if phase == 3.5:
			print "Checking phase 3.5"
			sha = hashlib.md5()
			try:
				file = open('phase_3.5.mf', "rb")
				sha.update(file.read())
				file.close()
				sha.hexdigest()
				if sha != patchmanifest["phase_3.5.mf"]["hash"]:
					newFileComp.retrieve("PATCHER_BACKEND" + "phase_3.5.mf", 'phase_3.5.mf')
				else:
					contine
				
			except IOError:
				newFileComp.retrieve("PATCHER_BACKEND" + "phase_3.mf", "phase_3.mf")
		if phase == 4:
			print "Checking phase 4"
			sha = hashlib.md5()
			try:
				file = open('phase_4.mf', "rb")
				sha.update(file.read())
				file.close()
				sha.hexdigest()
				if sha != patchmanifest["phase_4.mf"]["hash"]:
					newFileComp.retrieve("PATCHER_BACKEND" + "phase_4.mf", "phase_4.mf"
				else:
					continue
				
			except IOError:
				newFileComp.retrieve("PATCHER_BACKEND" + "phase_4.mf", "phase_4.mf")
		return 1

	def getPercentPhaseComplete(self, bytesWritten):
		if self.totalPatchDownload:
			return LauncherBase.getPercentPatchComplete(self, bytesWritten)
		else:
			return 0

	def startGame(self):
		self.newTaskManager()
		eventMgr.restart()
		from toontown.toonbase import ToontownStart
