import wx
import wx.lib.agw.aui as aui

import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphPanelData:
    def __init__(self, title, getData) -> None:
        self.title = title
        self.getData = getData


class GraphPanel(wx.Panel):
    def __init__(self, parent, data: GraphPanelData):
        super().__init__(parent)

        self.data = data
