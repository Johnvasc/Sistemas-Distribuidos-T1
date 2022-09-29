import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
conexoes = []
count = 0

def gadget():
    while True:
        re = conn.recv(1024).decode()
        print(f"gadget disse: {re}")
        if not data: break
        try:
            aplConn.sendall(bytes(re, 'utf-8'))
        except:
            print("nn achei o aplicativo")

while True:
    print('aguardando conexao')
    conn, addr = s.accept()
    data = conn.recv(1024).decode()
    if data == 'iotGadget':
        print(f"gadget iot encontrado\naddr:{addr}\n")
        threading.Thread(target=gadget).start()
    elif data == 'iotAplication':
        print("aplicativo conectado!")
        aplConn = conn
        aplAddr = addr
        msg = 'conectado ao servidor.'
        aplConn.sendall(bytes(msg, 'utf-8'))
        '''threading.Thread(target='apli')'''
    if not data: break
    '''conn.sendall(data.upper())
    conn.close()
'''
