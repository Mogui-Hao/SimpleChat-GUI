
import socket
from json import loads, dumps
from .api.terminal import Terminal
from .api.terminal import MessageType
from traceback import format_exception_only, format_exc

class ClientTCP(socket.socket):
    def __init__(self, Address: tuple[str, int], name: str, terminal, password: str = "", language: list | None= None):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        # self.error = False
        self.terminal = Terminal(terminal)
        self.connect(Address)
        self.password = password
        self.name = name
        self.send(dumps({
            "name": name,
            "password": password
        }).encode("utf-8"))
        date = self.recv(pow(2, 25)).decode("utf-8")
        for info in loads(date):
            self.terminal.log(f'{info["sender"]}: {info["message"]}')
        # self.terminal.log(language[0], Type=MessageType.Error)
        # self.error = True

    def GetMessage(self):
        try:
            while ...:
                date = self.recv(pow(2, 25))
                print(date)
                date = loads(date.decode("utf-8"))
                if (self.Qualified(date)):
                    self.terminal.log(f'{date["sender"]}: {date["message"]}', MessageType.Info if date["sender"] != self.name else MessageType.Me)
        except Exception as e:
            self.terminal.log(f"Traceback (most recent call last):\n{format_exc()}{format_exception_only(type(e), e)[0]}", MessageType.Error)
    
    def SendMessage(self, message):
        try:
            date = dumps({
                "type": "message",
                "sender": self.name,
                "message": message
            }).encode("utf-8")
            self.send(date)
        except Exception as e:
            self.terminal.log(f"Traceback (most recent call last):\n{format_exc()}{format_exception_only(type(e), e)[0]}", MessageType.Error)
    
    def Qualified(self, message: dict):
        if ("message" in message and "sender" in message):
            return True
        return False

# 14284
