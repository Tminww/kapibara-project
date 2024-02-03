import json


def get_districts_data():
    with open("./parser/assets/districts.json", "r") as file:
        data = json.load(file)
        return data
