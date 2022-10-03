from concurrent.futures import thread
import socket
import threading
import pickle

def Helpme():
    print('\nBem-vindo a aplicação IoT!')
    print('- Opções 1 e 2: Permite conectar-se ou desconectar-se a um tipo de sensor e receber seus dados.')
    print('   -  neste caso insira a id do gadget e pronto!')
    print('- Opção 3: Permite que vizualise os dados de sensores continuos.')
    print('- Opção 4: Lista todos os sensores conectados e mais algumas informações.')
    print('- Opção 5: Seta o nº de dados recebidos em 3 até encerrar.')
    print('- Opção 6: Permite ligar ou desligar lampadas.')
    print('   -  escolha a opção 1 para ligar ou 2 para desligar a lampada.')
    print('   -  o status da lampada pode ser visualizado na opção 4.\n')

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
bdConexoes = []
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
        escolha = input('1 - Conectar gadget\n2 - Desconectar gadget\n3 - Visualizar dados\n4 - Listar gadgets\n5 - Escolher n dados recebidos\n6 - Ligar/desligar gadget\nh - ajuda\n')
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
            escolha = input('1 - Atualizar banco de dados\n2 - ñ atualizar o banco de dados\n')
            if escolha == '1':
                msg = 'lis'
                s.sendall(bytes(msg, 'utf-8'))
                aux = s.recv(4096)
                print(aux)
                bdConexoes = pickle.loads(aux)
                print('o banco de dados foi atualizado!')
            for i in bdConexoes:
                print(i)
        elif escolha == '5':
            dataReceptEnd = input('Escolha o número de dados recebidos até fechar conexão: ')
            dataReceptEnd = int(dataReceptEnd)
        elif escolha == '6':
            escolha = input('1 - Ligar Gadget\n2 - Desligar Gadget\n')
            id = input('escolha o id do gadget: ')
            if escolha == '1': msg = f'gon_{id}'
            elif escolha == '2': msg = f'gof_{id}'
            try: s.sendall(bytes(msg, 'utf-8'))
            except: print('o comando falhou!')
        elif escolha == 'h': Helpme()

