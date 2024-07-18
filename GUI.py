
from os import makedirs
from os.path import exists
from json import dumps, loads
from threading import Thread
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests

if not (exists("libraries")): [makedirs(f'libraries/{f}', exist_ok=True) for f in ['api', 'language']]
makedirs("libraries/api") if not (exists("libraries/api")) else ...
makedirs("libraries/language") if not (exists("libraries/language")) else ...
def Dependency(File):
    if not (exists(File)):
        try:
            with open(File, "w", encoding="utf-8") as f:f.write(requests.get(f"https://raw.githubusercontent.com/Mogui-Hao/SimpleChat-GUI/main/{File}").text)
        except:
            with open(File, "w", encoding="utf-8") as f:f.write(requests.get(f"https://gitee.com/moguihao/simple-chat-gui/raw/master/{File}").text)

for f in ["config.py", "libraries/api/terminal.py", "libraries/api/terminal.pyi", "libraries/language/zh-cn.json", "libraries/client.py", "libraries/server.py"]:
    Dependency(f)
import config
from libraries.api.terminal import Terminal
from libraries.server import ServerTCP
from libraries.client import ClientTCP

if (exists(config.ConfigPath)):
    with open(config.ConfigPath, "r", encoding="utf-8") as f:
        Config = loads(f.read())
else:
    with open(config.ConfigPath, "w", encoding="utf-8") as f:
        Config = config.DefaultConfigContent
        f.write(dumps(Config, indent=4))

ServerConfig = Config["server"]
ClientConfig = Config["client"]
SetUpConfig = Config["setup"]

