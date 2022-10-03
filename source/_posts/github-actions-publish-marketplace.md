---
title: GitHub Actions 发布至 GitHub Marketplace
date: 2021-02-07 11:02:15
categories: [GitHub]
tags: [GitHub, GitHub Actions]
---

[GitHub Actions](https://docs.github.com/en/actions) 是 GitHub 提供的一款 `CI/CD（持续集成/持续部署）`工具，可以帮助我们自动构建、测试、编译、打包、部署项目，功能十分强大

[GitHub Marketplace](https://github.com/marketplace?type=actions) 中收录了许多官方和第三方开发者所发布的一系列 actions

下面以本人所发布的 [Bark Notify](https://github.com/marketplace/actions/bark-action) 为例，讲述将自己开发的 action 发布到 GitHub Marketplace 的详细过程以及在开发过程中遇到的坑

<!-- more -->

## 编写 metadata file

action 由一个 YAML 语法的元数据文件所定义，因此须在仓库中新建一个 `action.yml` 或 `action.yaml` 文件作为 action 的入口

> You can create actions to perform tasks in your repository. Actions require a metadata file that uses YAML syntax.
>
> ——[Metadata syntax for GitHub Actions](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions)

以下是元数据文件中的几个关键字段

- `name`: action 的名称，也是在 GitHub Marketplace 中所展示的名称
- `author`: 作者信息

- `description`:  aciton 的简短描述
- `inputs`:  定义输入参数集合，可以包含多个参数
  - `inputParamterName`: 输入参数名称
    - `description`:  输入参数描述
    - `required`: 是否必填，是一个 bool 变量
    - `default`: 默认值

- `outputs`: 定义输出参数集合，可以包含多个参数
  - `outputParamterName`: 输出参数名称
    - `description`:  输出参数描述

- `runs`: 配置 action 代码的路径和用于执行代码的应用程序

- `branding`: 在 GitHub Marketplace 中显示的图标样式
  - `icon`: 图标名称，须从[Feather](https://feathericons.com/) 中选取
  - `color`: 图标颜色，可以使以下 8 种颜色：`white`、`yellow`、`blue`、`green`、`orange`、`red`、`purple` 或 `gray-dark`

### 定义输入参数

`inputs` 对象定义了 action 所依赖的输入参数，根据 [官方文档](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputs) 中的描述，输入参数会被存储到名为 `INPUT_<VARIABLE_NAME>` 的环境变量中，参数名称会被转换为大写，空格替换为 `_` 字符，action 代码中可以读取该环境变量从而得到输入参数的值

例如，`inputs` 中所定义的 `inputParamterName`输入参数的值，会被存储到名为 `INPUT_INPUTPARAMTERNAME` 的环境变量中

但是，尽管官方文档中这样说，但在使用的过程中却遇到了坑。所定义的输入参数并不能够直接通过读取该环境变量取值，事实上通过在执行过程中打印日志，在环境变量中并没有发现输入参数

因此，解决办法是手动将其定义到  `env` 对象中，这样在脚本中就可以通过 `$INPUT_<PARAMTER_NAME>` 获取到输入变量的值了

```yaml
steps:
    - name: Run script
      shell: bash
      run: $GITHUB_ACTION_PATH/script.sh
      env:
        INPUT_KEY: ${{ inputs.key }}
        INPUT_TITLE: ${{ inputs.title }}
        INPUT_BODY: ${{ inputs.body }}
        INPUT_SOUND: ${{ inputs.sound }}
        INPUT_ISARCHIVE: ${{ inputs.isArchive }}
        INPUT_URL: ${{ inputs.url }}
        INPUT_AUTOMATICALLYCOPY: ${{ inputs.automaticallyCopy }}
        INPUT_COPY: ${{ inputs.copy }}
```

> 对于不方便公开的输入参数，例如密码、私钥等，可以先保存至仓库的 `Secrets` 中，传入时通过以下方式传入

```yaml
- name: Push notifications
  uses: shink/bark-action@v1
  with:
    key: ${{ secrets.KEY }}
```

![1](https://gitee.com/tsund/data/raw/master/blog/2021/02/publish-actions-in-github-marketplace/1.png)

### 定义运行步骤

action 支持 JavaScript、Docker 和 组合运行三种运行步骤方式

#### JavaScript 运行方式

示例：

```yaml
runs:
  using: 'node12'
  main: 'main.js'
```

可参考 [官方文档](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#runs-for-javascript-actions)

#### Docker 运行方式

```yaml
runs:
  using: 'docker'
  image: 'docker://debian:stretch-slim'
```

可参考 [官方文档](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#runs-for-docker-actions)

#### 组合运行方式

示例：

```yaml
runs:
  using: "composite"
  steps:
    - run: ${{ github.action_path }}/test/script.sh
      shell: bash
```

组合运行方式支持各类脚本，更加灵活易用

- `using`: 组合运行方式必须设置为 `composite`
- `steps`: 运行步骤集合，可以包含多个步骤，每个步骤顺序执行
  - `name`: 步骤名称
  - `id`: 该步骤的唯一标识
  - `shell`: 运行方式，支持 [using-a-specific-shell](https://docs.github.com/cn/actions/reference/workflow-syntax-for-github-actions#using-a-specific-shell) 中所列的所有 shell，常用的有 `bash`、`python`
  - `run`: 脚本文件路径
  - `env`: 仅用于该步骤的环境变量
  - `working-directory`: 工作目录路径

### 示例

[shink/bark-action](https://github.com/shink/bark-action) 中的 `action.yml`示例：

```yaml
name: 'Bark Action'
description: 'An action for bark'
author: Ji Yuanhao <jiyuanhao1997@gmail.com>
branding:
  icon: 'message-circle'
  color: 'red'
inputs:
  key:
    description: Secret key
    required: true
  title:
    description: Message title
    required: false
  body:
    description: Message body
    required: false
  sound:
    description: Message sound
    required: false
  isArchive:
    description: Whether to archive this message
    required: false
  url:
    description: URL to redirect
    required: false
  automaticallyCopy:
    description: Whether to copy this message automatically
    required: false
  copy:
    description: Content copied to clipboard
    required: false
runs:
  using: "composite"
  steps:
    - name: Run script
      shell: bash
      run: $GITHUB_ACTION_PATH/script.sh
      env:
        INPUT_KEY: ${{ inputs.key }}
        INPUT_TITLE: ${{ inputs.title }}
        INPUT_BODY: ${{ inputs.body }}
        INPUT_SOUND: ${{ inputs.sound }}
        INPUT_ISARCHIVE: ${{ inputs.isArchive }}
        INPUT_URL: ${{ inputs.url }}
        INPUT_AUTOMATICALLYCOPY: ${{ inputs.automaticallyCopy }}
        INPUT_COPY: ${{ inputs.copy }}
```

至此，编写好 `action.yml` 文件后，在当前仓库中的 `.github/workflows/<CI_NAME>.yml` 中就可以通过以下方式使用自定义的 action 了

```yaml
- name: Run my action
  uses: ./
```

例如，在 [shink/bark-action](https://github.com/shink/bark-action) 的 `.github/workflows/push-notification.yml` 中：

```yaml
name: 'Push Notifications to Bark'

on: 
  repository_dispatch:
  workflow_dispatch:

jobs:
  job:
    name: Push notification job
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Push notifications
        uses: ./
        with:
          key: ${{ secrets.KEY }}
          title: Message title
          body: Message body
          sound: alarm
          isArchive: 1
          url: https://yuanhaoji.com
          automaticallyCopy: 1
          copy: Content copied to clipboard
```

## 发布至 GitHub Marketplace

编写好 `action.yml` 及运行代码后，就可以发布至 GitHub Marketplace 供他人使用了

如果仓库根目录下有 `action.yml` 或 `action.yaml`  文件，仓库页面上方就会提示是否需要发布

![2](https://gitee.com/tsund/data/raw/master/blog/2021/02/publish-actions-in-github-marketplace/2.png)

点击 `Draft a release` 按钮，进入发布页面，勾选  `Publish this Action to the GitHub Marketplace`

![3](https://gitee.com/tsund/data/raw/master/blog/2021/02/publish-actions-in-github-marketplace/3.png)

会自动检测 `action.yml` 文件中是否包含必填字段，以及仓库中是否有 `README.md` 文档

填写 `Primary Category` 和 `Another Category`，为 action 选择类别

接下来是 `Tag`，输入 `Tag version`，建议使用 `v1`、`v1.2.3` 等作为标签版本名称

![4](https://gitee.com/tsund/data/raw/master/blog/2021/02/publish-actions-in-github-marketplace/4.png)

最后是 `Release`，填写 `Release title` 和 `Release description`，点击 `Publish release` 后即可完成发布

![5](https://gitee.com/tsund/data/raw/master/blog/2021/02/publish-actions-in-github-marketplace/5.png)

发布完成后，即可在 GitHub Marketplace 页面看到自己发布的 action

## 参考

[Github action 的开发到发布](https://juejin.cn/post/6870372475188969479)

[Metadata syntax for GitHub Actions](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions)