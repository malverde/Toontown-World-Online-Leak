import httplib
import urllib
import wx
import json
import subprocess
import os
import sys
import threading
import ButtonGo, Background, ButtonX, ButtonMin
import json
import webbrowser
import urllib2

# First pass at a wxPython Toontown Rewritten launcher... basically converted from C++ to Python and ruined horribly in the process.

class ImageButton(wx.StaticBitmap):
    def __init__(self, parent, bitmap, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, name=""):
        wx.StaticBitmap.__init__(self, parent, id, bitmap, pos, size, style, name)
        self.normal = bitmap
        self.hover = None
        self.depressed = None
        self.isHovering = False
        self.isDepressed = False
        # At least we're not depressed.

        self.enabled = True

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

    def SetHoverBitmap(self, bitmap):
        self.hover = bitmap

    def SetDepressedBitmap(self, bitmap):
        self.depressed = bitmap

    def OnEnterWindow(self, event):
        self.isHovering = True
        if self.hover and not self.isDepressed and self.enabled:
            self.SetBitmap(self.hover)
            self.Refresh()

    def OnLeaveWindow(self, event):
        self.isHovering = False
        if not self.isDepressed:
            self.SetBitmap(self.normal)
            self.Refresh()

    def OnMouseDown(self, event):
        if not self.enabled:
            return
        self.isDepressed = True
        if self.depressed:
            self.SetBitmap(self.depressed)
            self.Refresh()

    def OnMouseUp(self, event):
        if not self.enabled:
            self.SetBitmap(self.normal)
            return
        self.isDepressed = False
        if self.isHovering and self.hover:
            self.SetBitmap(self.hover)
        else:
            self.SetBitmap(self.normal)
        if self.enabled:
            self.Clicked()
        self.Refresh()

    def Clicked(self):
        pass

class XButton(ImageButton):
    def __init__(self, parent, bitmap, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, bitmap, pos=pos, id=id)

    def Clicked(self):
        app.Exit()

class MButton(ImageButton):
    def __init__(self, parent, bitmap, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, bitmap, pos=pos, id=id)

    def Clicked(self):
        frame.Iconize()

# Thank you google for this. <3
# Used for one text field. ONE.
class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()

