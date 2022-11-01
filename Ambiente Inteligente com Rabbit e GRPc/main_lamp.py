
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

#----------------RabbitMQ setup
connection, channel = lamp.connect_rabbit()

lamp.set_queue(channel, lamp.queue) #queue do objeto ac
lamp.set_queue(channel, queue_principal) #se liga com a queue principal
lamp.set_queue(channel, end_queue)
lamp.send_queue(channel, f"{lamp.queue} {lamp_port}", queue_principal) #envia a queue do objeto lamp pro home assistent conectar com sua fila (queue recepção)
lamp.send_luminosity_updates(channel)

#----------------GRPC Setup

#lamp.start_grpc_server(lamp) -- não funciona se for encapsulado dessa forma(motivos misteriosos)
lamp_grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
object_pb2_grpc.add_ObjectServicer_to_server(ObjectServicer(lamp), lamp_grpc_server)
lamp_grpc_server.add_insecure_port(f"localhost:{lamp_port}")
lamp_grpc_server.start()
#-----------------------Procurar como refatorar isso depois

input('Pressione ENTER para sair\n')
lamp.close(connection, channel, end_queue)