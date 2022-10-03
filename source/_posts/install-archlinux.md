---
title: ArchLinux 双系统安装
date: 2022-10-03 22:01:20
categories: [ArchLinux]
tags: [ArchLinux, 环境安装]
---

## 参考：

[Installation guide](https://wiki.archlinux.org/title/Installation_guide)

[2021 Archlinux双系统安装教程（超详细）](https://zhuanlan.zhihu.com/p/138951848)

[2021年vmware安装archlinux_ITKEY_的博客-CSDN博客_archlinux 安装](https://blog.csdn.net/lxyoucan/article/details/115226297)

[【archlinux】双系统真机安装演示_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1ag411K725)

<!-- more -->

## 1. 验证启动方式

```bash
ls /sys/firmware/efi/efivars
```

> 对于NVMe硬盘，要把从硬盘的启动方式改成 **AHCI**
> 

## 2. 联网

```bash
ip link
ping archlinux.org
```

## 3. 设置镜像

使用`reflector`来获取速度最快的6个镜像，并将地址保存至`/etc/pacman.d/mirrorlist`

```bash
reflector -c China -a 6 --sort rate --save /etc/pacman.d/mirrorlist
```

或直接设置清华镜像：

[archlinux | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/archlinux/)

编辑`/etc/pacman.d/mirrorlist`， 在文件的最顶端添加：

```bash
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
```

更新软件包缓存：

```bash
sudo pacman -Syy
```

## 4. 硬盘分区

ArchLinux官方文档参考：UEFI with GPT

| 挂载点                | 分区                      | 分区类型              | 分区大小       |
| --------------------- | ------------------------- | --------------------- | -------------- |
| /mnt/boot or /mnt/efi | /dev/efi_system_partition | EFI system partition  | 至少300MiB     |
| [SWAP]                | /dev/swap_partition       | Linux swap            | 超过512MiB     |
| /mnt                  | /dev/root_partition       | Linux x86-64 root (/) | 磁盘的剩余空间 |

> 这里实际采用以下方式：
>
> 1. 与 Windows 共用 EFI 分区
> 2. 不设置 SWAP 分区，采用`swapfile`
> 3. 将磁盘所有空间全部挂载到`/mnt`
1. 检查硬盘情况

```bash
lsblk
fdisk -l
```

1. 建立分区

```bash
fdisk /dev/nvme1n1
```

如果是全新的硬盘，则输入`g`，创建GPT分区表，若不是，则跳过该步骤：

```bash
Command(m for help): g
```

输入`n`，创建分区，分别输入分区类型，分区号、起始扇区、终止扇区

> 这里均采用默认配置，将整个磁盘划分为一个分区
> 

输入`w`，将更改写入磁盘

```bash
Command(m for help): w
```

检查分区情况：

```bash
lsblk
```

分区格式化：

```bash
mkfs.ext4 /dev/nvme1n1p6
```

挂载分区：

```bash
mount /dev/nvme1n1p6 /mnt
```

挂载EFI分区：

```bash
mkdir /mnt/boot
mount /dev/nvme1n1p1 /mnt/boot
```

## 5. 安装基本系统

1. 安装基本系统：

```bash
pacstrap /mnt base base-devel linux linux-firmware dhcpcd vim
```

1. 生成`fstab`文件

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

1. 检查生成的`fstab`文件

```bash
cat /mnt/etc/fstab
```

## 6. 正式配置系统

1. 切换到装好的系统

```bash
arch-chroot /mnt
```

1. 建立`swapfile`

```bash
dd if=/dev/zero of=/swapfile bs=2048 count=1048576 status=progress
```

设置权限：

```bash
chmod 600 /swapfile
```

建立swap空间：

```bash
mkswap /swapfile
```

激活swap空间：

```bash
swapon /swapfile
```

编辑`/etc/fstab`文件：

```bash
vim /etc/fstab
```

文件末尾输入：

```bash
/swapfile none swap defaults 0 0
```

1. 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

同步硬件时钟：

```bash
hwclock --systohc
```

1. 设置地区

```bash
vim /etc/locale.gen
# 取消 en_US 和 zh_CN 注释
```

生成locale：

```bash
locale-gen
```

创建并写入`/etc/locale.conf`文件：

```bash
echo 'LANG=en_US.UTF-8'  > /etc/locale.conf
```

1. 修改`hostname`

```bash
echo ArchLinux > /etc/hostname
```

1. 修改`hosts`

```bash
vim /etc/hosts
```

添加下列内容：

```bash
127.0.0.1 localhost
::1       localhost
127.0.1.1 ArchLinux.localdomain ArchLinux
```

其中，最后一行格式为，`YOUR_HOSTNAME`为设置的主机名

```bash
127.0.1.1 YOUR_HOSTNAME.localdomain YOUR_HOSTNAME
```

1. 安装微码

```bash
pacman -S intel-ucode   # Intel
pacman -S amd-ucode     # AMD
```

1. 设置root密码

```bash
passwd
```

1. 安装所需要的包

```bash
pacman -S grub efibootmgr networkmanager network-manager-applet dialog \
					wireless_tools wpa_supplicant os-prober mtools dosfstools \
					ntfs-3g base-devel linux-headers reflector git sudo vim
```

1. 配置grub

编辑`/etc/default/grub`文件，输入：

```bash
GRUB_DISABLE_OS_PROBER=false
```

安装grub引导程序：

```bash
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchLinux
```

生成`grub.cfg`配置文件：

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

1. 退出系统并取消挂载

```bash
exit
```

取消挂载：

```bash
umount -a
```

重启：

```bash
reboot
```

## 7. 配置系统

重启后输入root用户名和密码进入系统

1. 开启DHCP

```bash
systemctl enable dhcpcd  # 设置开机启动
systemctl start dhcpcd  # 立即启动dhcp
```

1. 通过`neofetch`查看硬件信息 

```bash
pacman -S neofetch
neofetch
```

1. 更新系统

```bash
pacman -Syyu
```

1. 创建新用户

```bash
useradd -m -G wheel shenke
```

设置密码：

```bash
passwd shenke
```

1. 配置用户`sudo`权限

添加文件写入权限：

```bash
chmod +w /etc/sudoers
```

编辑`/etc/sudoers`，取消该行注释：

```bash
%wheel ALL=(ALL) ALL
```

删除文件写入权限，使文件仅可读：

```bash
chmod -w /etc/sudoers
```

1. 安装OpenSSH

```bash
pacman -S openssh
```

设置SSH开机启动：

```bash
systemctl enable sshd && systemctl start sshd
```

1. 安装桌面环境

安装NVIDIA独显驱动：

```bash
pacman -S nvidia nvidia-utils
```

安装****Display Manager：****

```bash
pacman -S sddm
```

设置开机自启：

```bash
systemctl enable sddm
```

安装KDE：

```bash
pacman -S plasma kde-applications packagekit-qt5
```

安装中文字体：

```bash
pacman -S ttf-sarasa-gothic noto-fonts-cjk
```

1. 添加ArchLinuxCN源

```bash
vim /etc/pacman.conf
```

去掉`[multilib]`一节中两行的注释，来开启 32 位库支持

并在结尾添加如下内容：

```bash
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

修改后的文件末尾如下：

```bash
[multilib]
Include = /etc/pacman.d/mirrorlist
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

同步并安装`archlinuxcn-keyring` ：

[GitHub - archlinuxcn/archlinuxcn-keyring: ArchlinuxCN repo developer's gpg key](https://github.com/archlinuxcn/archlinuxcn-keyring)

```bash
pacman -Syu && pacman -S archlinuxcn-keyring
```

1. 重启

```bash
reboot
```