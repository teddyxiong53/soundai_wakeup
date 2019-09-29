import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,title="test wxpython", style=wx.DEFAULT_FRAME_STYLE, pos=(200,200), size=(800,600))
        self.CreateToolBar()
        self.statusBar = self.CreateStatusBar()
        self.layout = wx.BoxSizer(orient=wx.VERTICAL)
        self.label1 = wx.StaticText(self, label="label1")
        self.button1 = wx.Button(self, label="button")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button1)
        self.layout.Add(self.label1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.layout.Add(self.button1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(self.layout)
        self.Show(True)
    def OnClick(self, event):
        self.statusBar.SetStatusText("click")

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        return True

app = MyApp()
app.MainLoop()
