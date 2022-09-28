import socket
import threading
import sys

#clientes_online = {}

HOST='localhost'
PORT=12345

clientes_atuais = [] 
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(HOST), int(PORT)))
server.listen(5)
print('Server is listening...')

def broadcast(message):
    for client in clientes_atuais:
        client.send(message)
        print('hello')

def msg_solo(msg, client):
    try:
        client.send(msg)
    except:
        clientes_atuais.remove(client)

def leave_chat(client):
    index = clientes_atuais.index(client)
    clientes_atuais.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast(f'{nickname} left the chat!'.encode('utf-8'))
    nicknames.remove(nickname)

#Não sei se precisa entrar com client tambem (nem pode kk)
def handle(client):
    while True:
        if len(clientes_atuais) > 0:
            try:
                message = client.recv(1024).decode('utf-8')
                if message:
                    msg_client = message.split('/')
                    if len(msg_client) > 1:
                        if msg_client[1] == 'USUARIOS':
                            msg_online = 'Mensagem do Servidor!\nUsuarios onlines:\n'
                            for on in clientes_atuais:
                                print(clientes_atuais[on])
                                msg_online += "{} \n".format(str(clientes_atuais[on][0]))
                            print(msg_online)
                            msg_solo(msg_online,client)
                        elif msg_client[1] == 'SAIR':
                            leave_chat(client)
                        else:
                            wrong_msg = "Comando invalido.\nComandos válidos: /USUARIOS\n/SAIR\n"
                            print(wrong_msg)
                            client.send(wrong_msg)
                else:
                    msg_chat = message.decode('utf-8')
                    broadcast(msg_chat)
                
            except:
                index = clientes_atuais.index(client)
                clientes_atuais.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break

def receive():
    print('Pronto para receber os usuários!')
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        #client.send('NICK'.encode('utf-8'))
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clientes_atuais.append(client)
        print(len(clientes_atuais))

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        handle_clients = threading.Thread(target=handle, args=(client,))
        #handle_clients.daemon = True
        handle_clients.start()

receive_clients = threading.Thread(target=receive)
#receive_clients.daemon = True
receive_clients.start()
#handle_clients = threading.Thread(target=handle)
#handle_clients.daemon = True
#handle_clients.start()

while True: #QUANDO DA CLOSE DA UM ERRO, PRA TENTAR ARRUMAR
    message = input('/> ')
    if message == 'close':
        server.close()
        sys.exit()
    else:
        pass