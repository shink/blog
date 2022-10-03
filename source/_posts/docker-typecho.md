---
title: 通过 Docker 搭建 Typecho 详细教程
date: 2020-08-29 12:00:42
categories: [Docker]
tags: [Docker]
---

下面以 Centos 7 为例

<!-- more -->

## 1. 安装 Docker 和 Docker Compose

### 1.1 安装 Docker

安装依赖

```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
```

设置yum源

```shell
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```
	
查看所有仓库中所有docker版本

```shell
yum list docker-ce --showduplicates | sort -r
```

安装docker

```shell
yum install -y docker-ce
```

设置开机启动

```shell
systemctl enable docker
```

启动 Docker

```shell
systemctl start docker
```
	
查看版本

```shell
docker version
```
	
测试

```shell
docker pull ubuntu
```

### 1.2 安装 Docker Compose

下载

```shell
curl -L https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m) > /usr/bin/docker-compose
```

赋予执行权限

```shell
chmod +x /usr/bin/docker-compose
```

查看版本

```shell
docker-compose --version
```

## 2. 构建镜像

这里使用如下三个镜像

- nginx
- tsund/php:7.2.3-fpm
- mysql:5.7

其中 `nginx` 为官方最新镜像，`mysql:5.7` 为官方 5.7 镜像，`tsund/php:7.2.3-fpm` 的 Dockerfile 如下：

```dockerfile
FROM php:7.2.3-fpm
LABEL maintainer="tsund" \
      email="tsund@qq.com" \
      version="7.2.3"

RUN apt-get update \
    && docker-php-ext-install pdo_mysql \
    && echo "output_buffering = 4096" > /usr/local/etc/php/conf.d/php.ini
```

在官方镜像的基础上，添加了 `PDO_MYSQL`（如果使用 MySQL 作为 Typecho 的数据库，则需安装此扩展），并设置 buffer 为 4kb，即一个内存页

## 3. 配置

新建 `blog` 文件夹，其目录结构如下：

```
.
├── docker-compose.yml      Docker Compose 配置文件
├── mysql                   mysql 持久化目录
├── mysql.env               mysql 配置信息
├── nginx                   nginx 配置文件的持久化目录
├── ssl                     ssl 证书目录
└── typecho                 站点根目录
```

### 3.1 配置 docker-compose.yml

```yml
version: "3"

services:
  nginx:
    image: nginx
    ports:
      - "80:80"
      - "443:443"
    restart: always
    volumes:
      - ./typecho:/var/www/html
      - ./ssl:/var/www/ssl
      - ./nginx:/etc/nginx/conf.d
    depends_on:
      - php
    networks:
      - web

  php:
    image: tsund/php:7.2.3-fpm
    restart: always
    ports:
      - "9000:9000"
    volumes:
      - ./typecho:/var/www/html
    environment:
      - TZ=Asia/Shanghai
    depends_on:
      - mysql
    networks:
      - web

  mysql:
    image: mysql:5.7
    restart: always
    ports:
      - "3306:3306"
    volumes:
      - ./mysql/data:/var/lib/mysql
      - ./mysql/logs:/var/log/mysql
      - ./mysql/conf:/etc/mysql/conf.d
    env_file:
      - mysql.env
    networks:
      - web

networks:
  web:
```

其中

- `version` 指定 docker-compose 版本
- `image` 指定镜像名称
- `volumes` 指定文件挂载映射
- `ports` 指定端口映射
- `depends_on` 指定服务启动时的先后顺序，指定的服务会先于当前服务启动
- `networks` 指定容器连接的虚拟网络，连接在同一网络的服务可以使用服务名进行通信。version 3 不推荐使用 `--link`，使用 `network` 替代其功能，也更方便管理
- 一级标签的 `networks` 是虚拟网络的定义，可以指定网络类型和参数等，这里使用了默认的网络类型，参数部分留空即可

### 3.2 配置 nginx

在 `./nginx` 目录下新建 `default.conf` 文件，参考内容如下：

```nginx
server {
    listen       80;
    server_name  tsund.cn;
    rewrite ^(.*) https://tsund.cn$1 permanent;
}

server {
    listen 443 ssl http2 reuseport;
    server_name tsund.cn;

    root /var/www/html;
    index index.php;

    access_log /var/log/nginx/typecho_access.log main;

    ssl_certificate /var/www/ssl/tsund_cn.crt;
    ssl_certificate_key /var/www/ssl/tsund_cn.key;
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    if (!-e $request_filename) {
        rewrite ^(.*)$ /index.php$1 last;
    }

    location ~ .*\.php(\/.*)*$ {
        fastcgi_pass   php:9000;
        fastcgi_index  index.php;
        fastcgi_param  PATH_INFO $fastcgi_path_info;
        fastcgi_param  PATH_TRANSLATED $document_root$fastcgi_path_info;
        fastcgi_param  SCRIPT_NAME $fastcgi_script_name;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }
    
}
```

### 3.3 配置 mysql

`mysql.env` 参考内容如下：

```
# MySQL的root用户默认密码，这里自行更改
MYSQL_ROOT_PASSWORD=password
# MySQL镜像创建时自动创建的数据库名称
MYSQL_DATABASE=blog
# MySQL镜像创建时自动创建的用户名
MYSQL_USER=shenke
# MySQL镜像创建时自动创建的用户密码
MYSQL_PASSWORD=password
# 时区
TZ=Asia/Shanghai
```

## 4. 安装

### 4.1 编排容器

在 `blog` 目录下

```shell
docker-compose up -d
```

查看进程

```shell
docker-compose ps
```

### 4.2 安装 Typecho

编排成功后，浏览器输入 URL，进入 typecho 安装页面

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/docker-typecho/1.png" width=800>
</p>

> 需注意的是，数据库地址需填入 mysql 镜像的名称（与 `docker-compose.yml` 中的配置相对应），数据库名与 `mysql.env` 中创建的数据库名一致

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/08/docker-typecho/2.png" width=800>
</p>

> 若出现以上页面，只需按照提示在 `./typecho` 目录下新建 `config.inc.php` 文件，并写入内容即可

## 5. 博客迁移

迁移时只需将整个 `blog` 目录打包传输至安装有 Docker 和 Docker Compose 的新服务器，然后重新编排容器即可

```shell
docker-compose up -d
```

## 6. 参考资料

- [使用 Docker 搭建 Typecho 个人博客](https://blog.anguiao.com/archives/build-blog-with-docker.html)

- [Docker安装typecho](https://pjf.name/blogs/install-typecho-by-docker.html)

- [使用Docker搭建Caddy+Typecho个人博客网站](https://zhuanlan.zhihu.com/p/93839317)
