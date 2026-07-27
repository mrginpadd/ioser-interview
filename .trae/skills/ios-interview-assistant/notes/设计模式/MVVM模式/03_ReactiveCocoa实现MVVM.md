# MVVM - ReactiveCocoa实现方式

## 【核心思路】
使用ReactiveCocoa（RAC）的响应式编程特性，实现ViewModel和View之间的数据绑定。RAC提供了信号（Signal）、订阅（Subscribe）、操作符（map/filter/combine等），让数据绑定更灵活、更强大。

## 【ReactiveCocoa简介】

```
┌─────────────────────────────────────────────────────┐
│  ReactiveCocoa是什么                                 │
├─────────────────────────────────────────────────────┤
│  定义：                                               │
│  基于响应式编程的Objective-C/Swift框架               │
│  灵感来自于Reactive Extensions（Rx）                 │
│  将各种事件流统一抽象成"信号"（Signal）               │
├─────────────────────────────────────────────────────┤
│  核心概念：                                           │
│  ├── Signal（信号）：数据流，会发送一系列的值         │
│  ├── Subscriber（订阅者）：监听信号，接收值           │
│  ├── RACCommand：封装带状态的操作（如网络请求）       │
│  ├── RACObserve：KVO的RAC封装，监听属性变化          │
│  └── 操作符：map、filter、combineLatest、flatten等   │
├─────────────────────────────────────────────────────┤
│  优点：                                               │
│  ✅ 声明式编程：描述"是什么"，不是"怎么做"            │
│  ✅ 统一的数据流模型：各种事件都是信号                │
│  ✅ 丰富的操作符：map/filter/combine/skip/take等     │
│  ✅ 自动管理生命周期：不需要手动移除观察者            │
│  ✅ 组合能力强：多个信号可以组合成新信号              │
├─────────────────────────────────────────────────────┤
│  缺点：                                               │
│  ⚠️ 学习成本高，需要理解响应式编程思想                │
│  ⚠️ 调试困难（数据流不直观）                          │
│  ⚠️ 代码可读性不如Block（新手看不懂）                 │
│  ⚠️ 库体积较大                                       │
└─────────────────────────────────────────────────────┘
```

## 【代码示例】

### ViewModel层

```objective-c
// LoginViewModel.h
@interface LoginViewModel : NSObject

@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;

// RACCommand封装登录操作（自带executing、enabled、errors等状态）
@property (nonatomic, strong, readonly) RACCommand *loginCommand;

// 登录结果信号
@property (nonatomic, strong, readonly) RACSignal *loginSuccessSignal;
@property (nonatomic, strong, readonly) RACSignal *loginErrorSignal;

@end

// LoginViewModel.m
#import <ReactiveObjC/ReactiveObjC.h>

@implementation LoginViewModel

- (instancetype)init {
    self = [super init];
    if (self) {
        [self setupLoginCommand];
    }
    return self;
}

- (void)setupLoginCommand {
    // 1. 用户名和密码是否有效 → 控制按钮enabled
    RACSignal *validSignal = [RACSignal combineLatest:@[
        RACObserve(self, username),
        RACObserve(self, password)
    ] reduce:^id(NSString *username, NSString *password) {
        return @(username.length >= 6 && password.length >= 8);
    }];
    
    // 2. RACCommand封装登录操作
    _loginCommand = [[RACCommand alloc] initWithEnabled:validSignal signalBlock:^RACSignal *(id input) {
        return [self loginSignal];
    }];
    
    // 3. 从command中提取成功和失败信号
    _loginSuccessSignal = [[_loginCommand.executionSignals flatten] filter:^BOOL(id value) {
        return [value boolValue];
    }];
    
    _loginErrorSignal = _loginCommand.errors;
}

- (RACSignal *)loginSignal {
    return [RACSignal createSignal:^RACDisposable *(id<RACSubscriber> subscriber) {
        // 模拟网络请求
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 1.0 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
            BOOL success = self.username.length >= 6 && self.password.length >= 8;
            if (success) {
                [subscriber sendNext:@(YES)];
                [subscriber sendCompleted];
            } else {
                NSError *error = [NSError errorWithDomain:@"login" code:-1 userInfo:@{NSLocalizedDescriptionKey: @"用户名或密码格式错误"}];
                [subscriber sendError:error];
            }
        });
        return nil;
    }];
}

@end
```

### ViewController层

