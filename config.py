
import pyautogui
from os.path import join, isfile, splitext
from os import getcwd, listdir
from json import loads

Size = (720, 360)
Width = pyautogui.size().width
Height = pyautogui.size().height
Position = (int((Width - Size[0]) / 2), int((Height - Size[1]) / 2))
Title = "SimpleChat"
InfoBytes = pow(2, 50)
ConfigName = "config.json"
ConfigPath = join(getcwd(), ConfigName)
DefaultConfigContent = {
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
        "password": ""
    },
    "client": {
        "host": "127.0.0.1",
        "port": 5000,
        "name": "",
        "password": ""
    },
    "setup": {
        "language": "zh-cn",
    }

}
LibrariesPath = join(getcwd(), "libraries")
LanguagePath =  join(LibrariesPath, "language")
LanguagePathList = [f for f in listdir(LanguagePath) if isfile(join(LanguagePath, f)) and f.endswith('.json')]
LanguageNameList = [
    loads(open(join(LanguagePath, f), encoding="utf-8").read())["info"]["name"] 
    for f in LanguagePathList
]
LanguageDict = {
    name: loads(open(join(LanguagePath, f), encoding="utf-8").read()) 
    for name, f in zip(LanguageNameList, LanguagePathList)
}
LanguageFileToNameDict = {splitext(f)[0]: n for f, n in zip(LanguagePathList, LanguageNameList)}
LanguageNameToFileDict = {v: k for k, v in LanguageFileToNameDict.items()}