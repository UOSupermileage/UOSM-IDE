import wx
import wx.dataview as dv
import plistlib
from data.PanelData import EditorPanelData


class EditorPanel(wx.Panel):
    def __init__(self, parent, data: EditorPanelData):
        super().__init__(parent)

        self.data = data

        self.tree = dv.TreeListCtrl(
            self, style=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS | wx.TR_ROW_LINES
        )

        self.tree.AppendColumn("Key")
        self.tree.AppendColumn("Value")
        self.tree.Bind(dv.EVT_TREELIST_ITEM_ACTIVATED, self.OnTreeItemActivated)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

    def OnTreeItemActivated(self, event):
        item = event.GetItem()

        if item:
            # Get the data associated with the item
            data = self.tree.GetItemData(item)

            if data:
                # Create the value editor based on the data type
                if isinstance(data, dict):
                    self.create_dict_editor(data)
                elif isinstance(data, list):
                    self.create_list_editor(data)
                else:
                    self.create_scalar_editor(data)

                self.Layout()
