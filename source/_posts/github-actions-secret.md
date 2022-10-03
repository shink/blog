---
title: GitHub Actions 中 python 脚本获取仓库 secrets
date: 2020-06-01 16:05:33
categories: [GitHub]
tags: [GitHub, GitHub Actions]
---

GitHub Actions 提供的 `CI/CD（持续集成/持续部署）` 服务非常方便，可以帮助我们自动完成一些功能。但是当我们在跑一些脚本的时候，不免会存放一些密码、密钥之类的内容。我们期望跑脚本的同时，不以明文的方式存储这类密码

将 GitHub Actions 与 GitHub 仓库的 Secrets 结合，可以轻松帮助我们满足这项需求

下面以基于 ServerChan 的 LeetCode 周赛提醒功能为例

<!-- more -->

## 1. 添加 Secrets

ServerChan 的推送功能需要设置 `SCKEY` 字段，但是该字段不应以明文方式存储

打开仓库「Settings」中的「Secrets」，点击「New secret」

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/06/github-actions-secret/1.png" width=800></img>
</p>

## 2. 配置 GitHub Actions

用来向 ServerChan 接口发送请求的文件名为 `main.py`

git bash 中键入命令，新建文件

```shell
mkdir -p .github/workflows && touch .github/workflows/leetcode-weekly.yml
```

编辑 leetcode-weekly.yml，键入以下内容

```yml
name: 'GitHub Actions LeetCode Weekly Bot'

on:
  push:
    branches: 
      - master
  schedule:
    - cron: '0 2 * * 0'

jobs:
  leetcode-weekly:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout'
        uses: actions/checkout@v2
      - name: 'Set up Python'
        uses: actions/setup-python@v1
        with:
          python-version: 3.7
      - name: 'Install requirements'
        run: pip install -r leetcode-weekly/requirements.txt
      - name: 'Working'
        env:
          SCKEY: ${{ secrets.SCKEY }}
        run: python leetcode-weekly/main.py
```

其中，在 `Working` 步骤中，指定了环境变量 `SCKEY`，并将它的 value 设为 `secrets.SCKEY`

## 3. python 脚本中获取环境变量

```python
import os

if __name__ == '__main__':
    SCKEY = os.environ["SCKEY"]
```

同理，对于一些需要登录的脚本也可以使用以上方式实现加密
