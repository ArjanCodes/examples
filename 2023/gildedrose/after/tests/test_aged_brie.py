from gilded_rose import (
    Item,
    update_quality,
)

AGED_BRIE = "Aged Brie"


def test_aged_brie_increases_quality():
    item = Item(AGED_BRIE, 0, 0)
    update_quality([item])
    assert 2 == item.quality
