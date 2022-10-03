---
title: Markdown 语法之数学公式
date: 2020-02-02 11:11:33
categories: [Markdown]
tags: [Markdown]
---

**注**：VS Code中需安装插件，如 Markdown All in One

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/markdown-math/markdown-plugin.png" width="650">
</p>

<!-- more -->

## 1. 使用 `$` 包裹公式

使用 `$` 或 `$$` 包裹公式，被包裹的内容会全部展示为 `LaTex` 公式（使用 `$$` 包裹的公式会独占一行且水平居中）

> **小贴士**：字体控制，可以使公式更加美观，符号：`\displaystyle`  
   不使用字体控制的情况：\$\frac{x+y}{y+z}\$，效果：$\frac{x+y}{y+z}$     
   使用字体控制的情况：\$\displaystyle \frac{x+y}{y+z}\$，效果：$\displaystyle \frac{x+y}{y+z}$

## 2. 括号、分隔符

1. **下划线**，符号：`\underline` 或 `<u></u>`  
   如：\$\underline{x + y + z}\$，效果：$\underline{x + y + z}$

2. **上大括号**，符号：`\overbrace{算式}`   
   如：\$\overbrace{a+b+c+d}^{2.0}\$，效果：$\overbrace{a+b+c+d}^{2.0}$

3. **下大括号**，符号：`\underbrace{算式}`  
   如：\$a+\underbrace{b+c}_{1.0}+d\$，效果：$a+\underbrace{b+c}_{1.0}+d$

4. **上位符号**，符号：`\stacrel{上位符号}{基位符号}`   
   如：\$\vec{x}\stackrel{\mathrm{def}}{=}{x_1,\cdots,x_n}\$，效果：$\vec{x}\stackrel{\mathrm{def}}{=}{x_1,\cdots,x_n}$

5. **自适应括号**，符号：`\left符号 内容 \right符号`     
   在配对符号中可以让括号自动适应公式的高度，如：   
   \$\displaystyle \left( \frac{x}{2} \right)\$，效果：$\displaystyle \left( \frac{x}{2} \right)$
   
   **另**：在非配对符号中，使用 `\left. 内容 \right符号` 或 `\left符号 内容 \right.`（注意：有个 `.` ）

   如：\$\displaystyle \left. \frac{du}{dx} \right|_{x=0}\$，效果：$\displaystyle \left. \frac{du}{dx} \right|_{x=0}$

## 3. 公式编号

**注意**：需编号的公式必须独占一行且居中，即 **必须使用 `$$` 符号**

常用 `\tag{编号}` 或 `\tag*{编号}`

|     编号      |                         说明                         |
| :-----------: | :--------------------------------------------------: |
| `\tag{编号}`  | 公式宏包序号设置命令，可用于带星号公式环境中的公式行 |
| `\tag*{编号}` |    作用与 \tag 相同，只是标号两侧 **没有圆括号**     |

例如：

> \$\$ x^2+y^2=z^2 \\tag{\$1.1\$} \$\$
>   
> \$\$ x^2+y^2=z^2 \\tag*{\$1.2\$} \$\$

效果：

$$ x^2+y^2=z^2 \tag{$1.1$} $$
$$ x^2+y^2=z^2 \tag*{$1.2$} $$


## 4. 变量表示

| 描述  |      符号      |     表达式     |
| :---: | :------------: | :------------: |
| 上标  |     $x^2$      |     `x^2`      |
| 下标  |     $y_4$      |     `y_4`      |
| 矢量  |   $\vec{a}$    |   `\vec{a}`    |
|       |   $\hat{a}$    |   `\hat{a}`    |
|       |  $\check{a}$   |  `\check{a}`   |
|       |  $\breve{a}$   |  `\breve{a}`   |
|       |  $\tilde{a}$   |  `\tilde{a}`   |
|       |   $\bar{a}$    |   `\bar{a}`    |
|       |  $\acute{a}$   |  `\acute{a}`   |
|       | $\mathring{a}$ | `\mathring{a}` |

## 5. 其他常用符号

