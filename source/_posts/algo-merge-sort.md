---
title: Java 分治策略实现归并排序
date: 2020-02-02 11:03:10
categories: [算法]
tags: [算法, Java]
---

## Thought

能不能使用分治策略的关键是 **子问题的最优解是否可以通过某种手段得到原问题的最优解**。对于归并排序，将两个已经有序的子问题序列进行合并，就可得到一个有序序列，以此类推，最终可将所有子问题序列合并成一个有序序列，而得到的有序序列就是最终答案。

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/merge-sort/merge-sort.png" width="800">
</p>

<!-- more -->

> 图片来自简书，链接：<https://www.cnblogs.com/chengxiao/p/6194356.html>

至于如何合并，直接想到的就是开辟一个新空间，拿这两个子问题序列元素一一比对，将元素有序放到新空间里。

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/merge-sort/merge.png" width="800">
</p>

> 图片来自简书，链接：<https://www.cnblogs.com/chengxiao/p/6194356.html>

## Java Codes

```java
public class MergeSort {

	public MergeSort() {

	}

	public void mergeSort(double[] array) {
//		开辟一个临时数组，避免在递归中频繁开辟空间
		double[] result = new double[array.length];
		mergeSort(array, 0, array.length - 1, result);
	}

	public void mergeSort(double[] array, int left, int right, double[] result) {
		if (left < right) {
			int mid = (left + right) / 2;
			mergeSort(array, left, mid, result);
			mergeSort(array, mid + 1, right, result);

//			将两个子问题序列合并
			merge(array, left, mid, right, result);
		}
	}

	private void merge(double[] array, int left, int mid, int right, double[] result) {
		int i = left;
		int j = mid + 1;
		int k = 0;

		while (i <= mid && j <= right) {
			if (array[i] >= array[j]) {
				result[k++] = array[j++];
			} else {
				result[k++] = array[i++];
			}
		}

//		将剩余的左子问题序列填充到result中
		while (i <= mid) {
			result[k++] = array[i++];
		}

//		将剩余的右子问题序列填充到result中
		while (j <= right) {
			result[k++] = array[j++];
		}

//		将result中元素填充到原序列中，以便继续排序
		i = left;
		k = 0;
		while (i <= right) {
			array[i++] = result[k++];
		}
	}

}
```

## Test

```java
public static void main(String[] args) {
//  随机产生double数组
    int length = 1000000;
	long start, end;
	double[] array = new double[length];
	for (int i = 0; i < length; i++) {
        double num = Math.random() * 10;
//      将double值精确到小数点后两位
        num = new BigDecimal(num).setScale(2, BigDecimal.ROUND_HALF_UP).doubleValue();
        array[i] = num;
    }
    System.out.println(Arrays.toString(array));

//	归并排序开始
    start = System.currentTimeMillis(); // 获取开始时间

    MergeSort mergeSort = new MergeSort();
    mergeSort.mergeSort(array);

    end = System.currentTimeMillis(); // 获取结束时间
    System.out.println("归并排序运行时间： " + (end - start) + "ms");
    System.out.println(Arrays.toString(array));
}
```

## Time Complexity

归并排序的开销除了递归求解子问题外，还需要将子问题合并，开销为 $O(n)$

故，归并排序的时间复杂度等式为：$T(n) = 2T(n/2) + O(n)$

根据算法时间复杂度的 master 方法，此时 $a = 2, b = 2, \log_b{a} = 1$

由于 $f(n) = n = \Theta(n^{\log_b{a}})$ （简单起见，假定$f(n) = O(n) = n$）, 满足 master 方法的 case 2, 故时间复杂度为：

$T(n) = \Theta(n^{\log_b{a}}logn) = \Theta(nlogn)$

归并排序无论在什么情况下都需要对每一个子问题进行排序，所以它的最好、最坏、平均情况的时间复杂度均为 $O(nlogn)$
