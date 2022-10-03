---
title: GitHub 多人队伍合作详细教程
date: 2020-02-22 18:42:20
categories: [Git]
tags: [GitHub, Git]
---

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/1.jpg" width="900">
</p>

本文将分场景详细讲述如何通过 GitHub 实现多人队伍协同开发

> 示例中所使用的仓库是 [shink/cooperation-test](https://github.com/shink/cooperation-test)，欢迎加入，一起熟练 Git 的使用

<!-- more -->

## 开发规范

### 分支管理

为了规范开发、保持 commit 历史、方便后期维护，Git 的分支管理是必不可少的工作

分支管理示例：

- `main` 分支：
  - 主分支，最终的、稳定的、经过测试没有 bug 的、可部署于生产环境的分支
  - 只能由 `release` 和 `hotfix` 分支合并，任何情况下都不能直接修改代码
- `dev` 分支：
  - 主要开发分支，贯穿于整个项目的生命周期
  - 始终保持最新版本，功能模块开发任务交给 `feature` 分支，测试任务交给 `release` 分支
- `hotfix` 分支：
  - 热修复分支，当 `main` 分支部署到生产环境后发生紧急状况，需要及时处理时，该分支负责热修复，即在保证应用不下线的条件下，对 bug 进行紧急修复
  - 该分支以 `main` 分支为基线，修复 bug 后，合并到 `main` 分支部署上线，同时也合并到 `dev` 分支保持最新进度
  - 命名规则： `hotfix/NAME` 或 `hotfix-NAME`
- `feature` 分支：
  - 功能模块开发分支，对应于一个特定的功能模块
  - 该分支以 `dev` 分支为基线，完成开发工作后再合并到 `dev` 分支
  - 命名规则：`feature/NAME` 或 `feature-NAME`
- `release` 分支：
  - 预发布分支，在发布正式版本前进行全面测试和修复
  - 该分支以 `dev` 分支为基线进行全面测试，若发生 bug 则可直接在该分支修复并提交
  - 经过测试没有问题之后，合并到 `main` 分支部署上线，同时也合并到 `dev` 分支保持最新进度
  - 命名规则：`release/NAME` 或 `release-NAME`

| 分支名称  |     分支职责     | 基线分支 | 合并分支  |
| :-------: | :--------------: | :------: | :-------: |
|  `main`   |      主分支      |    -     |     -     |
|   `dev`   |     开发分支     |   main   |     -     |
| `hotfix`  |    热修复分支    |   main   | main, dev |
| `feature` | 功能模块开发分支 |   dev    |    dev    |
| `release` |    预发布分支    |   dev    | main, dev |

总结：

- `main` 分支和 `dev` 分支都贯穿于整个项目的生命周期
- `hotfix`、`feature`、`release` 分支都是临时分支，分别负责热修复、功能模块开发、预发布

下图很好地展示了在时间轴上各分支的职责划分情况

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/2.jpg" width="800">
</p>

### Commit message

每次 commit 到本地库时，必须添加 commit message，以对本次提交做出说明

在团队合作时，commit message 的书写格式也应当遵守相应规范，清晰明了的 commit message 有利于快速定位提交、自动生成 change log 文档

下图是 Angular 规范

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/3.png" width="750">
</p>

具体的规范说明可参考阮一峰老师的博客：[Commit message 和 Change log 编写指南](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html)

## 任务划分

团队合作中，合理的划分任务有助于项目顺利开展

下面以一个二人队伍为例（队长 A 和队员 B），多人队伍的话其他队员操作同队员 B

队长 A 的任务：

- 统一规范，包括命名规范、文档规范等
- review 代码，维护 issue 和 PR，管理 `main` 分支和 `dev` 分支
- 承担部分开发任务

队员 B 的任务：

- 承担主要开发任务，完成系统功能

## 初始状态

以队长 A 的仓库为基准，首先队员 B Fork 队长 A 的项目仓库

假设仓库初始状态为：`main` 分支和 `dev` 分支下分别只有 `README.md` 文件

```
 ┌── main: README.md
 │
 └── dev: README.md
```

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/4.png" width="850">
</p>

开始时首先 clone 远程仓库到本地

```bash
git clone https://github.com/user/repo.git
```

clone 完之后，可以看到本地仓库中只有 `main` 分支

```bash
git branch

* main
```

通过下列命令查看所有分支

```bash
git branch -a

* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/dev
  remotes/origin/main
```

可以看到远程仓库中虽然有 `dev` 分支，但是本地仓库中并没有分支与远程仓库的 `dev` 分支关联

通过下列命令在本地仓库中创建并切换到 `dev` 分支

```bash
git checkout -b dev origin/dev
```

此时，在本地分支中就可以看到 `dev` 分支了

```bash
git branch

* dev
  main
```

## 场景一：队员与主仓版本保持同步

在开始工作前，须先拉取当前当前分支的最新版本，保证代码是最新版本

以队员 B 为例：

添加主仓的远程仓库地址

```bash
git remote add upstream https://github.com/captain_a/project.git
```

查看当前仓库所连接的远程仓库

```bash
git remote -v
```

此时，当前仓库所连接的远程仓库为：

```
origin    https://github.com/member_b/project.git (fetch)
origin    https://github.com/member_b/project.git (push)
upstream    https://github.com/captain_a/project.git (fetch)
upstream    https://github.com/captain_a/project.git (push)
```

切换到 `dev` 分支

```bash
git checkout dev
```

获取 upstream 的最新内容

```bash
git fetch upstream dev
```

合并

```bash
git merge upstream/dev
```

至此，`dev` 分支就包含最新版本代码了（`main` 分支同理）

## 场景二：队员开发特定功能模块

> 在开发阶段，应当尽量避免发生冲突，同时保持 commit 历史的干净整洁，善用 `git rebase` 命令可以保证 commit 历史更加清爽，rebase 的同时还是可以 squash，将逻辑相似的多个 commit 合并到一个 commit，并附上描述性更强的 commit message， 这样 commit 历史就会非常清晰、一目了然了

以队员 B 开发登录模块为例

在本地创建 `feature/login_module` 分支，首先切换到 `dev` 分支

```bash
git checkout dev
```

以 `dev` 分支为基线，创建 `feature/login_module` 分支，并切换到该分支

```bash
git checkout -b feature/login_module
```

查看各分支情况

```bash
git branch -v

  dev                  333e2b6 Init README.md
* feature/login_module 333e2b6 Init README.md
  main                 333e2b6 Init README.md
```

将该分支 push 到远程仓库

```bash
git push origin feature/login_module:feature/login_module
```

假设队员 B 完成了开发任务，创建了 `login_module.txt` 文件

```bash
 echo "login module finished" > login_module.txt
```

add 到暂存区

```bash
git add login_module.txt
```

commit 到本地库

```bash
git commit -m "login module finished"
```

push 到远程仓库

```bash
git push origin feature/login_module
```

在 GitHub 页面可以看到提交成功了

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/5.png" width="900">
</p>

## 场景三：队员提交 PR，请求与主仓合并

队员 B 已经在自己的仓库中完成了功能模块的开发，但并没有合并到队长 A 的仓库中，因此队长 A 目前还无法看到队员 B 所做的工作

队员可以提交 PR，即 Pull Request，请求与主仓进行合并

> 在提交 PR 时，PR 中尽量只包含一个 commit

此时，队员 B 可以选择先将 `feature` 分支合并到 `dev` 分支，再提交 PR，请求合并到主仓的 `dev` 分支，即

```
member_b:dev -> captain_a:dev
```

也可以请求将 `feature` 分支合并到主仓的 `dev` 分支，即

```
member_b:feature -> captain_a:dev
```

还可以请求将 `feature` 分支合并到主仓的 `feature` 分支，即

```
member_b:feature -> captain_a:feature
```

这主要取决于主仓是否需要保存临时分支，以及谁负责解决冲突

下面以第一种情况进行演示，即队员 B 先将 `feature` 分支合并到 `dev` 分支，再提交 PR，请求合并到主仓的 `dev` 分支

首先切换到 `dev` 分支

```bash
git checkout dev
```

合并 `feature` 分支

```bash
git merge feature --no-ff
```

> merge 时推荐加上 `--no-ff` 选项，避免 `feature` 分支扰乱 `dev` 分支的 commit 历史

若加上了 `--no-ff` 选项，会自动创建一个 merge 的 commit 记录

输入 commit 信息后，按 `Ctrl + O` 将 commit 信息保存到 `MERGE_MSG` 文件中，`Ctrl + X` 退出

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/6.png" width="850">
</p>

push 到远程仓库

```bash
git push origin dev
```

可以看到清爽的 commit 历史：

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/7.png" width="850">
</p>

接下来就是提交 PR 阶段了

首先队员 B 在自己的 GitHub 仓库中点击 `New pull request` 按钮创建 PR

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/8.png" width="900">
</p>

选择分支，然后点击 `Create pull request` 按钮

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/9.png" width="900">
</p>

填写 title 和 comment后，点击 `Create pull request` 按钮即可提交 PR

接下来，队长 A 需要打开该 PR 并 review 代码，如果没有问题并且没有冲突则可允许 merge

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/10.png" width="900">
</p>

其中，Merge pull resquest 有三个选项：

- `Create a merge commit` ：表示把这个 PR 作为一个分支合并，并保留分支上的所有提交记录
- `Squash and merge` ：表示只为这次合并保留一个提交记录
- `Rebase and merge` ：找到两个分支共同的祖先，然后在当前分支上合并从共同祖先到现在的所有 commit

三个选项的不同点：

- `Create a merge commit` ：不能保持 main 分支干净，但是保留了所有的 commit history，当 PR 中 commit 次数较多时不推荐此方式
- `Squash and merge` ：也可以保持 main 分支干净，但是 main 中 author 都是 maintainer，而不是原 author
- `Rebase and merge` ：可以尽可能保持 main 分支干净整洁，并且易于识别 author

这里选择 `Rebase and merge`

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/11.png" width="900">
</p>

merge 完成后该 PR 就自动 closed 了，合并工作完成

队长更新本地仓库，在 `dev` 分支下，拉取最新代码

```bash
git pull origin dev
```

此时，主仓中的 commit 历史如图所示：

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/github-cooperation/12.png" width="900">
</p>

## 场景四：合并时出现冲突

冲突产生有两种情况：

- 两个分支都修改了同一文件（不管什么地方）
- 两个分支都修改了同一文件的名称

对于产生的冲突，需要手动修改冲突代码

解决冲突之后，还需要 add 并 commit

```shell
git add CONFLICT_FILE

git commit -m "fix conflict"
```

## 场景五：版本回退

有时候当前版本可能有许多 bug，不得不重新从头开始工作，这时候就需要先回退到上一版本

`git reset` 命令可以将当前 branch 回退到之前某一个 commit 节点

回退到上一版本

```shell
git reset HEAD^
```

其中，`HEAD^` 表示上一个版本，`HEAD^^` 表示上上个版本，`HEAD~100` 表示前 100 个版本

另外，还可以使用以下命令回退到指定版本

```shell
git reset 版本号
```

版本号可以通过以下命令查看

```shell
git log --oneline
```

另外，`git reset` 还有三个选项：

- `--soft`: 仅回退本地库中的内容，相当于撤销 `git commit`
- `--mixed`: （默认方式）同时回退本地库和暂存区内容，相当于进一步撤销 `git add`
- `--hard`: 同时回退本地库、暂存区和工作区内容，相当于进一步撤销本地仓库文件夹中的改动

**注意**：回退版本后，日志中就会删除回退前版本的 commit 记录，如果想查看回退前的版本记录，可以使用如下命令查看

```shell
git reflog
```
