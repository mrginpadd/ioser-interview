# GCD死锁场景分析

## 【场景题1】
**题目：** 以下代码会发生什么？为什么？

```objective-c
- (void)test {
    dispatch_sync(dispatch_get_main_queue(), ^{
        NSLog(@"hello");
    });
    NSLog(@"world");
}
```

**答案：** 死锁！不打印任何东西。

```
死锁原因：
├── 1. test方法在主线程执行
├── 2. dispatch_sync阻塞主线程，等待Block执行完成
├── 3. Block被提交到主队列，需要在主线程执行
├── 4. 但主线程已经被sync阻塞了，无法执行Block
├── 5. sync等Block完成，Block等主线程空闲
└── 6. 互相等待 → 死锁
```

## 【场景题2】
**题目：** 以下代码会死锁吗？为什么？

```objective-c
dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_SERIAL);

dispatch_async(queue, ^{
    NSLog(@"1");
    dispatch_sync(queue, ^{
        NSLog(@"2");
    });
    NSLog(@"3");
});
```

**答案：** 会死锁！

```
死锁原因：
├── 1. async把任务提交到串行队列queue，在queue线程执行
├── 2. 任务执行到dispatch_sync，阻塞queue线程
├── 3. sync的Block被提交到同一个串行队列queue
├── 4. 串行队列是顺序执行，前一个任务（当前任务）没完成，Block排不上
├── 5. sync等Block完成，Block等当前任务完成，当前任务等sync返回
└── 6. 互相等待 → 死锁
```

## 【死锁规律总结】

```
┌─────────────────────────────────────────────────────┐
│  死锁条件                                            │
├─────────────────────────────────────────────────────┤
│  串行队列 + sync（提交到当前所在的队列）= 死锁       │
├─────────────────────────────────────────────────────┤
│  主队列是特殊的串行队列                              │
│  所以：主队列 + sync = 死锁                          │
├─────────────────────────────────────────────────────┤
│  不会死锁的情况：                                     │
│  ├── 串行队列 + async                                │
│  ├── 并发队列 + sync                                 │
│  ├── 串行队列 + sync（提交到另一个队列）              │
│  └── 主队列 + async                                  │
└─────────────────────────────────────────────────────┘
```

## 【代码示例】
```objective-c
// ❌ 死锁：主队列 + sync
dispatch_sync(dispatch_get_main_queue(), ^{ ... });

// ❌ 死锁：串行队列 + sync（同一个队列）
dispatch_queue_t serial = dispatch_queue_create("s", DISPATCH_QUEUE_SERIAL);
dispatch_async(serial, ^{
    dispatch_sync(serial, ^{ ... }); // 死锁
});

// ✅ 不死锁：主队列 + async
dispatch_async(dispatch_get_main_queue(), ^{ ... });

// ✅ 不死锁：并发队列 + sync
dispatch_queue_t concurrent = dispatch_queue_create("c", DISPATCH_QUEUE_CONCURRENT);
dispatch_sync(concurrent, ^{ ... });

// ✅ 不死锁：串行队列 + sync（另一个队列）
dispatch_queue_t serial1 = dispatch_queue_create("s1", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t serial2 = dispatch_queue_create("s2", DISPATCH_QUEUE_SERIAL);
dispatch_async(serial1, ^{
    dispatch_sync(serial2, ^{ ... }); // 不死锁，在serial2执行
});
```

## 【答题要点】
- 死锁条件：串行队列 + sync（提交到当前所在队列）
- 主队列是特殊的串行队列，主队列 + sync必死锁
- 死锁原因：互相等待（sync等任务完成，任务等队列空闲）
- 避免方法：用async替代sync，或提交到不同的队列
- 并发队列 + sync不会死锁（可以并发执行）
