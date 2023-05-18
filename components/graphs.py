import wx

import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from components.DataSources import DataObservable, DataSource, ObservableData
from data.PanelData import GraphPanelData


class GraphPanel(wx.Panel):
    data: GraphPanelData
    figure: Figure

    def __init__(self, parent, data: GraphPanelData):
        super().__init__(parent)

        self.data = data

        self.figure = Figure(figsize=(5, 4), dpi=100)

        canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def Update(self, source: DataSource):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        ax.plot(t, s)
