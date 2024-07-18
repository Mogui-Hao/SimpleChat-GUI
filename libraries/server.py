
import socket
from json import loads, dumps
from .api.terminal import Terminal, MessageType
from threading import Thread
from traceback import format_exception_only, format_exc

class ServerTCP(socket.socket):
    def __init__(self, Address: tuple[str, int], Language: dict, terminal, listen: int = 0, byte: bytes = 0, password: str = ""):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.password = password
        self.terminal = Terminal(terminal)
        self.Language = Language
        self.terminal.log(self.Language[0])
        self.terminal.log(self.Language[1])
        self.Clients = {}
        self.ops = {}
        self.News = []
        self.bind(Address)
        self.terminal.log(self.Language[2] % Address)
        self.listen(listen)
        self.terminal.log(self.Language[3])
    
    def GetUser(self):
        try:
            while ...:
                Client, Addr = self.accept()
                self.terminal.log(self.Language[4] % Addr)
                Thread(target=self.GetMessage, args=(Client,)).start()
        except Exception as e:
            self.terminal.log(f"Traceback (most recent call last):\n{format_exc().split()}{format_exception_only(type(e), e)[0].strip()}", MessageType.Error)

    def GetMessage(self, Client: socket.socket):
        try:
            date = loads(Client.recv(pow(2, 25)).decode("utf-8"))
            if date["name"] in list(self.Clients.keys()) or date["password"] != self.password:
                raise Exception
            self.Clients[date["name"]] = Client
            Client.send(dumps(self.News).encode("utf-8"))
            while ...:
                Message = loads(Client.recv(pow(2, 25)).decode("utf-8"))
                if (not self.Qualified(Message)):
                    continue
                if Message["type"] == "message":
                    SendNews = dumps({
                            "message": Message["message"],
                            "sender": Message["sender"]
                        })
                    self.News.append(loads(SendNews))
                    self.terminal.log(f'{Message["sender"]}: {Message["message"]}', MessageType="Info")
                    for client in list(self.Clients.values()):
                        client.send(SendNews.encode("utf-8"))
        except Exception as e:
            del self.Clients[date["name"]]
            Client.close()
    
    def Qualified(self, message: dict):
        if ("type" in message):
            if (message["type"] == "message"):
                if ("message" in message and "sender" in message):
                    return True
            elif (message["type"] == "command"):
                if ("command" in message and "sender" in message and message["sender"] in list(self.ops.keys())):
                    return True
        return False
        