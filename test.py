# -*- coding: utf-8 -*-
_author_ = 'xiao_lu'
from Tkinter import *
from ScrolledText import ScrolledText
import platform
import nmap
import tkMessageBox
import os
#test
index=1.0
class Scan:
    def __init__(self,root):
        #页面可视化
        self.root=root
        self.ip = StringVar()
        frame = Frame(root)
        root.title("端口扫描")
        frame.pack(padx=8, pady=8, ipadx=4)
        iplabel = Label(frame, text="输入IP:",font='Helvetica -15 bold')
        iplabel.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ipentry = Entry(frame, textvariable=self.ip,width=30)
        ipentry.grid(row=0, column=1, sticky='ew', columnspan=2, padx=5, pady=5)
        ok = Button(frame, text="确认", default='active',command=submit)
        ok.grid(row=0, column=3,padx=8, pady=5)
        resultlabel = Label(frame, text="扫描结果如下:", font='Helvetica -15 bold')
        resultlabel.grid(row=1, column=0, padx=5, pady=5, sticky=W,columnspan=2)
        self.resulttext=ScrolledText(frame,width=30, height=12,font=('Courier New', 13),fg='black',bg='white')
        self.resulttext.grid(row=2,column=0,columnspan=4)
        #退出
        quitscan= Button(frame, text="退出", default='active',command=quit,width=8,height=1)
        quitscan.grid(row=3, column=1, padx=8, pady=5)
        clearscan=Button(frame, text="清空", default='active',command=clear,width=8,height=1)
        clearscan.grid(row=3, column=2, padx=8, pady=5)
def nmapScan(tgtHost, tgtPort):
        global index
        nmScan = nmap.PortScanner()
        nmScan.scan(tgtHost, tgtPort)
        state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
        theport_is_open= "[+]" + tgtHost + ':' + tgtPort + " "+ state+"\n"
        app.resulttext.tag_config('b', foreground='blue')
        app.resulttext.insert(index, theport_is_open, 'b')
        index += 1.0
        app.resulttext.update()
        return
def get_os():
        '''''
       判断系统类型
       '''
        os = platform.system()
        if os == "Windows":
            return "n"
        else:
            return "c"
def ping_ip(ip_str):
        global index
        #ping 该主机
        cmd = ["ping", "-{op}".format(op=get_os()),
               "1", ip_str]
        output = os.popen(" ".join(cmd)).readlines()
        flag = False
        #得到PING 数据
        for line in list(output):
            if not line:
                continue
            if str(line).upper().find("TTL") >= 0:
                flag = True
                break
        #存在一个主机
        if flag:
            s="[*]IP: %s is exist\n"%ip_str
            print s
            #输出一个主机
            app.resulttext.tag_config('a', foreground='red')
            app.resulttext.insert(index,s,'a')
            index+=1.0
            app.resulttext.update()
            #namp该主机的端口
            usalPorts={22,25,43,80,107,139,158,518,990,1863,3306,3389}
            for usalPort in usalPorts:
               nmapScan(ip_str,str(usalPort))
#扫描数据存在主机
def submit():
    #得到一个ip地址的网段
   tgrip=app.ip.get()
   args = "".join(tgrip)
   ip_prefix = '.'.join(args.split('.')[:-1])
   #搜索主机
   for i in range(1, 255):
       ip = '%s.%s' % (ip_prefix, i)
       ping_ip(ip)
   tkMessageBox.showinfo(title='Ending', message="the scan was over")
#清空数据
def clear():
    global index
    #清空全部的数据
    app.ip.set("")
    app.resulttext.delete(1.0,index)
    index=1.0
if __name__ == '__main__':
    global app
    root = Tk()
    app = Scan(root)
    app.root.update_idletasks()
    #显示在屏幕中间
    x = (app.root.winfo_screenwidth() - app.root.winfo_reqwidth()) / 2
    y = (app.root.winfo_screenheight() -app. root.winfo_reqheight()) / 2
    app.root.geometry("+%d+%d" % (x, y))
    #页面大小
    app.root.geometry("400x400")
    app.root.mainloop()
    app.root.destroy()