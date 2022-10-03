---
title: 记录整数反转的溢出问题
date: 2020-02-02 10:54:22
categories: [算法]
tags: [算法]
---

## Leetcode simple problem: Reverse Integer

给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。**注意**：假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [Integer.*``MIN_VALUE``*, Integer.*``MAX_VALUE``*]。请根据这个假设，如果反转后整数溢出那么就返回 0

<!-- more -->

## Thought

- 先不考虑溢出问题，对整数取反很简单，先把 x 不断对 10 取余，然后 result 乘 10 加上余数覆盖掉原来的 result，最后 x /= 10

- 对于溢出问题，就需要判断最终得到的 result 的范围是否合法，而问题是如果 result 已经溢出，那么 result 就不能是 int 类型，要扩充一下的它的存储空间，让它表示比 int 还要大的数，那么它的类型就必须是 long（_我没想到这点，提交了三遍都不对，最后看了评论才悟出来..._）

- 另外，官方给出的答案有点复杂的味道：

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2019/10/reverse-integer/reverse-integer.png" width="700">
</p>

> 图片来自 Leetcode 官方答案，链接：<https://leetcode-cn.com/problems/reverse-integer/solution/zheng-shu-fan-zhuan-by-leetcode/>

其实个人感觉才是最稳妥最万能的做法，因为如果按刚才的做法，用一个 long 类型来保存结果，那如果题目改成是对 long 类型的数进行取反呢，再去用 long long 类型保存结果吗，但是对于这个题目来说这确实是最巧妙的解法了

## Java Codes

```java
public int reverse(int x) {

	// 用long类型判断溢出
	long result = 0;

	while (x != 0) {
		result = result * 10 + x % 10;
		x /= 10;
	}

	return (int) ((result >= Integer.MIN_VALUE && result <= Integer.MAX_VALUE) ? result : 0);

}
```

## Notes

> Integer.MIN_VALUE(-2^31)： -2147483648\
> Integer.MAX_VALUE(2^31-1)： 2147483647

> 函数 Math.pow(a, b)，返回的是 a 的 b 次方，类型是 Double\
> a ^ b 得到的也是 a 的 b 次方，但是返回的是 Integer 类型
