---
title: 搭建 Hadoop 集群详细教程
date: 2020-08-06 21:55:14
categories: [Big Data]
tags: [Hadoop, Big Data, 环境安装]
---

## 1. 准备工作

### 1.1 环境

- Centos 7
- JDK 1.8
- Hadoop 2.10.0

<!-- more -->

### 1.2 集群部署规划

<!--
|       |      hadoop1       |           hadoop2            |           hadoop3           |
| :---: | :----------------: | :--------------------------: | :-------------------------: |
| HDFS  | NameNode, DataNode |           DataNode           | SecondaryNameNode, DataNode |
| Yarn  |    NodeManager     | ResourceManager, NodeManager |         NodeManager         |
-->

<table style="margin:0 auto;text-align:center;">

  <tr>
    <th></th>
	  <th>hadoop1</th>
    <th>hadoop2</th>
    <th>hadoop3</th>  
  </tr >

  <tr >
	    <td rowspan="2">HDFS</td>
	    <td>NameNode</td>
	    <td></td>
      <td>SecondaryNameNode</td>
	</tr>

  <tr >
	    <td>DataNode</td>
	    <td>DataNode</td>
      <td>DataNode</td>
	</tr>

  <tr >
	    <td rowspan="2">Yarn</td>
	    <td></td>
	    <td>ResourceManager</td>
      <td></td>
	</tr>

  <tr >
	    <td>NodeManager</td>
	    <td>NodeManager</td>
      <td>NodeManager</td>
	</tr>

</table>

## 2. 配置主节点

### 2.1 创建虚拟机

1. 选择新建虚拟机
2. 选择典型类型
3. 选择稍后安装操作系统
4. 选择 Linux，Centos 7 64位
5. 命名虚拟机 hadoop1
6. 使用默认 20G 磁盘大小
7. 不修改虚拟机硬件配置，完成创建虚拟机
8. 选择创建好的虚拟机，点击编辑虚拟机
9. 移除 USB 控制器、声卡、打印机
10. 选择 CD/DVD，使用 ISO 映像文件，选择 ISO 文件位置
11. 开启并安装虚拟机
    - 时区选 Asia Shanghai
    - 需创建 root 用户

### 2.2 配置

1. 「编辑」->「虚拟网络编辑器」->「VMnet8」->「设置 NAT」，如下图

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/hadoop-cluster/1.png" width=900>
</p>

2. 虚拟机网络配置选择 NAT 模式

3. 配置静态 ip

切换到 root 用户

```shell
su root
```

编辑配置文件

```shell
vi /etc/sysconfig/network-scripts/ifcfg-ens32
```

> 也有可能是 eth0、ens33 等，跟 Centos 版本有关

配置文件内容如下，其中需要修改 `BOOTPROTO` 字段值为 `static`；`ONBOOT` 字段值为 `yes`，表示开机启动网络；`IPADDR` 字段为 ip 地址，需与 NAT 子网 ip 在同一网段；`GATEWAY` 字段为网关，需与 NAT 网关相同

```
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens32
UUID=4d0b744b-8ebf-4c75-b35c-324d9f671ce6
DEVICE=ens32
ONBOOT=yes
IPADDR=192.168.144.101
GATEWAY=192.168.144.2
DNS1=8.8.8.8
DNS2=8.8.4.4
```

重启网络

```shell
systemctl restart network
```

查看 ip

```shell
ip addr
```

4. 关闭防火墙

```shell
systemctl stop firewalld.service
systemctl disable firewalld.service
systemctl status firewalld
```

5. 修改 hostname

```shell
echo hadoop1 > /etc/hostname
```

编辑文件

```shell
vi /etc/sysconfig/network
```

写入以下内容

```
NETWORKING=yes # 使用网络
HOSTNAME=hadoop1 # 设置主机名
```

6. 配置 Host

```shell
vi /etc/hosts
```

追加以下内容

```
192.168.144.101 hadoop1
192.168.144.102 hadoop2
192.168.144.103 hadoop3
```

8. 重启

```shell
reboot
```

9. 切换回普通用户

```shell
su shenke
```

创建安装目录

