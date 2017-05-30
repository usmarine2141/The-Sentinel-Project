from ctypes import Structure, c_ubyte, c_ushort, c_ulong


map = {1: "ICMP", 6: "TCP", 17: "UDP"}

class IP(Structure):
    _fields_ = [("ihl", c_ubyte, 4),
                ("version", c_ubyte, 4),
                ("tos", c_ubyte),
                ("length", c_ushort),
                ("id", c_ushort),
                ("offset", c_ushort),
                ("ttl", c_ubyte),
                ("protocol_id", c_ubyte),
                ("sum", c_ushort),
                ("source_address", c_ulong),
                ("dest_address", c_ulong)]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)    
    
    def __init__(self, socket_buffer=None):
        self.source_address = socket.inet_ntoa(struct.pack("<L", self.source_address))
        self.dest_address = socket.inet_ntoa(struct.pack("<L", self.dest_address))
        self.protocol = self.protocol_map[map] if self.protocol_id in map else self.protocol_id

class ICMP(Structure):
    _fields_ = [("type",         c_ubyte),
                ("code",         c_ubyte),
                ("checksum",     c_ushort),
                ("unused",       c_ushort),
                ("next_hop_mtu", c_ushort)]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)    
    
    def __init__(self, socket_buffer):
        pass
