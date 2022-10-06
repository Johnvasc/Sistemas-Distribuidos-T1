from objetos.ac import Ac

geladinho = Ac(False, 18)
addr = geladinho.get_addr_by_mult()

socket = geladinho.connect_tcp(addr)
msg = f'{geladinho.type}'

geladinho.write(socket, msg)
geladinho.receive(socket)