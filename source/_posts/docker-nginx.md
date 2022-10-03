---
title: Nginx 的 Docker 镜像使用教程
date: 2020-07-21 20:51:02
categories: [Docker]
tags: [Docker]
---

## 官方镜像说明

用户可以将宿主主机上的网页文件、config 文件挂载到官方镜像中

官方镜像中 nginx 的安装目录为：`/etc/nginx`，配置文件目录为：`/etc/nginx/config.d/default.conf`，网页文件目录为：`/usr/share/nginx/html`

可以通过下面命令进入容器查看

```docker
docker exec -it CONTAINER /bin/bash
```

> 官方镜像地址：[https://hub.docker.com/_/nginx](https://hub.docker.com/_/nginx)

<!-- more -->

## 使用教程

1. 拉取镜像

```docker
docker pull nginx
```

2. 运行容器，这里将 `/data/web` 挂载到容器中的 `/usr/share/nginx/html`

```docker
docker run -d --name nginx -p 80:80 -p 443:443 -v /data/web:/usr/share/nginx/html nginx
```

其中，各参数含义如下：

> `-d`: 表示使容器在后台运行    
> `--name`: 指定容器名称    
> `-p`: 指定容器与宿主主机的端口映射，格式为：宿主主机端口:容器端口     
> `-v`: 指定容器与宿主主机的文件挂载，格式为：宿主主机目录:容器目录

3. 将容器中的 nginx 目录拷贝到 `/usr/local/` 目录下

```docker
docker cp nginx:/etc/nginx /usr/local/
```

4. 停止并删除容器

```docker
docker stop nginx

docker rm nginx
```

> **注意**：以上步骤必须执行，因为容器的运行依赖 `/etc/nginx`，如果将一个空文件目录挂载到该目录，容器将无法启动，所以需要先将该文件目录拷贝到主机中，再挂载上去

5. 重新运行一个新容器，这里将 `/usr/local/nginx` 挂载到容器中的 `/etc/nginx`

```docker
docker run -d --name nginx -p 80:80 -p 443:443 -v /usr/local/nginx:/etc/nginx -v /data/web:/usr/share/nginx/html nginx
```

6. 编辑配置文件

在宿主主机中，编辑 `/usr/local/nginx/config.d/default.conf`，修改网页文件路径，例如网页文件存放在宿主主机中的 `/data/web/homepage`，主页为 `/data/web/homepage/index.html`，由于将 `/data/web` 挂载到了 `/usr/share/nginx/html`，故配置文件中应该写为

```nginx
location / {
    root   /usr/share/nginx/html/homepage;
    index  index.html index.htm;
}
```

7. HTTPS 配置

在 `/usr/local/nginx/config.d/default.conf` 中追加以下内容：

```nginx
server {
    listen 443 ssl http2;
    server_name  tsund.me;

    ssl                      on;
    ssl_certificate          /usr/share/nginx/html/ssl/tsund_me/tsund.pem;
    ssl_certificate_key      /usr/share/nginx/html/ssl/tsund_me/tsund.key;

    ssl_session_timeout  5m;

    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers   on;

    location / {
        root   /usr/share/nginx/html/homepage;
        index  index.html index.htm;
    }
}
```

其中，`server_name` 为域名，`ssl_certificate` 为 ssl 证书的路径，`ssl_certificate_key` 为 ssl 证书私钥的路径

8. 重启容器

配置完后，需要重启容器

```docker
docker restart nginx
```

至此，打开 `https://your-domain.com` 就可以看到网页内容了
