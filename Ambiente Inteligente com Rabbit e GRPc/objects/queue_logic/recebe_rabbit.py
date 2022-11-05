# Esse arquivo realiza a logica para o recebimento de informações em filas
import pika

#Cria conexao RabbitMQ
def connect():
    conexao = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = conexao.channel()
    return conexao, channel

#Funcao de consumo de mensagens nas filas (qualquer fila)
def consume_queue(nome_queue, callback):
    conexao, channel = connect()
    channel.queue_declare(queue = nome_queue) 
    channel.basic_consume(queue = nome_queue, on_message_callback = callback, auto_ack = True)
    print(f' [*] Esperando {nome_queue} por mensagens.')
    channel.start_consuming()
