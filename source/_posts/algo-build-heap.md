---
title: Java 建立大顶堆
date: 2020-02-02 11:00:11
categories: [算法]
tags: [算法, Java]
---

## Thought

- 从最后一个有孩子的父节点开始调整，若父节点的值小于左右孩子结点的值（如果有的话），就与该孩子结点交换位置。若发生了交换，由于原来父节点到了他的孩子结点上，可能破坏了现在这颗以原来父节点为根节点的子树，所以需要重复以上步骤，即递归。
- 数组的范围是从 0 ~ length - 1，设父节点的下标为 p，则：

```
p的左孩子下标为：2 * p + 1
p的右孩子下标为：2  *p + 2
```

> 最后一个有孩子的父节点下标为（length - 2）/ 2

<!-- more -->

## Java Codes

```java
public class BuildHeap {

	public void heapify(int[] heap, int item) {
		int length = heap.length;
		int left = 2 * item + 1;
		int right = 2 * item + 2;

		int largest;
		if (left <= length - 1 && heap[left] > heap[item]) {
			largest = left;
		} else {
			largest = item;
		}
		if (right <= length - 1 && heap[right] > heap[largest]) {
			largest = right;
		}
		if (largest != item) {
			// 父节点小于左右孩子结点,需要交换
			int temp = heap[item];
			heap[item] = heap[largest];
			heap[largest] = temp;

			// 发生过交换后,原来父结点现在所在位置的值不一定还满足大顶堆的定义，需要递归继续建堆
			heapify(heap, largest);
		}

	}

	public void build(int[] heap) {
		int length = heap.length;
		// 最后一个有孩子的结点的下标
		int lastParent = (length - 2) / 2;
		for (int item = lastParent; item >= 0; item--) {
			heapify(heap, item);
		}
	}

}
```

## Test

```java
public class Test {

	public static void main(String[] args) {

		BuildHeap buildHeap = new BuildHeap();
		int[] heap = new int[] { 1, 2, 16, 14, 8, 7 };
		buildHeap.build(heap);
		System.out.println(Arrays.toString(heap));
	}

}
```
