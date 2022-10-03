---
title: Git 仓库中脚本无执行权限问题的解决方法
date: 2021-02-07 11:55:34
categories: [Git]
tags: [Git, Solutions]
---

## 参考

[why-when-i-use-github-actions-ci-for-a-gradle-project-i-face-gradlew-permiss](https://stackoverflow.com/questions/58282791/why-when-i-use-github-actions-ci-for-a-gradle-project-i-face-gradlew-permiss)

## 问题描述

由于在 Windows 环境下写脚本时对权限问题不太敏感，并没有为仓库中的脚本赋予执行权限，因此在 actions 执行过程中报了以下错误

```
/home/runner/work/_temp/35b69792-52fd-48f2-9411-ec8be68d25ef.sh: line 1: /home/runner/work/bark-action/bark-action/.//script.sh: Permission denied
Error: Process completed with exit code 126.
```

![1](https://gitee.com/tsund/data/raw/master/blog/2021/02/github-actions-permission-denied/1.png)

原因是因为 `script.sh` 没有执行权限

<!-- more -->

## 解决方法

使用 `--chmod=(+|-)x`

```
--chmod=(+|-)x
  Set the execute permissions on the updated files.
```

为仓库中的脚本赋予执行权限

```shell
git update-index --chmod=+x script.sh
```

commit 并 push 后，问题就解决了
