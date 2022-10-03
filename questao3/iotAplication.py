from concurrent.futures import thread
import socket
import threading

def Helpme():
    print('Bem-vindo a aplicação IoT!')
    print('As opções 1 e 2 conectam os sensores do Gateway a aplicação, assim vc pode observar os dados na opção 3')
    print('A opção 4 lista todos os sensores conectados')
    print('A opção 5 vc seta o nº de dados recebidos em 3 até encerrar\n')

# Cabeçalho do cliente

PORT = 6789
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = 'iotAplication'
s.sendall(bytes(msg, 'utf-8'))
id = 0
ola = False
dataReceptEnd = 5
nConect = 0

# Vizualização dos dados

def recept():
    i = 0
    while True:
        data = s.recv(1024).decode('utf-8')
        if not data:
            s.close()
            break
        print(data)
        if i >= dataReceptEnd:
            i = 0
            break
        i += 1

checkThread = False
while 1:
    checkThread = threading.Thread(target=recept).is_alive()
    if checkThread == False:
        escolha = input('1 - Conectar gadget\n2 - Desconectar gadget\n3 - Visualizar dados\n4 - Listar gadgets\n5 - Escolher n dados recebidos\nh - ajuda\n')
        if escolha == '1':
            id = input('escolha o id do gadget: ')
            msg = f'onn_{id}'
            try:
                s.sendall(bytes(msg, 'utf-8'))
                nConect += 1
            except: print('a conexao falhou!')
        elif escolha == '2':
            id = input('escolha o id do gadget: ')
            msg = f'off_{id}'
            try:
                s.sendall(bytes(msg, 'utf-8'))
                nConect -= 1
            except: print('a conexão falhou!')
        elif escolha == '3':
            print(nConect)
            if nConect > 0:
                threading.Thread(target=recept).run()
            else: print('não existe nenhum sensor conectado. Se conecte e tente novamente!')
        elif escolha == '4':
            msg = f'lis_{id}'
            s.sendall(bytes(msg, 'utf-8'))
        elif escolha == '5':
            dataReceptEnd = input('Escolha o número de dados recebidos até fechar conexão: ')
            dataReceptEnd = int(dataReceptEnd)
        elif escolha == 'h': Helpme()

