import os
import json

class Data:
    item_table = []
    location_table = []
    item_name_groups = {}

    @classmethod
    def load_data(cls):
        data_file_path = os.path.join(os.path.dirname(__file__), 'items.json')
        with open(data_file_path, 'r') as f:
            Data.item_table = json.load(f)

        location_file_path = os.path.join(os.path.dirname(__file__), 'locations.json')
        with open(location_file_path, 'r') as f:
            Data.location_table = json.load(f)
