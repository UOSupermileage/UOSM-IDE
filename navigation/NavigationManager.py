from typing import Protocol
import wx


class ViewHost(Protocol):
    def DisplayView(view: wx.Panel):
        """Displays a view on the host"""
        pass


class NavigationManager:
    """Handle navigation in app"""

    target: ViewHost

    views: dict[type[wx.Panel], wx.Panel] = {}

    def SetTarget(self, target: ViewHost) -> None:
        self.target = target

    def OpenView(self, view: type[wx.Panel]) -> None:
        if self.target is None:
            raise AttributeError("No target defined for NavigationManager")

        # If view is in dictionary keys, but the view does not exist. Pop the key.
        if view in self.views.keys() and not self.views[view]:
            self.views.pop(view)

        if view not in self.views.keys():
            self.views[view] = self.__InstantiateView(view)

        self.target.DisplayView(self.views[view])

    def __InstantiateView(self, view: type[wx.Panel]) -> wx.Panel:
        v = view(parent=self.target, viewManager=self)
        v.SetLabel(getattr(v, "title", "Default Title"))
        return v
