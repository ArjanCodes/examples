from typing import Iterable, Protocol

from item import Item


def decrease_item_quality(item: Item, amount: int = 1) -> None:
    item.quality = max(item.quality - amount, 0)


def increase_item_quality(item: Item, amount: int = 1, max_quality: int = 50) -> None:
    item.quality = min(item.quality + amount, max_quality)


# Item types
AGED_BRIE = "Aged Brie"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
CONJURED = "Conjured Mana Cake"


class ItemUpdater(Protocol):
    def update_sell_in(self, item: Item) -> None:
        ...

    def update_quality(self, item: Item) -> None:
        ...


class DefaultItemUpdater:
    def update_sell_in(self, item: Item) -> None:
        item.sell_in = item.sell_in - 1

    def update_quality(self, item: Item) -> None:
        decrease_item_quality(item)
        if item.sell_in < 0:
            decrease_item_quality(item)


class AgedBrieItemUpdater(DefaultItemUpdater):
    def update_quality(self, item: Item) -> None:
        increase_item_quality(item)
        if item.sell_in < 0:
            increase_item_quality(item)


class BackstagePassesItemUpdater(DefaultItemUpdater):
    def update_quality(self, item: Item) -> None:
        increase_item_quality(item)
        if item.sell_in < 10:
            increase_item_quality(item)
        if item.sell_in < 5:
            increase_item_quality(item)
        if item.sell_in < 0:
            item.quality = 0


class SulfurasItemUpdater(DefaultItemUpdater):
    def update_sell_in(self, item: Item) -> None:
        pass

    def update_quality(self, item: Item) -> None:
        pass


class ConjuredItemUpdater(DefaultItemUpdater):
    def update_quality(self, item: Item) -> None:
        decrease_item_quality(item, 2)
        if item.sell_in < 0:
            decrease_item_quality(item, 2)


ITEM_UPDATERS: dict[str, ItemUpdater] = {
    AGED_BRIE: AgedBrieItemUpdater(),
    BACKSTAGE_PASSES: BackstagePassesItemUpdater(),
    SULFURAS: SulfurasItemUpdater(),
    CONJURED: ConjuredItemUpdater(),
}


def update_quality(items: Iterable[Item]) -> None:
    for item in items:
        update_quality_single(item)


def update_quality_single(item: Item):
    item_updater = ITEM_UPDATERS.get(item.name, DefaultItemUpdater())

    # update the sell in value
    item_updater.update_sell_in(item)

    # update the quality
    item_updater.update_quality(item)
