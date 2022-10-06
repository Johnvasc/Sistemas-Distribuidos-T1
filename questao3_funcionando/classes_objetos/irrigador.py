
from cliente import Cliente

class Irrigador(Cliente):

    #Atributos do irrigador
    def __init__(self, estado):
        self.estado = False
        self.tipo = 'irrig'

    def receive(self, client):
        while True:
            try:
                #Recebe requisicao
                mensagem = client.recv(1024).decode(Cliente.FORMAT)
                print(f"Comando: {mensagem}")

                #Dependendo do comando, caiu em alguma condicao
                if mensagem.split()[0] == "estado_objeto":
                    msg = f"Irrig {self.estado}"
                    self.write(client, msg)
                elif mensagem.split()[0] == "mudar_estado":
                    if mensagem.split()[1] == "true":
                        self.estado = True
                    elif mensagem.split()[1] == "false":
                        self.estado = False
                    else:
                        pass
                    print(f"Novo estado: {self.estado}")
                else:
                    pass
            except:
                print("Ocorreu um erro!")
                client.close()
                break