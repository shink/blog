---
title: SSH 免密登录（设置后仍需输入密码的原因及解决方法）
date: 2020-08-20 19:37:11
tags: [Solutions]
---

## 1. 需求

机器 A （客户端）使用 SSH 免密连接机器 B（服务端）

<!-- more -->

## 2. 客户端配置

1. 进入用户目录的 `.ssh` 目录，生成公钥和私钥

```shell
ssh-keygen -t rsa -C "email@domain.com" -f filename
```

> 其中，`-C` 设置注释文字，例如邮箱；`-f` 指定密钥文件存储文件名

2. 将生成的公钥分发到服务端

方法一：使用 `ssh-copy-id` 命令，将公钥添加到服务端的 `authorized_keys` 文件中

```shell
ssh-copy-id -i ~/.ssh/filename.pub user@host
```

> 其中，`user` 是要登录服务端的用户名，`host` 是服务端的 ip 或 domain

方法二：将公钥拷贝到服务端，使用 `cat` 命令追加到 `authorized_keys` 文件中

```shell
cat filename.pub >> authorized_keys
```

3. 配置 config 文件

**注意**：由于密钥认证时默认使用 `~/.ssh/id_rsa` 文件作为私钥，因此还需额外配置。如果使用的公钥和私钥是默认名，即 `id_rsa`，则该步可跳过

在 `~/.ssh` 目录下新建一个 `config` 文件

```shell
touch config
```

编辑 `config` 文件

```shell
vi config
```

写入以下内容

```
Host aliyun
HostName ip
User root
IdentityFile ~/.ssh/filename
```

> 其中，`Host` 标识一个配置区段，每个配置区段是用 Host 来区分的，例如我这里使用 `aliyun` 作为一个配置区段   
> `HostName` 指定远程主机名     
> `User` 指定登录用户名     
> `IdentityFile` 指定密钥认证使用的私钥文件路径     
> 此外，还可以使用 `Port` 指定远程主机端口号，默认 22

## 3. 测试

在客户端尝试连接服务端

```shell
ssh user@host
```

若无需输入密码即可登录，则配置成功

## 4. 设置无效的原因及解决方法

### 4.1 原因

1. 客户端私钥文件路径未配置或配置错误

2. 服务端配置错误

   - 权限错误

   - `/etc/ssh/sshd_config` 文件配置错误

### 4.2 解决方法

1. 检查客户端 `~/.ssh/config` 文件，配置方法如前所述

2. 在服务端修改权限

```shell
chmod 700 ~/.ssh

chmod 600 ~/.ssh/authorized_keys
```

3. 配置 `/etc/ssh/sshd_config` 文件，修改以下内容，启用秘钥验证

```
PubkeyAuthentication yes
```

修改后重启 sshd 服务

```shell
service sshd restart
```
