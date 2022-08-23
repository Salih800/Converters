import json


class JsonEditor:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = json.load(open(json_file, "r"))

    def add_parameter(self, parameter_to_add):
        for device in self.data.keys():
            self.data[device].update(parameter_to_add)

    def remove_parameter(self, parameter_to_remove):
        for device in self.data.keys():
            self.data[device].pop(parameter_to_remove)

    def show_data(self):
        for device in self.data.keys():
            print(f"{device}: {self.data[device]}")

    def save_file(self):
        json.dump(self.data, open(self.json_file, "w"), indent=4)


