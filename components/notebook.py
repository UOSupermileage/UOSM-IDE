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

    def __AddPage(self, panel: wx.Panel, label: str):
        self.AddPage(panel, label)

    def __PopPage(self, index):
        pass

    def DisplayPanel(self, title: str, panel: wx.Panel):
        index: int = self.GetPageIndex(panel)

        if index is wx.NOT_FOUND:
            panel.Reparent(self)
            self.AddPage(panel, title, select=True)
        else:
            self.SetSelection(index)

    # def UndockPage(self, PanelType):
    #     frame = FloatingWindow(self.GetTopLevelParent(), title)
    #     panel = PanelManager.CreatePanel(panelKey, frame)
    #     sizer = wx.BoxSizer(wx.VERTICAL)
    #     sizer.Add(panel, 1, wx.EXPAND)
    #     frame.SetSizer(sizer)

    #     frame.Show()
