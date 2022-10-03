---
title: Docker 入门及常用命令
date: 2020-02-21 12:40:06
categories: [Docker]
tags: [Docker]
---

## 1. Docker 基础知识

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/docker-introduction/1.jpg" width="1000">
</p>

<p align="center"><i>Build, Ship and Run Any App, Anywhere.</i></p>


Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的镜像中，然后发布到任何流行的 Linux 或 Windows 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口

<!-- more -->

Docker 的三个重要概念：

- Image（镜像）
- Container（容器）
- Repository（仓库）

其中，Image 是 Docker 的核心，它可以看作是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境变量、用户等）。镜像不包含任何动态数据，其内容在构建之后也不会被改变

Container，顾名思义，它就是一个容器，其中装的就是 Image 镜像，它与 Image 的关系就好比是面向对象中的实例和类，Image 是静态的定义，Container 是 Image 运行时的实例。Image 说白了只是一个文件系统，而装载 Image 的 Container 可以被创建、启动、停止、删除、暂停等

Repository 是一个代码控制中心，用来保存镜像。每个仓库可以包含多个 Tag（标签），每个 Tag 对应一个镜像。通常，一个 Repository 会包含同一个软件不同版本的 Image，而 Tag 就常用于对应该软件的各个版本。我们可以通过 `<仓库名>:<标签>` 的格式来指定具体是这个软件哪个版本的 Image。如果不给出 Tag，将以 latest 作为默认标签

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/docker-introduction/2.png" width="900">
</p>

## 2. Docker 基本命令

### 2.1 容器管理

- `docker run` ：通过镜像创建一个新的容器并运行一个命令

```shell
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

> 常用 OPTIONS：
> - `-d` ：后台运行 Container
> - `-i` ：以交互模式运行 Container，通常与 -t 同时使用
> - `-t` ：为 Container 重新分配一个伪输入终端，通常与 -i 同时使用（即 -it）
> - `-p` ：指定 Container 与主机的端口映射，格式为：**主机(宿主)端口:容器端口**
> - `--name="container-name"`: 为容器指定一个名称

- `docker start` ：启动一个或多个已经被停止的容器

```shell
docker start CONTAINER
```

- `docker stop` ：停止一个运行中的容器

```shell
docker stop CONTAINER
```

- `docker restart` ：重启一个运行中的容器

```shell
docker restart CONTAINER
```

- `docker rm` ：删除一个或多个容器

> 常用 OPTIONS：
> - `-f` ：强制删除 Container

删除所有已停止的 Container

```shell
docker rm $(docker ps -a -q)
```

- `docker exec` ：在指定运行的容器中执行操作，exit 后容器不会停止运行

```shell
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

常用 -it 进入容器并执行命令（<u>在伪终端中输入 `exit` 退出</u>）

```shell
docker exec -it CONTAINER /bin/bash
```

### 2.2 容器操作

- `docker ps` ：查看正在运行的容器

> 常用 OPTIONS：
> - `-a` ：列出所有 Container，包括未运行的
> - `-q` ：只列出 Container ID
> - `-s` ：显示总的文件大小

- `docker inspect` ：获取指定容器/镜像的元数据，返回内容格式默认为 json

```shell
docker inspect CONTAINER
```

- `docker port` ：列出指定容器的端口映射

```shell
docker port CONTAINER
```

- `docker top` ：查看指定运行容器中的进程信息，支持 ps 命令参数

```shell
docker top [OPTIONS] CONTAINER [ps OPTIONS]
```

### 2.3 镜像管理

- `docker images` ：列出本地镜像

> 常用 OPTIONS：
> - `-a` ：列出本地所有的镜像（含中间映像层，默认情况下，过滤掉中间映像层）
> - `-q` ：列出本地镜像 ID

- `docker rmi` ：删除本地一个或多个镜像

```shell
docker rmi [OPTIONS] IMAGE [IMAGE...]
```

> 常用 OPTIONS：
> - `-f` ：强制删除 Image

- `docker tag` ：标记本地镜像，将其归入某一仓库

```shell
docker tag [OPTIONS] IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]
```

- `docker build` ：使用 Dockerfile 创建镜像

```shell
docker build [OPTIONS] PATH | URL | -
```

> 常用 OPTIONS：
> - `-t` ：镜像的名字及标签，通常 name:tag 或者 name 格式，可以在一次构建中为一个镜像设置多个标签
> - `-f` ：指定要使用的 Dockerfile 路径

### 2.4 仓库操作

- `docker pull` ：从镜像仓库中拉取或者更新指定镜像

```shell
docker pull ubuntu
```

- `docker search` ：从 Docker Hub 中查找镜像

```shell
docker search [OPTIONS] TERM
```

> 常用 OPTIONS：
> - `--automated` ：只列出 automated build类型的镜像
> - `--no-trunc` ：显示完整的镜像描述
> - `-s` ：列出 star 数不小于指定值的镜像

