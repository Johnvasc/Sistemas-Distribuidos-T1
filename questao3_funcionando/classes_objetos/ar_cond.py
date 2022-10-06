import socket
import threading
import time
from cliente import Cliente

class Ar_cond(Cliente):

    #Atributos do ar-condicionado
    def __init__(self, estado, temp):
        self.estado = False
        self.temp = 18
        self.tipo = 'AC'

    #Funcao separada para se conectar ao gateway via TCP
    def AC_gtw_conexaoTCP(self, addr):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(addr)
        client_socket.connect(addr)
        print("Conectado ao gateway!")

        #Thread para receber mensagens
        receive_thread = threading.Thread(target = self.receive, args=(client_socket,))
        receive_thread.start()

        #Thread para ficar atualizando a temperatura
        update_thread = threading.Thread(target=self.atualizao_temp, args=(client_socket,))
        update_thread.start()

        return client_socket
    
    #Receber requisicoes do gateway
    def receive(self, client):
        while True:
            try:
                #Recebe requisicao
                mensagem = client.recv(1024).decode(Cliente.FORMAT)
                print(f"Comando: {mensagem}")

                #Dependendo do comando, caiu em alguma condicao
                if mensagem.split()[0] == "mudar_estado":
                    if mensagem.split()[1] == "true":
                        self.estado = True
                    elif mensagem.split()[1] == "false":
                        self.estado = False
                    else:
                        pass
                    print(f"Novo estado: {self.estado}")
                elif mensagem.split()[0] == "mudar_temp":
                    self.temp = int(mensagem.split()[1])
                    print(f"Nova temperatura: {self.temp}")
                else:
                    pass
            except:
                print("Ocorreu um erro!")
                client.close()
                break

    
    def atualizao_temp(self, client):
        while True:
            #Pensado como tradeoff para quando a aplicacao mudar a temp
            #e ja querer saber a temp atual
            time.sleep(5)
            msg = f"AC {self.temp} {self.estado}"
            self.write(client, msg)
