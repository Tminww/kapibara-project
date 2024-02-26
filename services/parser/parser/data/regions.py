import json


def get_regions_data():
    with open("./parser/assets/regions.json", "r") as file:
        data = json.load(file)
        return data
