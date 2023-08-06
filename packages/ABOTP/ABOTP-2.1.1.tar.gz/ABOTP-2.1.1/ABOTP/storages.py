class Flags:
    def __init__(self):
        self.flags = []
        self.TCP_clients = []
        self.UDP_clients = []

    def append(self, TCP, UDP, flags) -> None:
        self.TCP_clients.append(TCP)
        self.UDP_clients.append(UDP)
        self.flags.append(flags)

    def set_flags(self, search: dict, flags: dict) -> bool:
        key, value = list(search.items())[0]
        index = None
        for _index, _flags in enumerate(self.flags):
            if key in _flags.keys() and _flags.get(key, None) == value:
                index = _index
                break
        if index is None:
            return False
        self.flags[index] |= flags
        return True

    def remove(self, search: dict) -> bool:
        key, value = list(search.items())[0]
        index = None
        for _index, flags in enumerate(self.flags):
            if key in flags.keys() and flags.get(key, None) == value:
                index = _index
                break
        if index is None:
            return False
        self.TCP_clients.pop(index).close()
        self.UDP_clients.pop(index).close()
        self.flags.pop(index)
        return True

    def sockets(self, protocol: int):
        match int(protocol):
            case 0:
                for client in self.TCP_clients:
                    yield client
            case 1:
                for client in self.UDP_clients:
                    yield client

    def get_socket(self, flag: dict, protocol: int):
        key, value = list(flag.items())[0]
        index = None
        for i, flags in enumerate(self.flags):
            if key in flags.keys() and flags.get(key) == value:
                index = i
                break
        if index is None:
            return False
        match int(protocol):
            case 0:
                return self.TCP_clients[index]
            case 1:
                return self.UDP_clients[index]
