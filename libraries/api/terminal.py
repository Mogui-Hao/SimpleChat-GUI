
import ttkbootstrap as ttk

class MessageType:
    Error = "error"
    Accepted = "accepted"
    Abnormal = "abnormal"
    Info = "info"
    Me = "me"

class Terminal:
    def __init__(self, Text):
        self.Text = Text
    def log(self, message = "", Type = MessageType.Accepted, end = "\n"):
        self.Text.config(state=ttk.NORMAL)
        self.Text.insert(ttk.END, message+end, Type)
        self.Text.config(state=ttk.DISABLED)