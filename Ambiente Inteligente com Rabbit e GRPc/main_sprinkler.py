
from objects.sprinkler import Sprinkler

from objects.grpc_logic.object_servicer import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import grpc

#-----------------Setup de variáveis
queue_principal = 'home'
end_queue = 'close'

name_queue = input('Nome do sprinkler: ')
hum_initial = input("Qual a umidade atual do solo (em %)? ")
sprinkler_port = input("Port: ")

sprinkler = Sprinkler(False, hum_initial, name_queue)

#----------------RabbitMQ setup
connection, channel = sprinkler.connect_rabbit()

sprinkler.set_queue(channel, sprinkler.queue) #queue do objeto sprinkler
sprinkler.set_queue(channel, queue_principal) #se liga com a queue principal
sprinkler.set_queue(channel, end_queue)
sprinkler.send_queue(channel, f"{sprinkler.queue} {sprinkler_port}", queue_principal) #envia a queue do objeto sprinkler pro home assistent conectar com sua fila (queue recepção)
sprinkler.send_frequency_updates(channel)

#----------------GRPC Setup

#sprinkler.start_grpc_server(sprinkler) -- não funciona se for encapsulado dessa forma(motivos misteriosos)
sprinkler_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(sprinkler), sprinkler_grpc_server)
sprinkler_grpc_server.add_insecure_port(f"localhost:{sprinkler_port}")
sprinkler_grpc_server.start()
#-----------------------Procurar como refatorar isso depois

input('Pressione ENTER para sair\n')
sprinkler.close(connection, channel, end_queue)