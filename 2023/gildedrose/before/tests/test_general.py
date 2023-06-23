from gilded_rose import (
    Item,
    update_quality,
)


def test_fixme():
    item = Item("foo", 0, 0)
    update_quality([item])
    assert "fixme" == item.name
