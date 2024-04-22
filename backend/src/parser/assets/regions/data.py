import json


def get_regions_data():
    with open("./src/parser/assets/regions/regions.json", "r") as file:
        data = json.load(file)
        return data
