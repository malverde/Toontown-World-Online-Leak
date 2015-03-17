from direct.interval.IntervalGlobal import Sequence
from sys import argv
from direct.directbase import DirectStart
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

from direct.controls.GravityWalker import GravityWalker

from direct.interval.IntervalGlobal import *
import urllib, os, __main__, random
from pandac.PandaModules import *
from random import choice
base.disableMouse()
from direct.task import Task
import math
from math import pi, sin, cos

from direct.task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from direct.gui.DirectGui import *
from direct.actor.Actor import Actor

from direct.filter.CommonFilters import *
import sys
from random import randint
import direct.directbase.DirectStart
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText

import os


if (os.path.exists('GameData.pyd')):
	os.unlink('GameData.pyd')
 
def downloadTask(task):
	
	if channel.run():
		# Still waiting for file to finish downloading.
		return task.cont
	if not channel.isDownloadComplete():
		print "Error downloading file."
		return task.done
	data = rf.getData()
	print "got data:"
	print data
	return task.done
http = HTTPClient()
channel = http.makeChannel(True)
channel.beginGetDocument(DocumentSpec('https://toontownworldonline.com/download/GameData.pyd'))
rf = Ramfile()
channel.downloadToRam(rf)
channel.downloadToFile('GameData.pyd')
taskMgr.add(downloadTask, 'download')

import os


if (os.path.exists('GameData.so')):
	os.unlink('GameData.so')
 
def downloadTask(task):
	
	if channel.run():
		# Still waiting for file to finish downloading.
		return task.cont
	if not channel.isDownloadComplete():
		print "Error downloading file."
		return task.done
	data = rf.getData()
	print "got data:"
	print data
	return task.done
http = HTTPClient()
channel = http.makeChannel(True)
channel.beginGetDocument(DocumentSpec('https://toontownworldonline.com/download/GameData.so'))
rf = Ramfile()
channel.downloadToRam(rf)
channel.downloadToFile('GameData.so')
taskMgr.add(downloadTask, 'download')
