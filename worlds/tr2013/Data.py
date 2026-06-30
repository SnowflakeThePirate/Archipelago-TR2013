import os
import json
from BaseClasses import Item, Location

class TR2013Item(Item):
    name: str
    id: int
    game_id: str
    type: str
    tier: str

class TR2013Location(Location):
    name: str
    id: int
    item_id: str
    region: str

class Data:
    item_table = []
    location_table = []
    item_name_groups = {}

    @classmethod
    def load_data(cls):
        data_file_path = os.path.join(os.path.dirname(__file__), 'items.json')
        with open(data_file_path, 'r') as f:
            Data.item_table = [TR2013Item(**item) for item in json.load(f)]

        location_file_path = os.path.join(os.path.dirname(__file__), 'locations.json')
        with open(location_file_path, 'r') as f:
            Data.location_table = [TR2013Location(**location) for location in json.load(f)]
