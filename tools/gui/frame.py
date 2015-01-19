import wx
from gui.images import Background
from gui.buttons import *
import Queue
from launcher import messagetypes, localizer, settings
import webbrowser

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

class LauncherPanel(wx.Panel):
    LAUNCHER_DATA_CHECK = 1 # wx ID for the timer checking for new data
    LAUNCHER_DATA_CHECK_INTERVAL = 100 # check for new stuff every 100ms
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(900, 680))
        self.frame = parent
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self.xButton = XButton(self, pos=wx.Point(740, 49))

        self.bg = Background.Background.GetBitmap()

        self.label = TransparentText(self, wx.ID_ANY, pos=(548, 172), size=(187, 23))
        self.label.SetForegroundColour((255, 255, 255)) # TODO - better color

        self.progress = wx.Gauge(self, wx.ID_ANY, pos=(548, 192), range=100)
        self.progress.Hide()

        self.mButton = MButton(self, pos=wx.Point(685, 49))

        self.ubox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(515, 323), wx.Size(214, 29), wx.BORDER_NONE | wx.TE_RICH2 | wx.TE_PROCESS_ENTER)
        self.pbox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(515, 366), wx.Size(214, 29), wx.BORDER_NONE | wx.TE_RICH2 | wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)

        self.goButton = GoButton(self, wx.Point(747, 345))

        self.dragging = False

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseUp)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)

        self.inputPoll = wx.Timer(self, self.LAUNCHER_DATA_CHECK)
        self.Bind(wx.EVT_TIMER, self.PollInput, self.inputPoll)
        self.inputPoll.Start(self.LAUNCHER_DATA_CHECK_INTERVAL)

        self.versionLabel = TransparentText(self, wx.ID_ANY, pos=(100, 130), size=(187, 23))
        self.versionLabel.SetForegroundColour((255, 255, 255)) # TODO - better color
        version = 'dev'
        if settings.Version is not None:
            version = settings.Version
        self.versionLabel.SetLabel(localizer.GUI_VersionLabel % version)
        self.Show()
    
    ##########
    # Management of the transparent window shape
    ##########
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

    def OnMouseMove(self, event):
        if self.dragging: # Prevents the launcher from following the mouse when user has left the window
            mousePos = wx.GetMousePosition()
            mouseDelta = mousePos - self.lastMousePos
            self.GetParent().SetPosition(self.GetParent().GetPosition() + mouseDelta)
            self.lastMousePos = mousePos

    def OnMouseDown(self, event):
        self.lastMousePos = wx.GetMousePosition()
        self.dragging = True

    def OnMouseUp(self, event):
        self.dragging = False

    ##########
    # Data handler
    ##########
    def PollInput(self, evt):
        try:
            self.HandleInput(self.input.get(block=False))
        except Queue.Empty, e:
            pass

    def HandleInput(self, data):
        # We got something from the launcher object!
        if type(data) == tuple and len(data) > 0:
            msg = data[0]
        elif type(data) == int:
            msg = data

        if msg == messagetypes.LAUNCHER_ERROR:
            wx.MessageBox(data[1], localizer.GUI_Error, wx.OK | wx.ICON_ERROR)
            self.SetLoginControlsEditable(True)
        elif msg == messagetypes.LAUNCHER_VERSION_UPDATE:
            version = data[1]
            changelog = data[2]
            url = data[3]
            wx.MessageBox(localizer.LauncherUpdateAvailabile % (version, changelog), localizer.LauncherUpdateHeader, wx.OK | wx.ICON_ERROR)
            webbrowser.open(url)
            self.app.Exit()
        elif msg == messagetypes.LAUNCHER_REQUEST_TFA:
            dlg = wx.TextEntryDialog(self, data[1], localizer.GUI_TFA)
            if dlg.ShowModal() == wx.ID_OK:
                self.output.put(dlg.GetValue(), block=True, timeout=1.0)
            else:
                self.output.put(None, block=True, timeout=1.0) # send a None to say the user cancelled after TFA
                self.SetLoginControlsEditable(True)
        elif msg == messagetypes.LAUNCHER_STATUS:
            self.SetStatusLabel(data[1])
        elif msg == messagetypes.LAUNCHER_PROGRESS:
            self.progress.Show()
            self.progress.SetValue(int(data[1]))
        elif msg == messagetypes.LAUNCHER_PLAY_RETRY:
            dlg = wx.MessageDialog(self, localizer.GUI_CrashedQuestion, localizer.GUI_CrashedTitle, wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.output.put(True, block=True, timeout=1.0)
                dlg.Destroy()
            else:
                self.app.Exit()
        elif msg == messagetypes.LAUNCHER_ENABLE_CONTROLS:
            self.SetLoginControlsEditable(True)
        elif msg == messagetypes.LAUNCHER_CLEAR_PASSWORD:
            self.pbox.SetValue('')
        elif msg == messagetypes.LAUNCHER_HIDE:
            self.frame.Hide()
        elif msg == messagetypes.LAUNCHER_SHOW:
            self.frame.Show()
        elif msg == messagetypes.LAUNCHER_EXIT:
            self.app.Exit()


    ##########
    # Form helpers, etc
    ##########
    def OnEnterPressed(self, event):
        self.goButton.Clicked()

    def SetLoginControlsEditable(self, areEditable):
        self.ubox.SetEditable(areEditable)
        self.pbox.SetEditable(areEditable)
        self.goButton.enabled = areEditable
        # If we're editable now, also do some cleanup
        if areEditable:
            self.progress.Hide()
            self.SetStatusLabel('')

    def SetStatusLabel(self, text):
        self.label.SetLabel(text)

class LauncherFrame(wx.Frame):
    def __init__(self, parent, title, app, input, output):
        wx.Frame.__init__(self, parent, title=title, size=(900, 680), style= wx.FRAME_SHAPED | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_CHILDREN)

        self.SetDoubleBuffered(True)

        # Things like the XButton need access to the app, so that they can tell the app to exit
        self.panel = LauncherPanel(self)
        self.panel.app = app

        # output is how we send stuff to the launcher
        self.panel.output = output
        # input is how the launcher sends stuff to us
        self.panel.input = input

        self.Centre()

        shape = Background.Alpha.GetBitmap()
        shape.SetMask(wx.Mask(shape, wx.WHITE))
        self.SetShape(wx.RegionFromBitmap(shape))

        self.Show()
