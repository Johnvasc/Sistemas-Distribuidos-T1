
import socket
import threading
import time
from prettytable import PrettyTable

#Formato das mensagens
FORMAT = 'UTF-8'

#Constante para ligar/desligar a aplicacao
CONNECTION = False

#IP da aplicacao/Porta da aplicacao
ip_server = socket.gethostbyname(socket.gethostname())
port = 12356

#Endereco da aplicacao
ADDR = (ip_server, port)

#Enquanto a conexao com o Home assistant nao eh feita...
app_socket = None

#Funcao de recebimento de mensagens
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

##Funcao de envio de mensagens
def write(client_socket, message):
    client_socket.send(message.encode(FORMAT))

#Funcao criada para apresentacao dos comandos validos para o usuario
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

#Funcao de recebimento de comandos do usuario da aplicacao
def command_line(client_socket):
    global CONNECTION
    print("Seja bem vindo!")
    print("######################")
    print("Digite o comando desejado, para saber os comandos digite: /commands")
    while True:
        time.sleep(3)   #Evitar spam e dar tempo de alguma modificacao ser realizada
        command = input('\nWrite a command: ')
        command_split = command.split()
        try:
            #Lista dos diferentes comandos
            if command_split[0] == 'request_list':
                write(client_socket, command)
            elif command_split[0] == 'exit':
                write(client_socket, command)
                print('Desconectando....')
                client_socket.close()
                print('Desconectado do Home Assistant')
                #Quebra do Loop infinito rodando na Main()
                CONNECTION = False
                break
            elif command_split[0] == '/commands':
                #Funcao com a tabela com os comandos validos
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
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect(ADDR)
        print("Server Conected!")

        receive_thread = threading.Thread(target=receive, args=(client_socket,), daemon = True)
        receive_thread.start()

        receive_thread = threading.Thread(target=command_line, args=(client_socket,), daemon = True)
        receive_thread.start()

        app_socket = client_socket
    except:
        print("Tentando estabelecer conexão...")

#Com a conexao com o Home assistant, ficamos em um Loop infinito ate a conexao ser fechada.

CONNECTION = True
while CONNECTION: CONNECTION

app_socket.close()

#Comandos validos para nao se esquecer:
# request_list
# <objeto> set_status_on
# <objeto> set_status_off
# <objeto> set_attribute <valor>
# <objeto> request_status true/false