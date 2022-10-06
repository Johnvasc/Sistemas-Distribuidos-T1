import socket
import threading
import protobuf.mensagens_apl_gate_pb2 as troca_msg
import time

#Padronizacao do formato das mensagens
FORMAT = 'utf-8' 

#Setando o IP e a porta do gateway que a aplicacao vai se comunicar
IP_gateway = socket.gethostbyname(socket.gethostname())
PORT_gateway = 12345
ADDR_gateway = (IP_gateway, PORT_gateway)

#Setando o IP e a porta da aplicacao em si
IP_apl = socket.gethostbyname(socket.gethostname())
PORT_apl = 1245
ADDR_apl = (IP_apl, PORT_apl)

def receive(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            message_decoded = troca_msg.MensagemGateway()
            message_decoded.ParseFromString(message)

            print(message_decoded)
        except Exception as e:
            print(e)
            client_socket.close()
            break

def write(client_socket, message):
    client_socket.send(message)

def lista_objetos(client_socket):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "lista_objetos"

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(client_socket, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

def estado_objeto(client_socket, objeto):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "estado_objeto"
    mensagem.valor = objeto

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(client_socket, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

def mudar_estado(client_socket, valor):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "mudar_estado"
    mensagem.valor = valor

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(client_socket, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

def mudar_valor(client_socket, valor):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "mudar_valor"
    mensagem.valor = valor

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(client_socket, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

#Funcao main para receber os comandos a serem enviados ao gateway
def main(client_socket):
    while True: 
        time.sleep(1)     #Esperar um tempo antes de mandar outro comando (evitar spam) 
        comando = input('\nLista de comandos possiveis:\n1.lista_objetos\n2.estado_objeto nome_objeto\n3.mudar_estado nome_objeto funcao\n4.mudar_valor nome_objeto atributo valor\n\nDigite seu comando: ')
        commando_split = comando.split()

        #Lista de opcoes possiveis
        try:
            if commando_split[0] == 'lista_objetos': #Lista objetos presentes no gateway
                lista_objetos(client_socket)
            elif commando_split[0] == 'estado_objeto':  #Saber os atributos do objeto
                estado_objeto(client_socket, commando_split[1])
            elif commando_split[0] == 'mudar_estado':   #Mudar o estado do objeto (ligado/desligado)
                mudar_estado(client_socket,f"{commando_split[1]} {commando_split[2]}")
            elif commando_split[0] == 'mudar_valor':    #Mudar o valor do atributo (se existir) no objeto
                mudar_valor(client_socket,f"{commando_split[1]} {commando_split[2]} {commando_split[3]}")
            else:
                print('Comando invalido. Tente novamente!')
        except:
            print('Comando invalido. Tente novamente!')

#Abertura de conexao via TCP com o gateway
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(ADDR_apl)
client_socket.connect(ADDR_gateway)
print("-> Conectado com o Gateway!")

#Thread para ficar recebendo as mensagens do gateway
receive_thread = threading.Thread(target=receive, args=(client_socket,  ))
receive_thread.start()
print("-> Pronto para receber as mensagens do Gateway!")

main(client_socket)