from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class EncryptorDecryptor:
    def __init__(self):
        self.keyLen = 2048
        self._enc_block_size = self.keyLen // 8 - 43
        self._dec_block_size = self.keyLen // 8
        self._key = RSA.generate(self.keyLen)

        self.privKey = self._key.export_key('PEM')
        self.privKey = RSA.importKey(self.privKey)
        self.privKey = PKCS1_OAEP.new(self.privKey)

        self.pubKey = self._key.publickey().exportKey('PEM')
        self.pubKey = RSA.importKey(self.pubKey)
        self.pubKey = PKCS1_OAEP.new(self.pubKey)

        self.pubKey2 = None

    def encrypt(self, message):
        if len(message) > self._enc_block_size:
            return self._partial_enc(message)
        if type(message) != bytes:
            message = message.encode()
        return self.pubKey2.encrypt(message)

    def _partial_enc(self, message):
        result = b''

        lo, hi, l = 0, self._enc_block_size, len(message)

        while True:
            if hi > l:
                result += self.encrypt(message[lo:])
                break
            result += self.encrypt(message[lo:hi])
            lo = hi
            hi += self._enc_block_size

        return result

    def decrypt(self, message):

        if len(message) > self._dec_block_size:
            return self._partial_dec(message)
        return self.privKey.decrypt(message)

    def _partial_dec(self, message):
        result = b''
        lo, hi, l = 0, self._dec_block_size, len(message)

        while True:
            if hi >= l:
                result += self.decrypt(message[lo:])
                break
            result += self.decrypt(message[lo:hi])
            lo = hi
            hi += self._dec_block_size

        return result

    def get_pubKey(self):
        return self._key.publickey().exportKey('PEM')

    def set_pubKey2(self, key):
        self.pubKey2 = RSA.importKey(key)
        self.pubKey2 = PKCS1_OAEP.new(self.pubKey2)


def HandshakeParser(data):
    results = {}
    data = data.split('\r\n')
    # not possible to not get int in string
    code = int(data[0])

    results['code'] = code

    if "Message=" == data[1][:8]:
        results['message'] = data[1][8:]
    if "Key-len=" == data[2][:8]:
        results['key-len'] = int(data[2][8:])
    if len(data[3]) == 454:  # check if rsa key exists in array and it's length is correct
        if "Key=" == data[3][:4]:
            results['key'] = data[3][4:]
    else:
        results['key'] = 'Bad key'
    return results
