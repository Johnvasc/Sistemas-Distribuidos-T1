
#Arquivo voltado para comunicacao via RabbitMQ (filas)

from objects.queue_logic import enviar_pra_rabbit as sr
import time

class PublisherQueueObjects():
    #Cria conexao via RabbitMQ
    def connect_rabbit(self):
        connection, channel = sr.create_connection()
        return connection, channel
    
    #Criacao da fila no RabbitMQ
    def set_queue(self, channel, nome_queue):
        sr.create_queue(channel, nome_queue)

    #Envio constante do atributo do objeto em questao
    def send_attribute_updates(self, channel, nome_queue, attribute):
        while True:
            time.sleep(5)
            #Conteudo da mensagem a ser enviada para a fila
            mensagem = f"{nome_queue} {self.state} {attribute} {getattr(self, attribute)}\n"
            sr.send_info(channel, mensagem, nome_queue)

    #Envio do nome da propria fila para outra fila (criar conexao)
    def send_queue(self, channel, nome_queue, queue_principal):
        sr.send_info(channel, nome_queue, queue_principal)
    
    #Fechamento de conexao
    def close(self, connection, channel, close_queue):
        sr.send_info(channel, self.queue, close_queue)
        sr.close_connection(connection)