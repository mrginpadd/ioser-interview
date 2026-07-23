# 缓存策略

## 【理论题】
**题目：** 请解释HTTP缓存机制，以及NSURLCache的常用缓存策略有哪些？
**答案：**

**HTTP缓存机制：**

```
┌─────────────────────────────────────────────────────┐
│                    HTTP缓存流程                       │
│                                                     │
│  客户端请求                                           │
│      │                                               │
│      ▼                                               │
│  检查本地缓存是否存在                                   │
│      │                                               │
│   存在 ──────┬─────── 不存在                         │
│      │       │             │                         │
│      ▼       ▼             ▼                         │
│  是否过期？  发请求         发请求                     │
│      │       │             │                         │
│   没过期     │             │                         │
│      │       │             │                         │
│      ▼       ▼             ▼                         │
│  返回缓存   304未修改     200新数据                    │
│             返回缓存       更新缓存                    │
└─────────────────────────────────────────────────────┘
```

**HTTP缓存头部：**

| 头部字段 | 作用 | 示例 |
|---------|------|------|
| **Cache-Control** | 控制缓存行为 | `max-age=3600` |
| **Expires** | 过期时间 | `Mon, 18 Jul 2026 08:00:00 GMT` |
| **Last-Modified** | 最后修改时间 | `Mon, 17 Jul 2026 08:00:00 GMT` |
| **ETag** | 资源标识 | `"abc123"` |
| **If-Modified-Since** | 条件请求 | 配合Last-Modified |
| **If-None-Match** | 条件请求 | 配合ETag |

**NSURLCache缓存策略：**

| 策略 | 作用 | 使用场景 |
|------|------|---------|
| **NSURLRequestUseProtocolCachePolicy** | 默认策略 | 根据HTTP头部决定 |
| **NSURLRequestReloadIgnoringLocalCacheData** | 忽略本地缓存 | 强制刷新数据 |
| **NSURLRequestReturnCacheDataElseLoad** | 有缓存就用，否则请求 | 离线优先 |
| **NSURLRequestReturnCacheDataDontLoad** | 只用缓存，不请求 | 完全离线模式 |
| **NSURLRequestReloadIgnoringLocalAndRemoteCacheData** | 忽略所有缓存 | 强制获取最新 |

## 【场景题】
**题目：** 列表页如何实现"下拉刷新获取最新数据，上滑加载更多使用缓存"？

**答案：**

```objective-c
// 下拉刷新：忽略缓存，强制请求
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
request.cachePolicy = NSURLRequestReloadIgnoringLocalCacheData;

// 上滑加载更多：使用缓存（如果有）
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
request.cachePolicy = NSURLRequestUseProtocolCachePolicy;
```

## 【代码示例】
```objective-c
// 1. 配置全局缓存
NSURLCache *cache = [[NSURLCache alloc] initWithMemoryCapacity:10 * 1024 * 1024  // 10MB内存
                                                  diskCapacity:50 * 1024 * 1024    // 50MB磁盘
                                                      diskPath:nil];
[NSURLCache setSharedURLCache:cache];

// 2. 默认缓存策略（根据HTTP头部）
NSURLRequest *request = [NSURLRequest requestWithURL:url];
// 默认使用 NSURLRequestUseProtocolCachePolicy

// 3. 忽略本地缓存，强制请求
NSMutableURLRequest *reloadRequest = [NSMutableURLRequest requestWithURL:url];
reloadRequest.cachePolicy = NSURLRequestReloadIgnoringLocalCacheData;

// 4. 离线优先：有缓存就用，否则请求
NSMutableURLRequest *offlineRequest = [NSMutableURLRequest requestWithURL:url];
offlineRequest.cachePolicy = NSURLRequestReturnCacheDataElseLoad;

// 5. 完全离线：只用缓存，不请求
NSMutableURLRequest *cacheOnlyRequest = [NSMutableURLRequest requestWithURL:url];
cacheOnlyRequest.cachePolicy = NSURLRequestReturnCacheDataDontLoad;

// 6. 设置响应缓存（服务器端）
// 在响应头中设置：
// Cache-Control: max-age=3600
// ETag: "abc123"

// 7. 清除缓存
[[NSURLCache sharedURLCache] removeAllCachedResponses];
[[NSURLCache sharedURLCache] removeCachedResponseForRequest:request];

// 8. 检查缓存是否存在
NSCachedURLResponse *cachedResponse = [[NSURLCache sharedURLCache] cachedResponseForRequest:request];
if (cachedResponse) {
    NSLog(@"缓存存在");
}

// 9. NSURLSession配置缓存策略
NSURLSessionConfiguration *config = [NSURLSessionConfiguration defaultSessionConfiguration];
config.requestCachePolicy = NSURLRequestUseProtocolCachePolicy;
```

## 【答题要点】
- HTTP缓存流程：检查缓存 → 判断过期 → 返回缓存或请求服务器
- Cache-Control优先级高于Expires
- ETag比Last-Modified更精确（支持秒级变化）
- NSURLRequestUseProtocolCachePolicy：默认策略，根据HTTP头部决定
- NSURLRequestReloadIgnoringLocalCacheData：忽略本地缓存
- NSURLRequestReturnCacheDataElseLoad：离线优先
- NSURLRequestReturnCacheDataDontLoad：完全离线
- NSURLCache配置全局缓存大小
- 下拉刷新用reloadIgnoringLocalCacheData
- 列表加载用useProtocolCachePolicy
