---
title: 知识图谱 KBQA Demo：fuseki sparql python 版本问题详细解决方案
date: 2020-02-20 21:34:52
categories: [知识图谱]
tags: [知识图谱, Solutions]
---

刚入坑知识图谱，看了一位大神的教程，但是由于 jena、fuseki、python 等版本不同，踩了不少坑，特此记录一下

本文不做具体知识的讲解（具体知识可移步 <https://zhuanlan.zhihu.com/knowledgegraph>），仅罗列实践过程中遇到的坑及解决方案

以下内容大多从教程下面几百条评论中提炼总结而来

<!-- more -->

## 环境版本

- jena ：3.14.0
- fuseki ：3.14.0
- jdk ：1.8.0_201
- python ：3.7.6
- anaconda ：4.8.2

## 具体问题及解决方案

### 1. 通过 D2RQ 生成 mapping 文件

此时须打开 MySQL 服务，进入 D2RQ 目录

```
generate-mapping -u root -p 密码 -o kg_demo_movie_mapping.ttl jdbc:mysql:///kg_demo_movie?useSSL=false
```

- `-u` ：指定 mysql 用户名
- `-p` ：指定用户密码
- `-o` ：指定输出文件路径及名称
- `jdbc:mysql:///` 后面指定 mysql 中的数据库名称

对于博主的 kg_demo_movie 项目，mapping 文件生成后还需要修改，所以直接使用博主 GitHub 仓库中的 mapping 文件即可

### 2. 通过 D2RQ 将数据转为 RDF

同样需要打开 MySQL 服务，在 D2RQ 目录下

```
.\dump-rdf.bat -o kg_demo_movie.nt .\kg_demo_movie_mapping.ttl
```

### 3. 添加环境变量

在系统变量中，添加以下变量

- `JENA_HOME` ：jena 压缩包的解压位置，例如 `D:\apache-jena`
- `FUSEKI_HOME` ：fuseki 压缩包的解压位置，例如 `D:\apache-jena\apache-jena-fuseki`

在系统变量中，追加以下变量

- `CLASSPATH` ：追加 `%JENA_HOME%\lib`
- `path` ：添加 `%JENA_HOME%\bin`、`%JENA_HOME%\bat`、`%FUSEKI_HOME%`

### 4. 通过 Jena 将 RDF 数据以 TDB 方式存储

存放在 jena 的 tdb 目录下

```
.\tdbloader.bat --loc="D:\apache-jena\tdb" "D:\D2RQ\kg_demo_movie.nt"
```

### 5. 使用 OWL 推理机

**注意**：博主用的 fuseki 3.5 版本，其中不少语法在 3.14 版本中已经有所改动，所以直接使用下面的配置文件，只需修改其中本体文件及 TDB 的路径即可

```xml
@prefix :      <http://base/#> .
@prefix tdb:   <http://jena.hpl.hp.com/2008/tdb#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ja:    <http://jena.hpl.hp.com/2005/11/Assembler#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix fuseki: <http://jena.apache.org/fuseki#> .

<#service1>       rdf:type            fuseki:Service ;
    fuseki:name                       "kg_demo_movie" ;
    fuseki:serviceQuery               "sparql" ;
    fuseki:serviceQuery               "query" ;
    fuseki:serviceUpdate              "update" ;
    fuseki:serviceUpload              "upload" ;
    fuseki:serviceReadWriteGraphStore "data" ;
    fuseki:serviceReadGraphStore      "get" ;
    fuseki:dataset                    <#dataset> ;
    .


<#dataset> rdf:type ja:RDFDataset ;
    ja:defaultGraph <#model_inf> ;
    .

<#model_inf> rdf:type ja:InfModel ;
    ja:MemoryModel <#tdbGraph> ;

    #本体文件的路径
    ja:content [ja:externalContent <file:///D:/apache-jena/apache-jena-fuseki/run/databases/ontology.ttl> ] ;

    #启用OWL推理机
    ja:reasoner [ja:reasonerURL <http://jena.hpl.hp.com/2003/OWLFBRuleReasoner>] .

<#tdbGraph> rdf:type tdb:GraphTDB ;
    tdb:dataset <#tdbDataset> ;
    .

<#tdbDataset> rdf:type tdb:DatasetTDB ;
    tdb:location "D:/apache-jena/tdb" ;
    .
```

**注意**：修改配置文件后，还需要将 RDF 数据（即 `.nt` 文件）上传到 fuseki 中，如图（这个坑真的填了好久 ···）

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/kg-demo/1.png" width="900">
</p>

### 6. 自定义推导规则

**注意**：`rules.ttl` 文件中需要用逗号隔开，如下

```xml
@prefix : <http://www.kgdemo.com#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

[ruleComedian: (?p :hasActedIn ?m), (?m :hasGenre ?g), (?g :genreName '喜剧') -> (?p rdf:type :Comedian)]
[ruleSymmetric: (?p :hasActedIn ?m) -> (?m :hasActor ?p)]
```

### 7. 运行最终 Demo

**注意**：博主使用的是 python2，其中许多语法在 python3 中也有所改动，修改方法如下

- 所有的 `.decode('utf-8')`、`.encode('utf-8')` 全部删掉，即全部替换为 `''`
- 所有的 `iteritems()` 替换为 `items()`
- 所有的 `print content` 替换为 `print(content)`，`print` 替换为 `print('\n')`
- 所有的 `raw_input()` 替换为 `input()`
- `question2sparql.py` 文件中第 44 行 `return queries_dict.values()[0]` 改为 `return list(queries_dict.values())[0]`

附 PyCharm 全局替换的方法，如图

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/kg-demo/2.png" width="900">
</p>

最终效果

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/02/kg-demo/3.png" width="900">
</p>