```shell
sudo mkdir /opt/module
```

修改安装目录所有者

```shell
sudo chown shenke:shenke /opt/module
```

### 2.3 安装 JDK

1. 将在 `/tmp` 目录下的 `jdk-8u261-linux-x64.tar.gz` 解压

```shell
tar -zxvf jdk-8u261-linux-x64.tar.gz
```

2. 移动到 `/opt/module` 目录下，并重命名为 `jdk`

```shell
mv jdk1.8.0_261 /opt/module/jdk
```

3. 配置环境变量

```shell
sudo vi /etc/profile
```

追加以下内容

```profile
# JAVA_HOME
export JAVA_HOME=/opt/module/jdk
export PATH=$PATH:$JAVA_HOME/bin
```

使环境变量生效

```shell
source /etc/profile
```

4. 验证是否安装成功

```shell
java -version
```

### 2.4 安装 Hadoop

1. 将在 `/tmp` 目录下的 `hadoop-2.10.0.tar.gz` 解压

```shell
tar -zxvf hadoop-2.10.0.tar.gz
```

2. 移动到 `/opt/module` 目录下，并重命名为 `hadoop`

```shell
mv hadoop-2.10.0 /opt/module/hadoop
```

3. 配置环境变量

```shell
sudo vi /etc/profile
```

追加以下内容

```profile
# HADOOP_HOME
export HADOOP_HOME=/opt/module/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
```

使环境变量生效

```shell
source /etc/profile
```

4. 验证是否安装成功

```shell
hadoop
```

### 2.5 安装其他包

```shell
sudo yum install -y net-tools rsync
```

## 3. 配置从节点

### 3.1 克隆虚拟机

先将 hadoop1 关机，「右键」->「管理」->「克隆」

1. 选择创建完整克隆

2. 修改虚拟机名称为 hadoop2

### 3.2 配置网络

如 2.2 中第 3 步，修改 `/etc/sysconfig/network-scripts/ifcfg-ens32` 文件中的 `IPADDR` 为 `192.168.144.102`，并删除 `UUID`

如 2.2 中第 5 步，修改 hostname 为 hadoop2

重复以上步骤，克隆一个 hadoop3 节点

### 3.3 测试

尝试能否 ping 通其他节点

```shell
ping hadoop2
```

## 4. 配置集群

### 4.1 设置 SSH 无密码登录

1. 生成公钥

```shell
ssh-keygen -t rsa
```

2. 分发公钥

```shell
ssh-copy-id hadoop1
ssh-copy-id hadoop2
ssh-copy-id hadoop3
```

在三个节点上重复以上命令

### 4.2 编写集群分发脚本 xsync

1. 在 hadoop1 的 `/home/user/bin` 目录下创建 `xsync` 文件

```shell
mkdir bin && touch bin/xsync
```

> 如果是 root 用户则可将脚本放在 `/usr/local/bin` 目录下

编辑脚本

```shell
vi bin/xsync
```

