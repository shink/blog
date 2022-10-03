---
title: 微信小程序：生成随机且不重复字符
date: 2020-02-02 10:58:43
categories: [小程序]
tags: [小程序]
---

## Thought

第一步，产生一个随机 code

第二步，从数据库中查询这个 code

第三步，判断，若已存在则退回第一步，若不存在则返回这个 code

> 不难发现这是一个递归的过程，而跳出递归的条件就是中途出错或者已经找到不重复的 code。

<!-- more -->

## Promise Style

fileUtil.js 中

```javascript
/**
 * 产生一个不重复的code
 */
function generateCode() {
  let promise = new Promise(function(resolve, reject) {
    let code = getRandomCode();

    queryCode(code).then(res => {
      if (res[0]) {
        //  需要结束
        resolve(res[1]);
      } else {
        //  重复，不能结束，进行递归
        return generateCode();
      }
    });
  });

  return promise;
}

/**
 * 产生四位数字+字母随机字符
 */
function getRandomCode() {
  let code = "";
  const array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 
  'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 
  'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

  for (let i = 0; i < 4; i++) {
    let id = Math.round(Math.random() * 61);
    code += array[id];
  }
  return code;
}

/**
 * 从云数据库中查询code
 */
function queryCode(code) {
  let promise = new Promise(function(resolve, reject) {
    //  result[0] 代表是否需要结束，true：需要结束，false：不需要结束
    var result = [false, ""];

    wx.cloud.callFunction({
      name: "query-code",
      data: {
        code: code
      },
      success: res => {
        let data = res.result.data;

        if (data.length === 0) {
          //  查询成功，code未重复
          result = [true, code];
        } else {
          //  查询成功，code重复,则继续生成code并判断
          result[0] = false;
        }
      },
      fail: error => {
        //  查询失败
        result[0] = true;
      },
      complete: () => {
        resolve(result);
      }
    });
  });

  return promise;
}
```

## Test

detail.js 中

```javascript
fileUtil.generateUrl(this.data.fileID).then(res => {
  console.log(res);
});
```
