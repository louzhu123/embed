import webview
import win32gui,win32api
import configparser

cf = configparser.ConfigParser()
cf.read("./config.ini")
url = cf.get("pywebview", "url")

tmpHwnd = None

# 遍历所有窗口，关闭Pogman前面的WokerW窗口，否则会遮挡被嵌入的窗口
def EnumWindowsProc(hwnd,lParam):
    global tmpHwnd
    className = win32gui.GetClassName(hwnd)
    if className == "WorkerW":
        SHELLDLL_DefView = win32gui.FindWindowEx(hwnd,0,"SHELLDLL_DefView",None)
        if SHELLDLL_DefView == 0:
            tmpHwnd = hwnd
    if className == "Progman":
        win32gui.SendMessage(tmpHwnd, 16, 0, 0)

# 嵌入到桌面
def embed():
    desk = win32gui.FindWindow("Progman","Program Manager")
    background = win32gui.FindWindowEx(desk,0,"SHELLDLL_DefView",None)
    program = win32gui.FindWindow(None,"123")
    win32gui.SendMessage(desk, 0x052c, 0, 0)
    win32gui.EnumWindows(EnumWindowsProc,0)
    win32gui.SetParent(program,desk)

def on_shown():
    print('pywebview window shown')
    embed()
    
window = webview.create_window(
    title='123',
    url = url,
    width=1920,
    height=1080,
    resizable=True,
    text_select=True,
    confirm_close=True,
    fullscreen=True,
)
window.shown += on_shown
webview.start()


