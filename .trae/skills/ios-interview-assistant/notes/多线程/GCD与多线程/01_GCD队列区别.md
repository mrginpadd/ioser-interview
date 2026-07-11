# GCD队列

## 【理论题】
**题目：** 请解释GCD中的串行队列、并发队列和主队列的区别，以及它们的使用场景？
**答案：**

**GCD（Grand Central Dispatch）：**
- Apple提供的**多核编程技术**，用于管理并发任务
- 基于**队列**和**任务**的概念，自动管理线程创建和调度

**三种队列的区别：**

| 队列类型 | 执行方式 | 线程数量 | 特点 |
|----------|----------|----------|------|
| **串行队列** | 按顺序执行，**必须等待上一个完成** | 1个线程 | 任务有序，适合需要顺序执行的场景 |
| **并发队列** | 可同时执行多个任务 | 多个线程 | 任务无序完成，适合独立任务并行执行 |
| **主队列** | 按顺序执行，运行在主线程 | 主线程 | 用于更新UI，必须等待主线程空闲 |

**关键特性：**

```objective-c
// 串行队列：任务1完成→任务2开始→任务3开始
dispatch_queue_t serialQueue = dispatch_queue_create("com.example.serial", DISPATCH_QUEUE_SERIAL);

// 并发队列：任务1、2、3可同时执行
dispatch_queue_t concurrentQueue = dispatch_queue_create("com.example.concurrent", DISPATCH_QUEUE_CONCURRENT);

// 主队列：所有任务都在主线程执行
dispatch_queue_t mainQueue = dispatch_get_main_queue();
```

**使用场景：**
- **串行队列**：文件读写、数据库操作（保证顺序）
- **并发队列**：网络请求、图片加载（提高效率）
- **主队列**：UI更新、回调结果处理

## 【场景题】
**题目：** 以下代码的输出顺序是什么？为什么？

```objective-c
dispatch_queue_t serial = dispatch_queue_create("serial", DISPATCH_QUEUE_SERIAL);

dispatch_async(serial, ^{ NSLog(@"1"); });
dispatch_async(serial, ^{ NSLog(@"2"); });
dispatch_sync(serial, ^{ NSLog(@"3"); });
dispatch_async(serial, ^{ NSLog(@"4"); });
```

**答案：**

输出顺序：`1 → 2 → 3 → 4`

**分析：**
- `dispatch_async`：异步提交，不等待执行完成
- `dispatch_sync`：同步提交，**必须等待执行完成**才返回
- 串行队列保证任务按顺序执行
- 第3个任务是同步的，会阻塞当前线程直到执行完成

## 【代码示例】
```objective-c
// 常用模式：后台执行 + 主线程更新UI
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    // 后台任务：网络请求、图片下载
    NSData *data = [NSData dataWithContentsOfURL:url];
    
    dispatch_async(dispatch_get_main_queue(), ^{
        // 主线程任务：更新UI
        self.imageView.image = [UIImage imageWithData:data];
    });
});

// 串行队列保证顺序
dispatch_queue_t queue = dispatch_queue_create("com.example.operation", DISPATCH_QUEUE_SERIAL);
dispatch_async(queue, ^{ [self step1]; });
dispatch_async(queue, ^{ [self step2]; });  // 等待step1完成
dispatch_async(queue, ^{ [self step3]; });  // 等待step2完成

// 并发队列提高效率
dispatch_queue_t concurrent = dispatch_queue_create("com.example.concurrent", DISPATCH_QUEUE_CONCURRENT);
dispatch_async(concurrent, ^{ [self loadImage1]; });
dispatch_async(concurrent, ^{ [self loadImage2]; });  // 可同时执行
dispatch_async(concurrent, ^{ [self loadImage3]; });  // 可同时执行
```

## 【答题要点】
- GCD是Apple的多核编程技术，自动管理线程
- 串行队列：顺序执行，必须等待上一个完成
- 并发队列：可同时执行，完成顺序不确定
- 主队列：运行在主线程，用于UI更新
- dispatch_sync会阻塞当前线程，dispatch_async不会
- 使用场景：串行用于顺序操作，并发用于并行任务，主队列用于UI
