import wx
from components.DataCollectors import DataCollectorManager, MockValueDataCollector
from components.PanelManager import PanelManager
from components.navigation import TreeView
from components.notebook import Notebook
from components.DataSources import DataSource, ObservableData


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title="UOSM IDE", size=(1000, 800))
        pm = PanelManager(defaultParent=self)
        ds = DataSource()
        dc = MockValueDataCollector(ds, ObservableData.ACTUAL_TORQUE)
        dcm = DataCollectorManager()
        dcm.Register(dc)

        self.splitter = wx.SplitterWindow(self)

        # Create views for inside the splitter
        self.treeView = TreeView(self.splitter, pm)
        self.notebook = Notebook(self.splitter, ds)

        pm.RegisterPanelTarget(self.notebook)

        # Configure splitter
        self.splitter.SplitVertically(self.treeView, self.notebook)
        self.splitter.SetMinimumPaneSize(200)
        self.SetSash()

        # Bind the main frame resize event
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self.Centre()

    def SetSash(self):
        self.splitter.SetSashPosition(int(self.GetSize()[0] * 0.2))

    def OnResize(self, event):
        self.SetSash()
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
