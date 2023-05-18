from uuid import UUID
import wx

from navigation.NavigationManager import NavigationManager
from views.navigation.SidebarTreeViewModel import (
    SidebarTreeViewModel,
    NavigationTreeItem,
)


class SidebarTreeView(wx.TreeCtrl):
    """View for tool sidebar"""

    viewmodel: SidebarTreeViewModel

    def __init__(self, parent, navigationManager: NavigationManager):
        super().__init__(parent)
        self.navigationManager = navigationManager

        self.viewmodel = SidebarTreeViewModel(self.navigationManager)

        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)

        self.UpdateTree()
        self.ExpandAll()

    def OnActivated(self, event: wx.Event):
        item = event.GetItem()
        id: UUID = self.GetItemData(item)

        treeItem = self.viewmodel.GetItem(id)
        treeItem.onClick(self.viewmodel)

    def UpdateTree(self):
        root = self.AddRoot("Tools")
        self.__UpdateTree(root, self.viewmodel.GetItems())

    def __UpdateTree(self, node: wx.TreeItemId, items: list[NavigationTreeItem]):
        for item in items:
            newNode = self.AppendItem(
                node, item.title, item.image, item.selImage, data=item.id
            )
            self.__UpdateTree(newNode, item.children)
