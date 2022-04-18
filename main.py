import wx
import os
import time
import sys
import configparser


class Frame(wx.Frame):
  def __init__(self):
      wx.Frame.__init__(self, None, title='文件夹备注工具', size=(
          505, 139), name='frame', style=541072384)
      self.runW = wx.Panel(self)
      self.Centre()
      self.editB0x1 = wx.TextCtrl(self.runW, size=(291, 31), pos=(
          82, 10), value='', name='text', style=0)
      self.editB0x1.Bind(wx.EVT_LEFT_DOWN, self.editB0x1_mLeftC)
      self.leb1 = wx.StaticText(self.runW, size=(61, 18), pos=(
          11, 19), label='文件夹路径', name='staticText', style=2321)
      self.leb2 = wx.StaticText(self.runW, size=(61, 20), pos=(
          12, 60), label='备注', name='staticText', style=2321)
      self.editB0x2 = wx.TextCtrl(self.runW, size=(291, 31), pos=(
          82, 53), value='', name='text', style=0)
      self.button2 = wx.Button(self.runW, size=(91, 70), pos=(
          389, 14), label='校验/保存', name='button')
      button2_font = wx.Font(12, 74, 90, 700, False, 'Microsoft YaHei UI', 28)
      self.button2.SetFont(button2_font)
      self.button2.Bind(wx.EVT_LEFT_DOWN, self.button2_mLeftC)

  def editB0x1_mLeftC(self,event):
    print('editB0x1,mLeftC')
    # 选择文件夹
    dlg = wx.DirDialog(self, "选择文件夹", style=wx.DD_DEFAULT_STYLE)
    if dlg.ShowModal() == wx.ID_OK:
      self.editB0x1.SetValue(dlg.GetPath())
    dlg.Destroy()


  def button2_mLeftC(self,event):
    print('button2,mLeftC')
    # 判断路径是否存在
    if not os.path.exists(self.editB0x1.GetValue()):
      print('路径不存在')
      dlg = wx.MessageDialog(self, '路径不存在', '提示', wx.OK | wx.ICON_INFORMATION)
      dlg.ShowModal()
      dlg.Destroy()
      return False
    
    if not self.editB0x2.GetValue():
      print('备注不能为空')
      dlg = wx.MessageDialog(self, '备注不能为空', '提示', wx.OK | wx.ICON_INFORMATION)
      dlg.ShowModal()
      dlg.Destroy()
      return False
    dirPath = self.editB0x1.GetValue()
    InfoTip = self.editB0x2.GetValue()
    if os.path.exists(dirPath+'/desktop.ini') == False:
      print('不存在,准备创建')
      file = open(dirPath+'/desktop.ini', 'w')
      file.close()
    else:
      # 弹框询问
      dlg = wx.MessageDialog(self, '是否覆盖原有备注', '提示', wx.YES_NO | wx.ICON_INFORMATION)
      if dlg.ShowModal() == wx.ID_YES:
        # 先删除文件
        os.system('attrib '+dirPath+'/desktop.ini -r -h')
        time.sleep(0.05)
        os.remove(dirPath+'/desktop.ini')
        file = open(dirPath+'/desktop.ini', 'w')
        file.close()
      else:
        print('不覆盖')
        return False
    
    # 创建管理对象
    conf = configparser.ConfigParser()
    # 读ini文件
    conf.read(dirPath+'/desktop.ini', encoding="GBK")
    # 获取所有的section
    sections = conf.sections()
    print(sections)

    # 添加一个select
    conf.add_section(".ShellClassInfo")
    conf.set(".ShellClassInfo", "IconResource",
            "C:\WINDOWS\System32\SHELL32.dll,4")
    conf.set(".ShellClassInfo", "InfoTip", '"'+InfoTip+'"')
    print(conf.sections())

    # 添加一个select
    conf.add_section("ViewState")
    conf.set("ViewState", "Mode", "")
    conf.set("ViewState", "Vid", "")
    conf.set("ViewState", "FolderType", "Generic")
    print(conf.sections())

    conf.write(open(dirPath+'/desktop.ini', "a"))  # 追加模式写入
    # 关闭文件
    file.close()

    # 设置权限 
    os.system('attrib '+dirPath+'/desktop.ini +r +h')
    time.sleep(0.05)
    # 刷新
    os.system('attrib '+dirPath+' +s /d')
    time.sleep(0.05)
    
    dlg = wx.MessageDialog(self, '备注设置完成，退出本程序后生效', '提示', wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


class myApp(wx.App):
  def OnInit(self):
    self.frame = Frame()
    self.frame.Show(True)
    return True

def age_c():
  print('命令行模式')
  print('文件夹路径:')
  dirPath = input()
  # 判断路径是否存在
  if not os.path.exists(dirPath):
    print('路径不存在')
    exit()

  # 路径下是否存在'./desktop.ini'文件

  if os.path.exists(dirPath+'/desktop.ini') == False:
    print('不存在,准备创建')
    file = open(dirPath+'/desktop.ini', 'w')
    file.close()
  else:
    print('已存在,是否删除(Y/N)?')
    isDel = input()
    # 不区分大小写判断
    if isDel.upper() == 'Y':
      # 先删除文件
      os.system('attrib '+dirPath+'/desktop.ini -r -h')
      time.sleep(0.05)
      os.remove(dirPath+'/desktop.ini')
      file = open(dirPath+'/desktop.ini', 'w')
      file.close()
    else:
      exit()

  print('路径备注:')
  InfoTip = input()

  # 创建管理对象
  conf = configparser.ConfigParser()
  # 读ini文件
  conf.read(dirPath+'/desktop.ini', encoding="GBK")
  # 获取所有的section
  sections = conf.sections()
  print(sections)

  # 添加一个select
  conf.add_section(".ShellClassInfo")
  conf.set(".ShellClassInfo", "IconResource",
          "C:\WINDOWS\System32\SHELL32.dll,4")
  conf.set(".ShellClassInfo", "InfoTip", '"'+InfoTip+'"')
  print(conf.sections())

  # 添加一个select
  conf.add_section("ViewState")
  conf.set("ViewState", "Mode", "")
  conf.set("ViewState", "Vid", "")
  conf.set("ViewState", "FolderType", "Generic")
  print(conf.sections())

  conf.write(open(dirPath+'/desktop.ini', "a"))  # 追加模式写入
  # 关闭文件
  file.close()

  # 设置权限
  os.system('attrib '+dirPath+'/desktop.ini +r +h')
  time.sleep(0.05)
  # 刷新
  os.system('attrib '+dirPath+' +s /d')
  time.sleep(0.05)

def age_u():
  print('GUI模式')
  app = myApp()
  app.MainLoop()

if __name__ == '__main__':
  # 默认执行age_c 当接收到u时执行age_u
  if '-c' in sys.argv:
    age_c()
  else:
    age_u()