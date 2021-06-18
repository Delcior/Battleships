from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class EncryptorDecryptor:
    def __init__(self):
        self.keyLen = 2048
        self._key = RSA.generate(self.keyLen)

        self.privKey = self._key.export_key('PEM')
        self.privKey = RSA.importKey(self.privKey)
        self.privKey = PKCS1_OAEP.new(self.privKey)

        self.pubKey = self._key.publickey().exportKey('PEM')
        self.pubKey = RSA.importKey(self.pubKey)
        self.pubKey = PKCS1_OAEP.new(self.pubKey)

        self.pubKey2 = None

    def encrypt(self, message):
        if len(message) >= self.keyLen//8:
            return self._partial_enc(message)
        if type(message) != bytes:
            message = message.encode()

        return self.pubKey2.encrypt(message)

    def _partial_enc(self, message):
        result = b''

        lo, hi, l = 0, 200, len(message)

        while True:
            if hi > l:
                result+=self.encrypt(message[lo:])
                break
            result+=self.encrypt(message[lo:hi])
            lo = hi
            hi += 200

        print("enc_len ", len(result))
        return result

    def decrypt(self, message):

        if len(message) > self.keyLen//8:
            return self._partial_dec(message)
        #print((message))
        print("---", len(message))
        return self.privKey.decrypt(message)

    def _partial_dec(self, message):
        result = b''

        lo, hi, l = 0, self.keyLen//8, len(message)

        while True:
            if hi >= l:
                result+=self.decrypt(message[lo:])
                break
            result+=self.decrypt(message[lo:hi])
            lo = hi
            hi += self.keyLen//8

        print("den_len ", len(result))
        return result

    def get_pubKey(self):
        return self._key.publickey().exportKey('PEM')

    def set_pubKey2(self, key):
        self.pubKey2 = RSA.importKey(key)
        self.pubKey2 = PKCS1_OAEP.new(self.pubKey2)


def HandshakeParser(data):
    results = {}
    data = data.split('\r\n')
    try:

        code = int(data[0])
    except ValueError:
        return '302\r\nBAD CODE ERROR'

    results['code'] = code

    # TODO:co jesli jest blad
    if "Message=" == data[1][:8]:
        results['message'] = data[1][8:]
    if "Key=" == data[2][:4]:
        results['key'] = data[2][4:]
    if "Key-len=" == data[3][:8]:
        results['key-len'] = int(data[3][8:])

    return results


#enc = EncryptorDecryptor()

# aa = b'123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123ewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewr2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef123r2wefdewfwfwefwef\r\n'
# print("pre_len ",type(aa) == bytes)
# #aa = enc.encrypt(aa)
# print("post_len ", len(aa), aa)
# #aa = enc.decrypt(aa)
# print("post2_len ", len(aa), aa)