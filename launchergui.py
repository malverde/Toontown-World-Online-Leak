#updater with GUI :D
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
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
from direct.task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from patcher import *
from direct.filter.CommonFilters import *
import sys
from random import randint
import direct.directbase.DirectStart
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import VirtualFileSystem
from panda3d.core import Multifile
from panda3d.core import Filename
import os

vfs = VirtualFileSystem.getGlobalPtr()
vfs.mount(Filename("phase_2.mf"), ".", VirtualFileSystem.MFReadOnly)
def start():
	os.system('gamelaunch.py')
	sys.exit()



ButtonImage = loader.loadModel("phase_2/models/gui/tt_m_gui_mat_nameShop.bam")
B1 = DirectButton(frameSize=None, text='Start Game', image=(ButtonImage.find('**/tt_t_gui_mat_namePanelSquareUp'), \
ButtonImage.find('**/tt_t_gui_mat_namePanelSquareDown'), ButtonImage.find('**/tt_t_gui_mat_namePanelSquareHover')), relief=None, command=start, text_pos=(0, -0.015), \
geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-0.37, 0, -0.93), text_scale=0.050, borderWidth=(0.13, 0.01), scale=.7) 


def update():
	import davidsgameupdater

ButtonImage = loader.loadModel("phase_2/models/gui/tt_m_gui_mat_nameShop.bam")
B2 = DirectButton(frameSize=None, text='Update Main Game', image=(ButtonImage.find('**/tt_t_gui_mat_namePanelSquareUp'), \
ButtonImage.find('**/tt_t_gui_mat_namePanelSquareDown'), ButtonImage.find('**/tt_t_gui_mat_namePanelSquareHover')), relief=None, command=update, text_pos=(0, -0.015), \
geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-0.77, 0, -0.93), text_scale=0.050, borderWidth=(0.13, 0.01), scale=.7) 


def updateph():
	import phaseupdater

ButtonImage = loader.loadModel("phase_2/models/gui/tt_m_gui_mat_nameShop.bam")
B3 = DirectButton(frameSize=None, text='Update Phase files', image=(ButtonImage.find('**/tt_t_gui_mat_namePanelSquareUp'), \
ButtonImage.find('**/tt_t_gui_mat_namePanelSquareDown'), ButtonImage.find('**/tt_t_gui_mat_namePanelSquareHover')), relief=None, command=updateph, text_pos=(0, -0.015), \
geom=None, pad=(0.01, 0.01), suppressKeys=0, pos = (-1.16, 0, -0.93), text_scale=0.050, borderWidth=(0.13, 0.01), scale=.7) 



run()
