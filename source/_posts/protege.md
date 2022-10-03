---
title: Protege 使用教程
date: 2020-04-03 15:22:34
categories: [知识图谱]
tags: [知识图谱]
---

Protégé 软件是斯坦福大学医学院生物信息研究中心基于 Java 语言开发的本体编辑和知识获取软件，或者说是本体开发工具，也是基于知识的编辑器，属于开放源代码软件。该软件主要用于语义网中本体的构建，是语义网中本体构建的核心开发工具

Protégé 提供了本体概念类、关系、属性和实例的构建，并且屏蔽了具体的本体描述语言，用户只需在概念层次上进行领域本体模型的构建

- Protégé 官网：<https://protege.stanford.edu>，GitHub 地址：<https://github.com/protegeproject>

- 下载地址：[官网下载](https://protege.stanford.edu/products.php#desktop-protege) or [百度云盘](https://pan.baidu.com/s/1n0bzKFnr-ON2A55Ui7XJBA)（提取码：p2hy）

<!-- more -->

## 1. 界面

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/1.png" width="900">
</p>

Protégé 功能非常强大，不过常用的一般只有 `Classes`、`Object properties`、`Data properties` 等几个功能

## 2. Classes

这里的类与面向对象中的类是一个含义，是对现实生活中一类具有共同特征的事物的抽象，在本体论中就表明是一个本体

在 `Classes` 标签下声明类，所有的类都是 Thing 的子类

右键「Add subclass」可以创建子类，但这样创建比较麻烦，可以使用下面的方法快速创建类结构

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/2.png" width="750">
</p>

通过缩进表示层次关系，prefix 和 suffix 分别表示前缀和后缀

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/3.png" width="650">
</p>

点击 Continue 后，选项表示是否使同一层次的类不相交，即同一对象不会同属于多个类，比如一个食物不可能同时既是披萨又是配料

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/4.png" width="650">
</p>

## 3. Object properties

object properties，即对象属性，它表示本体与本体间的关系，比如披萨与配料之间的关系：披萨有哪些配料（hasTopping），配料可以做哪些披萨（isToppingOf）

这些关系可以看做是一个映射，有定义域、值域，在 Protégé 中就是 Domains 和 Ranges，如 hasTopping 这个对象属性，披萨就是定义域（Domains），配料就是值域（Ranges），并且与 isToppingOf 是互为相反（Inverse of）的关系，即两者的定义域与值域相反

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/5.png" width="750">
</p>

在对象属性中有以下特性（Characteristics）：

- `Functional`: **函数性**，即每个输入值对应唯一输出值，允许多个输入值对应同一输出值，但不允许同一输入值对应多个输出值。以 hasFather 为例，已知 john 的 Father 是 Mike 和 Smith，可以看出它违反了函数性，所以经过推导，得出 Mike 和 Smith 是同一个人
- `Inverse functional`: **反函数性**，与函数性相反，允许同一输入值对应多个输出值，不允许多个输入值对应同一输出值。例如 isMotherOf，Linda 和 Sara 是 Amy 的母亲，可以推导出 Linda 和 Sara 是同一个人
- `Transitive`: **传递性**。以 hasAncestor 为例，已知 Matthew 的祖先是 Peter，Peter 的祖先是 William，可以推导出 William 也是 Matthew 的祖先
- `Symmetric`: **对称性**。以 hasSibling 为例，已知 Matthew 的兄弟是 Gemma，同时可以推导出 Gemma 也是 Matthew 的兄弟
- `Asymmetric`: **反对称性**，与对称性相反。以 hasChild 为例，已知 Jean 有一个叫 Matthew 的孩子，那么 Matthew 就不能是 Jean 的孩子
- `Reflexive`: **自反性**。以 knows 为例，已知 George 认识 Simon，那么也可以推导出 George 认识自己，Simon 也认识自己
- `Irreflexive`: **反自反性**，与自反性相反。以 isFatherOf 为例，已知 Alex 是 Bob 的父亲，那么 Alex 就不能是自己的父亲，同样 Bob 也不能是自己的父亲

## 4. Data properties

Data properties，即数据属性，用来描述本体的属性。如 People 这个本体可能有 age、sex、name 等属性

创建 Data properties 同样也可以一次输入多个属性，使用制表符表示层次关系

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/04/protege/6.png" width="650">
</p>

Data properties 同样可指定函数性，与 Object properties 相似，允许多个输入值对应同一输出值，但不允许同一输入值对应多个输出值

Domains 指定拥有该属性的本体，pepoleProperties 的 Domains 自然就是 People 了，Ranges 指定属性值的类型，如 float、string、datetime 等





