import wx
from enum import Enum

from components.graphs import GraphPanel, GraphPanelData


class PanelType(Enum):
    TORQUE_GRAPH = 1
    VELOCITY_GRAPH = 2
    POSITION_GRAPH = 3

    def GetData(self):
        match self:
            case PanelType.TORQUE_GRAPH:
                return GraphPanelData("Torque Graph", None)
            case PanelType.VELOCITY_GRAPH:
                return GraphPanelData("Velocity Graph", None)
            case PanelType.POSITION_GRAPH:
                return GraphPanelData("Position Graph", None)

        return None


class PanelManager:
    def CreatePanel(type: PanelType, parent: any) -> wx.Panel:
        match type:
            case PanelType.TORQUE_GRAPH | PanelType.VELOCITY_GRAPH | PanelType.POSITION_GRAPH:
                return GraphPanel(parent, type.GetData())
