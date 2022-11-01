
from objects.ac import Ac

from objects.grpc_logic.object_servicer import ObjectServicer
from concurrent import futures
from generated import object_pb2_grpc
import grpc

#-----------------Setup de variáveis
queue_principal = 'home'
end_queue = 'close'

name_queue = input('Nome do AC: ')
temp_inicial = input("Qual a temperatura ambiente (em °C)? ")
ac_port = input("Port: ")

ac = Ac(False, temp_inicial, name_queue)

#----------------RabbitMQ setup
connection, channel = ac.connect_rabbit()

ac.set_queue(channel, ac.queue) #queue do objeto ac
ac.set_queue(channel, queue_principal) #se liga com a queue principal
ac.set_queue(channel, end_queue)
ac.send_queue(channel, f"{ac.queue} {ac_port}", queue_principal) #envia a queue do objeto ac pro home assistent conectar com sua fila (queue recepção)
ac.send_temperature_updates(channel)

#----------------GRPC Setup

#ac.start_grpc_server(ac) -- não funciona se for encapsulado dessa forma(motivos misteriosos)
ac_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(ac), ac_grpc_server)
ac_grpc_server.add_insecure_port(f"localhost:{ac_port}")
ac_grpc_server.start()
#-----------------------Procurar como refatorar isso depois

input('Pressione ENTER para sair\n')
ac.close(connection, channel, end_queue)