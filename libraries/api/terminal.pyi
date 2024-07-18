
import ttkbootstrap as ttk

class MessageType:
    Error: str
    Accepted: str
    Abnormal: str
    Info: str
    Me: str

class Terminal:
    def __init__(self, Text: ttk.Text) -> None: ...
    def log(self, message: str = "", Type: MessageType = MessageType.Accepted, end: str = "\n") -> bool: ...
    
# 2024-7-17-20-29:559