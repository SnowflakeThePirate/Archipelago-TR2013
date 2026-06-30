from worlds.AutoWorld import World

from .Data import Data, TR2013Item, TR2013Location
from BaseClasses import ItemClassification, Item, Location, Region, CollectionState, LocationProgressType
from typing import Optional

Data.load_data()

def run_client():
    # hook into tomb raider
    # watch memory for flag flips
    # when certain flag flips grant items
    # Case 1, pick up Document: flag should show in client
    pass

class TR2013World(World):
    """
    Tomb Raider is a 2013 action-adventure game developed by Crystal Dynamics and published by Square Enix. 
    It is the tenth main entry and a reboot of the Tomb Raider series, 
    acting as the first instalment in the Survivor trilogy that reconstructs the origins of Lara Croft.
    """
    game: str = "Tomb Raider (2013)"

    item_name_to_id = { item.name: item.id for item in Data.item_table }
    location_name_to_id = { location.name: location.id for location in Data.location_table }
    # item_name_groups = { key: set(values) for key, values in Data.item_name_groups.items() }


    def __init__(self, world, player):
        super(TR2013World, self).__init__(world, player)

    def create_items(self) -> None:
        item_pool = [self.create_item(item) for item in Data.item_table]
        while len(item_pool) < len(Data.location_table):
            item_pool.append(self.create_item(None))
        self.multiworld.itempool += item_pool

    def create_item(self, item: Optional[TR2013Item]) -> Item:
        if not item:
            name = "Junk"
            item_classification = ItemClassification.filler
        else:
            if item.type in ['weapon', 'gear']:
                item_classification = ItemClassification.progression
            else:
                item_classification = ItemClassification.useful
        return Item(name, item_classification, self.item_name_to_id[name], self.player)