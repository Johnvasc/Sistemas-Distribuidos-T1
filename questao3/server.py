import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
conexoes = []
index = 0
interrupt = {"active": True, "index": 0}
dinossauro = True

# Thread que faz a recepção de dados do gadget

def gadget():
    partiConn = conn
    partiIndex = index
    while True:
        re = partiConn.recv(1024).decode()
        print(f"gadget disse: {re}")
        if not re: break
        if conexoes[partiIndex]['status'] == True:
            try:
                aplConn.sendall(bytes(re, 'utf-8'))
            except:
                print("nn achei o aplicativo")
        else: print("mas o gateway nn enviou ao iotApp!")

# Thread que faz a recepção de dados da aplicação IoT
def iotApp():
    print("aplicativo conectado!")
    while True:
        le = aplConn.recv(1024).decode()
        print(le)
        if le[0:3] == 'onn' or le[0:3] == 'off':
            for i in conexoes:
                if le[4:8] == i['id']:
                    try:
                        if le[0:3] == 'onn':
                            i['status'] = True
                            print([f'o {i["nome"]} foi habilitado!'])
                        elif le[0:3] == 'off':
                            i['status'] = False
                            print([f'o {i["nome"]} foi desabilitado!'])
                    except:
                        print('o gadget não foi encontrado!')
        if not le: break

while True:
    print('aguardando conexao...')
    conn, addr = s.accept()
    data = conn.recv(1024).decode()

# Conexão do gadget com o gateway
    if data[0:9] == 'iotGadget':
        print(f"gadget iot encontrado\naddr:{addr}\n")
        # serialização aqui!!!!!!!!!!!!!!
        var = {'nome': data[29:], 'id': data[13:17], 'tipo': data[21:25], 'link': conn, 'status': False}
        conexoes.append(var)
        threading.Thread(target=gadget).start()
        index += 1

# Conexão da aplicação iot com o gateway
    elif data == 'iotAplication':
        aplConn = conn
        aplAddr = addr
        msg = 'conectado ao servidor.'
        aplConn.sendall(bytes(msg, 'utf-8'))
        threading.Thread(target=iotApp).start()

