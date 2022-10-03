---
title: GitHub Actions 部署爬虫并定时发送邮件
date: 2020-02-02 11:22:40
categories: [GitHub]
tags: [GitHub, GitHub Actions, 爬虫]
---

本文将介绍如何在 GitHub Actions 上部署爬虫并定时发送邮件，<u>无需额外购买服务器</u>

## 1. GitHub Actions

GitHub Actions 是在 GitHub Universe 大会上发布的，被 Github 主管 Sam Lambert 称为 “再次改变软件开发” 的一款重磅功能（“*we believe we will once again revolutionize software development.*”）。于 2018 年 10 月推出，内测了一段时间后，于 2019 年 11 月 13 日正式上线

GitHub 会提供一个以下配置的服务器做为 runner：

- 2-core CPU
- 7 GB of RAM memory
- 14 GB of SSD disk space

（免费额度最多可以同时运行 20 个作业，心动了有木有💘）

GitHub Actions 是一个 `CI/CD（持续集成/持续部署）`工具，持续集成由很多操作组成，比如 **抓取代码**、**运行测试**、**登录远程服务器**、**发布到第三方服务** 等等。GitHub 把这些操作统称为 actions

<u>actions 是 GitHub Actions 的核心，简单来说，它其实就是一段可以执行的代码</u>，可以用来做很多事情。比如，你在 python 3.7 环境下写了一个 python 项目放到了 GitHub 上，但是考虑到其他用户的生产环境各异，可能在不同的环境中运行结果都不一样，甚至无法安装，这时你总不能在自己电脑上把所有的 python 环境都测试一遍吧

但是如果有了 GitHub Actions，你可以在 runner 服务器上部署一段 actions 代码来自动完成这项任务。你不仅可以指定它的操作系统（支持 Windows Server 2019、Ubuntu 18.04、Ubuntu 16.04 和 macOS Catalina 10.15），还可以指定触发时机、指定 python 版本、安装其他库等等

此外，它还可以用来做很多有趣的事，比如当有人向仓库里提交 issue 时，给你的微信发一条消息；爬取课程表，每天早上准时发到你的邮箱；当向 master 分支提交代码时，自动构建 Docker 镜像并打上标签发布到 Docker Hub 上 ……

慢慢的，你会发现很多操作在不同项目里面是类似的，完全可以共享。GitHub 也注意到了这一点，于是它允许开发者把每个操作写成独立的脚本文件，存放到代码仓库，使得其他开发者可以引用

> **`总而言之，GitHub Actions 就是为我们提供了一个高效易用的 CI/CD（持续集成/持续部署）工作流，帮助我们自动构建、测试、部署我们的代码`**

<!-- more -->

具体的用法可以参考这些资料：

