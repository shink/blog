---
title: frp 远程连接内网主机详细教程
date: 2020-07-24 22:35:16
categories: [路由器]
tags: [路由器, Tools]
---

## 1. 准备工作

- 一台有公网 ip 的 server
- 一台内网主机或路由器

## 2. 服务端配置（远程 server）

这里以阿里云 Centos 7 为例

<!-- more -->

### 2.1 下载与安装

进入 `/tmp` 目录

```shell
cd /tmp
```

在 [Releases](https://github.com/fatedier/frp/releases) 页面下载与 server 系统、架构相符的 frp 版本

```shell
wget https://github.com/fatedier/frp/releases/download/v0.33.0/frp_0.33.0_linux_amd64.tar.gz
```

解压

```shell
tar -zxvf frp_0.33.0_linux_amd64.tar.gz
```

移动到 `/usr/local` 目录下，并重命名为 `frp`

```shell
mv frp_0.33.0_linux_amd64 /usr/local/frp
```

### 2.2 配置

进入安装目录 `/usr/local/frp`，并删除客户端相关文件

```shell
cd /usr/local/frp && rm -rf frpc*
```

编辑配置文件

```shell
vi frps.ini
```

写入以下内容：

```
[common]
bind_port = 7000
privilege_token = 123456
dashboard_port = 7500
dashboard_user = admin
dashboard_pwd = admin
```

> 其中，`bind_port` 为客户端与服务端进行通信的端口；`privilege_token` 为特权模式密钥，需与客户端配置一致；`dashboard_port` 为可视化面板的端口号；`dashboard_user` 为登录面板的用户名；`dashboard_pwd` 为登录密码

> `privilege_token` 参数的作用是提供身份验证机制，避免其他客户端随意连接服务端

### 2.3 设置开机启动和后台运行

新建文件

```shell
vi /etc/systemd/system/frps.service
```

写入以下内容

```
[Unit]
Description=frps daemon
After=syslog.target  network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/frp/frps -c /usr/local/frp/frps.ini
Restart=always
RestartSec=1min

[Install]
WantedBy=multi-user.target
```

> 注意修改第 8 行的路径

设置开机启动

```shell
systemctl enable frps
```

启动 frps

```shell
systemctl start frps
```

## 3. 客户端配置（本地主机）

这里以 win10 为例

### 3.1 下载与安装

在 [Releases](https://github.com/fatedier/frp/releases) 页面下载 `windows_amd64` 版本，并解压

删除 `frps`、`frps.ini`、`frps_full.ini`

### 3.2 配置

编辑 `frpc.ini` 文件，写入以下内容：

```
[common]
server_addr = tsund.me
server_port = 7000
privilege_token = 123456

[rdp]
type = tcp
local_ip = 0.0.0.0
local_port = 3389
remote_port = 3389
```

> 其中，`server_addr` 为 server ip 地址或解析到该 ip 的域名，`server_port` 需与服务端 `bind_port` 保持一致，`privilege_token` 需与服务端 `privilege_token` 保持一致，下面的 `rdp` 标签设定了远程桌面连接的端口映射

### 3.3 设置开机启动

在 frp 目录下新建文件 `frp.vbs`，并写入以下内容：

```
dim objShell 
set objShell=wscript.createObject("WScript.Shell") 
iReturnCode=objShell.Run("D:\frp\frpc.exe -c D:\frp\frpc.ini", 0, TRUE)
```

> 注意修改第 3 行的路径

将 `frp.vbs` 放入 `C:\Users\shenke\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` 目录下，即可实现开机启动

双击运行 `frp.vbs` ，即可启动 frpc 服务

### 3.4 允许远程桌面连接

「右键此电脑」->「属性」->「高级系统设置」->「远程」->「允许远程连接到此计算机」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/1.png" width=450>
</p>

## 4. 客户端配置（路由器）

这里以 Padavan 固件的 PHICOMM K2 路由器为例。Padavan 固件内置了 frps 和 frpc，这里以 frpc 为例

1. 绑定本地主机的 ip 地址和 mac 地址

「高级设置」->「内部网络（LAN）」->「DHCP 服务器」->「手动指定 IP 的 DHCP 列表」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/2.png" width=600>
</p>

2. 配置 frpc

「扩展功能」->「花生壳内网版」->「frp」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/3.png" width=800>
</p>

配置方法同 3.2，只需修改 `local_ip` 为 DHCP 服务器分配给本地主机的 ip

## 5. 测试

访问 `http://your-ip:7500`，进入 frp 的 dashboard 页面，如果无法访问，说明 frp 尚未启动成功或者 server 的端口未成功开放

查看 frp 进程是否运行

```shell
top
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/4.png" width=750>
</p>

> 如果 frp 进程没有运行，可能是因为 frp 版本与 server 的操作系统或架构不符，再次下载相符的版本重新配置即可

查看 server 端口占用情况

```shell
# linux
netstat -nltp

# windows
netstat -an
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/5.png" width=800>
</p>

通过站长工具的 [端口扫描](http://tool.chinaz.com/port/) 查看 server 端口是否对外开放

> 如果 server 中端口开放，但是端口扫描显示关闭，只需去控制台配置安全组即可

## 6. 连接

这里以 win10 电脑为例，远程连接内网中的 win10 主机

`win + r`，输入 `mstsc`，进入远程桌面连接

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/07/frp-remote-desktop/6.png" width=450>
</p>

输入计算机：`ip:port` 或 `domain:port`，根据前面的配置，我这里输入的是 `tsund.me:3389`

用户名和密码填写的是内网主机的用户名和密码（内网主机中我登录的是 MicroSoft 账户，开机密码是六位 PIN 码，但是输入了电脑用户名和 MicroSoft 账户密码才进去的）
