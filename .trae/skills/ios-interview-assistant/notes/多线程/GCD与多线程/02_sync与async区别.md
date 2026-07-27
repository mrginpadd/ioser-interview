# sync与async区别

## 【概念题】
**题目：** 请简述GCD中dispatch_sync和dispatch_async的区别？

**答案：**

```
┌─────────────────────────────────────────────────────┐
│  核心区别                                            │
├─────────────────────────────────────────────────────┤
│  dispatch_sync（同步）                               │
│  ├── 阻塞当前线程，等待任务完成才返回                 │
│  ├── 任务在当前线程执行（不开新线程）                 │
│  ├── 必须等任务执行完，才继续往下走                   │
│  └── 场景：需要立即得到结果                          │
├─────────────────────────────────────────────────────┤
│  dispatch_async（异步）                              │
│  ├── 不阻塞当前线程，立即返回                        │
│  ├── 任务在队列对应的线程执行（可能开新线程）         │
│  ├── 不等任务执行完，继续往下走                      │
│  └── 场景：耗时任务，不阻塞UI                        │
└─────────────────────────────────────────────────────┘
```

## 【场景题】
**题目：** 以下代码会发生什么？为什么？

```objective-c
- (void)test {
    dispatch_sync(dispatch_get_main_queue(), ^{
        NSLog(@"hello");
    });
    NSLog(@"world");
}
```

**答案：** 死锁！永远不会打印"hello"和"world"。

```
死锁原因分析：
├── 1. test方法在主线程执行
├── 2. dispatch_sync阻塞主线程，等待Block执行完成
├── 3. Block被提交到主队列，需要在主线程执行
├── 4. 但主线程已经被sync阻塞了，无法执行Block
├── 5. sync等Block完成，Block等主线程空闲
└── 6. 互相等待 → 死锁

记忆口诀：
├── sync = 停下来等（阻塞）
├── async = 丢出去不等（不阻塞）
└── 主队列 + sync = 死锁 ⚠️
```

## 【代码示例】
```objective-c
// sync：阻塞当前线程，顺序执行
NSLog(@"1");
dispatch_sync(queue, ^{
    NSLog(@"2"); // 在当前线程执行
});
NSLog(@"3"); // 必须等2执行完才执行
// 输出：1 → 2 → 3

// async：不阻塞当前线程
NSLog(@"1");
dispatch_async(queue, ^{
    NSLog(@"2"); // 在队列线程执行
});
NSLog(@"3"); // 不等2执行完
// 输出：1 → 3 → 2（2的时机不确定）

// ❌ 死锁！主队列 + sync
dispatch_async(dispatch_get_main_queue(), ^{
    dispatch_sync(dispatch_get_main_queue(), ^{
        NSLog(@"死锁"); // 永远不会执行
    });
});

// ✅ 正确：主队列 + async
dispatch_async(dispatch_get_main_queue(), ^{
    dispatch_async(dispatch_get_main_queue(), ^{
        NSLog(@"不死锁");
    });
});

// ✅ 正确：子队列 + sync（不死锁）
dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_SERIAL);
dispatch_async(dispatch_get_main_queue(), ^{
    dispatch_sync(queue, ^{
        NSLog(@"不死锁"); // 在queue线程执行，不阻塞主线程
    });
});
```

## 【答题要点】
- sync阻塞当前线程，async不阻塞
- sync在当前线程执行任务，async在队列线程执行
- 主队列 + sync = 死锁（最常考）
- 死锁原因：互相等待
- 记忆口诀：sync停下来等，async丢出去不等
