---
title: 阿里云 CentOS 搭建 Hexo 详细教程
date: 2020-02-18 19:31:31
categories: [Blog]
tags: [Hexo, Blog]
---

本文将详细介绍如何在 CentOS 7 搭建 hexo 博客

<!-- more -->

## 1. 安装 Git

这里使用压缩包的方式进行安装，尽管一键 `yum install -y` 更加简单粗暴，但是这样会把文件打散，使用压缩包的方式安装还能顺便学习许多命令和配置

安装依赖库和编译工具

```shell
yum install -y curl-devel expat-devel gettext-devel openssl-devel zlib-devel gcc perl-ExtUtils-MakeMaker
```

下载 git 最新版本（`tmp` 目录用来存放临时文件，服务器重启后会自动清除）

```shell
cd /tmp && wget https://www.kernel.org/pub/software/scm/git/git-2.25.2.tar.gz
```

解压

```shell
tar -zvxf git-2.25.2.tar.gz
```

编译

```shell
cd git-2.25.2 && make all prefix=/usr/local/git
```

安装

```shell
make install prefix=/usr/local/git
```

配置环境变量

```shell
echo 'export PATH=$PATH:/usr/local/git/bin' >> /etc/bashrc
```

使环境变量配置生效

```shell
source /etc/bashrc
```

查看版本

```shell
git version
```

配置用户名和邮箱

```shell
git config --global user.name "你的账号"
git config --global user.email "你的邮箱"
```

查看配置信息

```shell
git config -l
```

生成 ssh 密钥

```shell
ssh-keygen -t rsa -C "你的 github 邮箱"
```

打开 `/root/.ssh/id_rsa.pub` ，将其中内容添加到 GitHub 的 SSH Key

尝试使用 ssh clone 你的仓库

```shell
git clone git@github.com:yourgithubid/repo.git
```

如果 clone 成功则说明 ssh 设置成功

## 2. 安装 Nodejs

这里同样使用压缩包的方式进行安装

下载 nodejs 最新版本

```shell
cd /tmp && wget https://nodejs.org/dist/v12.16.0/node-v12.16.0-linux-x64.tar.xz
```

解压

```shell
tar xvJf node-v12.16.0-linux-x64.tar.xz
```

将 `/tmp/node-v12.16.0-linux-x64` 文件夹移动到 `/usr/local` 目录下，并重命名为 `node`

```shell
mv node-v12.16.0-linux-x64 /usr/local/node
```

添加软连接到 /bin 目录

```shell
ln -s /usr/local/node/bin/node /bin/node

ln -s /usr/local/node/bin/npm /bin/npm
```

配置环境变量

```shell
echo 'export PATH=/usr/local/node/bin:$PATH' >> /etc/profile
```

使环境变量配置生效

```shell
source /etc/profile
```

查看 nodejs 和 npm 版本

```shell
node -v

npm -v
```

如果正常显示，则安装成功

## 3. 安装 Hexo

设置 npm 源为淘宝源

```shell
npm config set registry https://registry.npm.taobao.org
```

安装 hexo

```shell
npm install -g hexo-cli
```

查看版本

```shell
hexo -v
```

## 4. 创建 Hexo 博客

这里将博客放在 `/data/blog` 目录下

创建文件夹

```shell
mkdir -p /data/blog && cd /data/blog
```

初始化 hexo

```shell
hexo init
```

生成 hexo 页面

```shell
hexo g
```

此时会在目录下生成一个 `public` 文件，其中的 `index.html` 就是博客的主页面

## 5. 安装 Nginx

这里同样使用压缩包的方式进行安装

安装依赖

```shell
yum install -y gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel
```

同样在 `/tmp` 目录下，下载 nginx 最新版本

```shell
cd /tmp && wget http://nginx.org/download/nginx-1.16.1.tar.gz
```

解压

```shell
tar -zxvf nginx-1.16.1.tar.gz
```

编译

```shell
cd nginx-1.16.1 && ./configure --with-http_ssl_module
```

`--with-http_ssl_module` : 配置 ssl 模块

编译完后，会显示配置信息，默认将 nginx 安装到 `/usr/local/nginx`

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/aliyun-build-hexo/1.png" width="650">
</p>

安装

```shell
make && make install
```

nginx 的配置文件在 `/usr/local/nginx/conf` 目录下，编辑 `nginx.conf`，按 `i` 进入 `INSERT` 模式

```shell
vi /usr/local/nginx/conf/nginx.conf

# 保存并退出
:wq

# 退出但不保存
:q!
```

需在配置文件中修改监听的 `server_name` 为你的域名，以及 ssl 证书的目录和博客的目录

```nginx
server {
       listen       443 ssl;

       # 修改域名或ip
       server_name  blog.tsund.cn;
       
       # 修改ssl证书目录
       ssl_certificate      /data/ssl/blog_tsund_cn/chain.crt;
       ssl_certificate_key  /data/ssl/blog_tsund_cn/key.key;

       ssl_session_cache    shared:SSL:1m;
       ssl_session_timeout  10m;

       ssl_ciphers  ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
       ssl_prefer_server_ciphers  on;
       
       # 修改博客目录
       location / {
           root   /data/blog/public;
           index  index.html index.htm;
       }
    }
```

重启 nginx

```shell
cd /usr/local/nginx/sbin

./nginx -s reload

# 启动 nginx
./nginx

# 关闭 nginx
./nginx -s stop
```

访问博客地址，出现 hexo 界面

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/aliyun-build-hexo/2.png" width="1100">
</p>

接下来，就可以将 GitHub 的博客迁移到服务器了
