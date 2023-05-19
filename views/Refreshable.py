from typing import Protocol


class Refreshable(Protocol):
    def Refresh() -> None:
        """Trigger refresh"""