|       描述       |         符号         |    表达式     |
| :--------------: | :------------------: | :-----------: |
|       无穷       |       $\infty$       |   `\infty`    |
|      上箭头      |      $\uparrow$      |  `\uparrow`   |
|    加粗上箭头    |      $\Uparrow$      |  `\Uparrow`   |
|      下箭头      |     $\downarrow$     | `\downarrow`  |
|    加粗下箭头    |     $\Downarrow$     | `\Downarrow`  |
|      左箭头      |     $\leftarrow$     | `\leftarrow`  |
|    加粗左箭头    |     $\Leftarrow$     | `\Leftarrow`  |
|      右箭头      |    $\rightarrow$     | `\rightarrow` |
|    加粗右箭头    |    $\Rightarrow$     | `\Rightarrow` |
| 底端对齐的省略号 |    $1,2,\ldots,n$    |   `\ldots`    |
| 中线对齐的省略号 | $1 + 2 + \cdots + n$ |   `\cdots`    |
| 竖直对齐的省略号 |       $\vdots$       |   `\vdots`    |
|  斜对齐的省略号  |       $\ddots$       |   `\ddots`    |

## 6. 数学运算

1. **除法运算（分数表示）**，符号：`\frac{分子}{分母}` 或 `分子 \over 分母`     
如：\$\frac{1-x}{y+1}\$ 或 \$x \over x+y\$，效果：$\frac{1-x}{y+1}$ 或 $x \over x+y$

2. **平均数运算**，符号：`\overline{算式}`  
如：\$\overline{x + y + z}\$，效果：$\overline{x + y + z}$

3. **开方运算**，符号：`\sqrt[开方数]{被开方数}` （开二次方可直接使用 `\sqrt 被开方数` ）    
如：\$\sqrt x\$，效果：$\sqrt x$    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\$\sqrt[3] y\$，效果：$\sqrt[3] y$

4. **对数运算**，符号：`\log_低数{真数}`   
如：\$\log_5{8}\$，效果：$\log_5{8}$

5. **极限运算**，符号：`\lim`   
如：\$\lim_{x \to +\infty}{\frac{1}{x}}\$，效果：$\lim_{x \to +\infty}{\frac{1}{x}}$

> 建议搭配 `\displaystyle` 使用：\$\displaystyle \lim_{x \to +\infty}{\frac{1}{x}}\$，效果：$\displaystyle \lim_{x \to +\infty}{\frac{1}{x}}$

6. **求和运算**，符号：`\sum`   
如：\$\sum^{+\infty}_{i = 1}{\frac{1}{i}}\$，效果：$\sum^{+\infty}_{i = 1}{\frac{1}{i}}$

> 建议搭配 `\displaystyle` 使用：\$\displaystyle \sum^{+\infty}_{i = 1}{\frac{1}{i}}\$，效果：$\displaystyle \sum^{+\infty}_{i = 1}{\frac{1}{i}}$

7. **积分运算**，符号：`\int`

|   积分   |   符号   |  表达式  |
| :------: | :------: | :------: |
|  定积分  |  $\int$  |  `\int`  |
| 二重积分 | $\iint$  | `\iint`  |
| 三重积分 | $\iiint$ | `\iiint` |
| 曲线积分 | $\oint$  | `\oint`  |
| 曲面积分 | $\oiint$ | `\oiint` |

如：\$\int^{\infty}_{1}{\frac{1}{x}dx}\$，效果：$\int^{\infty}_{1}{\frac{1}{x}dx}$

> 建议搭配 `\displaystyle` 使用：\$\displaystyle \int^{\infty}_{1}{\frac{1}{x}dx}\$，效果：$\displaystyle \int^{\infty}_{1}{\frac{1}{x}dx}$

8. **偏微分运算**，符号：`\partial`     
如：\$\frac{\partial xy^2}{\partial y}\$，效果：$\frac{\partial xy^2}{\partial y}$

> 建议搭配 `\displaystyle` 使用：\$\displaystyle \frac{\partial xy^2}{\partial y}\$，效果：$\displaystyle \frac{\partial xy^2}{\partial y}$

