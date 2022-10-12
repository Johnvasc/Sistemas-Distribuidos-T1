
import socket
import struct
import time

FORMAT = "utf-8"

def send_multicast(mensagem):
    #Endereco do grupo
    grupo_multicast = ('224.1.1.1', 24865)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)

    #Tempo de vida da mensagem
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        #Tenta enviar a mensagem pelo multicast
        print(f'Enviando pelo multicast: {mensagem}\n')
        time.sleep(10)
        mensagem = mensagem.encode(FORMAT)
        sock.sendto(mensagem, grupo_multicast)
    except:
        print('Comunicacao multicast fechada!\n')
        sock.close()

    #Independente de ter enviado ou nao, eh fechada a conexao
    #finally:
    #    print('Comunicacao multicast fechada!\n')
    #    sock.close()