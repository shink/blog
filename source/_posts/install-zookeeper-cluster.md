---
title: 搭建 Zookeeper 集群详细教程
date: 2020-08-07 16:19:52
categories: [Big Data]
tags: [Zookeeper, Big Data, 环境安装]
---

下面以 [搭建 Hadoop 集群详细教程](https://blog.csdn.net/sculpta/article/details/107850280) 中搭建的 hadoop 集群为例

<!-- more -->

## 1. 安装 Zookeeper

1. 将在 `/tmp` 目录下的 `zookeeper-3.4.14.tar.gz` 解压

```shell
tar -zxvf zookeeper-3.4.14.tar.gz
```

2. 移动到 `/opt/module` 目录下，并重命名为 `zookeeper`

```shell
mv zookeeper-3.4.14 /opt/module/zookeeper
```

3. 配置环境变量

```shell
sudo vi /etc/profile
```

追加以下内容

```profile
# ZK_HOME
export ZK_HOME=/opt/module/zookeeper
export PATH=$PATH:$ZK_HOME/bin
```

使环境变量生效

```shell
source /etc/profile
```

> 还需分别在其他节点手动配置环境变量

## 2. 配置集群

### 2.1 配置节点编号

1. 在 Zookeeper 安装目录下创建 `data` 目录，并在该目录下创建 `myid` 文件

```shell
mkdir data && touch data/myid
```

2. 在 `myid` 中填写与节点对应的编号

```shell
echo 1 > data/myid
```

### 2.2 配置 zoo.cfg 文件

1. 重命名 `conf` 目录下的 `zoo_sample.cfg` 为 `zoo.cfg`

```shell
mv conf/zoo_sample.cfg conf/zoo.cfg
```

2. 编辑文件

```shell
vi conf/zoo.cfg
```

修改数据存储路径配置

```shell
dataDir=/opt/module/zookeeper/data
```

追加以下内容

```
server.1=hadoop1:2888:3888
server.2=hadoop2:2888:3888
server.3=hadoop3:2888:3888
```

### 2.3 同步文件

```shell
xsync /opt/moudle/zookeeper
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/zookeeper-cluster/1.png" width=750>
</p>

> 脚本内容可参考 [xsync.sh](https://github.com/shink/data/blob/master/script/shell/xsync.sh)

在其他节点修改 `myid` 与节点对应，如本例中，hadoop1 为 1，hadoop2 为 2，hadoop3 为 3

```shell
echo 2 > data/myid
```

## 3. 启动集群

在各个节点分别启动 Zookeeper

```shell
bin/zkServer.sh start
```

查看状态

```shell
bin/zkServer.sh status
```

停止 Zookeeper

```shell
bin/zkServer.sh stop
```

> 如果配置了环境变量的话，在任意位置使用 `zkServer.sh COMMAND` 即可

## 4. 编写群起脚本

在 `/home/shenke/bin` 目录下，新建并编辑脚本

```shell
vi ~/bin/zookeeper
```

内容参考 [zookeeper.sh](https://github.com/shink/data/blob/master/script/shell/zookeeper.sh)

使用

```shell
# 开启
zookeeper start

# 停止
zookeeper stop

# 查看状态
zookeeper status
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/zookeeper-cluster/2.png" width=800>
</p>