- 阮一峰老师的一篇文章：[GitHub Actions 入门教程](http://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)

- GitHub Actions 中文文档：[GitHub Actions Documentation](https://help.github.com/cn/actions)

- GitHub Actions 官方市场：[Actions Marketplace](https://github.com/marketplace?type=actions)

熟悉了基本用法之后，本文将通过一个简单的爬虫例子，演示如何在 GitHub Actions 上部署爬虫，并定时发送邮件

完整代码可以从 GitHub 仓库 [shink/actions-bot](https://github.com/shink/actions-bot) 获取，里面包含了几个基于 GitHub Actions 的小机器人（<u>有福利哦</u> 😏）

## 2. 步骤

爬虫内容就不细说了，这里以一个特别简单的例子为例——爬取 CSDN 用户的 profile 信息，即 <https://blog.csdn.net/sculpta> 这个页面中左边一栏的访问量、排名等信息，并定时发送到邮箱

### 2.1 准备爬虫

可以先 star 并 fork 本仓库（推荐）或 clone

`git clone https://github.com/shink/actions-bot.git`

👇 修改 CSDN_ID

```shell
#!/bin/bash

set -eux

# 修改为你的CSDN_ID
CSDN_ID="sculpta"

python csdn-emailbot/spider.py $CSDN_ID
```

### 2.2 开通邮件免费发送服务

以网易邮箱为例，选择「设置」中的 「POP3/SMTP/IMAP」，打上勾 ✔ 之后保存，然后设置密码

> **注意**：该密码不能跟邮箱密码一致

### 2.3 配置 GitHub Actions

触发 GitHub Actions 需要在项目仓库新建一个 `.github/workflows` 子目录，里面存放 YAML 格式配置文件

```yaml
name: 'GitHub Actions CSDN Email Bot'

on:
  push:
    branches: 
      - master
  schedule:
    - cron: '0 14 * * *'
```

👆 上面代码中，`name` 是该配置文件的名字，`on` 是触发条件，我们指定两种情况下触发，第一种是向 master 分支 push 代码时触发，第二种是定时任务，每天在国际标准时间 14 点（北京时间 22 点）运行

需要注意的是，必须使用 [POSIX cron 语法](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07) 安排工作流程在特定的 UTC 时间（**国际标准时间，等于北京时间减去 8 个小时**）运行，并且最短间隔为每 5 分钟一次

计划任务语法有五个字段，中间用空格分隔，每个字段代表一个时间单位

> ┌───────────── minute (0 - 59)    
> │ ┌───────────── hour (0 - 23)    
> │ │ ┌───────────── day of the month (1 - 31)  
> │ │ │ ┌───────────── month (1 - 12 or JAN-DEC)    
> │ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)     
> │ │ │ │ │  
> │ │ │ │ │  
> │ │ │ │ │  
> \* &nbsp;\* &nbsp;\* &nbsp;\* &nbsp;\*

可在这五个字段中使用以下运算符：

| 运算符 |     描述     |                                       示例                                       |
| :----: | :----------: | :------------------------------------------------------------------------------: |
|   *    |    任意值    |                          `* * * * *` 在每天的每分钟运行                          |
|   ,    | 值列表分隔符 |          `2,10 4,5 * * *` 在每天第 4 和第 5 小时的第 2 和第 10 分钟运行          |
|   -    |   值的范围   |                  `0 4-6 * * *` 在第 4、5、6 小时的第 0 分钟运行                  |
|   /    |    步骤值    | `20/15 * * * *` 从第 20 分钟到第 59 分钟每隔 15 分钟运行（第 20、35 和 50 分钟） |

> 注：GitHub 操作 不支持非标准语法 @yearly、@monthly、@weekly、@daily、@hourly 和 @reboot

👇 接下来，定义了一个名为 `csdn-emailbot` 的 job，其中包含许多步骤，它们会按顺序依次执行

```yaml
jobs:
  csdn-emailbot:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
```

👆 上面代码中，`run-on` 字段指定当前 job 的运行环境为最新版的 ubuntu 系统。

接下来的 steps 中，第一步是从当前仓库中获取代码，使用的是官方提供的 [checkout action](https://github.com/marketplace/actions/checkout) 的 2.0.0 版本

```yaml
- name: 'Set up Python'
  uses: actions/setup-python@v1
  with:
    python-version: 3.7
- name: 'Install lib'
  run: pip install -r ./csdn-emailbot/requirements.txt
```

👆 上面代码就是 **部署爬虫环境** 了，首先安装 python 3.7 的环境，然后通过 pip 安装所需要的 beautifulsoup4 和 requests

👇 部署完环境后，就要执行我们写好的爬虫程序了

```yaml
- name: 'Working'
  run: bash ./csdn-emailbot/main.sh
```

👇 最后，发送邮件

```yaml
- name: 'Send mail'
  uses: dawidd6/action-send-mail@master
  with:
    server_address: smtp.163.com
    server_port: 465
    username: ${{ secrets.MAIL_USERNAME }}
    password: ${{ secrets.MAIL_PASSWORD }}
    subject: CSDN Report
    body: file://email.txt
    to: shenkebug@qq.com
    from: GitHub Actions
    content_type: text/plain
```

👆 上面代码中，使用了一个开发者写好的 [发送邮件的 action](https://github.com/dawidd6/action-send-mail)，其中需要注意的是，SMTP 服务器的用户名和密码使用的是加密变量，需要在仓库的「Settings」中设置「Secrets」，如下图所示：

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/github-actions-spider/img.png" width="800">
</p>

其中，`MAIL_USERNAME` 是你开通 SMTP 服务的邮箱，`MAIL_PASSWORD` 是你设置的 SMTP 服务的密码（**不是邮箱的登录密码**）

最后，将 `to` 修改为你要接受邮件的邮箱地址

👌 写好配置，推送到仓库以后，就可以每天晚上收到一封 CSDN profile 的邮件了

### 2.4 完整 yml 文件

```yaml
name: 'GitHub Actions CSDN Email Bot'

on:
  push:
    branches: 
      - master
  schedule:
    - cron: '0 14 * * *'

jobs:
csdn-emailbot:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v2
    - name: 'Set up Python'
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    # - name: 'Install dependencies'
    #   run: python -m pip install --upgrade pip
    - name: 'Install requirements'
      run: pip install -r ./csdn-emailbot/requirements.txt
    - name: 'Working'
      run: bash ./csdn-emailbot/main.sh
    - name: 'Send mail'
      uses: dawidd6/action-send-mail@master
      with:
        server_address: smtp.163.com
        server_port: 465
        username: ${{ secrets.MAIL_USERNAME }}
        password: ${{ secrets.MAIL_PASSWORD }}
        subject: CSDN Report
        body: file://email.txt
        to: ${{ secrets.RECEIVER }}
        from: GitHub Actions
        content_type: text/plain
```

***

`另外`：**GitHub Actions 貌似仅支持保存在工作流程运行过程中产生的文件，当作业完成时，运行程序会终止并删除虚拟环境的实例，文件也会随之清空**

如果想实现永久存储，可以利用仓库进行存储，`将要保存的文件 push 到仓库里，每次工作运行时再从仓库获取文件，再执行后面的逻辑即可`
