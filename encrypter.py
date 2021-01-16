#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class to simplify the uses of encryption in strings.
"""

from cryptography.fernet import Fernet
import base64 # Para decodificar

class Encrypter(object):
    """
    Class to simplify the uses of encryption in strings.
    """
    def __init__(self):
        super(Encrypter, self).__init__()
        self.fernet = None
        self.init()

    def init(self):
        """
        Inits encryption. 
        """
        key = Fernet.generate_key()
        self.fernet = Fernet(key)

    def encode_encrypt(self, data):
        """
        Codes to bytes with base64 and encrypts.
        """
        return self.fernet.encrypt(data.encode('ascii'))

    def encrypt(self, data):
        """
        Encrypts the info that receives.

         - If receives a list, encrypts each one.
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
        Decrypts and decode from bytes to string with base64.
        """
        return self.fernet.decrypt(data, None).decode()

    def decrypt(self, data):
        """
        Decrypts.

         - Verifies if it is encrypted.
         - If it is a list, decrypts each one.
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
