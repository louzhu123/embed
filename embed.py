import win32gui,win32con,win32api
from ctypes import windll


'''
init
使用嵌入方法前需要做的工作 https://blog.csdn.net/bjbz_cxy/article/details/79893134
'''
def init():
    Program_Manager = win32gui.FindWindow("Progman","Program Manager")
    win32gui.SendMessage(Program_Manager, 0x052c, 0, 0)  # 发送多屏消息

    currentHwnd = None
    nextHwnd = None
    # 遍历寻找多余的WorkerW窗口
    while True:
        currentHwnd = win32gui.FindWindowEx(None, currentHwnd, None, None)
        if currentHwnd is None or currentHwnd == 0:
            break
        
        if win32gui.GetClassName(currentHwnd) == "WorkerW":
            nextHwnd = win32gui.FindWindowEx(None, currentHwnd, None, None)
            SHELLDLL_DefView = win32gui.FindWindowEx(currentHwnd,0,"SHELLDLL_DefView",None)
            if win32gui.GetClassName(nextHwnd) == "Progman" and SHELLDLL_DefView == 0:
                win32gui.SendMessage(currentHwnd, 16, 0, 0) # 关闭多余的这个Workerw窗口
                break

'''
canOperate
限制操作一些系统窗口，否则会影响体验
'''
def canOperate(windowHwnd):
    if win32gui.GetClassName(windowHwnd) == "Shell_TrayWnd":
        return False
    return True

'''
top
置顶操作
'''
def top(windowHwnd):
    print("置顶",win32gui.GetWindowText(windowHwnd))
    if canOperate(windowHwnd) is False:
        return False
    try:
        win32gui.SetParent(windowHwnd,0)
        win32gui.SetWindowPos(windowHwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)		
        return True
    except:
        return False

'''
bottom
置底操作（慎用），有些无法移动(酷狗音乐)，有些无法画全(文件管理器)
'''
def bottom(windowHwnd):
    print("置底",win32gui.GetWindowText(windowHwnd))
    if canOperate(windowHwnd) is False:
        return False
    try:
        currentHwnd = None
        while True:
            currentHwnd = win32gui.FindWindowEx(None, currentHwnd, None, None)
            if currentHwnd is None or currentHwnd == 0:
                break
            SHELLDLL_DefView = win32gui.FindWindowEx(currentHwnd,0,"SHELLDLL_DefView",None)
            if SHELLDLL_DefView:
                win32gui.SetParent(windowHwnd,currentHwnd)
                break
        return True
    except:
        return False

'''
embed
嵌入桌面
'''
def embed(windowHwnd):
    print("嵌入",win32gui.GetWindowText(windowHwnd))
    if canOperate(windowHwnd) is False:
        return False
    try:
        Program_Manager = win32gui.FindWindow("Progman","Program Manager")
        win32gui.SetParent(windowHwnd,Program_Manager)
        return True
    except:
        return False

'''
embed
还原所有窗口
'''
def recover(windows):
    for window in windows:
        win32gui.SetParent(window['hwnd'],0)
        win32gui.SetWindowPos(window['hwnd'], win32con.HWND_NOTOPMOST, 0,0,0,0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

    if len(windows) != 0:
        return

    # 程序异常退出时使用
    bottom_windows = get_bottom_windows()
    print("bottom_windows:",len(bottom_windows))
    for window in bottom_windows:
        win32gui.SetParent(window['hwnd'],0)
    
    embed_windows = get_embed_windows()
    print("embed_windows:",len(embed_windows))
    for window in embed_windows:
        win32gui.SetParent(window['hwnd'],0)

'''
get_subwindows
获取窗口下的所有子窗口
'''
def get_subwindows(hwnd):
    windows = []
    currentHwnd = None
    while True:
        currentHwnd = win32gui.FindWindowEx(hwnd, currentHwnd, None, None)
        if currentHwnd is None or currentHwnd == 0:
            break
        window = get_window(currentHwnd)
        windows.append(window)

    return windows


'''
get_window
获取window的一些信息
'''
def get_window(hwnd):
    window = {}
    window['hwnd'] = hwnd
    window['title'] = win32gui.GetWindowText(hwnd)
    window['className'] = win32gui.GetClassName(hwnd)
    return window

'''
get_top_windows
程序异常退出时使用
获取置顶的窗口，但是获取到很多其余窗口，无法只获取被用户置顶的窗口
'''
# def get_top_windows():
#     windows = []
#     currentHwnd = None
#     while True:
#         currentHwnd = win32gui.FindWindowEx(0, currentHwnd, None, None)
#         if currentHwnd is None or currentHwnd == 0:
#             break
#         if win32gui.GetWindowLong(currentHwnd, win32con.GWL_EXSTYLE) == win32con.WS_EX_TOPMOST:
#             windows.append(get_window(currentHwnd))
#     return windows


'''
get_bottom_windows
程序异常退出时使用
获取置底的窗口
'''
def get_bottom_windows():
    workerwHwnd  = None
    currentHwnd = None
    while True:
        currentHwnd = win32gui.FindWindowEx(0, currentHwnd, None, None)
        if currentHwnd is None or currentHwnd == 0:
            break
        
        SHELLDLL_DefView = win32gui.FindWindowEx(currentHwnd,None,"SHELLDLL_DefView",None)
        if SHELLDLL_DefView:
            workerwHwnd = currentHwnd
            break

    if workerwHwnd is None or workerwHwnd == 0:
        return []

    # 去掉SHELLDLL_DefView
    windows = get_subwindows(workerwHwnd)
    for index,window in enumerate(windows):
        if window["className"] == "SHELLDLL_DefView":
            windows.pop(index)
            break
        
    return windows

'''
get_bottom_windows
程序异常退出时使用
获取置底的窗口
'''
def get_embed_windows():
    Program_Manager = win32gui.FindWindow("Progman","Program Manager")
    windows = get_subwindows(Program_Manager)
    return windows

def get_next_hwnd():
    old = change_cursor()
    current_hwnd = win32gui.GetForegroundWindow()
    while(True):
        next_hwnd = win32gui.GetForegroundWindow()
        if next_hwnd != current_hwnd and next_hwnd != 0:
            windll.user32.SetSystemCursor(old, 32512)
            return next_hwnd

def change_cursor():
    hold = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED )
    old = windll.user32.CopyImage(hold, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
    new = win32gui.LoadImage(0, 'images/icon.cur', win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
    windll.user32.SetSystemCursor(new, 32512)
    return old

init()