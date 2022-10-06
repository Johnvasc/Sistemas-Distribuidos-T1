
from classes_objetos.ar_cond import Ar_cond

ar_cond_objeto = Ar_cond(False, 18)                         #Declaracao do objeto e seu(s) parametro(s)
ADDR = ar_cond_objeto.obj_gtw_multicast()                   #Recebe o endereco do gateway
ar_cond_socket = ar_cond_objeto.AC_gtw_conexaoTCP(ADDR)     #Conexao via TCP com o gateway

mensagem = f'{ar_cond_objeto.tipo}'                         #Tipo do objeto

ar_cond_objeto.write(ar_cond_socket, mensagem)              #Envia ao gateway seu tipo