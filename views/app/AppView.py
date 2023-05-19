import wx
from data.Datastore import AppDatastore, Datastore
from navigation.NavigationManager import NavigationManager
from views.navigation.AppNotebookView import AppNotebookView
from views.navigation.SidebarTreeView import SidebarTreeView


class AppView(wx.Frame):
    navigationManager: NavigationManager
    datastore = Datastore

    def __init__(self):
        super().__init__(None, title="UOSM IDE", size=(1000, 800))

        self.datastore = AppDatastore()
        self.navigationManager = NavigationManager(self.datastore)

        self.splitter = wx.SplitterWindow(self)

        # Create views for inside the splitter
        self.treeView = SidebarTreeView(self.splitter, self.navigationManager)
        self.notebook = AppNotebookView(self.splitter)

        # Configure notebook as target for new views
        self.navigationManager.SetTarget(self.notebook)

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
