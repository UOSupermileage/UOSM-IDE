from abc import ABC
from dataclasses import dataclass

from components.DataSources import ObservableData


@dataclass
class PanelData(ABC):
    pass


@dataclass
class GraphPanelData(PanelData):
    title: str
    observableData: ObservableData


@dataclass
class EditorPanelData(PanelData):
    pass
