from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class EncryptorDecryptor:
    def __init__(self):
        key = RSA.generate(2048)

        self.privKey = key.export_key('PEM')
        self.privKey = RSA.importKey(self.privKey)
        self.privKey = PKCS1_OAEP.new(self.privKey)

        self.pubKey = key.publickey().exportKey('PEM')
        self.pubKey = RSA.importKey(self.pubKey)
        self.pubKey = PKCS1_OAEP.new(self.pubKey)

        self.pubKey2 = self.pubKey

    def encrypt(self, message):
        return self.pubKey2.encrypt(message.encode())

    def decrypt(self, message):
        return self.privKey.decrypt(message)

    def get_pubKey(self):
        return self.pubKey

    def get_privKey(self):
        return self.privKey

    def set_pubKey2(self, key):
        self.pubKey2 = key


