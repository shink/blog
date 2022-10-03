---
title: Cloudflare Workers 实现301网址跳转
date: 2020-02-02 11:15:56
categories: [Cloudflare]
tags: [Cloudflare]
---

本文将介绍如何基于 Cloudflare Workers 使用 Node.js 实现一个网址跳转服务，并自定义域名

## Cloudflare Workers

- 在边缘运行代码，提供强大的 Web 可扩展性

- 在边缘应用 <u>自定义安全规则</u> 和 <u>过滤逻辑</u> 来检测恶意 Bots 病毒并防止它们消耗资源，从而提高安全性。

- 将更多个性化和交互性纳入静态 HTML 页面，并在边缘运行动态请求，从而改善用户体验。

- 将更多操作流程和请求处理转移到边缘，以提高缓存命中率并降低带宽成本，从而降低运营成本。

> Cloudflare Workers 可以通过自定义安全规则和过滤逻辑来提高网站的安全性，因此，`我们可以通过 t.domain1.com\blog 301重定向到真实地址，如：blog.domain2.com`，达到隐藏真实地址的目的

<!-- more -->

## 步骤

### 1. 创建 Workers

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/cf-workers-redirect/workers1.png" width="800">
</p>

点击创建 Worker

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/cf-workers-redirect/workers2.png" width="800">
</p>

代码的主要思想是：对于诸如 **to\.domain1\.com\/blog** 这样的请求，截取 `/` 后面的内容并查询 **redirectMap**，然后 301 跳转到相应网址，如 **blog\.domain2\.com**

代码如下，只需要根据需求自己修改 **redirectMap** 的内容就行了

```javascript
async function handleRequest(request) {
  let requestURL = new URL(request.url)
  let path = requestURL.pathname.split('/')[1]
  let location = redirectMap[path]
  if (location) {
    return Response.redirect(location, 301)
  }
  return fetch(request)
}
addEventListener('fetch', async event => {
  event.respondWith(handleRequest(event.request))
})

const redirectMap = {
  blog: 'https://blog.tsund.cn/'
}
```

### 2. 自定义域名

**注意**：要使用的域名必须是由 Cloudflare 管理的

进入 Cloudflare 的域名界面后，点击 Workers 标签，并添加一条 route

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/cf-workers-redirect/workers3.png" width="800">
</p>

然后是配置 route，可以使用通配符

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/cf-workers-redirect/workers4.png" width="600">
</p>

**注意**：如果是二级域名，需要先给这个二级域名添加一条 CNAME 记录，否则跳转会有问题。`Workers 会在 CNAME 之前拦截请求，只有未被拦截的才会走 CNAME 记录的地址。` 所以这个根据自己需求就可以了

至此，就实现了通过 Cloudflare Workers 实现 301 网址跳转，达到隐藏目标网址的目的

如：[https://t.shenke.codes/blog](https://t.shenke.codes/blog "点击跳转") 会跳转到 https:\/\/blog\.tsund\.cn

***

`更新`：如果 CNAME 记录指向的是 GitHub Pages 的页面，可能出现 404 错误，尽管仓库中已经定义好 404 页面，但是依然还是显示默认的 404 页面，影响浏览体验。这时可以通过修改 Workers 代码让所有的请求就都经 Cloudflare Workers 处理，但是 CNAME 记录依然不可以删掉（好像是该条 DNS 记录必须存在 😛）。修改后的代码如下：

```javascript
async function handleRequest(request) {
  let requestURL = new URL(request.url)
  let path = requestURL.pathname.split('/')[1]
  let location = redirectMap[path]
  if (location) {
    return Response.redirect(location, 301)
  } else {
    return Response.redirect('https://tsund.cn/404/', 301)
  }
}
addEventListener('fetch', async event => {
  event.respondWith(handleRequest(event.request))
})

const redirectMap = {
  '': 'https://tsund.cn/',
  'blog': 'https://blog.tsund.cn/'
}
```

这样，访问 [https://t.shenke.codes](https://t.shenke.codes "点击跳转") 就会跳转到 https:\/\/tsund\.cn，并且对于 **redirectMap** 中尚未定义的跳转规则，会跳转到自定义的 404 页面，从而提高用户浏览体验