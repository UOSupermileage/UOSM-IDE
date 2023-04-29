from typing import Protocol
import wx


class PanelHost(Protocol):
    def DisplayPanel(title: str, panel: wx.Panel):
        pass
