from objetos.lamp import Lamp

luzinha = Lamp(False)
addr = luzinha.get_addr_by_mult()
socket = luzinha.connect_tcp(addr)

msg = f'{luzinha.type}'
luzinha.write(socket, msg)