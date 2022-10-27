# ---------------------------- lógica RabbitMQ
from objects.queue_logic import send_rabbit as sr
import time

class PublisherQueueObjects():
    # conecções rabbit
    def connect_rabbit(self):
        connection, channel = sr.create_connection()
        return connection, channel
    
    # setando fila do rabbit
    def set_queue(self, channel, name_queue):
        sr.create_queue(channel, name_queue)

    # enviando periódicamente um atributo
    def send_attribute_updates(self, channel, name_queue, attribute):
        while 1:
            time.sleep(5)
            msg = f"{name_queue} {self.state} {attribute} {getattr(self, attribute)}\n"
            sr.send_info(channel, msg, name_queue)

    # enviando o nome da propria fila para a fila de conexão
    def send_queue(self, channel, name_queue, queue_principal):
        sr.send_info(channel, name_queue, queue_principal)
    
    # feichando a coneção
    def close(self, connection, channel, close_queue):
        sr.send_info(channel, self.queue, close_queue)
        sr.close_connection(connection)