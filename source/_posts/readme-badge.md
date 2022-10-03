---
title: GitHub 和 Docker Hub 中 README 常用的徽章
date: 2020-03-16 20:38:23
tags: [GitHub, Docker Hub]
---

README 文件通常用来让人快速了解项目，它应大体包括以下内容：

- 项目背景
- 安装
- 使用
- Badge
- 相关项目（可选）
- 主要项目负责人
- 参与贡献方式
- 开源协议

除了必要的描述外，使用几个漂亮的 Badge（徽章）能让介绍看起来不那么枯燥，而且如果包含几个如 `Travis CI`、`Coveralls` 这样的徽章的话，更能体现自己的代码质量

Travis CI 同 GitHub Actions 一样，都是一种提供持续继承服务的工具，Travis 绑定 GitHub 项目后，每次 push 时都会自动根据配置文件拉取最新代码、构建环境、按照测试模块进行自动测试，这样就能及时发现问题并修复

> 目前 GitHub 疯狂推荐 GitHub Actions，确实非常好用。还是推荐使用 GitHub Actions，不过顺便拿个 Travis CI 的徽章也不错

Coveralls 可以生成自动测试报告，完成测试覆盖率的统计

以上两种工具都与 GitHub 深度集成，不过略显繁琐，下面介绍一些简单实用又好看并且能够拿过来就用的徽章，主要用到 [shields.io](https://shields.io/)，它专门提供简洁、易读的 SVG 格式的徽章，并且支持许多 web 页面和持续集成服务

<!-- more -->

## GitHub README 常用徽章

### 1. 格式

```html
<img src="https://img.shields.io/github/:type/:user/:repo.svg"/>
```

其中，`:type` 表示类型，比如 license（开源协议）、repo-size（仓库大小）等，`:user` 是你 GitHub 的用户名，`:repo` 是你的仓库名

### 2. 开源协议

<img src="https://img.shields.io/github/license/tensorflow/tensorflow.svg"/>

```html
<img src="https://img.shields.io/github/license/tensorflow/tensorflow.svg"/>
```

### 3. 仓库大小

<img src="https://img.shields.io/github/repo-size/tensorflow/tensorflow.svg"/>

```html
<img src="https://img.shields.io/github/repo-size/tensorflow/tensorflow.svg"/>
```

### 4. 最后提交时间

<img src="https://img.shields.io/github/last-commit/tensorflow/tensorflow.svg"/>

```html
<img src="https://img.shields.io/github/last-commit/tensorflow/tensorflow.svg"/>
```

### 5. 编程语言

<img src="https://img.shields.io/badge/language-python-3572A5.svg">

这个功能需要自定义，自定义的格式如下

```html
<img src="https://img.shields.io/badge/<LABEL>-<MESSAGE>-<COLOR>.svg"/>
```

各大常用语言的徽章如下（颜色以 GitHub 仓库上方显示 language-color 为例）

|    语言    |  颜色   |                                  徽章                                   |
| :--------: | :-----: | :---------------------------------------------------------------------: |
|    java    | #B07219 |    <img src="https://img.shields.io/badge/language-java-B07219.svg">    |
|   python   | #3572A5 |   <img src="https://img.shields.io/badge/language-python-3572A5.svg">   |
|     c      | #555555 |     <img src="https://img.shields.io/badge/language-c-555555.svg">      |
|    c++     | #F34B7D |    <img src="https://img.shields.io/badge/language-c++-F34B7D.svg">     |
|    php     | #4F5D95 |    <img src="https://img.shields.io/badge/language-php-4F5D95.svg">     |
|   scala    | #C22D40 |   <img src="https://img.shields.io/badge/language-scala-C22D40.svg">    |
|    ruby    | #701516 |    <img src="https://img.shields.io/badge/language-ruby-701516.svg">    |
|    html    | #E34C26 |    <img src="https://img.shields.io/badge/language-html-E34C26.svg">    |
|    css     | #563D7C |    <img src="https://img.shields.io/badge/language-css-563D7C.svg">     |
| javascript | #F1E05A | <img src="https://img.shields.io/badge/language-javascript-F1E05A.svg"> |
|    vue     | #2C3E50 |    <img src="https://img.shields.io/badge/language-vue-2C3E50.svg">     |
|   shell    | #89E051 |   <img src="https://img.shields.io/badge/language-shell-89E051.svg">    |
|     go     | #00ADD8 |     <img src="https://img.shields.io/badge/language-go-00ADD8.svg">     |
| dockerfile | #384D54 | <img src="https://img.shields.io/badge/language-dockerfile-384D54.svg"> |

## Docker Hub README 常用徽章

### 1. 自动化

<img src="https://img.shields.io/docker/automated/tsund/tianchi_docker_practice.svg"/>

```html
<img src="https://img.shields.io/docker/automated/tsund/tianchi_docker_practice.svg"/>
```

### 2. star

<img src="https://img.shields.io/docker/stars/tsund/tianchi_docker_practice.svg"/>

```html
<img src="https://img.shields.io/docker/stars/tsund/tianchi_docker_practice.svg"/>
```

### 3. pull

<img src="https://img.shields.io/docker/pulls/tsund/tianchi_docker_practice.svg"/>

```html
<img src="https://img.shields.io/docker/pulls/tsund/tianchi_docker_practice.svg"/>
```

### 4. image-size

格式

```html
<img src="https://img.shields.io/docker/image-size/:user/:repo/:tag"/>
```

<img src="https://img.shields.io/docker/image-size/tsund/tianchi_docker_practice/latest"/>

### 5. version

格式

```html
<img src="https://img.shields.io/docker/image-size/:user/:repo/:tag"/>
```

<img src="https://img.shields.io/docker/v/tsund/tianchi_docker_practice/latest"/>

更多有趣的徽章可以参考 [shields.io](https://shields.io/)
