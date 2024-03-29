# rclone-gui


rclone官网：https://rclone.org/

#### 介绍
自己用py写的rclone-gui，方便rclone托盘使用

#### 安装教程

1.  如修改源码，请使用pyinstaller -F -w tray.py打包，结束后可以在dist文件夹中找到可执行文件。
2.  需要安装winsfp与rclone，把rclone.exe及它需要的文件放在tray.exe同级文件夹，双击tray.exe即可。

#### 使用说明

1.  配置文件名称后面的输入框中输入你已经设置好的配置文件，不会的话可以参考我的文章设置：https://www.bilibili.com/read/cv21803909
2.  挂载至会自动查找C-Z的所有可用硬盘。
3.  不验证SSL证书与开启缓存建议默认勾上，当然你要确认没问题可以不勾。
4.  右下角的文本框会显示当前软件启动的所有进程，格式为 "配置文件名 -> 挂载盘符"。
5.  删除连接时删除的不是右下角选中的进程，而是“挂载至”的按钮所选中的盘符对应的进程。
6.  隐藏窗口会将程序最小化到托盘，退出程序会直接退出程序。
7.  最小化到托盘后，对托盘图标右键有三个选项可以使用，包括显示窗口。

#### 已知BUG与不足
1.  不手动关闭所有连接可能会导致从软件启动的rclone无法一起关闭，已经在主线程最后强制关闭所有子进程了，但是依然还是建议点击“删除连接”按钮将连接手动删除后再退出程序。
2.  不会检查配置文件是否存在，这里后续可能会改进一下。
3.  如果配置文件有密码则无法输入，建议取消配置文件密码后再使用该软件。


#### 欢迎关注

橘里橘气橘子花@bilibili，https://space.bilibili.com/128589727
会带给你更多有意思的小东西。
