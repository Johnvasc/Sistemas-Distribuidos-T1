from objects.queue_logic import receive_rabbit as rr
import threading

FORMAT = 'utf-8'

class HomeAssistantRabbit():
  #Funcao de conexao via RabbitMQ
  def connect_rabbit(self):
    connection, channel = rr.connect()
    return connection, channel
    
  def start_principal_queue(self):
    def callback_new_queue(ch, method, properties, body):
      def callback_queue(ch, method, properties, body): 
          #QUANDO CHEGAR NOS OBJETOS, VOLTAR AQUI
          msg = body.decode(FORMAT)
          items = msg.split()
          self.objects_data[items[0]] = msg

      #POSSO COLOCAR ALGO AQUI DEPOIS
      msg = body.decode(FORMAT)
      new_queue = msg.split()[0]

      #Criando comunicacao via gRPC
      self.create_new_remote_object(msg)
      
      #Thread de consumo da nova fila criada (fila de comunicacao do objeto novo)
      queue_thread = threading.Thread(target = rr.consume_queue, args = (new_queue, callback_queue), daemon = True)
      queue_thread.start()

    #Thread de consumo da fila principal (home)
    consume_queue_thread = threading.Thread(target = rr.consume_queue, args = (self.queue_principal, callback_new_queue), daemon = True)
    consume_queue_thread.start()

  def start_end_queue(self):
    def callback_end_queue(ch, method, properties, body):
      #DEPOIS VOLTAR AQUI
      object_selected = body.decode(FORMAT)
      self.objects.pop(object_selected, None)
      self.objects_data.pop(object_selected, None)
      print(f"Objeto desconectado.. {object_selected}")

    #Thread de consumo da fila de fim de objetos (close)
    consume_queue_thread = threading.Thread(target = rr.consume_queue, args = (self.end_queue, callback_end_queue), daemon = True)
    consume_queue_thread.start()