class Windows(ttk.Window):
    def __init__(self,
                 title=config.Title,
                 themename="darkly",
                 iconphoto='',
                 size=config.Size,
                 position=config.Position,
                 minsize=None,
                 maxsize=None,
                 resizable=None,
                 hdpi=True,
                 scaling=None,
                 transient=None,
                 overrideredirect=False,
                 alpha=1):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha)
        self.TCP = None
        self.Language = self.UpdateLanguage(config.LanguageFileToNameDict[SetUpConfig["language"]])
        self.MainNotebook = self.MainNoteBooks()
        self.ServerButton = self.Button(self.ServerFrame, self.Language["server"][3], self.StartServer)
        self.ServerHostLabel = self.Host_Label(self.ServerFrame, self.Language["server"][0])
        self.ServerHostEntry = self.Host_Entry(self.ServerFrame, ServerConfig)
        self.ServerPortLabel = self.Port_Label(self.ServerFrame, self.Language["server"][1])
        self.ServerPortEntry = self.Port_Entry(self.ServerFrame, ServerConfig)
        self.ServerPasswordLabel = self.Password_Label(self.ServerFrame, self.Language["server"][2])
        self.ServerPasswordEntry = self.Password_Entry(self.ServerFrame, ServerConfig)
        self.TerminalOutputText = self.TerminalOutput_Text()
        self.TerminalPatternCombobox = self.TerminalPattern_Combobox()
        self.TerminalCommandEntry = self.TerminalCommand_Entry()
        self.ClientButton = self.Button(self.ClientFrame, self.Language["client"][4], self.StartClient)
        self.ClientHostLabel = self.Host_Label(self.ClientFrame, self.Language["client"][0])
        self.ClientHostEntry = self.Host_Entry(self.ClientFrame, ClientConfig)
        self.ClientPortLabel = self.Port_Label(self.ClientFrame, self.Language["client"][1])
        self.ClientPortEntry = self.Port_Entry(self.ClientFrame, ClientConfig)
        self.ClientPasswordLabel = self.Password_Label(self.ClientFrame, self.Language["client"][2])
        self.ClientPasswordEntry = self.Password_Entry(self.ClientFrame, ClientConfig)
        self.ClientNameLabel = self.Name_Label(self.ClientFrame, self.Language["client"][3])
        self.ClientNameEntry = self.Name_Entry(self.ClientFrame, ClientConfig)
        # self.AboutAuthorLabel = self.AboutAuthor_Label()
        self.LanguageLabel = self.Language_Label(self.SetUpFrame, self.Language["setup"][0])
        self.LanguageCombobox = self.Language_Combobox(self.SetUpFrame, self.Language["setup"][0])
        self.SaveButton = self.SaveButton(self.SetUpFrame, self.Language["setup"][1])
        self.terminal = Terminal(self.TerminalOutputText)
        self.TerminalSendButton = self.TerminalSend_Button()
        # self.terminal.log("green")
        # self.terminal.log("red", Type=MessageType.Error)
        # self.terminal.log("yellow", Type=MessageType.Abnormal)
        self.mainloop()

    def StartServer(self):
        self.Save()
        if not self.TCP is None:
            self.ClientButton.config(state=NORMAL)
            self.ServerButton.config(text=self.Language["server"][3], state=NORMAL)
            self.TerminalSendButton.config(state=DISABLED)
            self.TCP.close()
            return
        self.TerminalOutputText.config(state=NORMAL)
        self.TerminalOutputText.delete("1.0", END)
        self.TerminalOutputText.config(state=DISABLED)
        self.ServerButton.config(text=self.Language["server"][4], state=DISABLED)
        self.ClientButton.config(state=DISABLED)
        self.TCP = ServerTCP((self.ServerHostEntry.get(), int(self.ServerPortEntry.get())), self.Language["terminal"]["server"], self.TerminalOutputText, password=self.ServerPasswordEntry.get())
        GetUser = Thread(target=self.TCP.GetUser, args=())
        GetUser.daemon = True
        GetUser.start()
        self.ServerButton.config(text=self.Language["server"][5], state=NORMAL)
        self.TerminalSendButton.config(state=NORMAL)

    def StartClient(self):
        self.Save()
        if not self.TCP is None:
            self.ServerButton.config(state=NORMAL)
            self.ClientButton.config(text=self.Language["client"][5], state=NORMAL)
            self.TerminalSendButton.config(state=DISABLED)
            self.TCP.close()
            return
        self.TerminalOutputText.config(state=NORMAL)
        self.TerminalOutputText.delete('1.0', END)
        self.TerminalOutputText.config(state=DISABLED)
        self.ClientButton.config(text=self.Language["client"][5], state=DISABLED)
        self.ServerButton.config(state=DISABLED)
        self.TCP = ClientTCP((self.ClientHostEntry.get(), int(self.ClientPortEntry.get())), self.ClientNameEntry.get(), self.TerminalOutputText, self.ClientPasswordEntry.get(), self.Language["terminal"]["client"])
        GetMessage = Thread(target=self.TCP.GetMessage, args=())
        GetMessage.daemon = True
        GetMessage.start()
        self.ClientButton.config(text=self.Language["client"][6])
        self.TerminalSendButton.config(state=NORMAL)


    def UpdateLanguage(self, language):
        Language = config.LanguageDict[language]
        return Language["date"]

    def Save(self):
        with open(config.ConfigPath, "w", encoding="utf-8") as f:
            f.write(dumps({
                "server": {
                    "host": self.ServerHostEntry.get(),
                    "port": int(self.ServerPortEntry.get()),
                    "password": self.ServerPasswordEntry.get()
                },
                "client": {
                    "host": self.ClientHostEntry.get(),
                    "port": int(self.ServerPortEntry.get()),
                    "name": self.ClientNameEntry.get(),
                    "password": self.ClientPasswordEntry.get()
                },
                "setup": {
                    "language": config.LanguageNameToFileDict[self.LanguageCombobox.get()]
                }
            }, indent=4))

    def SaveButton(self, master, text):
        SaveButton = ttk.Button(master, text=text, bootstyle=(SUCCESS, OUTLINE), command=self.Save)
        SaveButton.place(x=600, y=22, width=100)
        return SaveButton

    def Terminal(self, master):
        self.TerminalFrame = ttk.Frame(master)
        return self.TerminalFrame

    def About(self, master):
        self.AboutFrame = ttk.Frame(master)
        return self.AboutFrame

    def AboutAuthor_Label(self):
        AboutLabelAuthor = ttk.Label(self.AboutFrame, text="作者: MoGui_Hao")
        AboutLabelAuthor.place(x=30, y=30)
        return AboutLabelAuthor

    def TerminalOutput_Text(self):
        TerminalTextOutput = ttk.Text(self.TerminalFrame)
        TerminalTextOutput.place(height=300, width=720)
        TerminalTextOutput.tag_configure("error", foreground="#FF0000")
        TerminalTextOutput.tag_configure("accepted", foreground="#00FF8C")
        TerminalTextOutput.tag_configure("abnormal", foreground="#FFEA00")
        TerminalTextOutput.tag_configure("info", foreground="#ADB5BD")
        TerminalTextOutput.tag_configure("me", foreground="#4582EC")
        TerminalTextOutput.config(state=DISABLED)
        return TerminalTextOutput

    def TerminalPattern_Combobox(self):
        TerminalComboboxPattern = ttk.Combobox(self.TerminalFrame, 
                                               values=self.Language["terminal"]["infoType"])
        TerminalComboboxPattern.current(0)
        TerminalComboboxPattern.place(x=0, y=295, width=100)
        return TerminalComboboxPattern
    
    def TerminalCommand_Entry(self):
        TerminalEntryCommand = ttk.Entry(self.TerminalFrame)
        TerminalEntryCommand.place(x=80, y=295, width=580)
        return TerminalEntryCommand

    def TerminalSend_Button(self):
        TerminalButtonSend = ttk.Button(self.TerminalFrame, 
                                            text=self.Language["terminal"]["infoType"][2], 
                                            bootstyle=(SUCCESS, OUTLINE), 
                                            command=self.TerminalSendMessageButtonFunction, 
                                            state=DISABLED
                                        )
        TerminalButtonSend.place(x=650, y=295, width=65)
        return TerminalButtonSend

    def TerminalSendMessageButtonFunction(self):
        if type(self.TCP) == ClientTCP:
        # self.terminal.log(self.TerminalCommandEntry.get(), MessageType.Info)
            self.TCP.SendMessage(self.TerminalCommandEntry.get())
            self.TerminalCommandEntry.delete(0, END)

    def Server(self, master):
        self.ServerFrame = ttk.Frame(master)
        return self.ServerFrame

    def Button(self, master, text, command):
        Button = ttk.Button(master, 
                                 text=text,
                                 bootstyle=(SUCCESS, OUTLINE), 
                                 width=25, 
                                 padding=8,
                                 command=lambda: (command(), self.MainNotebook.select(2))
                            )
        # StartServer.pack(side=RIGHT)
        Button.place(x=500, y=40)
        # Button.bind('<Button-1>', lambda event: (command(), self.MainNotebook.select(2)),)
        return Button
    
    def Host_Label(self, master, text):
        LabelHost = ttk.Label(master, text=text)
        LabelHost.place(x=10, y=30)
        return LabelHost

    def Host_Entry(self, master, Config):
        EntryHost = ttk.Entry(master)
        EntryHost.insert('0', Config["host"])
        EntryHost.place(x=10, y=55)
        return EntryHost

    def Port_Label(self, master, text):
        LabelPort = ttk.Label(master, text=text)
        LabelPort.place(x=10, y=100)
        return LabelPort

    def Port_Entry(self, master, Config):
        EntryPort = ttk.Entry(master)
        EntryPort.insert('0', Config["port"])
        EntryPort.place(x=10, y=125)
        return EntryPort

    def Password_Label(self, master, text):
        LabelPassword = ttk.Label(master, text=text)
        LabelPassword.place(x=10, y=170)
        return LabelPassword

    def Password_Entry(self, master, Config):
        EntryPassword = ttk.Entry(master)
        EntryPassword.insert('0', Config["password"])
        EntryPassword.place(x=10, y=195)
        return EntryPassword

    def Client(self, master):
        self.ClientFrame = ttk.Frame(master)
        return self.ClientFrame

    def Name_Label(self, master, text):
        LabelName = ttk.Label(master, text=text)
        LabelName.place(x=10, y=240)
        return LabelName

    def Name_Entry(self, master, Config):
        EntryName = ttk.Entry(master)
        EntryName.place(x=10, y=265)
        EntryName.insert('0', Config["name"])
        return EntryName

    def SetUp(self, master):
        self.SetUpFrame = ttk.Frame(master)
        return self.SetUpFrame
    
    def Language_Label(self, master, text):
        LanguageLabel = ttk.Label(master, text=text)
        LanguageLabel.place(x=30, y=30)
        return LanguageLabel
    
    def Language_Combobox(self, master, labelText):
        LanguageCombobox = ttk.Combobox(
            master, values=config.LanguageNameList)
        LanguageCombobox.set(config.LanguageFileToNameDict[SetUpConfig["language"]])
        LanguageCombobox.place(x=55+len(labelText)*5, y=25)
        return LanguageCombobox
  
    def MainNoteBooks(self):
        self.NoteBook = ttk.Notebook(self)
        self.NoteBook.add(self.Server(self), text=self.Language["tab"][0])
        self.NoteBook.add(self.Client(self), text=self.Language["tab"][1])
        self.NoteBook.add(self.Terminal(self), text=self.Language["tab"][2])
        self.NoteBook.add(self.SetUp(self), text=self.Language["tab"][3])
        self.NoteBook.add(self.About(self), text=self.Language["tab"][4])
        self.NoteBook.pack(expand=True, fill="both")
        return self.NoteBook

Windows()
