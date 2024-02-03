import json


def get_subjects_data():
    with open("./parser/assets/subjects.json", "r") as file:
        data = json.load(file)
        return data
