
import socket
import threading
import time
from prettytable import PrettyTable

#Formato das mensagens
FORMAT = 'UTF-8'

#Constante para ligar/desligar a aplicacao
CONNECTION = False

#IP da aplicacao/Porta da aplicacao
ip_server = 'localhost'
#ip_server = socket.gethostbyname(socket.gethostname())
port = 12345

#Endereco da aplicacao
endereco = (ip_server, port)

#Enquanto a conexao com o Home assistant nao eh feita...
socket_app = None

#Funcao de recebimento de mensagens
def receive(socket_cliente):
    global CONNECTION
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode(FORMAT)
            print(mensagem)
            #Caso nao seja recebida a mensagem ou ocorra algum problema, a conexao eh fechada
            if not mensagem:
                print("\nA conexão foi perdida...")
                CONNECTION = False
                break
        except:
            print("\nA conexão foi perdida...")
            CONNECTION = False
            break

##Funcao de envio de mensagens
def write(socket_cliente, mensagem):
    socket_cliente.send(mensagem.encode(FORMAT))

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
def command_line(socket_cliente):
    global CONNECTION
    print("Olá! Bem vindo(a)!")
    print("----------------------------------")
    print("Digite o comando que quer realizar. Se quer saber quais os comandos digite: /commands")
    while True:
        time.sleep(3)   #Evitar spam e dar tempo de alguma modificacao ser realizada
        command = input('\nWrite a command: ')
        command_split = command.split()
        try:
            #Lista dos diferentes comandos
            if command_split[0] == 'request_list':
                write(socket_cliente, command)
            elif command_split[0] == 'exit':
                write(socket_cliente, command)
                print('Desconexão em processamento....')
                socket_cliente.close()
                print('Desconexão do assistente finalizada')
                #Quebra do Loop infinito rodando na Main()
                CONNECTION = False
                break
            elif command_split[0] == '/commands':
                #Funcao com a tabela com os comandos validos
                print(get_commands())
            elif command_split[1] == 'set_status_on':
                write(socket_cliente, command)
            elif command_split[1] == 'set_status_off':
                write(socket_cliente, command)
            elif command_split[1] == 'set_attribute':
                write(socket_cliente, command)
            elif command_split[1] == 'request_status':
                write(socket_cliente, command)
            else:
                print('Comando inválido!')
        except Exception as e:
            print(f"Deu algo errado... \n{e}")

print('Aguardando conexão com o Home Assistant....')
while socket_app == None:
    try:
        time.sleep(1)
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket_cliente.connect(endereco)
        print("Servidor Conectado!")

        #Inicializacao da thread para receber mensagens
        receive_thread = threading.Thread(target=receive, args=(socket_cliente,), daemon = True)
        receive_thread.start()

        #Inicializacao da thread para enviar comandos (requisicoes)
        receive_thread = threading.Thread(target=command_line, args=(socket_cliente,), daemon = True)
        receive_thread.start()

        socket_app = socket_cliente
    except:
        print("Tentando estabelecer uma conexão...")

#Com a conexao com o Home assistant, ficamos em um Loop infinito ate a conexao ser fechada.

CONNECTION = True
while CONNECTION: CONNECTION

socket_app.close()

#Comandos validos para nao se esquecer:
# request_list
# <objeto> set_status_on
# <objeto> set_status_off
# <objeto> set_attribute <valor>
# <objeto> request_status true/false

#Comando para criar o docker para comunicacao RabbitMQ:
#docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management