9. **矩阵表示**，符号：`\begin{matrix} \end{matrix}`    
如：    
> \$\$A=     
> \\left(\\begin\{matrix\}   
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{11\} \&x\_\{12\} \&x\_\{13\} \&\\cdots \&x\_\{1n\} \\\   
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{21\} \&x\_\{22\} \&x\_\{23\} \&\\cdots \&x\_\{2n\} \\\   
> &nbsp;&nbsp;&nbsp;&nbsp;\\vdots \&\\vdots \&\\vdots \&\\ddots \&\\vdots \\\   
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{n1\} \&x\_\{n2\} \&x\_\{n3\} \&\\cdots \&x\_\{nn\}  
> \\end\{matrix\} \\right)\$\$

效果：

$$A=
\left(\begin{matrix}
    x_{11} &x_{12} &x_{13} &\cdots &x_{1n} \\
    x_{21} &x_{22} &x_{23} &\cdots &x_{2n} \\
    \vdots &\vdots &\vdots &\ddots &\vdots \\
    x_{n1} &x_{n2} &x_{n3} &\cdots &x_{nn}
\end{matrix} \right)$$

用竖线将矩阵分割为 `(A|b)` 形式，如：

> \$\$(A|b)=  
> \\left(\\begin\{array\}\{ccccc\|c\}     
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{11\} \&x\_\{12\} \&x\_\{13\} \&\\cdots \&x\_\{1n\} \&b\_1 \\\     
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{21\} \&x\_\{22\} \&x\_\{23\} \&\\cdots \&x\_\{2n\} \&b\_2 \\\     
> &nbsp;&nbsp;&nbsp;&nbsp;\\vdots \&\\vdots \&\\vdots \&\\ddots \&\\vdots \&\\vdots \\\      
> &nbsp;&nbsp;&nbsp;&nbsp;x\_\{n1\} \&x\_\{n2\} \&x\_\{n3\} \&\\cdots \&x\_\{nn\} \&b\_n     
> \\end\{array\} \\right)\$\$

效果：

$$(A|b)=
\left(\begin{array}{ccccc|c}
    x_{11} &x_{12} &x_{13} &\cdots &x_{1n} &b_1 \\
    x_{21} &x_{22} &x_{23} &\cdots &x_{2n} &b_2 \\
    \vdots &\vdots &\vdots &\ddots &\vdots &\vdots \\
    x_{n1} &x_{n2} &x_{n3} &\cdots &x_{nn} &b_n
\end{array} \right)$$

## 7. 逻辑运算

|  逻辑描述  |   符号    |  表达式   |
| :--------: | :-------: | :-------: |
|  大于等于  |  $\geq$   |  `\geq`   |
|  小于等于  |  $\leq$   |  `\leq`   |
|   不等于   |  $\neq$   |  `\neq`   |
| 不大于等于 |  $\ngeq$  |  `\ngeq`  |
| 不小于等于 |  $\nleq$  |  `\nleq`  |
|   约等于   | $\approx$ | `\approx` |
|   恒等于   | $\equiv$  | `\equiv`  |

## 8. 集合运算

|   描述   |                符号                 |               表达式                |
| :------: | :---------------------------------: | :---------------------------------: |
|   属于   |                $\in$                |                `\in`                |
|  不属于  |              $\notin$               |              `\notin`               |
|   子集   |      $\subseteq$ , $\supseteq$      |      `\subseteq` , `\supseteq`      |
|  非子集  |  $\not\subseteq$ , $\not\supseteq$  |  `\not\subseteq` , `\not\supseteq`  |
|  真子集  |     $\subsetneq$ , $\supsetneq$     |     `\subsetneq` , `\supsetneq`     |
| 非真子集 | $\not\subsetneq$ , $\not\supsetneq$ | `\not\subsetneq` , `\not\supsetneq` |
|   交集   |               $\cap$                |               `\cap`                |
|   并集   |               $\cup$                |               `\cup`                |
|   差集   |             $\setminus$             |             `\setminus`             |
|   同或   |             $\bigodot$              |             `\bigodot`              |
|   同与   |            $\bigotimes$             |            `\bigotimes`             |
|   异或   |             $\bigoplus$             |             `\bigoplus`             |

## 9. 希腊字母

将部分符号的表达式首字母大写，即为相应符号的大写形式

