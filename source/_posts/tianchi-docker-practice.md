---
title: 天池 Docker 练习场比赛攻略+代码
date: 2020-02-20 12:46:33
categories: [比赛]
tags: [Docker, 比赛]
---

本文将详细讲述天池 Docker 练习场的比赛流程，并贴出代码以供参考

## 1. 比赛内容

题目：

- 输出 Hello world
- 计算 `/tcdata/num_list.csv` 中一列数字的总和
- 在 `/tcdata/num_list.csv` 文件中寻找最大的 10 个数，从大到小生成一个 List

输出结果格式：

```json
{  
    "Q1":"Hello world", 
    "Q2":sum值, 
    "Q3":[top10_list] 
}
```

**注意事项**：

- 输出 Hello world 就是将 `"Hello world"` 直接写入 `result.json` 中就行
- `/tcdata/num_list.csv` ：提交镜像后评分系统中会有这个文件，所以在编程时直接引用就好

<!-- more -->

## 2. 编写代码

下面以阿里云 Centos 7 为例

创建文件夹

```shell
mkdir -p /data/tianchi_docker_test && cd /data/tianchi_docker_test
```

在 `tianchi_docker_test` 文件夹中创建文件

```shell
touch Dockerfile hello_world.py result.json run.sh
```

赋予权限

```shell
chmod 755 *
```

`Dockerfile` 中，直接复制模版就行

```
# Base Images
## 从天池基础镜像构建
FROM registry.cn-shanghai.aliyuncs.com/tcc-public/python:3

## 把当前文件夹里的文件构建到镜像的根目录下
ADD . /

## 指定默认工作目录为根目录（需要把run.sh和生成的结果文件都放在该文件夹下，提交后才能运行）
WORKDIR /

## 镜像启动后统一执行 sh run.sh
CMD ["sh", "run.sh"]
```

`hello-world.py` 中

```python
# coding:utf-8

import json
import csv

file_name = '/tcdata/num_list.csv'
data = []

# 第一题，直接写入 Hello world
result = {
    "Q1": "Hello world",
    "Q2": 0,
    "Q3": []
}

# 第二题，求和
with open(file_name, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(int(row[0]))

sum = sum(data)
result['Q2'] = sum

# 第三题
result['Q3'] = sorted(data, reverse=True)[0:10]

# 保存到 result.json
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
```

`run.sh` 中

```shell
python hello-world.py
```

## 3. 构建镜像并推送

登录阿里云容器镜像服务

```shell
docker login --username=用户名@aliyun.com registry.cn-shanghai.aliyuncs.com
```

构建镜像（**注意**：后面有个 `.`，表示使用当前目录下的 Dockerfile 构建镜像）

```shell
docker build -t registry.cn-shanghai.aliyuncs.com/命名空间/镜像名称:版本号 .
```

推送镜像

```shell
docker push registry.cn-shanghai.aliyuncs.com/命名空间/镜像名称:版本号
```

提交结果，镜像路径中填写：

```
registry.cn-shanghai.aliyuncs.com/命名空间/镜像名称:版本号
```

OK，good luck !