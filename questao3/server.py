import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
conexoes = []
broad = []
index = 0

# Thread que faz a recepção de dados do gadget

def broadcast():
    for i in broad:
        if i['verificado'] == False:
            i['conexao'].sendall(bytes('Gateway reconheceu', 'utf-8'))
            i['verificado'] == True

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
        #procura um gadget pela id na lista de conexões e seta i status de conexão True ou False (onn ou off)
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
        #procura a conexão do gadget pela lista de conexões e manda uma msg de ligar ou desligar
        elif le[0:3] == 'gon' or le[0:3] == 'gof':
            for i in conexoes:
                if le[4:8] == i['id'] and i['status'] == True:
                    try:
                        i['link'].sendall(bytes(le, 'utf-8'))
                    except:
                        print('o gadget não foi encontrado!')
        #envia a aplicação iot a lista de conectados
        elif le[0:3] == 'lis':
            try:
                aplConn.sendall(bytes(f'toApl_{conexoes}', 'utf-8'))
                print('banco de dados de conexoes mandado p/ o app!')
            except: print('falha ao mandar o banco de dados')
        if not le: break

while True:
    print('aguardando conexao...')
    conn, addr = s.accept()
    var = {'conexao': conn, 'verificado': False}
    broad.append(var)
    broadcast()
    data = conn.recv(1024).decode()
# Conexão do gadget com o gateway
    if data[0:9] == 'iotGadget':
        print(f"gadget iot encontrado\naddr:{addr}\n")
        if data[21:25] == 'Pass': ligado = 'sempre'
        else: ligado = 'desligado'
        var = {'nome': data[29:], 'id': data[13:17],'tipo': data[21:25], 'link': conn, 'status': False, 'ligado': ligado}
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

# Conexão de requisição de gadget
    elif data[0:4] == 'actv':
        for i in conexoes:
            if data[5:9] == i['id'] and i['status'] == True:        
                if data[9:] == 'True': i['ligado'] = 'ligado'
                elif data[9:] == 'False': i['ligado'] = 'desligado'

