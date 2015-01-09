from launcher.launcher import TTRLauncher
import threading
import Queue # python stdlib

guiToLauncher = Queue.Queue()
launcherToGui = Queue.Queue()

launcher = TTRLauncher(input=guiToLauncher, output=launcherToGui)
launcherThread = threading.Thread(target=TTRLauncher.start, name="Launcher-Thread", args=(launcher,))
launcherThread.daemon = True
launcherThread.start()

import wx
from gui.frame import LauncherFrame
app = wx.App()
from launcher import localizer
frame = LauncherFrame(None, localizer.GUI_WindowTitle, app=app, input=launcherToGui, output=guiToLauncher)
app.MainLoop()
