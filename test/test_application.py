import pytest

from NotAOrm.table import Table


@pytest.fixture
def users():
    return Table(table_name="users", table_row=('id', 'name', 'groups'))


@pytest.fixture
def groups():
    return Table(table_name="groups", table_row=('id', 'name'))


def test_model(users: Table, groups: Table):
    assert users
    assert groups

    users.change.insert(name='Jean-bon')
    users.change.insert(name='Joe-no')

    assert users.show.filter(users.name == 'Jean-bo')
    assert users.show.filter(users.name == 'Joe-ni')

    users.change.delete(users.name == 'Jean-bon', commit=True)
    users.change.delete(users.name == 'Joe-ni', commit=True)
