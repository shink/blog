---
title: C++ mmap 多进程文件读写
date: 2020-05-04 21:13:02
categories: [C++]
tags: [C++]
---

mmap 采用内存映射的方式，直接将磁盘上的文件映射到内存（准确的说是虚拟内存）中，不需要其他额外空间，对内存映射区的修改可以与磁盘文件保持同步，故 mmap 的读写速度非常快

使用 mmap 需注意以下两点：

- 仅支持 linux 系统

- mmap 映射区域大小必须是物理页大小（page size）的整倍数（32 位系统中通常是 4k 字节）

<!-- more -->

## 1. mmap 使用

```cpp
#include <sys/mman.h>
#include <fcntl.h>

//  开启映射
void *mmap(void *start, size_t length, int prot, int flags, int fd, off_t offset);

//  关闭映射
int munmap(void *start, size_t length);
```

函数形参含义：

- \*start: 指向欲映射的内存起始地址，通常设为 NULL，表示让系统自动选定地址，映射成功后返回该地址
- length: 表示将文件中多大的部分映射到内存，即映射区的长度
- prot: 映射区域的保护方式，不能与文件的打开模式冲突。可以为以下一种或几种方式，多种方式使用 or 组合（"`|`"）

    - `PROT_EXEC`: 映射区域可被执行
    - `PROT_READ`: 映射区域可被读取
    - `PROT_WRITE`: 映射区域可被写入
    - `PROT_NONE`: 映射区域不能存取

- flags: 影响映射区域的各种特性，指定映射对象的类型，映射选项和映射页是否可以共享。在调用 mmap() 时必须要指定 MAP_SHARED 或 MAP_PRIVATE，flags 可以是以下一个或者多个值：

    - `MAP_FIXED`: 如果参数 start 所指的地址无法成功建立映射时，则放弃映射，不对地址做修正。通常不鼓励这样设置
    - `MAP_SHARED`: 对映射区域的写入数据会复制回文件内，而且允许其他映射该文件的进程共享。与其它所有映射这个对象的进程共享映射空间。对共享区的写入，相当于输出到文件。直到 msync() 或者 munmap() 被调用，文件实际上不会被更新
    - `MAP_PRIVATE`: 对映射区域的写入操作会产生一个映射文件的复制，即私人的“写入时复制”（copy on write）对此区域作的任何修改都不会写回原来的文件内容，写入不会影响到原文件。这个标志和 MAP_SHARED 是互斥的，只能使用其中之一
    - `MAP_ANONYMOUS`: 建立匿名映射。此时会忽略参数fd，不涉及文件，而且映射区域无法和其他进程共享。
    - `MAP_DENYWRITE`: 只允许对映射区域的写入操作，其他对文件直接写入的操作将会被拒绝
    - `MAP_LOCKED`: 将映射区域锁定住，这表示该区域不会被置换（swap），从而防止页面被交换出内存
    - `MAP_NORESERVE`: 不为这个映射保留交换空间。当交换空间被保留，对映射区修改的可能会得到保证。当交换空间不被保留，同时内存不足，对映射区的修改会引起段违例信号
    - `MAP_LOCKED`: 锁定映射区的页面，从而防止页面被交换出内存
    - `MAP_GROWSDOWN`: 用于堆栈，告诉内核 VM 系统，映射区可以向下扩展
    - `MAP_POPULATE`: 为文件映射通过预读的方式准备好页表。随后对映射区的访问不会被页违例阻塞
    - `MAP_NONBLOCK`: 仅和 MAP_POPULATE 一起使用时才有意义。不执行预读，只为已存在于内存中的页面建立页表入口

- fd: 要映射到内存中的文件描述符
- offset: 文件映射的偏移量，通常设置为 0，表示从文件起始位置对应，offset 必须是 page size 的整数倍

返回值：

- 若映射成功，mmap() 返回映射区的内存起始地址，munmap() 返回 0
- 若映射失败，mmap() 返回 MAP_FAILED，其值为(void *)-1，munmap() 返回 -1

