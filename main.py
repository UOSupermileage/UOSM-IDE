import wx
from components.PanelManager import PanelManager
from components.navigation import TreeView


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(
            None, title="Tree View Example", size=(1000, 800)
        )
        pm = PanelManager()

        self.splitter = wx.SplitterWindow(self)

        # Create views for inside the splitter
        self.treeView = TreeView(self.splitter, pm)
        self.focusView = wx.Panel(self.splitter)

        # Configure splitter
        self.splitter.SplitVertically(self.treeView, self.focusView)
        self.SetSash()

        self.Centre()

    def SetSash(self):
        self.splitter.SetSashPosition(int(self.GetSize()[0] * 0.2))


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
