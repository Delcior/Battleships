'''
Klient TCP
'''
import socket
import numpy as np
CRLF = b"\r\n"
def rec(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        data_rec += sock.recv(1)
    return data_rec.decode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('localhost', 1769))

    a = [[4,2,3,4,2,1,3],[1,2,3,4,5,6,7,8]]
    s.sendall(str(a).encode())

    message_rec = rec(s, CRLF)

    print(message_rec)

    s.close()
except socket.error:
    print ('Error')
except KeyboardInterrupt:
    s.close()