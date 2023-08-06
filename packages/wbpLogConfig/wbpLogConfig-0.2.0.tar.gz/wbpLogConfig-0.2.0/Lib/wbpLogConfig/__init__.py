import logging

import wx
from wx import aui
from .logConfigPanel import LogConfigPanel

__version__ = "0.2.0"

name = "LogConfig"

info = aui.AuiPaneInfo()
info.Name(name)
info.Caption(name)
info.Dock()
info.Bottom()
info.Resizable()
info.MaximizeButton(True)
info.MinimizeButton(True)
info.CloseButton(False)
info.FloatingSize(wx.Size(300, 200))
info.BestSize(wx.Size(800, 400))
info.MinSize(wx.Size(300, 200))

def setupLogging(app):
    console = logging.StreamHandler()
    console.set_name(app.AppName + " - Console")
    formatter = logging.Formatter("%(name)-12s: %(lineno)-4d: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.root.addHandler(console)


panels = [(LogConfigPanel, info)]

app = wx.GetApp()
if app is not None:
    app.AddPostInitAction(setupLogging)
