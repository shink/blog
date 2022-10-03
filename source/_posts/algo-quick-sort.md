---
title: Java 分治策略实现快速排序
date: 2020-02-02 11:01:57
categories: [算法]
tags: [算法, Java]
---

## Thought

- Divide: Partition the array into two subarrays around a pivot x such that elements in lower subarray ≤ x ≤ elements in upper subarray.
- Conquer: Recursively sort the subarrays.
- Combine: Trivial.

> 以枢轴 x 为中点，每次排序将小于枢轴 x 的元素都放在 x 左边，大于 x 的元素都放在 x 右边，然后递归以同样方式对子数组排序

<!-- more -->

## Pseudo Code

递归求解两个子序列

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/quick-sort/quick-sort-code.png" width="700">
</p>

划分序列，返回枢轴 x

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2019/12/quick-sort/partition-code.png" width="700">
</p>

## Java Codes

```java
public class QuickSort {

	public void quickSort(double[] array) {
		quickSort(array, 0, array.length - 1);
	}

	public void quickSort(double[] array, int left, int right) {
		if (left < right) {
//			枢轴
			int pivot = partition(array, left, right);
			quickSort(array, left, pivot - 1);
			quickSort(array, pivot + 1, right);
		}
	}

	public int partition(double[] array, int left, int right) {
		int i = left;
		int j = right;

		while (i < j) {
			while (i < j && array[i] <= array[j]) {
				j--;
			}
			if (i < j) {
				double temp = array[j];
				array[j] = array[i];
				array[i] = temp;
				i++;
			}

			while (i < j && array[i] <= array[j]) {
				i++;
			}
			if (i < j) {
				double temp = array[j];
				array[j] = array[i];
				array[i] = temp;
			}
		}

		return i;
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

//	快速排序开始
    start = System.currentTimeMillis(); // 获取开始时间

   QuickSort quickSort = new QuickSort();
    quickSort.quickSort(array);

    end = System.currentTimeMillis(); // 获取结束时间
    System.out.println("快速排序运行时间： " + (end - start) + "ms");
    System.out.println(Arrays.toString(array));
}
```

## Time Complexity

### best-case

快速排序最优的情况就是**每一次取到的元素都刚好平分整个数组**

此时的时间复杂度等式为：$T(n) = 2T(n/2) + O(n)$。$T(n/2)$ 为平分后的子数组的时间复杂度，$O(n)$ 为平分这个数组时所花的时间

根据算法时间复杂度的 master 方法，此时 $a = 2, b = 2, \log_b{a} = 1$

由于 $f(n) = n = \Theta(n^{\log_b{a}})$ （简单起见，假定$f(n) = O(n) = n$）, 满足 master 方法的 case 2, 故时间复杂度为：

$T(n) = \Theta(n^{\log_b{a}}logn) = \Theta(nlogn)$

**故最优情况下时间复杂度为：$O(nlogn)$**

### worst-case

最差的情况就是每一次取到的元素刚好是数组中最小/最大的，这种情况就退化成冒泡排序了(每一次都选好一个元素的位置)

**故最坏情况下时间复杂度为：$O(n^2)$**

> 可以通过随机选择枢轴来避免最坏情况的发生

### average-case

**平均复杂度: $O(nlogn)$**
