from worlds.AutoWorld import World

from .Data import Data

Data.load_data()

def run_client():
    pass

class TR2013World(World):
    """
    Tomb Raider is a 2013 action-adventure game developed by Crystal Dynamics and published by Square Enix. 
    It is the tenth main entry and a reboot of the Tomb Raider series, 
    acting as the first instalment in the Survivor trilogy that reconstructs the origins of Lara Croft.
    """
    game: str = "Tomb Raider (2013)"

    item_name_to_id = { item['name']: item['id'] for item in Data.item_table }
    location_name_to_id = { location['name']: location['id'] for location in Data.location_table }
    # item_name_groups = { key: set(values) for key, values in Data.item_name_groups.items() }


    def __init__(self, world, player):
        super(TR2013World, self).__init__(world, player)