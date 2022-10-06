import socket
import threading
from multicast.receive_group import receive_multicast

class Cliente:
    #Padronizacao do formato das mensagens
    FORMAT = "utf-8"
    
    #Pegar o endereco do gateway via multicast
    def obj_gtw_multicast(self):
        addr = receive_multicast().decode(Cliente.FORMAT)

        # Tratando da mensagem recebida do multicast
        addr = addr.split()
        addr[1] = int(addr[1])
        addr = tuple(addr)

        return addr

    #Envio de mensagens
    def write(self, cliente, mensagem):
        cliente.send(mensagem.encode(Cliente.FORMAT))

    #Receber mensagens do gateway
    def receive(self, cliente):
        while True:
            try:
                mensagem = cliente.recv(1024).decode(Cliente.FORMAT)
                print(mensagem)
            except:
                print("Ocorreu um erro!")
                cliente.close()
                break

    #Abrir conexao via TCP do objeto com o gateway
    def obj_gtw_tcp(self, addr):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(addr)
        client_socket.connect(addr)
        print("Conectado ao gateway!")

        #Abrir thread para receber mensagens do gateway
        receive_thread = threading.Thread(target = self.receive, args=(client_socket,))
        receive_thread.start()

        return client_socket