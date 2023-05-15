import wx

import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from components.DataSource import DataObservable, ObservableData
from data.PanelData import GraphPanelData


class GraphPanel(wx.Panel):
    def __init__(self, parent, data: GraphPanelData):
        super().__init__(parent)

        self.data = data

        self.figure = Figure(figsize=(5, 4), dpi=100)

        ax = self.figure.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        ax.plot(t, s)

        canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def OnReceiveData(data: list) -> None:
        pass

    def Register(self, source: DataObservable, key: ObservableData) -> None:
        source.Register(key, self)
