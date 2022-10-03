---
title: 通过 GitHub Actions 将 GitHub 仓库自动备份到 Gitee、GitLab
date: 2020-03-16 13:23:54
categories: [GitHub]
tags: [GitHub, GitHub Actions]
---

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/03/github-mirror/github.jpg" width="800">
</p>

## 前言

目前开源已经逐渐形成了一种趋势，越来越多的 geeker 加入了开源大军，开源社区也逐渐壮大，推动了技术发展和快速迭代

作为全球知名的代码托管平台，GitHub、Gitee、GitLab 均拥有不小的用户量，尤其是 GayHub，作为全球最大的同性交友平台，拥有超过 4 千万的用户量，足以说明其在业内的知名度

但是，对于个人来说，使用一个托管平台就足够了，但是我们又有在其他平台备份的需求，并且希望有更新时能够自动备份

对于这种需求，解决办法大多是利用 webhook，或者是在本地仓库中 remote add 添加远程仓库，这样就可以 push 到多个远程仓库。但是这些方法较为繁琐，更何况还有更好用的办法——GitHub Actions，有关 GitHub Actions 的一些教程还可参考博客 [GitHub Actions 部署爬虫并定时发送邮件](https://blog.csdn.net/sculpta/article/details/104142607)

<!-- more -->

## 步骤

### 1. 生成 ssh

git bash 中敲入命令，会在 `~/.ssh` 文件夹下生成 `id_rsa.pub` 文件和 `id_rsa` 文件，分别存放公钥和私钥

```shell
ssh-keygen -t rsa -C "user@email.com"
```

### 2. 将公钥添加到 GitLab、Gitee

Gitee: 「设置」-->「安全设置」-->「SSH公钥」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/03/github-mirror/1.png" width="900">
</p>

GitLab: 「Settings」-->「SSH Keys」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/03/github-mirror/2.png" width="900">
</p>

### 3. 将私钥添加到 GitHub 仓库

GitHub Repository: 「Settings」-->「Secrets」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/03/github-mirror/4.png" width="900">
</p>

### 4. 取消 GitLab 仓库的受保护分支

由于 GitLab 仓库分支默认会受保护，即无法强制推送，如果不取消会报以下错误

```
GitLab: You are not allowed to force push code to a protected branch on this project.
```

GitLab Repository: 「Settings」-->「Repository」-->「Protected Branches」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/03/github-mirror/3.png" width="900">
</p>

### 5. 配置 GitHub Actions

git bash 中敲入命令

```shell
mkdir -p .github/workflows && touch .github/workflows/mirror.yml
```

用 VS Code 打开 `mirror.yml` 或使用 vi 编辑，将下列内容添加其中

```yml
name: 'GitHub Actions Mirror'

on: [push, delete]

jobs:
  mirror_to_gitee:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout'
        uses: actions/checkout@v1
      - name: 'Mirror to gitee'
        uses: pixta-dev/repository-mirroring-action@v1
        with:
          target_repo_url:
            git@gitee.com:tsund/test.git
          ssh_private_key:
            ${{ secrets.GITEE_KEY }}

  mirror_to_gitlab:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout'
        uses: actions/checkout@v1
      - name: 'Mirror to gitlab'
        uses: pixta-dev/repository-mirroring-action@v1
        with:
          target_repo_url:
            git@gitlab.com:tsund/test.git
          ssh_private_key:
            ${{ secrets.GITLAB_KEY }}
```

其中，使用了 [repository-mirroring-action](https://github.com/marketplace/actions/mirroring-repository)，定义了两个 job，分别负责备份 Gitee 和 GitLab 仓库，`target_repo_url` 指明目标仓库的 ssh 地址，`ssh_private_key` 指明 GitHub 仓库中 Secrets 存放的目标仓库的 ssh 私钥

配置完成后，向 GitHub 仓库 push 时就会自动备份到 Gitee、GitLab 对应的仓库了
