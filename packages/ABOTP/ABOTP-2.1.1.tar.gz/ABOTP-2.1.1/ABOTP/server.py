import socket
import struct
import support


class Server:

    class Client:
        def __init__(self, sock, addr):
            self.socket = sock
            self.addr = addr

        def recv(self) -> list[bytes, ...] | None:
            def picking(n):
                data = b''
                while len(data) < n:
                    try:
                        packet, _ = self.socket.recv(n - len(data))
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

        def send(self, data: list[bytes, ...]) -> None:
            num_objects = len(data)
            len_objects = [len(obj) for obj in data]
            packet = struct.pack('>I', num_objects)
            for len_obj, obj in zip(len_objects, data):
                packet += struct.pack('>I', len_obj) + obj
            self.socket.sendall(packet)

        def close(self) -> None:
            self.socket.close()

        def __del__(self):
            self.close()

    def __init__(self, IP: str, TCP_port: int, UDP_port: int):
        self.address = {
            'TCP': (IP, TCP_port),
            'UDP': (IP, UDP_port)
        }
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status = False

    def start(self) -> None:
        if not self.status:
            self.UDP.bind(self.address['UDP'])
            self.TCP.bind(self.address['TCP'])
            self.TCP.listen()
            self.status = True
        else:
            raise support.ConnectionStatusError('Attempt to start an already working socket')

    def recv(self) -> list[bytes, ...]:
        if self.status:
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
            raise support.ConnectionStatusError('Attempt to read data via UDP on an inactive socket')

    def accept(self) -> Client:
        if self.status:
            sock, addr = self.TCP.accept()
            return self.Client(sock, addr)
        else:
            raise support.ConnectionStatusError('Attempt to capture a client via TCP in an inactive socket')

    def __del__(self):
        self.TCP.close()
        self.UDP.close()