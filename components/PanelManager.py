from abc import ABC
from dataclasses import dataclass
from typing import Dict
import wx
from enum import Enum
from components.DataSource import ObservableData
from components.editors import EditorPanel

from components.graphs import GraphPanel, GraphPanelData
from protocols.PanelHost import PanelHost
from data.PanelData import PanelData


class PanelCategory(Enum):
    GRAPH = (1,)
    VALUE_EDITOR = 2


class PanelType(Enum):
    TORQUE_GRAPH = 1
    VELOCITY_GRAPH = 2
    POSITION_GRAPH = 3
    FAVORITES_VALUE_EDITOR = 4

    def GetCategory(self) -> PanelCategory:
        match self:
            case PanelType.TORQUE_GRAPH | PanelType.VELOCITY_GRAPH | PanelType.POSITION_GRAPH:
                return PanelCategory.GRAPH
            case PanelType.FAVORITES_VALUE_EDITOR:
                return PanelCategory.VALUE_EDITOR

    def GetData(self) -> PanelData:
        match self:
            case PanelType.TORQUE_GRAPH:
                return GraphPanelData("Torque Graph", None)
            case PanelType.VELOCITY_GRAPH:
                return GraphPanelData("Velocity Graph", None)
            case PanelType.POSITION_GRAPH:
                return GraphPanelData("Position Graph", None)
            case PanelType.FAVORITES_VALUE_EDITOR:
                return GraphPanelData("Favorites Editor", None)

        return None


class PanelManager:
    target: PanelHost
    panels: Dict[PanelType, wx.Panel]
    defaultParent: wx.Frame

    def __init__(self, defaultParent) -> None:
        self.target = None
        self.panels = {}
        self.defaultParent = defaultParent

    def __CreatePanel(self, type: PanelType, parent: any) -> wx.Panel:
        match type.GetCategory():
            case PanelCategory.GRAPH:
                return GraphPanel(parent, type.GetData())
            case PanelCategory.VALUE_EDITOR:
                return EditorPanel(parent, type.GetData())

    def OpenPanel(self, title: str, type: PanelType) -> bool:
        if self.target is None:
            return False

        if type in self.panels.keys() and not self.panels[type]:
            self.panels.pop(type)

        if type not in self.panels.keys():
            self.panels[type] = self.__CreatePanel(type, self.defaultParent)

        self.target.DisplayPanel(title, self.panels[type])

    def RegisterPanelTarget(self, target: PanelHost):
        self.target = target
