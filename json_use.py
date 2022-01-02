#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class to simplify the use and access of JSON files.
"""

import json

class JSONUse(object):
    """Class to simplify the use and access of JSON files."""
    def __init__(self, file=None):
        super(JSONUse, self).__init__()
        self.file = file
        self.json_data = None

    def serialize(self, data, own_decoder=None):
        """
        Serializes the information that receives:
            - If it not receives file, return the one generated.
            - If not get, same result.
            - Enable own decoder.
        """
        if self.file:
            json.dump(data, self.file, indent = 4, default = own_decoder)

        self.json_data = json.dumps(data, indent = 4, default = own_decoder)

    def deserialize(self):
        """
        Deserialize info.
         - If there is a file, from it.
         - Else, from a class member.
        """
        if self.file:
            return json.load(self.file)
        else:
            return json.loads(self.json_data)

def main():
    json_string = """
    {
        "researcher": {
            "name": "Ford Prefect",
            "species": "Betelgeusian",
            "relatives": [
                {
                    "name": "Zaphod Beeblebrox",
                    "species": "Betelgeusian"
                }
            ]
        }
    }
    """

    file = open("test.json", "w")

    json_object = JSONUse(file)

    json_object.serialize(json_string)

    print(json_object.json_data)

    file.close()

if __name__ == "__main__":
    main()
