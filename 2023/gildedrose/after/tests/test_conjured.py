from gilded_rose import (
    Item,
    update_quality,
)

CONJURED = "Conjured Mana Cake"


def test_conjured_degrades_twice_as_fast():
    item = Item(CONJURED, 0, 10)
    update_quality([item])
    assert 6 == item.quality
