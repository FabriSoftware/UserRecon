import collections
import struct
import socket
from colorama import Fore

class IncompletePacket(Exception):
    def __init__(self, minimum):
        self.minimum = minimum


Packet = collections.namedtuple("Packet", ("ident", "kind", "payload"))

def connection(host, port, password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5000)
    try:
     sock.connect((host, port))
     result = login(sock, password)

     # return false if password is incorrect
     if not result:
        sock.close()
        return False
     else:
        return sock

    except socket.error as msg:
       print("["+Fore.RED+"X"+Fore.RESET+"] connection error: ", msg)
       exit(1)
    


def decode_packet(data):
    if len(data) < 14:
        raise IncompletePacket(14)

    length = struct.unpack("<i", data[:4])[0] + 4
    if len(data) < length:
        raise IncompletePacket(length)

    ident, kind = struct.unpack("<ii", data[4:12])
    payload, padding = data[12:length-2], data[length-2:length]
    assert padding == b"\x00\x00"
    return Packet(ident, kind, payload), data[length:]


def encode_packet(packet):
    data = struct.pack("<ii", packet.ident, packet.kind) + packet.payload + b"\x00\x00"
    return struct.pack("<i", len(data)) + data


def receive_packet(sock):
    data = b""

    while True:
      try:
            return decode_packet(data)[0]
      except IncompletePacket as exc:
            while len(data) < exc.minimum:
                data += sock.recv(exc.minimum - len(data))

def send_packet(sock, packet):
    sock.sendall(encode_packet(packet))


def login(sock, password):
    send_packet(sock, Packet(0, 3, password.encode("utf8")))
    packet = receive_packet(sock)
    return packet.ident == 0
 

def send_command(sock, text):
    send_packet(sock, Packet(0, 2, text.encode("utf8")))
    send_packet(sock, Packet(1, 0, b""))
    response = b""
    while True:
        packet = receive_packet(sock)
        if packet.ident != 0:
            break
        response += packet.payload
        return response.decode("utf8")