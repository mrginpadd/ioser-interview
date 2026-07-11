# Block与循环引用

## 【理论题】
**题目：** 请解释Block的循环引用问题，以及如何解决？
**答案：**

**循环引用的原因：**
```objective-c
self.block = ^{
    NSLog(@"%@", self.property);  // block捕获了self，形成强引用
};
// self强引用block，block强引用self → 循环引用！
```

**解决方案：__weak + __strong dance**

```objective-c
__weak typeof(self) weakSelf = self;
self.block = ^{
    __strong typeof(weakSelf) strongSelf = weakSelf;
    if (strongSelf) {
        NSLog(@"%@", strongSelf.property);
    }
};
```

**核心要点：**
- `__weak`：打破循环引用，block不再强引用self
- `__strong`：在block执行期间保持self存活，防止野指针
- `typeof(self)`：类型推断，避免硬编码类型

**其他解决方案：**

| 方案 | 适用场景 |
|------|----------|
| `__weak self` | 异步任务，不关心self是否存在 |
| `__weak + __strong` | 异步任务，需要确保self存在 |
| `@weakify/@strongify` (RAC) | ReactiveCocoa中使用 |
| `[self class]` | 只需要类方法时 |

## 【场景题】
**题目：** 在使用`dispatch_after`时，如果block中访问了self，应该如何避免循环引用？
**答案：**

```objective-c
// 错误写法
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
    [self doSomething];  // 循环引用！
});

// 正确写法
__weak typeof(self) weakSelf = self;
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
    __strong typeof(weakSelf) strongSelf = weakSelf;
    if (strongSelf) {
        [strongSelf doSomething];
    }
});
```

**为什么需要strongSelf？**
- 如果只使用weakSelf，block执行期间self可能被释放
- strongSelf在block内部增加了一次强引用，确保self在block执行期间存活
- 执行完毕后，strongSelf作用域结束，强引用自动释放

## 【代码示例】
```objective-c
// UIViewController中使用Block
- (void)fetchData {
    __weak typeof(self) weakSelf = self;
    [self.networkManager fetchDataWithCompletion:^(NSArray *data, NSError *error) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;
        
        [strongSelf.dataSource addObjectsFromArray:data];
        [strongSelf.tableView reloadData];
    }];
}

// 使用typedef简化写法
typedef typeof(self) Self;
__weak Self weakSelf = self;
self.block = ^{
    __strong Self strongSelf = weakSelf;
    if (strongSelf) {
        [strongSelf performAction];
    }
};
```

## 【答题要点】
- Block捕获外部变量时，对于对象类型会自动进行强引用
- self强引用block + block强引用self = 循环引用
- __weak打破循环，__strong保证block执行期间self存活
- typeof(self)避免硬编码类型，提高代码可维护性
- 异步任务中必须使用weak+strong组合，同步任务可以只使用weak
