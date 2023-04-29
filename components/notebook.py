import wx
import wx.lib.agw.aui as aui
from wx.lib.agw.aui.aui_constants import AUI_NB_DEFAULT_STYLE, wx

from components.windows import FloatingWindow


class Notebook(aui.AuiNotebook):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS,
        agwStyle=AUI_NB_DEFAULT_STYLE,
        name="Notebook",
    ):
        super().__init__(parent, id, pos, size, style, agwStyle, name)

    def OnTabEndDrag(self, event):
        """Undock the tab"""
        super().OnTabEndDrag(event)

        page_index = event.GetSelection()
        print(page_index)

        if page_index >= 0:
            self.FloatPage(page_index)
            self.Update()

    def DisplayPanel(self, title: str, panel: wx.Panel):
        index: int = self.GetPageIndex(panel)

        if index is wx.NOT_FOUND:
            panel.Reparent(self)
            self.AddPage(panel, title, select=True)
        else:
            self.SetSelection(index)
