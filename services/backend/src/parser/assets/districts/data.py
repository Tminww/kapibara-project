import json


def get_districts_data():
    with open("./src/parser/assets/districts/districts.json", "r") as file:
        data = json.loads(file.read())
        return data
