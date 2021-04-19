import wx
import wx.adv
import embed

class TaskBar(wx.adv.TaskBarIcon):
    Icon = './images/icon.png'
    Title = 'embed'
    Windows = []

    MENU_ID1, MENU_ID2,MENU_ID3,MENU_ID4,MENU_ID5 = wx.NewIdRef(count=5)

    def __init__(self):
        super().__init__()

        self.SetIcon(wx.Icon(self.Icon), self.Title)

        self.Bind(wx.EVT_MENU, self.OnTop, id=self.MENU_ID1)
        self.Bind(wx.EVT_MENU, self.OnBottom, id=self.MENU_ID2)
        self.Bind(wx.EVT_MENU, self.OnEmbed, id=self.MENU_ID3)
        self.Bind(wx.EVT_MENU, self.OnRecover, id=self.MENU_ID4)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.MENU_ID5)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.MENU_ID1, '置顶')
        menu.Append(self.MENU_ID2, '置底(慎用)')
        menu.Append(self.MENU_ID3, '嵌入')
        menu.Append(self.MENU_ID4, '还原')
        menu.Append(self.MENU_ID5, '退出')
        return menu

    def OnTop(self, event):
        hwnd = embed.get_next_hwnd()
        window = embed.get_window(hwnd)
        self.Windows.append(window)
        ok = embed.top(hwnd)
        if not ok:
            wx.MessageBox('无法置顶此窗口')

    def OnBottom(self, event):
        hwnd = embed.get_next_hwnd()
        window = embed.get_window(hwnd)
        self.Windows.append(window)
        ok = embed.bottom(hwnd)
        if not ok:
            wx.MessageBox('无法置底此窗口')

    def OnEmbed(self, event):
        hwnd = embed.get_next_hwnd()
        window = embed.get_window(hwnd)
        self.Windows.append(window)
        ok = embed.embed(hwnd)
        if not ok:
            wx.MessageBox('无法嵌入此窗口')

    def OnRecover(self, event):
        embed.recover(self.Windows)
        self.Windows = []

    def onExit(self, event):
        wx.Exit()


if __name__ == "__main__":
    app = wx.App()
    TaskBar()
    app.MainLoop()
