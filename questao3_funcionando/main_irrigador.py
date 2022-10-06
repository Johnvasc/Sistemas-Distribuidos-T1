
from classes_objetos.irrigador import Irrigador

irrigador_objeto = Irrigador(False)                     #Declaracao do objeto e seu(s) parametro(s)
ADDR = irrigador_objeto.obj_gtw_multicast()             #Recebe o endereco do gateway
irrigador_socket = irrigador_objeto.obj_gtw_tcp(ADDR)   #Conexao via TCP com o gateway

mensagem = f'{irrigador_objeto.tipo}'                   #Tipo do objeto

irrigador_objeto.write(irrigador_socket, mensagem)      #Envia ao gateway seu tipo