from typing import Protocol
import wx

from components.DataSources import DataSource


class PanelHost(Protocol):
    def DisplayPanel(title: str, panel: wx.Panel):
        pass


class Updatable(Protocol):
    def Update(source: DataSource):
        pass
