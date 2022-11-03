
from objects.sprinkler import Sprinkler

from objects.grpc_logic.object_servicer import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import grpc

#Nome das filas criadas pelo home assistant
queue_principal = 'home'
end_queue = 'close'

#Nome da fila e do objeto que ficara salvo em uma lista no home assistant
name_queue = input('Nome do sprinkler: ')
#Umidade atual do ambiente
hum_initial = input("Qual a umidade atual do solo (em %)? ")
#Porta de comunicacao
sprinkler_port = input("Port: ")

#Status inicial do objeto
sprinkler = Sprinkler(False, hum_initial, name_queue)

#---------------------------------------------------------------------------------------------

#Comunicacao RabbitMQ
connection, channel = sprinkler.connect_rabbit()

#Cria fila para o objeto em questao
sprinkler.set_queue(channel, sprinkler.queue) #queue do objeto sprinkler
#Cria fila principal do home assistant, caso ela ja nao exista
sprinkler.set_queue(channel, queue_principal) #se liga com a queue principal
#Cria fila de termino do home assistant, caso ela ja nao exista
sprinkler.set_queue(channel, end_queue)

#Envio do nome da fila do objeto para o home assistent se conectar com sua fila
sprinkler.send_queue(channel, f"{sprinkler.queue} {sprinkler_port}", queue_principal) #envia a queue do objeto sprinkler pro home assistent conectar com sua fila (queue recepção)
#Envio da mensagem com seu conteudo (nome, estado, atributo)
sprinkler.send_frequency_updates(channel)

#---------------------------------------------------------------------------------------------

#Comunicacao gRPC
sprinkler_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(sprinkler), sprinkler_grpc_server)
sprinkler_grpc_server.add_insecure_port(f"localhost:{sprinkler_port}")
sprinkler_grpc_server.start()

#---------------------------------------------------------------------------------------------

input('Pressione ENTER para sair\n')
#Fecha conexao enviando o nome da fila/objeto para a fila close
sprinkler.close(connection, channel, end_queue)