from worlds.AutoWorld import World
from BaseClasses import (
    ItemClassification,
    Item,
    Location,
    Region,
)
from worlds.generic.Rules import set_rule

from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Data import Data
from Utils import visualize_regions

Data.load_data()


def launch_client(*args):
    from .Client import launch

    launch_subprocess(launch, name="TR2013Client", args=args)


components.append(
    Component(
        "Tomb Raider (2013) Client", func=launch_client, component_type=Type.CLIENT
    )
)


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
    item_id_to_name = {item["id"]: item["name"] for item in Data.item_table}
    item_name_to_id = {item["name"]: item["id"] for item in Data.item_table}
    item_name_to_item = {item["name"]: item for item in Data.item_table}
    location_id_to_name = {
        location["id"]: TR2013Location.stack_names(location["region"], location["name"])
        for location in Data.location_table
    }
    location_name_to_id = {
        TR2013Location.stack_names(location["region"], location["name"]): location["id"]
        for location in Data.location_table
    }
    location_name_to_location = {
        TR2013Location.stack_names(location["region"], location["name"]): location
        for location in Data.location_table
    }
    source_locations = {}

    def __init__(self, world, player):
        super().__init__(world, player)

    def create_items(self):
        item_pool = [self.create_item(item["name"]) for item in Data.item_table]
        while len(item_pool) < len(Data.location_table):
            item_pool.append(self.create_item("Junk"))
        self.multiworld.itempool += item_pool

    def create_item(self, item_name: str) -> Item:
        item_dict = self.item_name_to_item.get(item_name)
        if not item_dict:
            return Item("Junk", ItemClassification.filler, 0, self.player)
        if item_dict["type"] in ["weapon", "gear"]:
            item_classification = ItemClassification.progression
        return Item(item_dict["name"], item_classification, 0, self.player)

    def create_regions(self):
        regions = [
            Region(region["name"], self.player, self.multiworld)
            for region in Data.region_table
        ]

        for region in regions:
            region.locations = [
                TR2013Location(
                    self.player,
                    TR2013Location.stack_names(region.name, location["name"]),
                    location["id"],
                    region,
                )
                for location in Data.location_table
                if location["region"] == region.name
            ]

            self.multiworld.regions.append(region)

        for connection in Data.region_connections_table:
            from_name = (
                connection["from"] if "Menu" not in connection["from"] else "Menu"
            )
            to_name = connection["to"] if "Menu" not in connection["to"] else "Menu"

            region_from = self.multiworld.get_region(from_name, self.player)
            region_to = self.multiworld.get_region(to_name, self.player)
            entrance = region_from.connect(region_to)

            # if "condition" in connection and "items" in connection["condition"]:
            #     set_rule(entrance, lambda state, en=entrance, conn=connection: self._has_items(state, conn["condition"].get("items", [])))

        visualize_regions(self.multiworld.get_region("Menu", self.player), "region_uml")
