import json


def get_districts_data():
    with open("./parser/assets/districts.json", "r") as file:
        data = json.loads(file.read())
        return data