内容参考 [xsync.sh](https://github.com/shink/data/blob/master/script/shell/xsync.sh)，主要是通过以下命令实现文件同步，其中，`-r` 表示递归处理子目录，`-v` 表示以详细模式输出，`-l` 表示保留软链接，`--delete` 表示同步删除，`--ignore-errors` 表示即使出现 IO 错误也进行删除

```shell
rsync -rvl --delete --ignore-errors $directory/$file $user@$host:$directory
```

2. 赋予执行权限

```shell
chmod 777 bin/xsync
```

3. 使用

```shell
xsync $file

# 例如
xsync /home/shenke/bin
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/hadoop-cluster/2.png" width=650>
</p>

## 5. 配置集群

配置文件均在 hadoop 安装目录下的 `etc/hadoop` 目录下

### 5.1 核心配置文件

1. 编辑 `core-site.xml`

```shell
vi core-site.xml
```

在 `configuration` 标签中写入以下内容

```xml
<configuration>

  <!-- 指定 HDFS 中 NameNode 的地址 -->
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop1:9000</value>
  </property>

  <!-- 指定 Hadoop 运行时产生文件的存储目录 -->
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/opt/module/hadoop/data/tmp</value>
  </property>

</configuration>
```

2. 创建存储目录

```shell
mkdir -p /opt/module/hadoop/data/tmp
```

### 5.2 HDFS 配置文件

1. 配置 `hadoop-env.sh`

```shell
vi hadoop-env.sh
```

在文件末尾追加以下内容

```profile
export JAVA_HOME=/opt/module/jdk
```

2. 配置 `hdfs-site.xml`

```shell
vi hdfs-site.xml
```

在 `configuration` 标签中写入以下内容

```xml
<configuration>

  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>

  <!-- 指定 Hadoop 辅助名称节点主机配置 -->
  <property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>hadoop3:50090</value>
  </property>

</configuration>
```

### 5.3 Yarn 配置文件

1. 配置 `yarn-env.sh`

```shell
vi yarn-env.sh
```

在文件末尾追加以下内容

```profile
export JAVA_HOME=/opt/module/jdk
```

2. 配置 `yarn-site.xml`

```shell
vi yarn-site.xml
```

在 `configuration` 标签中写入以下内容

```xml
<configuration>

  <!-- Reducer 获取数据的方式 -->
  <property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
  </property>

  <!-- 指定 YARN 的 ResourceManager 的地址 -->
  <property>
		<name>yarn.resourcemanager.hostname</name>
		<value>hadoop2</value>
  </property>

</configuration>
```

### 5.4 MapReduce 配置文件

1. 配置 `mapred-env.sh`

```shell
vi mapred-env.sh
```

在文件末尾追加以下内容

```profile
export JAVA_HOME=/opt/module/jdk
```

2. 配置 `mapred-site.xml`

```shell
cp mapred-site.xml.template mapred-site.xml && vi mapred-site.xml
```

在 `configuration` 标签中写入以下内容

```xml
<configuration>

  <!-- 指定 MapReduce 运行在 Yarn 上 -->
  <property>
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
  </property>

</configuration>
```

### 5.5 配置 slaves

编辑 `slaves`

```shel
vi slaves
```

写入以下内容

```
hadoop1
hadoop2
hadoop3
```

### 5.6 同步配置文件

```shell
xsync /opt/module/hadoop
```

## 6. 启动集群

在 hadoop 安装目录下

1. 格式化

```shell
bin/hdfs namenode -format
```

> 如果需要重新格式化 NameNode，需要先将 `data/tmp` 和 `logs`下的文件全部删除

2. 启动 HDFS

```shell
sbin/start-dfs.sh
```

3. 启动 Yarn

```shell
sbin/start-yarn.sh
```

> **注意**：需在 ResouceManager 所在节点启动 Yarn，本例中在 hadoop2 中启动

4. 查看进程

```shell
jps
```

5. 查看 web 端

- NameNode: [hadoop1:50070](http://192.168.144.101:50070/)
- SecondaryNameNode: [hadoop3:50090](http://192.168.144.103:50090/)

6. 停止 HDFS

```shell
sbin/stop-dfs.sh
```

7. 停止 Yarn

```shell
sbin/stop-yarn.sh
```

## 7. 编写群起脚本

1. 启动和关闭脚本

同样是在 `/home/shenke/bin` 目录下，新建并编辑脚本

```shell
vi ~/bin/hdp
```

内容参考 [hadoop.sh](https://github.com/shink/data/blob/master/script/shell/hadoop.sh)

2. 查看进程脚本

新建并编辑脚本

```shell
vi ~/bin/xcall
```

内容参考 [xcall.sh](https://github.com/shink/data/blob/master/script/shell/xcall.sh)

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/hadoop-cluster/3.png" width=1000>
</p>

## 8. HDFS 测试

1. 上传文件

上传一个小文件到根目录

```shell
bin/hdfs dfs -put /home/shenke/bin/xsync /
```

上传一个大文件到根目录

```shell
bin/hdfs dfs -put /tmp/hadoop-2.10.0.tar.gz /
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/hadoop-cluster/4.png" width=900>
</p>

2. 查看文件存储路径

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/hadoop-cluster/5.png" width=900>
</p>
