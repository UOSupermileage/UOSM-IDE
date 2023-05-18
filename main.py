import wx

from views.app.AppView import AppView

if __name__ == "__main__":
    app = wx.App()
    frame = AppView()
    frame.Show()
    app.MainLoop()
