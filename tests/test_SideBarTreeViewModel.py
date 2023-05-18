import pytest
from tests.mock.MockViewManager import MockViewManager

from views.navigation.SidebarTreeViewModel import SidebarTreeViewModel


@pytest.fixture
def viewmodel():
    """Return SidevarTreeViewModel with default values"""
    viewManager = MockViewManager()
    return SidebarTreeViewModel(viewManager)


def test_SidebarTreeViewModelRegisterTreeItems(viewmodel: SidebarTreeViewModel):
    for item in viewmodel.GetItems():
        assert viewmodel.GetItem(item.id) is not None
