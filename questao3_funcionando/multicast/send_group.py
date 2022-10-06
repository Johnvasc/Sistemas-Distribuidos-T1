
import socket
import struct

FORMAT = "utf-8"

def send_multicast(mensagem):
    #Endereco do grupo
    grupo_multicast = ('224.1.1.1', 24865)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)

    #Tempo de vida da mensagem
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    #Tenta enviar a mensagem pelo multicast
    try:
        print(f'Enviando pelo multicast: {mensagem}\n')
        mensagem = mensagem.encode(FORMAT)
        sock.sendto(mensagem, grupo_multicast)

    #Independente de ter enviado ou nao, eh fechada a conexao
    finally:
        print('Comunicacao multicast fechada!\n')
        sock.close()