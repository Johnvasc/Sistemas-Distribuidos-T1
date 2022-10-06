
from classes_objetos.lampada import Lampada

lampada_objeto = Lampada(False)                     #Declaracao do objeto e seu(s) parametro(s)
ADDR = lampada_objeto.obj_gtw_multicast()           #Recebe o endereco do gateway
lampada_socket = lampada_objeto.obj_gtw_tcp(ADDR)   #Conexao via TVP com o gateway

mensagem = f'{lampada_objeto.tipo}'                 #Tipo do objeto

lampada_objeto.write(lampada_socket, mensagem)      #Envia ao gateway seu tipo