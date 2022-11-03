
from objects.lamp import Lamp

from objects.grpc_logic.object_servicer import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import grpc

#Nome das filas criadas pelo home assistant
queue_principal = 'home'
end_queue = 'close'

#Nome da fila e do objeto que ficara salvo em uma lista no home assistant
name_queue = input('Nome da Lâmpada: ')
#Luminosidade atual do ambiente
#Talvez se ja setasse um valor fixo, e pra cada lampada so somasse esse valor...
lum_inicial = input("Qual a luminosidade ambiente (em %)? ")
#Porta de comunicacao
lamp_port = input("Port: ")

#Status inicial do objeto
lamp = Lamp(False, lum_inicial, name_queue)

#---------------------------------------------------------------------------------------------

#Comunicacao RabbitMQ
connection, channel = lamp.connect_rabbit()

#Cria fila para o objeto em questao
lamp.set_queue(channel, lamp.queue)
#Cria fila principal do home assistant, caso ela ja nao exista
lamp.set_queue(channel, queue_principal)
#Cria fila de termino do home assistant, caso ela ja nao exista
lamp.set_queue(channel, end_queue)

#Envio do nome da fila do objeto para o home assistent se conectar com sua fila
lamp.send_queue(channel, f"{lamp.queue} {lamp_port}", queue_principal) 
#Envio da mensagem com seu conteudo (nome, estado, atributo)
lamp.send_luminosity_updates(channel)

#---------------------------------------------------------------------------------------------

#Comunicacao gRPC

lamp_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(lamp), lamp_grpc_server)
lamp_grpc_server.add_insecure_port(f"localhost:{lamp_port}")
lamp_grpc_server.start()

#---------------------------------------------------------------------------------------------

input('Pressione ENTER para sair\n')
#Fecha conexao enviando o nome da fila/objeto para a fila close
lamp.close(connection, channel, end_queue)