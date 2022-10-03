import socket
import random
import time

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mensagem de identificação do gadget ao servidor
s.connect((HOST, PORT))
msg = 'iotGadget_ID:1235_TY:Pass_NA:gadgetUmidade'
s.sendall(bytes(msg, 'utf-8'))
#funcionamento do gadget de sensor contínuo, da umidade entre 60 e 70% e dorme por 8s
while True:
    umid = random.randrange(60, 70)
    msg = f"umidade: {umid}%"
    print(msg)
    s.sendall(bytes(msg, 'utf-8'))
    time.sleep(8)
