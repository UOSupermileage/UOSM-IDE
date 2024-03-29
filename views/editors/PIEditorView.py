import wx
import wx.dataview as dv

from data.Data import DataKey
from views.editors.PIEditorViewModel import PIEditorViewModel


class PIEditorView(wx.Panel):
    """View for PI Editor"""

    title: str = "PI Editor"

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        self.viewmodel = PIEditorViewModel(self, args, **kwargs)

        self.tree = dv.TreeListCtrl(
            self, style=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS | wx.TR_ROW_LINES
        )

        self.tree.AppendColumn("Key")
        self.tree.AppendColumn("Value")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

    def Refresh(self) -> None:
        print("Refreshing view")
