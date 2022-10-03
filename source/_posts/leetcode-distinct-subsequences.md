---
title: "[LeetCode] 动态规划——不同的子序列"
date: 2021-03-17 19:36:48
categories: [算法]
tags: [算法, LeetCode]
---

## 题目描述

给定一个字符串 s 和一个字符串 t ，计算在 s 的子序列中 t 出现的个数

> 字符串的一个 子序列 是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串。（例如，"ACE" 是 "ABCDE" 的一个子序列，而 "AEC" 不是）

> 题目数据保证答案符合 32 位带符号整数范围

> 来源：力扣（LeetCode）    
> 链接：https://leetcode-cn.com/problems/distinct-subsequences  
> 著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处

<!-- more -->

### 示例

示例 1：

```
输入：s = "rabbbit", t = "rabbit"
输出：3
解释：
如下图所示, 有 3 种可以从 s 中得到 "rabbit" 的方案。
(上箭头符号 ^ 表示选取的字母)
rabbbit
^^^^ ^^
rabbbit
^^ ^^^^
rabbbit
^^^ ^^^
```

示例 2：

```
输入：s = "babgbag", t = "bag"
输出：5
解释：
如下图所示, 有 5 种可以从 s 中得到 "bag" 的方案。 
(上箭头符号 ^ 表示选取的字母)
babgbag
^^ ^
babgbag
^^    ^
babgbag
^    ^^
babgbag
  ^  ^^
babgbag
    ^^^
```

### 提示

- 0 <= s.length, t.length <= 1000

- s 和 t 由英文字母组成

## 解题思路

### 精选评论

1、为啥状态方程这样对？

我个人习惯 dp[i][j] 表示为 s[0-i] 和 t[0-j] 均闭区间的子序列个数，但这样不能表示s和t空串的情况，所以声明 int[][] dp = new int[m + 1][n + 1]; 这样 dp[0][x] 可以表示 s 为空串，dp[x][0] 同理

先不扣初始化的细节，假设 dp[i][j] 就是s[i] 和 t[j] 索引的元素子序列数量，为啥状态方程是： 

> s[i] == t[j] 时 dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
> s[i] != t[j] 时 dp[i][j] = dp[i-1][j]

先看s[i] == t[j] 时，以 s = "rara"，t = "ra" 为例，当 i = 3, j = 1 时，s[i] == t[j]，此时分为 2 种情况，s 串用最后一位的 a 或者 不用最后一位的 a，如果用 s 串最后一位的 a,那么 t 串最后一位的 a 也被消耗掉，此时的子序列其实等于 dp[i-1][j-1]

如果不用 s 串最后一位的 a，那就得看 "rar" 里面是否有 "ra" 子序列的了，就是 dp[i-1][j]，所以 dp[i][j] = dp[i-1][j-1] + dp[i-1][j]

再看s[i] != t[j] 比如 s = "rarb"，t = "ra" 还是当 i = 3, j = 1 时，s[i] != t[j]，此时显然最后的 b 想用也用不上啊。所以只能指望前面的 "rar" 里面是否有能匹配 "ra" 的，所以此时dp[i][j] = dp[i-1][j]

2：怎么想到这样的状态方程？

一点个人经验，见过的很多 2 个串的题，大部分都是 dp[i][j] 分别表示 s 串[0...i] 和 t 串[0...j] 怎么怎么样

然后都是观察 s[i] 和 t[j] 分等或者不等的情况，而且方程通常就是 dp[i-1][j-1] 要么 + 要么 || dp[i-1][j] 类似的

类似的题比如有

- 10：正则表达式匹配

- 44：通配符匹配 编辑距离

- 1143：最长公共子序列

> 以上内容摘录自评论

### 个人思考

dp[i][j] 表示 s[0-i) 的子序列中 t[0-j) 的数量，因此答案就是 dp[m][n]

要想得出状态 dp[i][j]，就需要考虑什么情况下可以从之前的状态转移而来，之前的状态相当于是 s[0-i) 的子串的子序列中 t[0-j) 的子串的数量，包括 dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]

因此与当前 s[0-i) 和 t[0-j) 的最后一个字符是否相等有关，若相等，则可以考虑从之前的状态转移过来

若 s[i - 1] == t[j - 1]，则 dp[i][j] = dp[i - 1][j - 1]，但是，上式只考虑了 dp[i - 1][j - 1]，未考虑 dp[i - 1][j] 和 dp[i][j - 1]

以示例中的 s = "rabbbit"，t = "rabbit" 为例，当 s = "rabb", t = "rab" 时，既可以从 s = "rab" 中搜索 t = "ra" ，也可以从 s = "rab" 中搜索 t = "rab"

而对于子状态 dp[i][j - 1]，尽管两子串最后一个字符已经相等，但是消耗掉 t[j] 的同时也必须消耗掉 s[j]，这样才能保证

若 s[i - 1] ！= t[j - 1]，显然，dp[i][j] = dp[i - 1][j]

## 代码

[github.com/shink/LeetCode](https://github.com/shink/LeetCode/blob/master/src/main/java/com/yuanhaoji/leetcode/dp/distinct_subsequences/Solution.java)

```java
public int numDistinct(String s, String t) {
    int m = s.length(), n = t.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 0; i <= m; i++) {
        dp[i][0] = 1;
    }

    for (int i = 0; i < m; i++) {
        for (int j = 0; j <= i && j < n; j++) {
            if (s.charAt(i) == t.charAt(j)) {
                dp[i + 1][j + 1] = dp[i][j] + dp[i][j + 1];
            } else {
                dp[i + 1][j + 1] = dp[i][j + 1];
            }
        }
    }

    return dp[m][n];
}
```
