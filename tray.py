import pystray
from PIL import Image as Img
from pystray import MenuItem
from tkinter import *
from threading import Thread
from subprocess import Popen, CREATE_NO_WINDOW
from psutil import disk_partitions


class OranRcloneTray():
    def __init__(self) -> None:
        self.now_connect_num = 0
        self.now_select = ""
        self.now_connceted_progess_list = dict()
        # 获取所有可用盘符
        used_disks = [disk[0] for disk in disk_partitions()]
        
        self.disks = []
        for i in range(24):
            now_disk = "%s:\\"%chr(67+i)
            if now_disk not in used_disks:
                self.disks.append(now_disk)
        print(self.disks)
        self.un_used_disks = self.disks
        self.used_disks = []
        self.now_select = self.disks[0]

        self.root = Tk()
        text1 = Label(self.root, text='配置文件名称')
        text2 = Label(self.root, text='挂载至')
        text3 = Label(self.root, text='已连接')
        domain = Entry(self.root)

        self.is_not_cert_check = IntVar()
        self.is_cache_check = IntVar()
        is_not_cert = Checkbutton (self.root, text="不验证SSL证书", variable=self.is_not_cert_check)
        is_cache = Checkbutton (self.root, text="开启缓存", variable=self.is_cache_check)

        # 下拉菜单绑定比较麻烦
        var = StringVar(self.root)
        var.set(self.disks[0])
        mount_to = OptionMenu(self.root, var, *self.disks)
        def callback(*args):
            self.now_select = var.get()
            print(var.get())
        var.trace("w", callback)
        self.mount_to = mount_to

        add_disk = Button(self.root, text="添加连接", command=self.add_disk)
        del_disk = Button(self.root, text="删除连接", command=self.del_disk)

        def hid_win():
            self.root.withdraw()
        def cls_win():
            self.root.destroy()
        hide_window = Button(self.root, text="隐藏窗口", command=hid_win)
        close_window = Button(self.root, text="退出程序", command=cls_win)

        self.connected = Listbox(self.root)
        # URL部分
        text1.grid(row=0, column=0)
        domain.grid(row=0, column=1)
        # 挂载部分
        text2.grid(row=1, column=0)
        mount_to.grid(row=1, column=1)
        
        # 其他选项
        is_not_cert.grid(row=2, column=0)
        is_cache.grid(row=2, column=1)
        # 添加按钮
        add_disk.grid(row=3, column=0)
        del_disk.grid(row=4, column=0)
        hide_window.grid(row=5, column=0)
        close_window.grid(row=6, column=0)
        # 已连接
        text3.grid(row=4, column=0)
        self.connected.grid(row=3, column=1, rowspan=4)
        # 声明一些后面要拿数据的组件
        self.domain = domain
        # 托盘
        menu = (MenuItem("显示窗口", lambda: self.root.deiconify()), MenuItem("隐藏窗口", lambda: self.root.withdraw()), MenuItem("关闭程序", lambda: self.root.destroy()))
        image = Img.open("static/img.jpg")
        self.icon = pystray.Icon("name", image, "rclone", menu)

    def start_tk(self):
        self.root.mainloop()

    def start_tray(self):
        self.icon.run()

    def start_progress(self):
        # 子线程启动托盘和控制台程序
        t1 = Thread(target=self.start_tray)
        t1.setDaemon(True)
        t1.start()
        # 启动程序
        self.start_tk()
    
    def add_disk(self):
        disk_flag = self.now_select
        if disk_flag in self.used_disks:
            print("重复选择")
        else:
            # 开始子进程
            domain = self.domain.get()
            is_cache = self.is_cache_check.get()
            is_not_cert = self.is_not_cert_check.get()
            print(domain, is_cache, is_not_cert)
            cmd = "./rclone.exe mount %s:/ %s --vfs-cache-mode %s --no-check-certificate=%s"%(domain, disk_flag, "full" if is_cache else "off", "true" if is_not_cert else "false")
            print(cmd)
            cmd = cmd.split(" ")
            self.now_connceted_progess_list[disk_flag] = Popen(cmd, shell=False,creationflags = CREATE_NO_WINDOW)
            self.now_connect_num += 1
            # 将该磁盘踢出队列
            self.un_used_disks.remove(disk_flag)
            self.used_disks.append(disk_flag)
            # 添加到已连接
            self.connected.insert(self.now_connect_num, "%s -> %s"%(domain, disk_flag))

    def del_disk(self):
        disk_flag = self.now_select
        if disk_flag in self.un_used_disks:
            print("重复选择")
        else:
            # 停止子进程
            subp = self.now_connceted_progess_list.get(disk_flag)
            subp.kill()
            del self.now_connceted_progess_list[disk_flag]
            self.now_connect_num -= 1
            # 删除已连接
            print(self.used_disks)
            n = self.used_disks.index(disk_flag)
            self.connected.delete(n, n)

            # 将该磁盘加入队列
            self.used_disks.remove(disk_flag)
            self.un_used_disks.append(disk_flag)
    
    def del_disk_(self, disk=None):
        disk_flag =disk
        # 停止子进程
        subp = self.now_connceted_progess_list.get(disk_flag)
        subp.kill()

    
if __name__ == "__main__":
    o = OranRcloneTray()
    o.start_progress()
    for disk in o.used_disks:
            o.del_disk_(disk=disk)