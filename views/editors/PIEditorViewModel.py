from typing import Union
from data.Data import DataKey
from data.Datastore import Datastore
from views.Refreshable import Refreshable


class PIEditorViewModel:
    """Model for PI Editor"""

    datastore: Datastore

    def __init__(self, view: Refreshable, *args, **kwargs) -> None:
        self.view = view
        self.datastore: Datastore = kwargs["datastore"]

        self.datastore.RegisterObserverWithKeys(
            [DataKey.TorqueP, DataKey.TorqueI], self
        )

    def OnDataChanged(self, key: DataKey) -> None:
        self.view.Refresh()
