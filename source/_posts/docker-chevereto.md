---
title: 通过 Docker 搭建 Chevereto 图床
date: 2020-09-16 20:04:06
categories: [Docker]
tags: [Docker]
---

Chevereto 是一套基于 PHP 构建，易于安装和配置使用的开源在线图片存储分享服务系统

结合上篇 [通过 Docker 搭建 Typecho 详细教程](https://blog.csdn.net/sculpta/article/details/108292853)，通过 Docker Compose 编排 Mysql、PHP、Nginx 容器，同时部署 Typecho 和 Chevereto

<!-- more -->

## 1. 构建 PHP 镜像

Dockerfile 内容如下所示：

```dockerfile
FROM php:7.2.3-fpm
LABEL maintainer="tsund" \
    email="tsund@qq.com" \
    version="7.2.3-fpm"

RUN apt-get update \
    && apt-get install -y libgd-dev libzip-dev \
    && apt-get clean && rm -rf /tmp/* && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-png-dir=/usr/include \
    && docker-php-ext-install gd pdo pdo_mysql mysqli zip

COPY ./php.ini /usr/local/etc/php/conf.d/
```

可通过以上 Dockerfile 自行构建，构建方法如下。亦可直接使用我构建好的镜像 [tsund/php:7.2.3-fpm](https://hub.docker.com/r/tsund/php)

1. 下载 [GitHub 仓库](https://github.com/shink/dockerfiles/tree/master/php) 中的 `7.2.3-fpm` 文件夹，cd 到该文件夹下，执行以下命令构建镜像

```shell
docker build username/repo:tag .
```

2. push 到 Docker Hub

```shell
docker push username/repo:tag
```

## 2. 配置

目录结构如下：

```
[root@shenke web]# tree -L 1
.
├── docker-compose.yml
├── html
├── mysql
├── mysql.env
├── nginx
└── ssl

4 directories, 2 files
```

### 2.1 配置 Nginx

编写图床页面的配置文件，内容如下所示：

```nginx
server {
    listen 443 ssl;
    server_name img.tsund.cn;

    root /var/www/html/chevereto;
    index index.php;

    access_log /var/log/nginx/typecho_access.log main;

    ssl_certificate /var/www/ssl/img_tsund_cn.crt;
    ssl_certificate_key /var/www/ssl/img_tsund_cn.key;
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location ~ .*\.php(\/.*)*$ {
        fastcgi_pass   php:9000;
        fastcgi_index  index.php;
        # fastcgi_connect_timeout 60s;
        # fastcgi_send_timeout 60s;
        # fastcgi_read_timeout 60s;
        fastcgi_param  PATH_INFO $fastcgi_path_info;
        fastcgi_param  PATH_TRANSLATED $document_root$fastcgi_path_info;
        fastcgi_param  SCRIPT_NAME $fastcgi_script_name;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }

    # Chevereto NGINX generated rules for https://img.tsund.cn/

    # Context limits
    client_max_body_size 20M;

    # Disable access to sensitive files
    location ~* /(app|content|lib)/.*\.(po|php|lock|sql)$ {
    deny all;
    }

    # Image not found replacement
    location ~ \.(jpe?g|png|gif|webp)$ {
        log_not_found off;
        error_page 404 /content/images/system/default/404.gif;
    }

    # CORS header (avoids font rendering issues)
    location ~* /.*\.(ttf|ttc|otf|eot|woff|woff2|font.css|css|js)$ {
    add_header Access-Control-Allow-Origin "*";
    }

    # Pretty URLs
    location / {
    index index.php;
    try_files $uri $uri/ /index.php$is_args$query_string;
    }

    # END Chevereto NGINX rules

}
```

### 2.2 编写 docker-compose.yml

内容参考如下:

```yaml
version: "3"

services:
  nginx:
    image: nginx
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    restart: always
    volumes:
      - ./html:/var/www/html
      - ./ssl:/var/www/ssl
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - php
    networks:
      - web

  php:
    image: tsund/php:7.2.3-fpm
    container_name: php
    restart: always
    ports:
      - "9000:9000"
    volumes:
      - ./html:/var/www/html
    environment:
      - TZ=Asia/Shanghai
    depends_on:
      - mysql
    networks:
      - web

  mysql:
    image: mysql:5.7
    container_name: mysql
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

> 以上内容详解可参考 [通过 Docker 搭建 Typecho 详细教程](https://blog.csdn.net/sculpta/article/details/108292853)

## 3. 启动容器

在存放目录下，执行以下命令启动容器

```shell
docker-compose up -d
```

之后，浏览器进入图床页面开始配置即可