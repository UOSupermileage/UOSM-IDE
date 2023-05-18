import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui.aui_constants import AUI_NB_DEFAULT_STYLE, wx


class AppNotebookView(aui.AuiNotebook):
    def __init__(
        self,
        parent,
    ):
        super().__init__(
            parent,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS,
            AUI_NB_DEFAULT_STYLE,
            "Notebook",
        )

    def DisplayView(self, view: wx.Panel):
        index: int = self.GetPageIndex(view)

        if index is wx.NOT_FOUND:
            view.Reparent(self)
            self.AddPage(view, view.GetLabel(), select=True)
        else:
            self.SetSelection(index)
