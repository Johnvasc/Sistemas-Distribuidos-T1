import socket
import threading

command_join = input('Bem-vindo!\nSe quiser participar do chat, digite o comando /ENTRAR.\nComando: ')

while command_join != '/ENTRAR':
    print(f'{command_join} não é um comando válido, tente novamente!')
    command_join = input('Se quiser participar do chat, digite o comando /ENTRAR.\nComando: \n')

print('Ok, estamos quase lá...')

server_ip = input('Informe o ip do servidor: ')
server_port = input('Informe a porta do servidor: ')

while True:
    if (server_ip == 'localhost' or server_ip == '127.0.0.1') and int(server_port) == 12345:
        print(f'Servidor: {server_ip} na porta: {server_port} encontrado!')
        break
    else:
        if (server_ip != 'localhost' or server_ip != '127.0.0.1') and int(server_port) == 12345:
            print(f'Servidor não encontrado!\nFalha ao se conectar ao ip informado!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                print(connect_resp)
                connect_resp = connect_resp.lower()
                print(connect_resp)
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    print(connect_resp)
                    connect_resp = connect_resp.lower()
                    print(connect_resp)
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()
        elif (server_ip == 'localhost' or server_ip == '127.0.0.1') and int(server_port) != 12345:
            print(f'Servidor não encontrado!\nFalha ao se conectar pela porta informada!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                connect_resp = connect_resp.lower()
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    connect_resp = connect_resp.lower()
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()
        else:
            print(f'Servidor não encontrado!\nip e porta inválidos!\n')
            connect_resp = input('Usuário ainda quer tentar se conectar? S para sim N para não\nResposta: ')
            connect_resp = connect_resp.lower()
            if connect_resp == 's':
                server_ip = input('Informe o ip do servidor: ')
                server_port = input('Informe a porta do servidor: ')
            elif connect_resp == 'n':
                print('Entendo, até mais!')
                exit()
            else:
                print('Valor inválido, tente novamente!')
                connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                connect_resp = connect_resp.lower()
                while connect_resp != 's' and connect_resp != 'n':
                    print('Valor inválido, tente novamente!')
                    connect_resp = input('Continuar tentando? S para sim N para não\nResposta: ')
                    connect_resp = connect_resp.lower()
                if connect_resp == 's':
                    server_ip = input('Informe o ip do servidor: ')
                    server_port = input('Informe a porta do servidor: ')
                else:
                    print('Entendo, até mais!')
                    exit()

#ISSO É UM TIRO NO PÉ, O SERVER TEM QUE ESTÁ ONLINE ANTES DISSO
#SENAO ELE PEDE O NICKNAME SEM O SERVER ESTAR ONLINE
print('Conectado ao servidor!')

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(server_ip), int(server_port)))

#receive_thread = threading.Thread(target=self.receive)
#receive_thread.daemon = True
#receive_thread.start()
#write_thread = threading.Thread(target=self.write)
#write_thread.daemon = True
#write_thread.start()

def receive():
    while True:
        try:
            #print('aaa')
            message = client.recv(1024).decode('utf-8')
            #print(message)
            #print('bbb')
            if message == 'NICK':
                #print('aaaaaaaaaaaaaa')
                client.send(nickname.encode('utf-8'))

            else:
                print(message)
        except:
            print('And error occurred!')
            client.close()
            break

#SE EU SAIU COM CRTL+C NAO SOME DA LISTA DE CLIENTES NA SERVIDOR
def write():
    while True:
        message = f'{nickname}: {input("")}'
        #print('aqui')
        #JA ENTENDI, A MENSAGEM NAO E A QUE TA NO SERVIDOR
        #ENTAO TEM QUE MODIFICAR AQUI COM ALGUMA QUEBRA, OU
        #QUE TALVEZ SEJA MELHOR, NO PROPRIO SERVIDOR, MAS ANTES
        #VER COMO FOI FEITO PELO RICARDO
        if message:
            print(message)
            if message == '/SAIR':
                client.send(message.encode('utf-8'))
                print('Sessão encerrada!')
                client.close()
                exit()
            elif message == 'sair': #TIRAR ISSO DEPOIS
                exit()
            else:        
                client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
#receive_thread.daemon = True
receive_thread.start()
write_thread = threading.Thread(target=write)
#write_thread.daemon = True
write_thread.start()
