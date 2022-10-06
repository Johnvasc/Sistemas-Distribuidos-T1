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

#Receber mensagens do gateway
def receive(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            mensagem_decod = troca_msg.MensagemGateway()
            mensagem_decod.ParseFromString(mensagem)

            print(mensagem_decod)
        except Exception as e:
            print(e)
            cliente.close()
            break

#Enviar mensagem
def write(cliente, mensagem):
    cliente.send(mensagem)

#Listar objetos mandando requisicao para o gateway
def lista_objetos(cliente):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "lista_objetos"

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(cliente, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

#Saber o estado do objeto requisitado mandando requisicao para o gateway
def estado_objeto(cliente, objeto):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "estado_objeto"
    mensagem.valor = objeto

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(cliente, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

#Mudar o estado do objeto requisitado mandando requisicao para o gateway
def mudar_estado(cliente, valor):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "mudar_estado"
    mensagem.valor = valor

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(cliente, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

#Mudar o valor de algum atributo do objeto requisitado mandando requisicao para o gateway
def mudar_valor(cliente, valor):
    mensagem = troca_msg.MensagemAplicacao()
    mensagem.tipo = troca_msg.MensagemAplicacao.TipoMensagem.COMANDO
    mensagem.comando = "mudar_valor"
    mensagem.valor = valor

    print("-> Enviando mensagem...")

    mensagem_serial = mensagem.SerializeToString()
    write(cliente, mensagem_serial)
    print("-> Mensagem enviada!")

    return None

#Funcao main para receber os comandos a serem enviados ao gateway
def main(cliente):
    while True: 
        time.sleep(1)     #Esperar um tempo antes de mandar outro comando (evitar spam) 
        comando = input('\nLista de comandos possiveis:\n1.lista_objetos\n2.estado_objeto nome_objeto\n3.mudar_estado nome_objeto funcao\n4.mudar_valor nome_objeto atributo valor\n\nDigite seu comando: ')
        commando_split = comando.split()

        #Lista de opcoes possiveis
        try:
            if commando_split[0] == 'lista_objetos': #Lista objetos presentes no gateway
                lista_objetos(cliente)
            elif commando_split[0] == 'estado_objeto':  #Saber os atributos do objeto
                estado_objeto(cliente, commando_split[1])
            elif commando_split[0] == 'mudar_estado':   #Mudar o estado do objeto (ligado/desligado)
                mudar_estado(cliente,f"{commando_split[1]} {commando_split[2]}")
            elif commando_split[0] == 'mudar_valor':    #Mudar o valor do atributo (se existir) no objeto
                mudar_valor(cliente,f"{commando_split[1]} {commando_split[2]} {commando_split[3]}")
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