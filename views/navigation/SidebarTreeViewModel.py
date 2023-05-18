from dataclasses import dataclass, field
from typing import Callable, NewType
from uuid import UUID, uuid4

from navigation.NavigationManager import NavigationManager
from views.editors.PIEditorView import PIEditorView


@dataclass
class NavigationTreeItem:
    """Data for node in a navigation tree"""

    title: str

    id: UUID = uuid4()
    image: int = -1
    selImage: int = -1
    onClick: Callable[["SidebarTreeViewModel"], None] = None
    children: list["NavigationTreeItem"] = field(default_factory=list)


class SidebarTreeViewModel:
    """Viewmodel for tool sidebar"""

    navigationManager: NavigationManager

    # Populated at runtime, dictionary of tree items with their id as key
    itemDict: dict[UUID, NavigationTreeItem] = {}

    items: list[NavigationTreeItem] = [
        NavigationTreeItem(
            title="Tools",
            children=[
                NavigationTreeItem(
                    title="PI Editor",
                    onClick=lambda self: self.navigationManager.OpenView(PIEditorView),
                )
            ],
        )
    ]

    def __init__(self, navigationManager: NavigationManager) -> None:
        self.navigationManager = navigationManager
        self.__RegisterNavigationTreeItems(self.items)

    def GetItems(self) -> list[NavigationTreeItem]:
        return self.items

    def GetItem(self, id: UUID) -> NavigationTreeItem:
        try:
            return self.itemDict[id]
        except KeyError:
            raise KeyError(
                "NavigationTreeItem with id not found. This should never happen!"
            )

    def __RegisterNavigationTreeItems(self, items: list[NavigationTreeItem]) -> None:
        for item in items:
            self.itemDict[item.id] = item
            self.__RegisterNavigationTreeItems(item.children)
