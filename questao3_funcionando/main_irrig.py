from objetos.irrig import Sprinkler

molhadinho = Sprinkler(False)
addr = molhadinho.get_addr_by_mult()

socket = molhadinho.connect_tcp(addr)
msg = f'{molhadinho.type}'

molhadinho.write(socket, msg)
molhadinho.receive(socket)