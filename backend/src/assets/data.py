import json

BASE_ASSETS_PATH = "./src/assets"


def get_deadlines_data():
    with open(f"{BASE_ASSETS_PATH}/deadlines.json", "r") as file:
        data = json.load(file)
        return data


def get_districts_data():
    with open(f"{BASE_ASSETS_PATH}/districts.json", "r") as file:
        data = json.loads(file.read())
        return data


def get_regions_data():
    with open(f"{BASE_ASSETS_PATH}/regions.json", "r") as file:
        data = json.load(file)
        return data
