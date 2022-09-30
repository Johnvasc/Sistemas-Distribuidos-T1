from pydoc import cli
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
    for c in clientes_atuais:
        c.send(message)

def see_users(client):
    print('entrei')
    msg_online = '\nUsuarios onlines:\n'
    aux = 0
    for clt_online in nicknames:
        #print(msg_online)
        msg_online += "{} \n".format(str(nicknames[aux]))
        aux+=1
    msg_solo(msg_online,client)

def msg_solo(msg, client):
    try:
        print('cheguei aqui')
        client.send(msg.encode('utf-8'))
    except:
        leave_chat(client)

def leave_chat(client):
    client.send('Saindo do servidor, espere...'.encode('utf-8'))
    index = clientes_atuais.index(client)
    clientes_atuais.remove(client)
    client.send('Desconectado!'.encode('utf-8'))
    client.close()
    nickname = nicknames[index]
    broadcast(f'{nickname} left the chat!'.encode('utf-8'))
    print(f'{nickname} left!')
    nicknames.remove(nickname)

def handle(client):
    while True:
        if len(clientes_atuais) > 0:
            try:
                message = client.recv(1024)
                msg_decode = message.decode('utf-8')
                #print(message)
                if msg_decode:
                    #print('entrei')
                    if msg_decode[0] == '/':
                        if msg_decode == '/USUARIOS':
                            #print('entrei')
                            print(msg_decode)
                            see_users(client)
                        elif msg_decode == '/SAIR':
                            leave_chat(client)
                            break
                        else:
                            wrong_msg = "Comando invalido.\nLista de comandos válidos: \n/USUARIOS\n/SAIR\n"
                            client.send(wrong_msg.encode('utf-8'))
                    else:
                        #print(message)
                        broadcast(message)
                
            except:
                print('Errei')
                if client in clientes_atuais:
                    leave_chat(client)
                    break

def receive():
    print('Pronto para receber os usuários!')
    while True:
        try:
            client, address = server.accept()
            print(f'Connected with {str(address)}')
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clientes_atuais.append(client)
            print(f'Nickname of the client is {nickname}')
            broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))

            handle_clients = threading.Thread(target=handle, args=(client,))
            handle_clients.start()
            
        except:
            pass

receive_clients = threading.Thread(target=receive)
receive_clients.daemon = True
receive_clients.start()
#handle_clients = threading.Thread(target=handle)
#handle_clients.daemon = True
#handle_clients.start()

while True:
    message = input('/> ')
    if message == 'close':
        server.close()
        sys.exit()
    else:
        pass