import wx


class FloatingWindow(wx.Frame):
    def __init__(self, parent, title):
        super(FloatingWindow, self).__init__(parent, title=title, size=(200, 150))
        self.Centre()
