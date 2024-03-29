import json


def get_deadlines_data():
    with open("./src/parser/assets/deadlines.json", "r") as file:
        data = json.load(file)
        return data
