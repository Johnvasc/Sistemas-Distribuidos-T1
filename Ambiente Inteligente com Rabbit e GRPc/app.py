import socket
import threading
import time
import sys
from prettytable import PrettyTable

FORMAT = 'UTF-8'
CONNECTION = False
ip_server = socket.gethostbyname(socket.gethostname())
port = 12356
ADDR = (ip_server, port)
app_socket = None

def connect_home_assistant(ADDR):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(ADDR)
    print("Server Conected!")

    receive_thread = threading.Thread(target=receive, args=(client_socket,), daemon = True)
    receive_thread.start()

    receive_thread = threading.Thread(target=command_line, args=(client_socket,), daemon = True)
    receive_thread.start()

    return client_socket

def receive(client_socket):
    global CONNECTION
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)
            if not message:
                print("\nConexão perdida...")
                CONNECTION = False
                break
        except:
            print("\nConexão perdida...")
            CONNECTION = False
            break

def write(client_socket, message):
    client_socket.send(message.encode(FORMAT))

def get_commands():
    table_commands = PrettyTable()
    table_commands.field_names = ["Comando", "Descrição"]
    table_commands.add_row(["request_list", "Retorna lista dos objetos disponíveis"])
    table_commands.add_row(["[objeto] set_status_on", "Liga o objeto desejado"])
    table_commands.add_row(["[objeto] set_status_off", "Desliga o objeto desejado."])
    table_commands.add_row(["[objeto] request_status", "Verifica se o objeto está ligado/desligado e o valor obtido pelo sensor ambiente"])
    table_commands.add_row(["[objeto] set_attribute [valor]", "Seta o valor desejado do atributo do objeto "])
    table_commands.add_row(["exit", "Desliga a aplicação"])

    return table_commands

def command_line(client_socket):
    global CONNECTION
    print("Seja bem vindo!")
    print("######################")
    print("Digite o comando desejado, para saber os comandos digite: /commands")
    while True:
        time.sleep(1)
        command = input('\nWrite a command: ')
        command_split = command.split()
        try:
            if command_split[0] == 'request_list':
                write(client_socket, command)
            elif command_split[0] == 'exit':
                write(client_socket, command)
                print('Desconectando....')
                client_socket.close()
                print('Desconectado do Home Assistant')
                CONNECTION = False
                break
            elif command_split[0] == '/commands':
                print(get_commands())
            elif command_split[1] == 'set_status_on':
                write(client_socket, command)
            elif command_split[1] == 'set_status_off':
                write(client_socket, command)
            elif command_split[1] == 'set_attribute':
                write(client_socket, command)
            elif command_split[1] == 'request_status':
                write(client_socket, command)
            else:
                print('Invalid Command!')
        except Exception as e:
            print(f"Algo deu errado... \n{e}")

print('Aguardando conexão com o Home Assistant....')
while app_socket == None:
    try:
        time.sleep(1)
        app_socket = connect_home_assistant(ADDR)
    except:
        print("Tentando estabelecer conexão...")

CONNECTION = True
while CONNECTION: CONNECTION

app_socket.close()
# request_list
# L1 SetStatusOn
# L1 SetStatusOff
# L1 SetAttribute 30
# L1 RequestStatus