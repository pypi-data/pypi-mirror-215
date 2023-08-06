class By:
    TCP = 0
    UDP = 1


class ConnectionStatusError(Exception):
    def __init__(self, *message):
        super().__init__(*message)
