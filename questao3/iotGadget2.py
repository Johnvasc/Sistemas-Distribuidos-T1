import socket
import random
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = 'iotGadget'
s.sendall(bytes(msg, 'utf-8'))
while True:
    temp = random.randrange(60, 70)
    msg = f"umidade: {temp}%"
    s.sendall(bytes(msg, 'utf-8'))
    time.sleep(15)
'''data = s.recv(1024).decode('utf-8')
s.close()
'''