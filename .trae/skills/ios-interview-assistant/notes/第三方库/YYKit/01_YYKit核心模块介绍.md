# YYKit高性能工具库

## 【理论题】
**题目：** 请简述YYKit的作用和核心模块？
**答案：**

**YYKit的作用：**
> YYKit是 ibireme 开发的iOS高性能工具库，包含多个核心模块，以性能极致优化著称。

**核心模块：**

| 模块 | 作用 |
|------|------|
| **YYModel** | 高性能JSON转Model |
| **YYCache** | 高性能缓存（内存+磁盘） |
| **YYImage** | 高性能图片解码（支持GIF/WebP） |
| **YYWebImage** | 网络图片加载（替代SDWebImage） |
| **YYText** | 富文本处理（替代TyattributeString） |
| **YYDispatchQueuePool** | GCD队列池优化 |

## 【场景题】
**题目：** YYCache和NSCache的区别？

**答案：**

| 特性 | YYCache | NSCache |
|------|---------|---------|
| **磁盘缓存** | 支持 | 不支持 |
| **内存缓存** | LRU算法 | 系统管理 |
| **线程安全** | 自带锁 | 自带锁 |
| **性能** | 极高 | 一般 |
| **持久化** | 支持App退出后保留 | 不支持 |

## 【代码示例】
```objective-c
// 1. YYCache使用
YYCache *cache = [YYCache cacheWithName:@"myCache"];

// 写入缓存
[cache setObject:@"数据" forKey:@"key"];

// 读取缓存
NSString *value = [cache objectForKey:@"key"];

// 检查是否存在
BOOL contains = [cache containsObjectForKey:@"key"];

// 删除缓存
[cache removeObjectForKey:@"key"];
[cache removeAllObjects];

// 2. YYModel使用
User *user = [User yy_modelWithJSON:json];
NSDictionary *json = [user yy_modelToJSONObject];

// 3. YYImage使用
// 支持GIF、WebP等格式
YYImage *image = [YYImage imageNamed:@"avatar.gif"];
YYAnimatedImageView *imageView = [YYAnimatedImageView new];
imageView.image = image;

// 4. YYText使用
YYLabel *label = [YYLabel new];
NSMutableAttributedString *text = [[NSMutableAttributedString alloc] initWithString:@"Hello World"];
[text yy_setColor:[UIColor redColor] range:NSMakeRange(0, 5)];
label.attributedText = text;

// 5. YYDispatchQueuePool使用
YYDispatchQueuePool *pool = [[YYDispatchQueuePool alloc] initWithName:@"myQueue" queueCount:5 qos:NSQualityOfServiceUserInitiated];
dispatch_queue_t queue = [pool queue];
dispatch_async(queue, ^{
    // 异步任务
});
```

## 【答题要点】
- YYKit是iOS高性能工具库，作者是ibireme
- 核心模块：YYModel、YYCache、YYImage、YYWebImage、YYText
- YYModel：高性能JSON转Model，避免KVC和消息转发
- YYCache：高性能缓存，支持内存+磁盘，LRU算法
- YYImage：支持GIF、WebP等格式，高性能解码
- YYText：富文本处理，支持图文混排
- YYDispatchQueuePool：GCD队列池，避免队列过多
- 性能优化核心：缓存、避免锁竞争、异步解码
