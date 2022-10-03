---
title: Java 求最大子数组
date: 2020-02-02 11:04:23
categories: [算法]
tags: [算法, Java]
---

## Background

在某天购入股票后抛出，求如何取得最大利润。已知股票趋势如图所示。

<p align="center">
	<img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/max-subarray/background.png" width="700">
</p>

## Thought

我们都知道——`利润 = 售价 - 成本`，即两者之差越大则利润越大。要求利润的最大值，不妨先计算出当天与前一天股价的差，得到的股价浮动数组，然后找其最大子数组，即为原问题的解。

对于最大子数组，最简单粗暴的方法就是两层 for，遍历所有子数组后，自然能求出最大子数组。

更好的解决办法是用**分治策略**。将原问题分解为两个子问题 left 和 right，设跨过两个子问题中点的数组为 cross，比较 left、right 和 cross 的最大值即为原问题的最优解。

<!-- more -->

## Brute Force

```java
public class MaxSubarray {

	private int[] variation;

	public MaxSubarray(int[] array) {
		variation = new int[array.length - 1];
		for (int i = 0; i < array.length - 1; ++i) {
			variation[i] = array[i + 1] - array[i];
		}
	}

//  暴力法
	public void bruteForce() {

		int sum = 0;
		int start = 0;
		int end = 0;

		for (int i = 0; i < variation.length; ++i) {
			int temp = 0;

			for (int j = i; j < variation.length; ++j) {
				temp += variation[j];

				if (temp > sum) {
					sum = temp;
					start = i;
					end = j;
				}
			}
		}

		System.out.println("maxPrice： " + sum + "，index： [" + start + ", " + end + "]");
	}
}
```

## Divide and Conquer

- Divide: Divide the array A[low..high] into two subarrays of n/2 elements, A[low..mid] and A[mid+1..high].
- Conquer: Find the maximum subarray recursively.
- Combine: Select a subarray with the largest sum of the sub-problems’.

> 分：将数组从中间一分为二\
> 治：递归寻找最大子数组\
> 合并：选出子问题中和最大的子数组

## Pseudo Code

递归寻找数组中子数组的最大值

`数组的最大值 = max{左子数组的最大值, 从中间向两边展开的数组的最大值, 右子数组的最大值}`

<p align="center">
	<img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/max-subarray/max-subarray-code.png" width="700">
</p>

<br>

寻找从中间位置向两边展开的数组的最大值

<p align="center">
	<img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/max-subarray/cross-code.png" width="700">
</p>

## Example

<p align="center">
	<img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/max-subarray/example.png" width="700">
</p>

## Java Codes

```java
public class MaxSubarray {

	private int[] variation;

	public MaxSubarray(int[] array) {
		variation = new int[array.length - 1];
		for (int i = 0; i < array.length - 1; ++i) {
			variation[i] = array[i + 1] - array[i];
		}
	}

	public int divideConquer() {
		return divideConquer(variation, 0, variation.length - 1);
	}

	private int divideConquer(int[] array, int left, int right) {
		if (left == right) {
			return array[left];
		} else {
			int mid = (left + right) / 2;
			int left_sum = divideConquer(array, left, mid);
			int right_sum = divideConquer(array, mid + 1, right);
			int cross_sum = crossing(array, left, mid, right);

//			比较三者最大值
			return left_sum > cross_sum ? (left_sum > right_sum ? left_sum : right_sum)
					: (cross_sum > right_sum ? cross_sum : right_sum);
		}
	}

//	求cross
	private int crossing(int[] array, int left, int mid, int right) {
		int temp_left = -99999;
		int temp_right = -99999;

//		从mid向前求最大值
		int sum = 0;
		for (int i = mid; i >= left; --i) {
			sum += array[i];
			if (sum > temp_left) {
				temp_left = sum;
			}
		}

//		从mid+1向后求最大值
		sum = 0;
		for (int j = mid + 1; j < right; ++j) {
			sum += array[j];
			if (sum > temp_right) {
				temp_right = sum;
			}
		}
		return temp_left + temp_right;
	}

}
```

## Test

```java
public static void main(String[] args) {
	int[] array = { 100, 113, 110, 85, 105, 102, 86, 63, 81, 101, 94, 106, 101, 79, 94, 90, 97 };
		MaxSubarray maxSubarray = new MaxSubarray(array);
		maxSubarray.bruteForce();
		System.out.println("分治：" + maxSubarray.divideConquer());
}
```

## Time Complexity

- 暴力法：$O(n^2)$

- 分治法：

对于规模为 $n$ 的数组，除了递归搜索左、右子数组外，还需要求 cross（开销为 $O(n)$），以及比较三个值的大小（开销为 $O(1)$）

故：$T(n) = 2T(n/2) + O(n) + O(1)$

根据算法时间复杂度的 master 方法，此时 $a = 2, b = 2, \log_b{a} = 1$

由于 $f(n) = n + 1 = \Theta(n^{\log_b{a}})$ （简单起见，假定$f(n) = O(n) + O(1) = n + 1$）, 满足 master 方法的 case 2, 故时间复杂度为：

$T(n) = \Theta(n^{\log_b{a}}logn) = \Theta(nlogn)$
