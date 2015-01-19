import wx

class ImageButton(wx.StaticBitmap):
    def __init__(self, parent, bitmap, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, name=""):
        wx.StaticBitmap.__init__(self, parent, id, bitmap, pos, size, style, name)
        self.parent = parent

        self.normal = bitmap
        self.hover = None
        self.depressed = None
        self.isHovering = False
        self.isDepressed = False

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
        pass # To be overridden

# gui.images contains classes such as ButtonX, ButtonGo, and ButtonMin
# the actual classes just contain base64'd versions of the launcher art 
# each class contains the version of the button in all 3 states: normal, hover, depressed
from gui.images import ButtonX, ButtonMin, ButtonGo

class XButton(ImageButton):
    def __init__(self, parent, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, ButtonX.Normal.GetBitmap(), pos=pos, id=id)
        self.SetHoverBitmap(ButtonX.Hover.GetBitmap())
        self.SetDepressedBitmap(ButtonX.Depressed.GetBitmap())

    def Clicked(self):
        self.parent.app.Exit()


class MButton(ImageButton):
    def __init__(self, parent, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, ButtonMin.Normal.GetBitmap(), pos=pos, id=id)
        self.SetHoverBitmap(ButtonMin.Hover.GetBitmap())
        self.SetDepressedBitmap(ButtonMin.Depressed.GetBitmap())

    def Clicked(self):
        self.parent.frame.Iconize()


import launcher.localizer
class GoButton(ImageButton):
    def __init__(self, parent, pos=wx.DefaultPosition, id=wx.ID_ANY):
        ImageButton.__init__(self, parent, ButtonGo.Normal.GetBitmap(), pos=pos, id=id)
        self.SetHoverBitmap(ButtonGo.Hover.GetBitmap())
        self.SetDepressedBitmap(ButtonGo.Depressed.GetBitmap())

    def Clicked(self):
        credentials = self.parent.ubox.GetLineText(0), self.parent.pbox.GetLineText(0)
        self.parent.output.put(credentials, block=True, timeout=1.0) # We will block for just a sec in case the launcher is busy doing something

        # Then disable the login boxes
        self.parent.SetLoginControlsEditable(False)