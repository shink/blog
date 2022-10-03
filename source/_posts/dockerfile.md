---
title: Docker 入门之 Dockerfile
date: 2020-02-21 12:06:35
categories: [Docker]
tags: [Docker]
---

## 1. Dockerfile

通常使用 Dockerfile 创建镜像，Dockerfile是一个 Docker 镜像的描述文件，其内部包含了一条条的指令，每一条指令构建一层，每一条指令的内容，就是描述该层应当如何构建。每条指令按顺序依次执行

<!-- more -->

## 2. 指令详解

### 2.1 FROM

指定基础镜像，并且必须是 Dockerfile 的第一条指令，如果不以任何镜像为基础，那么写法为：`FROM scratch`

```
FROM <image>
FROM <image>:<tag>
FROM <image>:<digest>

# 例如
FROM scratch
FROM centos:6
FROM ubuntu
```

### 2.2 MAINTAINER

指定作者信息

```
MAINTAINER <name>

# 例如
MAINTAINER shenke <shenkebug@gmail.com>
```

**注**：新版 docker 建议使用 `LABEL` 声明

### 2.3 LABEL

为镜像指定标签

```
LABEL <key>=<value> <key>=<value> <key>=<value> ···

# 例如
# 内容过长可用 \ 换行
LABEL maintainer="shenke" \
version="1.0" \
desc="This is \
a short description."
```

### 2.4 RUN

构建镜像时执行的 Shell 命令

```
RUN <command>
RUN ["executable", "param1", "param2"]

# 例如
RUN sh run.sh
RUN ["sh", "run.sh"]
RUN ["yum", "install", "nginx"]
```

### 2.5 CMD

启动容器时执行的 Shell 命令

```
CMD command param1 param2
CMD ["param1","param2"]
CMD ["executable","param1","param2"]

# 例如
CMD echo $HOME
CMD ["sh", "run.sh"]
CMD [ "sh", "-c", "echo $HOME"]
```

> `RUN` 与 `CMD` 的区别：   
> - `RUN` 指定的是构建镜像时要执行的命令，即 `docker build` 过程中要执行的命令  
> - `CMD` 指定的是启动容器时要执行的命令，即 `docker run` 时要执行的命令。`CMD` 指令的首要目的在于为启动的容器指定默认要运行的程序，程序运行结束，容器也就结束。**注意**：`CMD` 指令指定的程序可被 `docker run` 命令行参数中指定要运行的程序所覆盖

### 2.6 ENTRYPOINT

启动容器时执行的 Shell 命令

```
ENTRYPOINT command param1 param2
ENTRYPOINT ["executable", "param1", "param2"]  
```

> `ENTRYPOINT` 与 `CMD` 的异同：
> - 都是在启动容器时执行
> - `ENTRYPOINT` 启动的程序不会被 `docker run` 命令行指定的参数所覆盖，而且，这些命令行参数会被当作参数传递给 `ENTRYPOINT` 指令指定的程序

### 2.7 EXPOSE

暴露容器端口给外部

```
EXPOSE <port>/<tcp/udp>

# 例如
EXPOSE 80/tcp 443/tcp
```

### 2.8 ADD

将主机文件或目录拷贝到镜像中，**URL 会自动下载，压缩包会自动解压**

```
ADD <src> ··· <dest>
ADD ["<src>", ··· "<dest>"]

# 例如
ADD nginx-1.16.1.tar.gz /usr/local    # 将 nginx 压缩包解压到 /usr/local 目录下，即 /usr/local/nginx-1.16.1
ADD https://xxx.com/html.tar.gz /var/www/html    # 下载压缩包并解压到 /var/www/html 目录下
```

> **注意**：
> - src 为一个目录的时候，会自动把目录下的文件复制过去，目录本身不会复制
>  - 如果 src 为多个文件，dest 必须是一个目录

### 2.9 COPY

将主机文件或目录拷贝到镜像中，**同 `ADD` 类似，只是不支持自动下载和解压**

```
ADD <src> ··· <dest>
ADD ["<src>", ··· "<dest>"]
```

### 2.10 ENV

设置环境变量

```
ENV <key> <value>
ENV <key>=<value> ···

# 例如
ENV JAVA_HOME /usr/local/jdk
ENV MYSQL_ROOT_PASSWORD=123456 VERSION=1.0 NAME="Hello docker"
```

### 2.11 WORKDIR

为 `RUN`、`CMD`、`ENTRYPOINT` 以及 `COPY` 和 `ADD` 设置工作目录

```
WORKDIR /path/workdir

# 例如
WORKDIR /root
```

### 2.12 USER

设置启动容器的用户

```
USER <user>[:<usergroup>]
USER <UID>[:<UID>]

# 例如
USER root
```

### 2.13 VOLUME

实现文件挂载功能，可以将主机目录挂载到容器中，一般的使用场景为需要持久化存储数据时

```
VOLUME ["/data"]
```

### 2.14 ARG

在构建镜像时，传入一些参数

```
ARG <name>[=<default value>]

# 例如
ARG version=1.0
ARG user
USER $user
```

在 `docker build` 构建镜像的时候，使用 `--build-arg` 来指定参数，若未指定参数则会使用默认值，若未指定默认值就会报错

```
docker build --build-arg user=root -t myimage:1.0 .
```

### 2.15 HEALTHCHECK

健康检查，即指定如何测试容器以检查它是否仍在工作

```
HEALTHCHECK [OPTIONS] CMD command
HEALTHCHECK NONE    # 在基础镜像中取消健康检查命令

# 例如
HEALTHCHECK --interval=5m --timeout=3s --start-period=0s --retries=3 \
    CMD curl -f http:/localhost/ || exit 1
```

> OPTIONS： 
> - `--interval=DURATION` ：每隔多长时间探测一次，默认30秒
> - `--timeout=DURATION` ：服务响应超时时长，默认30秒
> - `--start-period=DURATION` ：服务启动多久后开始探测，默认0秒
> - `--retries=N` ：认为检测失败几次为宕机，默认3次

> 返回值：
> - `0` ：容器健康，随时可以使用
> - `1` ：容器不健康，无法使用
> - `2` ：保留值
