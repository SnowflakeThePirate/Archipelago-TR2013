from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item, Location, Region, CollectionState, LocationProgressType
from worlds.generic.Rules import set_rule
from .Data import Data
from Utils import visualize_regions

Data.load_data()

class TR2013Location(Location):
    @staticmethod
    def stack_names(*area_names: str) -> str:
        return " - ".join(area_names)

class TR2013World(World):
    """
    Tomb Raider is a 2013 action-adventure game developed by Crystal Dynamics and published by Square Enix. 
    It is the tenth main entry and a reboot of the Tomb Raider series, 
    acting as the first instalment in the Survivor trilogy that reconstructs the origins of Lara Croft.
    """
    game: str = "Tomb Raider (2013)"


    item_id_to_name = { item['id']: item['name'] for item in Data.item_table }
    item_name_to_id = { item['name']: item['id'] for item in Data.item_table }
    item_name_to_item = { item['name']: item for item in Data.item_table }
    location_id_to_name = { location['id']: TR2013Location.stack_names(location['region'], location['name']) for location in Data.location_table }
    location_name_to_id = { TR2013Location.stack_names(location['region'], location['name']): location['id'] for location in Data.location_table }
    location_name_to_location = { TR2013Location.stack_names(location['region'], location['name']): location for location in Data.location_table }
    source_locations = {} # this is used to seed the initial item pool from original items, and is indexed by player as lname:location locations

    def __init__(self, world, player):
        super().__init__(world, player)

    def create_items(self):
        item_pool = [self.create_item(item['name']) for item in Data.item_table]
        while len(item_pool) < len(Data.location_table):
            item_pool.append(self.create_item("Junk"))
        self.multiworld.itempool += item_pool

    def create_item(self, item_name: str) -> Item:
        item_dict = self.item_name_to_item.get(item_name)
        if not item_dict:
            return Item("Junk", ItemClassification.filler, 0, self.player)
        if item_dict['type'] in ["weapon", "gear"]:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.useful
        return Item(item_dict['name'], item_classification, 0, self.player)

    
    def create_regions(self):
        regions = [
            Region(region['name'], self.player, self.multiworld) 
                for region in Data.region_table
        ]

        for region in regions:
            region.locations = [
                TR2013Location(self.player, TR2013Location.stack_names(region.name, location['name']), location['id'],region)
                for location in Data.location_table if location['region'] == region.name
            ]

            self.multiworld.regions.append(region)

        for connection in Data.region_connections_table:
            from_name = connection['from'] if 'Menu' not in connection['from'] else 'Menu'
            to_name = connection['to'] if 'Menu' not in connection['to'] else 'Menu'

            region_from = self.multiworld.get_region(from_name, self.player)
            region_to = self.multiworld.get_region(to_name, self.player)
            entrance = region_from.connect(region_to)

            # if "condition" in connection and "items" in connection["condition"]:
            #     set_rule(entrance, lambda state, en=entrance, conn=connection: self._has_items(state, conn["condition"].get("items", [])))

        visualize_regions(self.multiworld.get_region("Menu", self.player), "region_uml")

    # def _has_items(self, state: CollectionState, item_names: list) -> bool:
    #     # if there are no item requirements, this location is open, they "have the items needed"
    #     if len(item_names) == 0:
    #         return True

    #     # if the requirements are a single set of items, make it a list of a single set of items to support looping for multiple sets (below)
    #     if len(item_names) > 0 and type(item_names[0]) is not list:
    #         item_names = [item_names]

    #     for set_of_requirements in item_names:
    #         # if it requires all unique items, just do a state has all
    #         if len(set(set_of_requirements)) == len(set_of_requirements):
    #             if state.has_all(set_of_requirements, self.player):
    #                 return True
    #         # else, it requires some duplicates, so let's group them up and do some has w/ counts
    #         else:
    #             item_counts = {
    #                 item_name: len([i for i in set_of_requirements if i == item_name]) for item_name in set_of_requirements # e.g., { Spare Key: 2 }
    #             }
    #             missing_an_item = False

    #             for item_name, count in item_counts.items():
    #                 if not state.has(item_name, self.player, count):
    #                     missing_an_item = True

    #             if missing_an_item:
    #                 continue # didn't meet these requirements, so skip to the next set, if any
                
    #             # if we made it here, state has all the items and the quantities needed, return True
    #             return True

    #     # if we made it here, state didn't have enough to return True, so return False
    #     return False