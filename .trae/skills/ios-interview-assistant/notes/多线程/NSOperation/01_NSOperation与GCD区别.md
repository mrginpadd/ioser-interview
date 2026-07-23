# NSOperation与GCD区别

## 【理论题】
**题目：** 请解释NSOperation的作用，以及和GCD的区别？
**答案：**

**NSOperation的作用：**
> NSOperation是面向对象的任务封装类，把"要执行的任务"封装成对象，配合NSOperationQueue管理任务执行。

```
NSOperation体系：
┌─────────────────────────────────────────────────────┐
│              NSOperation（抽象基类）                 │
│                    │                                │
│         ┌──────────┼──────────┐                     │
│         ▼          ▼          ▼                     │
│  NSInvocation  NSBlock  自定义子类                   │
│  Operation     Operation  （重写main方法）            │
└─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│              NSOperationQueue（队列）                │
│  - 最大并发数（maxConcurrentOperationCount）         │
│  - 暂停/恢复/取消                                    │
│  - 任务依赖（addDependency:）                        │
└─────────────────────────────────────────────────────┘
```

**NSOperation vs GCD：**

| 特性 | NSOperation | GCD |
|------|-------------|-----|
| **抽象层级** | 面向对象（高级） | C函数（底层） |
| **任务管理** | 封装成对象，可操作 | 代码块，不可操作 |
| **依赖关系** | ✅ addDependency | ❌ 不支持 |
| **暂停/恢复** | ✅ queue.suspended | ❌ 不支持 |
| **取消任务** | ✅ cancel | ❌ 不支持 |
| **最大并发数** | ✅ maxConcurrentOperationCount | ⚠️ 只能选串行/并发 |
| **任务状态** | ✅ KVO监听（ready/executing/finished） | ❌ 不支持 |
| **执行效率** | 稍低（额外开销） | 高（轻量级） |
| **适用场景** | 复杂任务管理 | 简单并发任务 |

## 【场景题】
**题目：** 什么时候用NSOperation，什么时候用GCD？

**答案：**

| 场景 | 选择 | 原因 |
|------|------|------|
| **简单并发** | GCD | 轻量、高效 |
| **任务有依赖** | NSOperation | 支持addDependency |
| **需要取消任务** | NSOperation | 支持cancel |
| **限制并发数** | NSOperation | maxConcurrentOperationCount |
| **监听任务状态** | NSOperation | KVO |
| **后台下载** | NSOperation | 可暂停/恢复/取消 |
| **一次性执行** | GCD | dispatch_once |
| **延时执行** | GCD | dispatch_after |

## 【代码示例】
```objective-c
// 1. NSBlockOperation（最常用）
NSBlockOperation *operation = [NSBlockOperation blockOperationWithBlock:^{
    NSLog(@"任务执行：%@", [NSThread currentThread]);
}];

// 添加额外的执行块
[operation addExecutionBlock:^{
    NSLog(@"额外任务：%@", [NSThread currentThread]);
}];

// 2. NSInvocationOperation（少用）
NSInvocationOperation *invocation = [[NSInvocationOperation alloc] 
    initWithTarget:self 
    selector:@selector(doSomething:) 
    object:nil];

// 3. 自定义NSOperation（复杂任务）
@interface MyOperation : NSOperation
@end

@implementation MyOperation
- (void)main {
    if (self.isCancelled) return;  // 检查是否被取消
    
    @autoreleasepool {
        NSLog(@"执行自定义任务");
        // 执行耗时操作...
        
        if (self.isCancelled) return;  // 执行中检查
    }
}
@end

// 4. NSOperationQueue使用
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
queue.maxConcurrentOperationCount = 2;  // 最大并发数

// 添加任务到队列
[queue addOperation:operation];
[queue addOperationWithBlock:^{
    NSLog(@"block任务");
}];

// 5. 任务依赖（A完成后才执行B）
NSBlockOperation *opA = [NSBlockOperation blockOperationWithBlock:^{
    NSLog(@"任务A");
}];
NSBlockOperation *opB = [NSBlockOperation blockOperationWithBlock:^{
    NSLog(@"任务B（依赖A）");
}];
[opB addDependency:opA];  // B依赖A

NSOperationQueue *queue = [[NSOperationQueue alloc] init];
[queue addOperations:@[opA, opB] waitUntilFinished:NO];

// 6. 暂停/恢复/取消
[queue setSuspended:YES];  // 暂停队列
[queue setSuspended:NO];   // 恢复队列
[queue cancelAllOperations];  // 取消所有任务

// 7. 监听任务完成（KVO）
[opA setCompletionBlock:^{
    NSLog(@"任务A完成了");
}];

// 8. 主队列（UI更新）
NSOperationQueue *mainQueue = [NSOperationQueue mainQueue];
[mainQueue addOperationWithBlock:^{
    self.label.text = @"更新UI";
}];

// 9. 对比GCD的写法
// GCD写法
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    NSLog(@"后台任务");
    dispatch_async(dispatch_get_main_queue(), ^{
        NSLog(@"更新UI");
    });
});

// NSOperation写法
NSBlockOperation *op = [NSBlockOperation blockOperationWithBlock:^{
    NSLog(@"后台任务");
    [[NSOperationQueue mainQueue] addOperationWithBlock:^{
        NSLog(@"更新UI");
    }];
}];
[[NSOperationQueue new] addOperation:op];
```

## 【答题要点】
- NSOperation是任务封装类，面向对象，配合NSOperationQueue管理任务
- 两个子类：NSBlockOperation（常用）、NSInvocationOperation（少用）
- 可自定义子类重写main方法
- NSOperation vs GCD：NSOperation更高级，支持依赖、暂停、取消、KVO
- GCD更轻量高效，适合简单并发
- 任务依赖：addDependency
- 最大并发数：maxConcurrentOperationCount
- 暂停/恢复：setSuspended
- 取消：cancel（需要任务内部检查isCancelled）
- 主队列：[NSOperationQueue mainQueue]
- AFNetworking和SDWebImage底层都用NSOperation
