
import socket
import struct

def receive_multicast():
    #Setando IP e porta para comunicacao multicast
    grupo_multicast_ip = '224.1.1.1'
    addr_servidor = ('', 24865)     #Tem que ser assim

    #Comunicacao sera feita via UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Solicita ao S.O. para adicionar o socket ao grupo multicast em todas as interfaces
    grupo = socket.inet_aton(grupo_multicast_ip)
    mult_req = struct.pack('4sL', grupo, socket.INADDR_ANY)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mult_req)

    #Bind na porta
    sock.bind(addr_servidor)

    #Fica esperando o gateway aparecer para participar do grupo multicast
    while True:
        print('\nEsperando resposta via multicast...\n')
        data, addr = sock.recvfrom(1024)    #Recebe o endereco do gateway
        
        print('Recebido %s bytes de %s\n' % (len(data), addr))

        if data != None:
            return data