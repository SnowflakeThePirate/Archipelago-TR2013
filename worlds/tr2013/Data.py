import os
import json
import pkgutil

from worlds.celeste_open_world import data


# blatantly copied from the re2 ap which copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    data_directory = "data"
    fname = os.path.join(data_directory, *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata


class Data:
    item_table = []
    location_table = []
    region_table = []
    region_connections_table = []

    item_name_groups = {}

    @classmethod
    def load_data(cls):
        # Load Regions
        Data.region_table.extend(load_data_file("regions.json"))

        # Load Items
        Data.item_table.extend(load_data_file("items.json"))

        # Load Locations
        for index, location_file in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), "data", "locations"))):
            if location_file.endswith(".json"):
                Data.location_table.extend(load_data_file("locations", location_file))

        for index, location in enumerate(Data.location_table):
            Data.location_table[index]['id'] = location.get('id', index + 1)

        # Load Region Connections
        Data.region_connections_table.extend(load_data_file("region_connections.json"))