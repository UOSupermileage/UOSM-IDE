from dataclasses import dataclass
import wx
from components.PanelManager import PanelManager, PanelType

from components.windows import FloatingWindow


@dataclass
class NavigationTreeItemData:
    """Class for associating data to navigation tree"""

    panelKey: PanelType


class TreeView(wx.TreeCtrl):
    def __init__(self, parent, panelManager: PanelManager):
        super(TreeView, self).__init__(parent)

        self.panelManager = panelManager

        root = self.AddRoot("Tools")
        controlModes = self.AppendItem(root, "Graphs")
        self.AppendItem(
            controlModes,
            "Torque Graph",
            data=NavigationTreeItemData(PanelType.TORQUE_GRAPH),
        )
        self.AppendItem(
            controlModes,
            "Velocity Graph",
            data=NavigationTreeItemData(PanelType.VELOCITY_GRAPH),
        )
        self.AppendItem(
            controlModes,
            "Position Graph",
            data=NavigationTreeItemData(PanelType.POSITION_GRAPH),
        )

        editors = self.AppendItem(root, "Editors")
        self.AppendItem(
            editors,
            "Favorites",
            data=NavigationTreeItemData(PanelType.FAVORITES_VALUE_EDITOR),
        )

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)

        self.ExpandAll()

    def OnActivated(self, event: wx.Event):
        item = event.GetItem()

        data: NavigationTreeItemData = self.GetItemData(item)

        self.panelManager.OpenPanel(self.GetItemText(item), data.panelKey)
