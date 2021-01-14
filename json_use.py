#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clase para facilitar el uso y acceso de archivos JSON.
"""

import json

class JSONUse(object):
    """Clase para facilitar el uso y acceso de archivos JSON"""
    def __init__(self, file=None):
        super(JSONUse, self).__init__()
        self.file = file
        self.json_data = None

    def serialize(self, data, own_decoder=None):
        """
        Serializa la informacion que se le pasa
         - Si no se le pasa archivo, devuelve
         - Si se le pasa get lo mismo
         - Permite que se pase un decodificador propio
        """
        if self.file:
                json.dump(data, self.file, indent = 4, default = own_decoder)

        self.json_data = json.dumps(data, indent = 4, default = own_decoder)

    def deserialize(self):
        """
        Deserializa la informacion.
         - Si hay un archivo, desde ahi.
         - Si no desde el miembro de la clase.
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

    file = open("prueba.json", "w")

    json_object = JSONUse(file)

    json_object.serialize(json_string)

    print(json_object.json_data)

    file.close()

if __name__ == "__main__":
    main()
