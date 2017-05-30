import socket, socks


def proxify(address: str, port: int):
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, address, port)
    socket.socket = socksocket
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo

class socksocket(socks.socksocket):
    def __init__(self, family: socket.AddressFamily = socket.AddressFamily.AF_INET, type: socket.SocketKind = socket.SocketKind.SOCK_STREAM, proto: int = 0,
                 address: str = "127.0.0.1", port: int = 9150, *args, **kwargs):
        super(socksocket, self).__init__(family, type, proto, *args, **kwargs)
        self.set_proxy(socks.PROXY_TYPE_SOCKS5, address, port)
        self.proxy_address = address
        self.proxy_port = port
    
    def getaddrinfo(self, *args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (args[0], args[1]))]
