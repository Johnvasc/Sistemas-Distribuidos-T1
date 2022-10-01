import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
conexoes = []
count = 0
interrupt = {"active": True, "index": 0}


def gadget():
    while True:
        if interrupt['active'] == False and interrupt['index'] == addr:
            break
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
#aqui faz a conexão com os gadgets iot
    if data == 'iotGadget':
        print(f"gadget iot encontrado\naddr:{addr}\n")
        threading.Thread(target=gadget).start()
        count += 1
        print(count)
#aqui faz a conexão com a aplicação iot
    elif data == 'iotAplication':
        print("aplicativo conectado!")
        aplConn = conn
        aplAddr = addr
        msg = 'conectado ao servidor.'
        aplConn.sendall(bytes(msg, 'utf-8'))
        '''threading.Thread(target='apli')'''
#aqui é o comando para desativar o gadget
    elif data[0:3] == 'des':
        interrupt['index'] = data[4:]
        interrupt['active'] = False
#aqui é o comando para ativar novamente o gadget
    elif data[0:3] == 'ati':
        num = data[5:]
        conexoes[num] = True
    if not data: break
    '''conn.sendall(data.upper())
    conn.close()
'''
