import socket
import threading
import protobuf.mensagens_apl_gate_pb2 as troca_msg
from multicast.send_group import send_multicast 

#Padronizacao do formato das mensagens
FORMAT = "utf-8"

#Setando o IP e a porta do gateway
IP_gateway = socket.gethostbyname(socket.gethostname())
PORT_gateway = 12345
ADDR_gateway = (IP_gateway, PORT_gateway)

#Endereco da aplicacao
ADDR_apl = ('192.168.1.103', 1245)

v_tipos_clientes = []
v_clientes = []
apl_socket = [] #Vou precisar para mandar mensagens dos objetos a aplicacao passando pelo gateway
ac_infos = ''   #Constantemente precisa saber disso

#Enviar o IP e porta via multicast
def gateway_msg_multicast():
    mensagem = f"{IP_gateway} {PORT_gateway}"
    while True:
        try:
            send_multicast(mensagem)
        except:
            print('Mensagem ao multicast nao enviada!')

#Enviar mensagem do gateway para um objeto
def gateway_objeto(index_objeto, mensagem):
    v_clientes[index_objeto].send(mensagem.encode(FORMAT))

def handle(client):    
    while True:
        try:
            #Para poder se comunicar com a aplicacao
            mensagem = troca_msg.MensagemGateway()
            mensagem.tipo_resposta = troca_msg.MensagemGateway.TipoMensagem.PEGAR

            #Para receber mensagem do objeto

            #bota um try aqui
            msg_objeto = client.recv(1024)
            msg_objeto_d = msg_objeto.decode(FORMAT)

            #Infos do ar-condicionado
            if msg_objeto_d.split()[0] == 'AC':
                global ac_infos 
                ac_infos = f"AC {msg_objeto_d.split()[1]} {msg_objeto_d.split()[2]}"
                print(ac_infos)

            #Infos dos demais objetos
            elif msg_objeto_d.split()[0] == 'Lamp' or msg_objeto_d.split()[0] == 'Irrig':
                info = msg_objeto_d
                print(info)
                
                objeto_aux = mensagem.objeto.add()
                objeto_aux.tipo = msg_objeto_d.split()[0]
                objeto_aux.estado = info.split()[1]

                mensagem_serial = mensagem.SerializeToString()
                apl_socket[0].send(mensagem_serial)

            #So retorna pra conexao normal
            else:
                mensagem = 'Conexao com o gateway estabelecida via TCP!\n'
                client.send(mensagem.encode(FORMAT))

        except Exception as e:
            print(e)
            client.close()
            break

#Funcao para objeto sensor com intuito de saber seus estados
def sensor(objeto):
    mensagem = troca_msg.MensagemGateway()
    mensagem.tipo_resposta = troca_msg.MensagemGateway.TipoMensagem.PEGAR

    if objeto == "AC":
        info = ac_infos

    #Separa todas as infos
    objeto_aux = mensagem.objeto.add()
    objeto_aux.tipo = info.split()[0]
    objeto_aux.temp = int(info.split()[1])
    objeto_aux.estado = info.split()[2]

    mensagem_serial = mensagem.SerializeToString()
    apl_socket[0].send(mensagem_serial)

#Listagem dos objetos conectados
def lista_objetos_gtw(client):
    mensagem = troca_msg.MensagemGateway()
    mensagem.tipo_resposta = troca_msg.MensagemGateway.TipoMensagem.LISTAR
    
    #Armazenar todos os tipos de objetos
    for i in v_tipos_clientes:
        tipo_ob = mensagem.objeto.add()
        tipo_ob.tipo = i

    mensagem_serial = mensagem.SerializeToString()
    client.send(mensagem_serial)

#Apresentar todos os estados do objeto requerido
def estado_objeto_gtw(objeto):

    objeto_aux = objeto

    #Como os estados mudam dependendo do objeto, procuro por tipo de objeto
    for i in range(0, len(v_tipos_clientes)):
        if v_tipos_clientes[i] == objeto_aux:
            if objeto_aux == "AC":
                sensor(objeto_aux)
            else:
                gateway_objeto(i , f"estado_objeto")

#Setar um estado para o objeto requerido
def mudar_estado_gtw(valor):
    objeto_aux = valor.split()[0]
    novo_estado = valor.split()[1]

    for i in range(0, len(v_tipos_clientes)):
        if v_tipos_clientes[i] == objeto_aux:
            gateway_objeto(i , f"mudar_estado {novo_estado}")

#Setar um valor para um atributo do objeto requerido
def mudar_valor_gtw(valor):
    objeto_aux = valor.split()[0]
    atributo = valor.split()[1]
    novo_valor = valor.split()[2]

    for i in range(0, len(v_tipos_clientes)):
        if v_tipos_clientes[i] == objeto_aux:
            gateway_objeto(i , f"mudar_{atributo} {novo_valor}")

def handle_aplicacao(client):
    while True:
        try:
            #Fica esperando a aplicacao enviar algum comando
            print("Esperando comando da aplicacao...")
            mensagem = client.recv(1024)
            mensagem_recebida = troca_msg.MensagemAplicacao()
            mensagem_recebida.ParseFromString(mensagem)
            
            #Dependendo do comando, caira em alguma das condicoes abaixo
            if mensagem_recebida.tipo == 1:
                if mensagem_recebida.comando == 'lista_objetos':
                    lista_objetos_gtw(client)
                elif mensagem_recebida.comando == 'estado_objeto':
                    estado_objeto_gtw(mensagem_recebida.valor)
                elif mensagem_recebida.comando == 'mudar_estado':
                    mudar_estado_gtw(mensagem_recebida.valor)
                elif mensagem_recebida.comando == 'mudar_valor':
                    mudar_valor_gtw(mensagem_recebida.valor)
                else:
                    pass
        except Exception as e:
            print(e)
            client.close()
            break
                    
def main(gateway_socket):
    print("Esperando clientes...\n")
    
    while True:
        try:
            #Aceitando requisicoes
            client, address = gateway_socket.accept()

            #Criacao thread para cuidar das requisicoes apenas da aplicacao
            if address == ADDR_apl: 
                apl_socket.append(client)
                thread_aplicacao = threading.Thread(target=handle_aplicacao, args=(client,))
                thread_aplicacao.start()

            #Criacao thread para cuidar das requisicoes apenas dos objetos
            else:
                #Saber inicialmente que tipo de objeto o cliente eh
                tipo_cliente = client.recv(1024).decode(FORMAT)
                
                v_tipos_clientes.append(tipo_cliente)   #Salvar o tipo do cliente
                v_clientes.append(client)   #Salvar o cliente em si
            
                print(f"Conectado com {str(address)}\n")

                thread_objeto = threading.Thread(target=handle, args=(client,))
                thread_objeto.start()
        except Exception as e:
            print(e)

#Criando gateway com conexao TCP
gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gateway_socket.bind(ADDR_gateway)
gateway_socket.listen()
print("Gateway pronto!\n")

thread_multicast = threading.Thread(target=gateway_msg_multicast)
thread_multicast.start()
#gateway_msg_multicast() #Enviando o IP e a porta do gateway via multicast para todos
main(gateway_socket)