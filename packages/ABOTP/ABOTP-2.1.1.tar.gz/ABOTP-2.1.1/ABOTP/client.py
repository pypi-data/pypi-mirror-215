import socket
import struct
import support


class Client:
    def __init__(self, IP: str, TCP_port: int, UDP_port: int):
        self.address = {
            'TCP': (IP, TCP_port),
            'UDP': (IP, UDP_port)
        }
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status = False

    def connect(self) -> None:
        if not self.status:
            self.TCP.connect((self.address['TCP']))
            self.status = True
        else:
            raise support.ConnectionStatusError('Attempt to connect an already connected socket')

    def recv(self, protocol: int) -> list[bytes, ...] | None:
        if self.status:
            match int(protocol):
                case 0:
                    def picking(n):
                        data = b''
                        while len(data) < n:
                            try:
                                packet, _ = self.TCP.recv(n - len(data))
                            except socket.error as e:
                                raise socket.error(f"Error receiving data: {e}")
                            if not packet:
                                return None
                            data += packet
                        return data

                    num_objects_data = picking(4)
                    if num_objects_data is None:
                        return None

                    num_objects = struct.unpack('>I', num_objects_data)[0]
                    objects = []
                    for _ in range(num_objects):
                        len_data = picking(4)
                        if len_data is None:
                            return None

                        len_data_value = struct.unpack('>I', len_data)[0]
                        obj_data = picking(len_data_value)
                        if obj_data is None:
                            return None

                        objects.append(obj_data)
                    return objects
                case 1:
                    def picking(n):
                        data = b''
                        while len(data) < n:
                            try:
                                packet, _ = self.UDP.recvfrom(n - len(data))
                            except socket.error as e:
                                print(f"Error receiving data: {e}")
                                return None
                            if not packet:
                                return None
                            data += packet
                        return data

                    num_objects_data = picking(4)
                    if num_objects_data is None:
                        return None

                    num_objects = struct.unpack('>I', num_objects_data)[0]
                    objects = []
                    for _ in range(num_objects):
                        len_data = picking(4)
                        if len_data is None:
                            return None

                        len_data_value = struct.unpack('>I', len_data)[0]
                        obj_data = picking(len_data_value)
                        if obj_data is None:
                            return None

                        objects.append(obj_data)
                    return objects
        else:
            raise support.ConnectionStatusError('Attempt to recv data via an unconnected socket')

    def send(self, protocol: int, data: list[bytes, ...]) -> None:
        if self.status:
            match int(protocol):
                case 0:
                    num_objects = len(data)
                    len_objects = [len(obj) for obj in data]
                    packet = struct.pack('>I', num_objects)
                    for len_obj, obj in zip(len_objects, data):
                        packet += struct.pack('>I', len_obj) + obj
                    self.TCP.sendall(packet)
                case 1:
                    num_objects = len(data)
                    len_objects = [len(obj) for obj in data]
                    packet = struct.pack('>I', num_objects)
                    for len_obj, obj in zip(len_objects, data):
                        packet += struct.pack('>I', len_obj) + obj
                    self.UDP.sendto(packet, self.address['UDP'])
        else:
            raise support.ConnectionStatusError('Attempt to send data via an unconnected socket')