|   小写符号    |    表达式     |  大写符号  |   表达式   |
| :-----------: | :-----------: | :--------: | :--------: |
|   $\alpha$    |   `\alpha`    |  $\Alpha$  |  `\Alpha`  |
|    $\beta$    |    `\beta`    |  $\Beta$   |  `\Beta`   |
|   $\gamma$    |   `\gamma`    |  $\Gamma$  |  `\Gamma`  |
|   $\delta$    |   `\delta`    |  $\Delta$  |  `\Delta`  |
|  $\epsilon$   |  `\epsilon`   | $\Epsilon$ | `\Epsilon` |
|     $\mu$     |     `\mu`     |   $\Mu$    |   `\Mu`    |
| $\varepsilon$ | `\varepsilon` |            |            |
|    $\zeta$    |    `\zeta`    |  $\Zeta$   |  `\Zeta`   |
|    $\eta$     |    `\eta`     |   $\Eta$   |   `\Eta`   |
|   $\theta$    |   `\theta`    |  $\Theta$  |  `\Theta`  |
|  $\vartheta$  |  `\vartheta`  |            |            |
|     $\pi$     |     `\pi`     |   $\Pi$    |   `\Pi`    |
|    $\phi$     |    `\phi`     |   $\Phi$   |   `\Phi`   |
|    $\psi$     |    `\psi`     |   $\Psi$   |   `\Psi`   |
|   $\omega$    |   `\omega`    |  $\Omega$  |  `\Omega`  |
|    $\rho$     |    `\rho`     |   $\Rho$   |   `\Rho`   |
|   $\sigma$    |   `\sigma`    |  $\Sigma$  |  `\Sigma`  |
|     $\xi$     |     `\xi`     |   $\Xi$    |   `\Xi`    |
|  $\partial$   |  `\partial`   |            |            |

## 10. 字体

1. **黑板粗体**（Blackboard bold），符号：`\mathbb{内容}`

|     字体     |    显示效果     |      表达式       |
| :----------: | :-------------: | :---------------: |
|     普通     |      abcd       |      `abcd`       |
| 普通数学形式 |     $abcd$      |     `$abcd$`      |
|     小写     | $\mathbb{abcd}$ | `$\mathbb{abcd}$` |
|     大写     | $\mathbb{ABCD}$ | `$\mathbb{ABCD}$` |

2. **正粗体**，符号：`\mathbf{内容}`

|   字体   |    显示效果     |      表达式       |
| :------: | :-------------: | :---------------: |
|   普通   |      abcd       |      `abcd`       |
| 普通加粗 |    **abcd**     |    `**abcd**`     |
|   小写   | $\mathbf{abcd}$ | `$\mathbf{abcd}$` |
|   大写   | $\mathbf{ABCD}$ | `$\mathbf{ABCD}$` |

3. **斜体数字**，符号：`\mathit{内容}`

|   字体   |     显示效果      |       表达式        |
| :------: | :---------------: | :-----------------: |
|   普通   |      3.1415       |      `3.1415`       |
| 普通斜体 |     *3.1415*      |     `*3.1415*`      |
|   斜体   | $\mathit{3.1415}$ | `$\mathit{3.1415}$` |

4. **罗马体**，符号：`\mathrm{内容}`

|     字体     |    显示效果     |      表达式       |
| :----------: | :-------------: | :---------------: |
|     普通     |      ABCD       |      `ABCD`       |
| 普通数学形式 |     $ABCD$      |     `$ABCD$`      |
|    罗马体    | $\mathrm{ABCD}$ | `$\mathrm{ABCD}$` |

5. **哥特体**，符号：`mathfrak{内容}`

|     字体     |     显示效果      |       表达式        |
| :----------: | :---------------: | :-----------------: |
|     普通     |       abcd        |       `abcd`        |
| 普通数学形式 |      $abcd$       |      `$abcd$`       |
|     小写     | $\mathfrak{abcd}$ | `$\mathfrak{abcd}$` |
|     大写     | $\mathfrak{ABCD}$ | `$\mathfrak{ABCD}$` |

6. **手写体**，符号：`\mathcal{内容}`

|     字体     |     显示效果     |       表达式       |
| :----------: | :--------------: | :----------------: |
|     普通     |       abcd       |       `abcd`       |
| 普通数学形式 |      $abcd$      |      `$abcd$`      |
|     小写     | $\mathcal{abcd}$ | `$\mathcal{abcd}$` |
|     大写     | $\mathcal{ABCD}$ | `$\mathcal{ABCD}$` |