## 2. mmap 读

```cpp
int fd = open(file_name.c_str(), O_RDONLY);
//  读取文件长度
int len = lseek(fd, 0, SEEK_END);
//  建立映射
char *buffer = (char *) mmap(NULL, len, PROT_READ, MAP_PRIVATE, fd, 0);
close(fd);

//  do something

//  关闭映射
munmap(buffer, len);
```

## 3. mmap 写

```cpp
int len = data.length();
// 打开文件
int fd = open(file_name.c_str(), O_RDWR | O_CREAT, 00777);
// lseek将文件指针往后移动 len - 1 位
lseek(fd, len - 1, SEEK_END);
// 预先写入一个空字符；mmap不能扩展文件长度，这里相当于预先给文件长度，准备一个空架子
write(fd, " ", 1);
// 建立映射
char *buffer = (char *) mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
// 关闭文件
close(fd);
// 将 data 复制到 buffer 里
memcpy(buffer, data, len);
// 关闭映射
munmap(buffer, len)
```

## 4. mmap 多进程写

不管是父子进程还是无亲缘关系的进程，都可以将自身用户空间映射到同一个文件或匿名映射到同一片区域。从而通过各自对映射区域的改动，达到进程间通信和进程间共享的目的

这里以 8 进程为例

```cpp
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>


using namespace std;


const int PROCESS_COUNT = 8;
const int RESULT_SIZE = 20000;


void work(const string &file_name, int pid) {
    int fd = open(file_name.c_str(), O_RDWR | O_CREAT, 0666);
    char *buffer = (char *) mmap(NULL, RESULT_SIZE * 2, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    close(fd);

    int start = pid * RESULT_SIZE / PROCESS_COUNT;
    int end = start + RESULT_SIZE / PROCESS_COUNT;
    for (int i = start; i < end; ++i) {
        buffer[i << 1] = (i % 2 != 0 ? '1' : '0');
        buffer[i << 1 | 1] = '\n';
    }

    munmap(buffer, RESULT_SIZE * 2);
}


int main() {
    string predict_file = "result.txt";

    //  填充文件
    int fd = open(predict_file.c_str(), O_RDWR | O_CREAT, 0666);
    lseek(fd, RESULT_SIZE * 2 - 1, SEEK_SET);
    write(fd, " ", 1);
    close(fd);

    //  mmap多进程写
    int id;
    pid_t pid;
    vector<pid_t> pids;
    for (int i = 1; i < PROCESS_COUNT; i++) {
        id = i;
        pid = fork();
        if (pid <= 0) break;
        pids.push_back(pid);
    }

    if (pid == -1) {
        cerr << "startup process failed" << endl;
    } else {
        if (pid == 0) {
            work(predict_file, id); //  子进程
            exit(0);
        } else {
            work(predict_file, 0);  //  main进程
        }
    }

    exit(0);
}
```

## 5. 注意事项

mmap 映射区域大小必须是物理页大小（page size）的整倍数（32 位系统中通常是 4k 字节）。原因是，内存的最小粒度是页，而进程虚拟地址空间和内存的映射也是以页为单位，为了匹配内存的操作，mmap 从磁盘到虚拟地址空间的映射也必须是页

但是我们要读写的文件大小往往并不是 4k 的整数倍，因此在建立映射时一定要准确把握文件大小与映射区的 length 大小

- 若文件不是 4k 的整数倍，此时实际映射区域依然是 4k 的整数倍，剩余部分用 0 填充。尽管剩余部分不在文件范围内，但是依然可以正常读写，该部分内容的改变并不影响原文件。（比如文件大小为 8000 字节，则实际映射区域大小为 8192 字节，8000 ~ 8192 字节用 0 填充，并且该区域可以正常访问）

- 若设置映射区域大小远大于文件大小，比如文件大小 8000 字节，设置 length 为 100000 字节，则只有与文件相对应的物理页读写有效，即仅有前两页有效，对于 8192 ~ 100000 区域以及 100000 以外的区域，进程不能读写
