---
title: 搭建 Kafka 集群详细教程
date: 2020-08-07 22:03:39
categories: [Big Data]
tags: [Kafka, Big Data, 环境安装]
---

下面以 [搭建 Zookeeper 集群详细教程](https://blog.csdn.net/sculpta/article/details/107864846) 中搭建的 zookeeper 集群为例

<!-- more -->

## 1. 安装 Kafka

1. 将在 `/tmp` 目录下的 `kafka_2.11-2.4.1.tgz` 解压

```shell
tar -zxvf kafka_2.11-2.4.1.tgz
```

2. 移动到 `/opt/module` 目录下，并重命名为 `kafka`

```shell
mv kafka_2.11-2.4.1 /opt/module/kafka
```

3. 配置环境变量

```shell
sudo vi /etc/profile
```

追加以下内容

```profile
# KAFKA_HOME
export KAFKA_HOME=/opt/module/kafka
export PATH=$PATH:$KAFKA_HOME/bin
```

使环境变量生效

```shell
source /etc/profile
```

> 还需分别在其他节点手动配置环境变量

## 2. 配置集群

### 2.1 配置 server.properties

在 Kafka 安装目录下，编辑 `config/server.properties` 文件

```shell
vi config/server.properties
```

修改以下内容

```
broker.id=0
log.dirs=/opt/module/kafka/logs
listeners=PLAINTEXT://hadoop1:9092
zookeeper.connect=hadoop1:2181,hadoop2:2181,hadoop3:2181
```

> **注意**：`broker.id` 须为全局唯一的 int 值，在本例中，hadoop1 为 0，hadoop2 为 1，hadoop3 为 2；`listeners` 也要与所在节点对应

### 2.2 修改生产者配置文件

编辑 `config/producer.properties`

```shell
vi config/producer.properties
```

修改以下内容

```
bootstrap.servers=hadoop1:9092,hadoop2:9092,hadoop3:9092
```

### 2.3 修改消费者配置文件

编辑 `config/consumer.properties`

```shell
vi config/consumer.properties
```

修改以下内容

```
bootstrap.servers=hadoop1:9092,hadoop2:9092,hadoop3:9092
```

### 2.4 同步文件

```shell
xsync /opt/moudle/kafka
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/kafka-cluster/1.png" width=650>
</p>

> 脚本内容可参考 [xsync.sh](https://github.com/shink/data/blob/master/script/shell/xsync.sh)

在其他节点修改 `config/server.properties` 中的 `broker.id` 和 `listeners`

## 3. 启动集群

1. 启动 Kafka 集群前需要先启动 Zookeeper

```shell
zookeeper start
```

在每个节点分别启动 Kafka 

```shell
bin/kafka-server-start.sh -daemon config/server.properties
```

2. 关闭集群

在每个节点分别关闭 Kafka 

```shell
bin/kafka-server-stop.sh
```

## 4. 编写群起脚本

在 `/home/shenke/bin` 目录下，新建并编辑脚本

```shell
vi ~/bin/kafka
```

内容参考 [kafka.sh](https://github.com/shink/data/blob/master/script/shell/kafka.sh)

使用

```shell
# 开启
kafka start

# 停止
kafka stop
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/kafka-cluster/2.png" width=650>
</p>

## 5. 集群测试

### 5.1 创建主题

创建一个副本数为 1、分区数为 3、名为 `test` 的主题

```shell
bin/kafka-topics.sh --zookeeper hadoop1:2181 --create --replication-factor 1 --partitions 3 --topic test
```

### 5.2 查看主题

1. 列出所有主题

```shell
bin/kafka-topics.sh --zookeeper hadoop1:2181 --list
```

2. 查看某个主题的详情

```shell
bin/kafka-topics.sh --zookeeper hadoop1:2181 --describe --topic test
```

### 5.3 删除主题

```shell
bin/kafka-topics.sh --zookeeper hadoop1:2181 --delete --topic test
```

### 5.4 生产消息

在 hadoop1 中生产消息

```shell
bin/kafka-console-producer.sh --broker-list hadoop1:9092 --topic test
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/kafka-cluster/3.png" width=900>
</p>

### 5.5 消费消息

在 hadoop2 中消费消息

```shell
bin/kafka-console-consumer.sh --bootstrap-server hadoop2:9092 --topic test
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/kafka-cluster/4.png" width=900>
</p>
