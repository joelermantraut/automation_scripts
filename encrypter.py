#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clase para facilitar el uso de la encriptacion y
desencriptacion de cadenas.
"""

from cryptography.fernet import Fernet
import base64 # Para decodificar

class Encrypter(object):
    """
    Clase para facilitar el uso de la encriptacion y
    desencriptacion de cadenas.
    """
    def __init__(self):
        super(Encrypter, self).__init__()
        self.fernet = None
        self.init()

    def init(self):
        """
        Inicializa las encriptacion.
        """
        key = Fernet.generate_key()
        self.fernet = Fernet(key)

    def encode_encrypt(self, data):
        """
        Codifica a bytes con base64 y encripta.
        """
        return self.fernet.encrypt(data.encode('ascii'))

    def encrypt(self, data):
        """
        Encripta la informacion que recibe.

         - Si recibe una lista, devuelve una lista con
           cada elemento encriptado.
        """
        if type(data) is list:
                new_data = []
                for dat in data:
                        new_data.append(self.encode_encrypt(dat))

                data = new_data
        else:
                data = self.encode_encrypt(data)

        return data

    def decode_decrypt(self, data):
        """
        Desencripta y decodifica de bytes a string con base64.
        """
        return self.fernet.decrypt(data, None).decode()

    def decrypt(self, data):
        """
        Desencripta la informacion encriptada que recibe.

         - Verifica que este encriptada.
         - Si es una lista, devuelve cada elemento desencriptado.
        """
        if type(data) is list:
                new_data = []
                for dat in data:
                        try:
                                new_data.append(self.decode_decrypt(data))
                        except InvalidToken:
                                return None
        else:
                try:
                        return self.decode_decrypt(data)
                except InvalidToken:
                        return None

def main():
    encriptador = Encrypter()

    print(encriptador.encrypt('hola'))

if __name__ == "__main__":
    main()
