from gilded_rose import (
    Item,
    update_quality,
)

BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"


def test_backstage_passes_increase_quality():
    item = Item(BACKSTAGE_PASSES, 11, 0)
    update_quality([item])
    assert 1 == item.quality


def test_backstage_passes_increase_quality_by_2_when_sell_in_is_10_or_less():
    item = Item(BACKSTAGE_PASSES, 10, 0)
    update_quality([item])
    assert 2 == item.quality


def test_backstage_passes_increase_quality_by_3_when_sell_in_is_5_or_less():
    item = Item(BACKSTAGE_PASSES, 5, 0)
    update_quality([item])
    assert 3 == item.quality


def test_backstage_passes_quality_is_0_when_sell_in_is_0():
    item = Item(BACKSTAGE_PASSES, 0, 10)
    update_quality([item])
    assert 0 == item.quality
