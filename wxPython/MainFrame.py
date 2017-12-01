#coding=utf-8
import wx
import urllib



def Load(event):
    #wx.MessageBox('you click the load button!')
    strURL = r'https://wxpython.org/pages/overview/'
    webPage = urllib.urlopen(strURL)
    print webPage.read()

    webPage.close()
def Save(event):
    wx.MessageBox('you click the save button!')

def main():
    '''
    main function
    :return:
    '''
    app = wx.App()
    winform = wx.Frame(None,title = '主窗口',size = (410,335))
    panel = wx.Panel(winform)

    loadButton = wx.Button(panel,label = 'Load(&L)')
    loadButton.Bind(wx.EVT_BUTTON,Load)
    saveButton = wx.Button(panel,label = 'Save(&S)')
    saveButton.Bind(wx.EVT_BUTTON, Save)
    filename = wx.TextCtrl(panel)
    content = wx.TextCtrl(panel,style = wx.TE_MULTILINE | wx.HSCROLL)
    hbox = wx.BoxSizer()
    hbox.Add(filename,proportion = 1,flag = wx.EXPAND)
    hbox.Add(loadButton,proportion = 0,flag = wx.LEFT,border=5)
    hbox.Add(saveButton, proportion = 0, flag = wx.LEFT, border=5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox,proportion = 0,flag = wx.EXPAND | wx.ALL,border = 5)
    vbox.Add(content,proportion = 1,flag = wx.EXPAND | wx.LEFT | wx.RIGHT,border = 5)

    panel.SetSizer(vbox)
    winform.Center()
    winform.Show()
    app.MainLoop()

if '__main__' == __name__:
    main()
