# ReactiveCocoa响应式编程

## 【理论题】
**题目：** 请简述ReactiveCocoa（RAC）的作用和核心概念？
**答案：**

**ReactiveCocoa的作用：**
> RAC是iOS的函数响应式编程框架（FRP），用于简化事件监听、UI绑定、异步操作，常用于MVVM架构。

**核心概念：**

| 概念 | 作用 | 类比 |
|------|------|------|
| **RACSignal** | 信号，数据流 | 水管 |
| **RACSubscriber** | 订阅者，接收数据 | 接水的人 |
| **RACSubject** | 可手动发送数据的信号 | 信号+订阅者合体 |
| **RACCommand** | 封装执行动作 | 按钮点击事件 |

**RAC三步流程：**

```
创建信号 → 订阅信号 → 发送数据

RACSignal *signal = [RACSignal createSignal:^RACDisposable *(id<RACSubscriber> subscriber) {
    [subscriber sendNext:@"数据"];      // 发送数据
    [subscriber sendCompleted];         // 发送完成
    return nil;
}];

[signal subscribeNext:^(id x) {
    NSLog(@"收到: %@", x);              // 接收数据
}];
```

## 【场景题】
**题目：** RAC在MVVM中如何实现数据绑定？

**答案：**

```objective-c
// ViewModel
@interface LoginViewModel : NSObject
@property (nonatomic, strong) NSString *username;
@property (nonatomic, strong) NSString *password;
@property (nonatomic, strong) RACSignal *loginEnabledSignal;
@end

@implementation LoginViewModel
- (instancetype)init {
    self = [super init];
    if (self) {
        // 用户名和密码都不为空时，登录按钮才可点击
        RACSignal *usernameSignal = RACObserve(self, username);
        RACSignal *passwordSignal = RACObserve(self, password);
        
        _loginEnabledSignal = [RACSignal combineLatest:@[usernameSignal, passwordSignal] 
            reduce:^(NSString *username, NSString *password) {
            return @(username.length > 0 && password.length > 0);
        }];
    }
    return self;
}
@end

// ViewController - 绑定
RAC(self.loginButton, enabled) = self.viewModel.loginEnabledSignal;
```

## 【代码示例】
```objective-c
// 1. 信号基本使用
RACSignal *signal = [RACSignal createSignal:^RACDisposable *(id<RACSubscriber> subscriber) {
    [subscriber sendNext:@"Hello"];
    [subscriber sendNext:@"World"];
    [subscriber sendCompleted];
    return nil;
}];

[signal subscribeNext:^(id x) {
    NSLog(@"%@", x);
} error:^(NSError *error) {
    NSLog(@"错误: %@", error);
} completed:^{
    NSLog(@"完成");
}];

// 2. RACSubject（可手动发送）
RACSubject *subject = [RACSubject subject];
[subject subscribeNext:^(id x) {
    NSLog(@"收到: %@", x);
}];
[subject sendNext:@"手动发送的数据"];

// 3. 信号操作 - map（转换数据）
[[signal map:^id(NSString *value) {
    return [value uppercaseString];
}] subscribeNext:^(NSString *x) {
    NSLog(@"大写: %@", x);
}];

// 4. 信号操作 - filter（过滤数据）
[[signal filter:^BOOL(NSString *value) {
    return value.length > 3;
}] subscribeNext:^(NSString *x) {
    NSLog(@"过滤后: %@", x);
}];

// 5. 信号操作 - merge（合并信号）
RACSignal *signal1 = [RACSignal createSignal...];
RACSignal *signal2 = [RACSignal createSignal...];
RACSignal *merged = [RACSignal merge:@[signal1, signal2]];

// 6. 信号操作 - combineLatest（组合最新值）
RACSignal *combined = [RACSignal combineLatest:@[signalA, signalB] reduce:^(id a, id b) {
    return [NSString stringWithFormat:@"%@%@", a, b];
}];

// 7. UI事件监听
[[self.button rac_signalForControlEvents:UIControlEventTouchUpInside] subscribeNext:^(UIButton *button) {
    NSLog(@"按钮被点击");
}];

// 8. 属性监听（KVO替代）
[RACObserve(self, name) subscribeNext:^(NSString *name) {
    NSLog(@"名字变了: %@", name);
}];

// 9. 绑定UI
RAC(self.label, text) = RACObserve(self, name);

// 10. 通知监听
[[[NSNotificationCenter defaultCenter] rac_addObserverForName:@"NotificationName" object:nil] 
    subscribeNext:^(NSNotification *notification) {
    NSLog(@"收到通知");
}];

// 11. 延迟执行
[[RACSignal interval:1.0 onScheduler:[RACScheduler mainThreadScheduler]] 
    subscribeNext:^(NSDate *date) {
    NSLog(@"每秒执行一次");
}];

// 12. flattenMap（信号嵌套）
[[signal flattenMap:^RACStream *(NSString *value) {
    return [RACSignal return:value.uppercaseString];
}] subscribeNext:^(NSString *x) {
    NSLog(@"%@", x);
}];
```

## 【答题要点】
- RAC是函数响应式编程框架（FRP）
- 核心概念：RACSignal（信号）、RACSubscriber（订阅者）、RACSubject
- RAC三步：创建信号 → 订阅信号 → 发送数据
- 常用信号操作：map（转换）、filter（过滤）、merge（合并）、combineLatest（组合）
- 常用宏：RACObserve（监听属性）、RAC（绑定UI）
- 用于MVVM架构中实现数据绑定
- 替代传统的事件监听、KVO、通知
- 信号链式调用：flattenMap、map、filter