```objective-c
// LoginViewController.m
#import <ReactiveObjC/ReactiveObjC.h>

@interface LoginViewController ()

@property (nonatomic, strong) LoginViewModel *viewModel;
@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;
@property (nonatomic, strong) UIButton *loginButton;
@property (nonatomic, strong) UIActivityIndicatorView *loadingIndicator;
@property (nonatomic, strong) UILabel *errorLabel;

@end

@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [self setupUI];
    [self bindViewModel];
}

- (void)setupUI {
    // ... UI创建代码（同Block版）
}

- (void)bindViewModel {
    self.viewModel = [[LoginViewModel alloc] init];
    
    // 1. View → ViewModel：双向绑定
    RAC(self.viewModel, username) = self.usernameField.rac_textSignal;
    RAC(self.viewModel, password) = self.passwordField.rac_textSignal;
    
    // 2. ViewModel → View：按钮enabled状态
    RAC(self.loginButton, enabled) = self.viewModel.loginCommand.enabled;
    
    // 3. ViewModel → View：加载状态
    [self.viewModel.loginCommand.executing subscribeNext:^(NSNumber *executing) {
        BOOL loading = [executing boolValue];
        self.loadingIndicator.hidden = !loading;
        self.loginButton.hidden = loading;
        if (loading) {
            [self.loadingIndicator startAnimating];
        } else {
            [self.loadingIndicator stopAnimating];
        }
    }];
    
    // 4. ViewModel → View：登录成功
    [self.viewModel.loginSuccessSignal subscribeNext:^(id x) {
        NSLog(@"登录成功");
    }];
    
    // 5. ViewModel → View：登录失败
    [self.viewModel.loginErrorSignal subscribeNext:^(NSError *error) {
        self.errorLabel.text = error.localizedDescription;
    }];
    
    // 6. View → ViewModel：按钮点击 → 执行command
    self.loginButton.rac_command = self.viewModel.loginCommand;
}

@end
```

## 【常用操作符】

```
┌─────────────────────────────────────────────────────┐
│  常用RAC操作符                                       │
├─────────────────────────────────────────────────────┤
│  map：转换值                                          │
│  ├── input: @1 → map: ^(NSNumber *n){ return @(n.intValue * 2); } → output: @2 │
│  └── 用途：数据格式转换                               │
├─────────────────────────────────────────────────────┤
│  filter：过滤值                                       │
│  ├── input: @1, @2, @3 → filter: ^(NSNumber *n){ return n.intValue > 2; } → output: @3 │
│  └── 用途：条件过滤                                   │
├─────────────────────────────────────────────────────┤
│  combineLatest：组合多个信号的最新值                   │
│  ├── signalA: 1, 2, 3                               │
│  ├── signalB: a, b                                  │
│  └── combineLatest: (3,a), (3,b)                    │
├─────────────────────────────────────────────────────┤
│  flatten / flattenMap：拍平（处理信号的信号）         │
│  ├── 信号里还嵌套信号 → 拍平成单层信号                │
│  └── 用途：网络请求、链式操作                         │
├─────────────────────────────────────────────────────┤
│  skip / take：跳过/取前N个                            │
│  ├── skip:2 → 跳过前2个值                            │
│  └── take:3 → 只取前3个值                            │
├─────────────────────────────────────────────────────┤
│  throttle / debounce：节流/防抖                       │
│  ├── throttle：指定时间内只取最新值                   │
│  └── 用途：搜索框输入防抖（停止输入后才请求）          │
└─────────────────────────────────────────────────────┘
```

## 【RACCommand的好处】

```
RACCommand自动提供：
├── executing：是否正在执行（用来显示loading）
├── enabled：是否可执行（用来控制按钮enabled）
├── errors：错误信号（统一处理错误）
├── executionSignals：执行信号流
└── allowsConcurrentExecution：是否允许并发执行

对比手动实现：
├── 手动：需要写loading、enabled、success、error四个Block
├── RACCommand：一个command全部搞定，代码更简洁
└── 还能利用操作符组合、转换
```

## 【使用场景】

```
适合场景：
├── 中大型项目（状态多、逻辑复杂）
├── 团队熟悉响应式编程
├── 需要复杂的数据流操作（map/filter/combine等）
├── 统一的错误处理和加载状态管理
└── 需要函数式编程的表达能力

不适合场景：
├── 小型项目（杀鸡用牛刀）
├── 团队不熟悉RAC（学习成本高）
├── 快速原型开发（代码量反而多）
└── 对包体积敏感（RAC库较大）
```

## 【面试话术】

> "ReactiveCocoa是OC中实现MVVM的另一种方式，基于响应式编程。
> ViewModel用RACSignal暴露数据流，ViewController订阅这些信号来更新UI。
> RAC提供了丰富的操作符（map、filter、combine等），让数据处理更灵活。
> RACCommand还可以封装带状态的操作（如网络请求），自动管理executing、enabled、errors等状态。
> 缺点是学习成本比较高，团队需要理解响应式编程的思想。"