class GoButton(ImageButton):
    # TODO - learn enough wx to know if this actually does anything
    TIMER_UPDATE = 1
    TIMER_DELAY = 2

    def __init__(self, parent, bitmap, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, bitmap, pos=pos, id=id)
        self.connection = httplib.HTTPSConnection('www.toontownrewritten.com', 443)
        self.delayTimer = None

    def Clicked(self):
        if not self.enabled:
            return
        username = frame.panel.ubox.GetLineText(0)
        password = frame.panel.pbox.GetLineText(0)
        params = urllib.urlencode({'username': username, 'password': password})
        # Disable the editing of the login controls while we figure out if the credentials are good or not
        frame.panel.SetLoginControlsEditable(False)
        def donePatching():
            frame.panel.label.SetLabel("Contacting account server...")
            self.Request(params)
            frame.panel.SetLoginControlsEditable(self.enabled)
            frame.panel.label.SetLabel('')
            # If we're disabled and still waiting on a response, you can't edit login controls
        frame.panel.label.SetLabel('Locating patch mirrors...')
        self.Patch(donePatching)


    def Request(self, params):
        # This should implement the entire login API...
        self.enabled = False
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        try:
            self.connection.request('POST', '/api/login?format=json', params, headers)
            response = self.connection.getresponse()
        except:
            wx.MessageBox("Could not connect to account server.", "Error", wx.OK | wx.ICON_ERROR)
            self.enabled = True
            return

        if response.status != httplib.OK:
            # We couldn't connect. RIP.
            wx.MessageBox("Could not connect to account server.", "Error", wx.OK | wx.ICON_ERROR)
            self.enabled = True
            return
        try:
            loginResult = json.loads(response.read())
        except ValueError:
            wx.MessageBox('Account server provided invalid response!', 'Error', wx.OK | wx.ICON_ERROR)
            self.enabled = True
            return
        success = loginResult['success']
        if success == 'true':
            # Successful login - update the game and run.
            self.Run(loginResult['gameserver'], loginResult['cookie'])
        elif success == 'false':
            # Something went wrong, tell the user.
            wx.MessageBox(loginResult['banner'], 'Error', wx.OK | wx.ICON_ERROR)
            self.enabled = True
            return
        elif success == 'partial':
            # User has 2-factor on, prompt for verification and then request again.
            dlg = wx.TextEntryDialog(self, loginResult['banner'], 'Two-Factor Authentication')
            if dlg.ShowModal() == wx.ID_OK:
                newParams = urllib.urlencode({'appToken': dlg.GetValue(), 'authToken': loginResult['responseToken']})
                self.Request(newParams)
            else:
                # Oh, they decided they didn't want to.
                self.enabled = True
                return
        elif success == 'delayed':
            # There's a login queue... let's wait.
            self.queueToken = loginResult['queueToken']
            self.DoDelayed(loginResult['eta'], loginResult['position'])

    def DoDelayed(self, eta, position):
        #TODO - actually ETA and queue position.
        frame.panel.label.SetLabel('#%s in queue - %ss remaining' % (position, eta))
        self.delayTimer = wx.Timer(self, self.TIMER_DELAY)
        self.Bind(wx.EVT_TIMER, self.DelayUpdate, self.delayTimer)
        if int(eta) < 15:
            self.delayTimer.Start((int(eta) + 1)*1000, wx.TIMER_ONE_SHOT)
        else:
            self.delayTimer.Start(15000, wx.TIMER_ONE_SHOT)
        # Check back in 15s.

    def DelayUpdate(self, event):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        try:
            self.connection.request('POST', '/api/login?format=json', urllib.urlencode({'queueToken' : self.queueToken}), headers)
            response = self.connection.getresponse()
        except:
            wx.MessageBox("Could not connect to account server.", "Error", wx.OK | wx.ICON_ERROR)
            self.enabled = True
            return
        if response.status != httplib.OK:
            wx.MessageBox("Could not connect to account server.", "Error", wx.OK | wx.ICON_ERROR)
            #rip?
            self.enabled = True
            frame.panel.SetLoginControlsEditable(True)
            return
        try:
            loginResult = json.loads(response.read())
        except ValueError:
            wx.MessageBox('Account server provided an invalid response!', 'Error', wx.OK | wx.ICON_ERROR)
            self.enabled = True
            frame.panel.SetLoginControlsEditable(True)
            return
        success = loginResult['success']
        if success == 'true':
            self.Run(loginResult['gameserver'], loginResult['cookie'])
        elif success == 'delayed':
            #Update information eventually...
            frame.panel.label.SetLabel('#%s in queue - %ss remaining' % (loginResult['position'], loginResult['eta']))
            eta = int(loginResult['eta'])
            if eta < 15:
                self.delayTimer.Stop()
                self.delayTimer.Start((eta + 1)*1000, wx.TIMER_ONE_SHOT)
            else:
                self.delayTimer.Stop()
                self.delayTimer.Start(15000, wx.TIMER_ONE_SHOT)
        else:
            # This shouldn't happen... but just in case, inform the user.
            banner = loginResult.get('banner')
            if banner:
                wx.MessageBox(loginResult['banner'], 'Error', wx.OK | wx.ICON_ERROR)
            self.delayTimer.Stop()
            self.enabled = True
            frame.panel.SetLoginControlsEditable(True)

    def Run(self, gameserver, cookie):
        frame.panel.label.SetLabel('Have fun!')
        if self.delayTimer is not None:
            self.delayTimer.Stop()
        # Set environment variables...
        os.environ['TTR_PLAYCOOKIE'] = cookie
        os.environ['TTR_GAMESERVER'] = gameserver
        # Start the game...
        subprocess.Popen('TTREngine', creationflags=0x08000000)
        app.Exit()

    def Patch(self, callback):
        import Patcher
        self.Patcher = Patcher
        self._donePatchingCallback = callback
        self.numFiles = len(Patcher.MANIFEST)

        # Show the progress bar
        frame.panel.progress.Show()
        self.patcherThread = threading.Thread(target=Patcher.Patch, name="Patcher", args=(self.__updateProgress,))
        self.patcherThread.start()
        # Start the patcher

        # Maybe - patcher is py, integrate into launcher
        #self.process = subprocess.Popen('Patcher')
        self.updateTimer = wx.Timer(self, self.TIMER_UPDATE)
        self.Bind(wx.EVT_TIMER, self.UpdatePoll, self.updateTimer)
        self.updateTimer.Start(1000)

    def __updateProgress(self, percentage):
        frame.panel.progress.SetValue(int(percentage))

    def UpdatePoll(self, event):
        # TODO - text field for this to go rather than just updating the username box [lol]
        frame.panel.label.SetLabel('Updating File %d of %d' % (self.Patcher.count, self.numFiles))
        # TODO - show user progress in launcher
        finished = not self.patcherThread.isAlive()
        if finished:
            self.updateTimer.Stop()
            frame.panel.label.SetLabel('')
            frame.panel.progress.Hide()
            self._donePatchingCallback()



class LauncherPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(900, 680))
        self.frame = parent
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        xButtonImage = ButtonX.Normal.GetBitmap()
        xButtonImageHover = ButtonX.Hover.GetBitmap()
        xButtonImagePush = ButtonX.Depressed.GetBitmap()
        self.xButton = XButton(self, xButtonImage, pos=wx.Point(740, 49))
        self.xButton.SetHoverBitmap(xButtonImageHover)
        self.xButton.SetDepressedBitmap(xButtonImagePush)

        self.bg = Background.Background.GetBitmap()

        self.label = TransparentText(self, wx.ID_ANY, pos=(548, 172), size=(187, 23))
        self.label.SetForegroundColour((255, 255, 255)) # TODO - better color

        self.progress = wx.Gauge(self, wx.ID_ANY, pos=(548, 192), range=100)
        self.progress.Hide()

        mButtonImage = ButtonMin.Normal.GetBitmap()
        mButtonImageHover = ButtonMin.Hover.GetBitmap()
        mButtonImagePush = ButtonMin.Depressed.GetBitmap()

        self.mButton = MButton(self, mButtonImage, pos=wx.Point(685, 49))
        self.mButton.SetHoverBitmap(mButtonImageHover)
        self.mButton.SetDepressedBitmap(mButtonImagePush)

        self.ubox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(515, 323), wx.Size(214, 29), wx.BORDER_NONE | wx.TE_RICH2 | wx.TE_PROCESS_ENTER)
        self.pbox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(515, 366), wx.Size(214, 29), wx.BORDER_NONE | wx.TE_RICH2 | wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)


        goButtonImage = ButtonGo.Normal.GetBitmap()
        goButtonImageHover = ButtonGo.Hover.GetBitmap()
        goButtonImagePush = ButtonGo.Depressed.GetBitmap()
        self.goButton = GoButton(self, goButtonImage, wx.Point(747, 345))
        self.goButton.SetHoverBitmap(goButtonImageHover)
        self.goButton.SetDepressedBitmap(goButtonImagePush)

        self.dragging = False

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseUp)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)

        self.currentVersion = '1.0.2'
        self.versionLabel = TransparentText(self, wx.ID_ANY, pos=(100, 130), size=(187, 23))
        self.versionLabel.SetForegroundColour((255, 255, 255)) # TODO - better color
        self.versionLabel.SetLabel('TTR Launcher v%s' % self.currentVersion)
        self.Show()

        # Give this build a version
        self.checkForUpdates()

    def checkForUpdates(self):
        jsonData = [{}]
        try:
            response = urllib2.urlopen('https://download.toontownrewritten.com/launcher/windows/ttr_launcher.json')
            jsonData = json.load(response)
        except Exception, e:
            self.versionLabel.SetLabel('TTR Launcher v%s - Couldn\'t check for launcher updates!' % self.currentVersion)
            return

        version = jsonData[0].get('version', '')
        download = jsonData[0].get('update', '')
        rnotes = jsonData[0].get('rnotes', '')
        if not version == self.currentVersion:
            releaseNotes = "An update for the launcher is available!\n\n%s" % rnotes
            update = wx.MessageBox(releaseNotes, "Toontown Rewritten Launcher Update", wx.OK | wx.ICON_EXCLAMATION)
            webbrowser.open(download)

    def OnEraseBackground(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        dc.DrawBitmap(self.bg, 0, 0)
        bmp = Background.Background.GetBitmap()
        dc.DrawBitmap(bmp, 0, 0)

    def OnEnterPressed(self, event):
        self.goButton.Clicked()

    def OnMouseMove(self, event):
        if self.dragging:
            mousePos = wx.GetMousePosition()
            mouseDelta = mousePos - self.lastMousePos
            self.GetParent().SetPosition(self.GetParent().GetPosition() + mouseDelta)
            self.lastMousePos = mousePos

    def OnMouseDown(self,event):
        self.lastMousePos = wx.GetMousePosition()
        self.dragging = True

    def OnMouseUp(self, event):
        self.dragging = False

    def SetLoginControlsEditable(self, areEditable):
        self.ubox.SetEditable(areEditable)
        self.pbox.SetEditable(areEditable)

class LauncherFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900, 680), style= wx.FRAME_SHAPED | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_CHILDREN)
        self.SetDoubleBuffered(True)
        self.panel = LauncherPanel(self)
        self.Centre()
        shape = Background.Alpha.GetBitmap()
        shape.SetMask(wx.Mask(shape, wx.WHITE))
        self.SetShape(wx.RegionFromBitmap(shape))

        self.Show()

app = wx.App()
frame = LauncherFrame(None, 'Toontown Rewritten Launcher')
app.MainLoop()
