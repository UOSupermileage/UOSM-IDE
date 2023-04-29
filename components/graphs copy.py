import wx
import wx.lib.agw.aui as aui

import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.notebook = aui.AuiNotebook(self)

        # Bind events to undock and redock pages
        self.notebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClose)
        self.notebook.Bind(aui.EVT_AUINOTEBOOK_END_DRAG, self.OnPageEndDrag)

        # Set up the layout of the notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def OnPageClose(self, event):
        event.Veto()

    def OnPageEndDrag(self, event):
        page = self.notebook.GetCurrentPage()
        mouse_state = wx.GetMouseState()
        # pos = mouse_state.GetPosition()
        self.notebook.FloatPage(self.notebook.GetPageIndex(page))
        self.notebook.Refresh()

        # Bind the EVT_AUI_PANE_CLOSE event to the floating window
        window = self.notebook.GetPage(self.notebook.GetPageIndex(page))
        window.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnClosePane)

    def OnClosePane(self, event):
        page = event.GetPane().window
        if event.GetPane().IsOk():
            if event.GetPane().IsFloating():
                event.GetPane().Float()
            else:
                self.notebook.Dock(page)

    def AddGraph(self, data, title: str):
        # Create panel to put in the notebook
        panel = wx.Panel(self.notebook)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        ax.plot(t, s)
        canvas = FigureCanvas(panel, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        # Add the panel to the notebook
        self.notebook.AddPage(panel, title)