# RunLoop工作机制

## 【理论题】
**题目：** 请解释RunLoop的工作机制，以及它在iOS应用中的作用？
**答案：**

**RunLoop工作机制：**

**RunLoop是一个事件处理循环，让线程在没有任务时休眠，有任务时唤醒处理。**

RunLoop核心模式:
┌─────────────────────────────────────────────────────┐
│              RunLoop循环流程                          │
│                                                     │
│   while (!stopped) {                                │
│       1. 通知观察者：即将进入RunLoop                  │
│       2. 通知观察者：即将处理Timer事件                │
│       3. 处理Timer事件                               │
│       4. 通知观察者：即将处理输入源事件               │
│       5. 处理输入源事件（触摸、网络等）                │
│       6. 通知观察者：即将进入休眠                     │
│       7. 进入休眠，等待唤醒                          │
│       8. 从休眠中唤醒                               │
│       9. 通知观察者：即将退出RunLoop                 │
│   }                                                 │
└─────────────────────────────────────────────────────┘

工作流程：
1. 通知观察者：即将进入RunLoop
2. 通知观察者：即将处理Timer事件
3. 处理Timer事件
4. 通知观察者：即将处理输入源事件
5. 处理输入源事件（触摸、网络等）
6. 通知观察者：即将进入休眠
7. 进入休眠，等待唤醒
8. 从休眠中唤醒
9. 通知观察者：即将退出RunLoop

**RunLoop的5种模式：**

| 模式 | 用途 |
|------|------|
| `NSDefaultRunLoopMode` | 默认模式，处理大部分事件 |
| `NSRunLoopCommonModes` | 通用模式，包含default和tracking |
| `UITrackingRunLoopMode` | 跟踪模式，处理滑动等交互 |
| `NSModalPanelRunLoopMode` | 模态面板模式 |
| `NSConnectionReplyMode` | 连接回复模式（已废弃） |

**RunLoop与线程的关系：**

每个线程都可以有一个RunLoop，但主线程的RunLoop会**自动启动**。

```objective-c
// 主线程的RunLoop自动启动
int main(int argc, char * argv[]) {
    @autoreleasepool {
        return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
        // UIApplicationMain内部会启动主线程的RunLoop
    }
}

// 子线程需要手动启动
- (void)startBackgroundThread {
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        NSRunLoop *runLoop = [NSRunLoop currentRunLoop];
        [runLoop addPort:[NSMachPort port] forMode:NSDefaultRunLoopMode];
        [runLoop run];  // 启动RunLoop
    });
}
```

**RunLoop的核心作用：**

1. **保持线程存活**：让线程不会执行完就退出
2. **事件处理**：处理触摸、定时器、网络等事件
3. **内存管理**：管理AutoreleasePool的创建和释放
4. **界面更新**：处理UI刷新

## 【场景题】
**题目：** 为什么滑动UITableView时，NSTimer会暂停？

**答案：**

因为滑动时RunLoop切换到了`UITrackingRunLoopMode`，而默认的NSTimer是添加到`NSDefaultRunLoopMode`的。

**解决方法：**

```objective-c
// 方法1：添加到CommonModes
[NSTimer scheduledTimerWithTimeInterval:1.0 
                                 target:self 
                               selector:@selector(timerAction) 
                               userInfo:nil 
                                repeats:YES];
// 或者手动添加到CommonModes
[[NSRunLoop currentRunLoop] addTimer:timer 
                             forMode:NSRunLoopCommonModes];

// 方法2：使用GCD定时器（不受RunLoop模式影响）
dispatch_source_t timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, dispatch_get_main_queue());
dispatch_source_set_timer(timer, dispatch_walltime(NULL, 0), 1.0 * NSEC_PER_SEC, 0);
dispatch_source_set_event_handler(timer, ^{
    // 定时器回调
});
dispatch_resume(timer);
```

## 【代码示例】
```objective-c
// RunLoop常用API
NSRunLoop *runLoop = [NSRunLoop currentRunLoop];

// 添加定时器
[NSTimer scheduledTimerWithTimeInterval:1.0 
                                 target:self 
                               selector:@selector(update) 
                               userInfo:nil 
                                repeats:YES];

// 添加端口
NSPort *port = [NSMachPort port];
[runLoop addPort:port forMode:NSDefaultRunLoopMode];

// 启动RunLoop
[runLoop run];

// RunLoop控制
[runLoop runUntilDate:[NSDate dateWithTimeIntervalSinceNow:10]];  // 运行10秒
[runLoop stop];  // 停止RunLoop

// 判断RunLoop是否在运行
BOOL isRunning = [runLoop isRunning];
```

## 【答题要点】
- RunLoop是事件处理循环，让线程休眠/唤醒
- 工作流程：处理事件 → 休眠 → 唤醒 → 处理事件
- 5种模式：Default、Common、Tracking、ModalPanel、ConnectionReply
- 主线程RunLoop自动启动，子线程需手动启动
- 核心作用：保持线程存活、事件处理、内存管理、界面更新
- 滑动时RunLoop切换模式，可能导致Timer暂停
