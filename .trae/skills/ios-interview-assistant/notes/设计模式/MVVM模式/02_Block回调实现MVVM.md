# MVVM - Block回调实现方式

## 【核心思路】
ViewModel暴露Block属性，ViewController给Block赋值，ViewModel内部状态变化时调用Block通知ViewController更新UI。

## 【为什么最简单】

```
┌─────────────────────────────────────────────────────┐
│  Block版MVVM的优点                                   │
├─────────────────────────────────────────────────────┤
│  ✅ 不需要KVO的addObserver/removeObserver            │
│  ✅ 不需要dealloc中手动移除观察者                     │
│  ✅ 没有keypath字符串（不会写错）                     │
│  ✅ 逻辑清晰：谁赋值谁负责                           │
│  ✅ 调试方便：断点直接在Block里                       │
│  ✅ 代码量少，不易出错                               │
├─────────────────────────────────────────────────────┤
│  缺点                                                │
│  ⚠️ 每个状态都要写一个Block                           │
│  ⚠️ 需要注意循环引用（__weak）                        │
│  ⚠️ 不如ReactiveCocoa灵活（但简单够用）               │
└─────────────────────────────────────────────────────┘
```

## 【代码示例】

### ViewModel层

```objective-c
// LoginViewModel.h
@interface LoginViewModel : NSObject

@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;

// 暴露Block属性，状态变化时回调
@property (nonatomic, copy) void(^loginEnabledChanged)(BOOL enabled);
@property (nonatomic, copy) void(^loadingChanged)(BOOL loading);
@property (nonatomic, copy) void(^loginSuccess)(void);
@property (nonatomic, copy) void(^loginFailed)(NSString *errorMsg);

- (void)login;

@end

// LoginViewModel.m
@implementation LoginViewModel

- (void)setUsername:(NSString *)username {
    _username = [username copy];
    [self updateLoginEnabled];
}

- (void)setPassword:(NSString *)password {
    _password = [password copy];
    [self updateLoginEnabled];
}

- (void)updateLoginEnabled {
    BOOL enabled = self.username.length >= 6 && self.password.length >= 8;
    if (self.loginEnabledChanged) {
        self.loginEnabledChanged(enabled);
    }
}

- (void)login {
    if (self.loadingChanged) {
        self.loadingChanged(YES);
    }
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 1.0 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
        if (self.loadingChanged) {
            self.loadingChanged(NO);
        }
        
        BOOL success = self.username.length >= 6 && self.password.length >= 8;
        if (success) {
            if (self.loginSuccess) {
                self.loginSuccess();
            }
        } else {
            if (self.loginFailed) {
                self.loginFailed(@"用户名或密码格式错误");
            }
        }
    });
}

@end
```

### ViewController层

```objective-c
// LoginViewController.m
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
    [self setupViewModel];
}

- (void)setupUI {
    self.view.backgroundColor = [UIColor whiteColor];
    
    self.usernameField = [[UITextField alloc] initWithFrame:CGRectMake(20, 60, 280, 40)];
    self.usernameField.placeholder = @"用户名";
    self.usernameField.borderStyle = UITextBorderStyleRoundedRect;
    [self.usernameField addTarget:self action:@selector(usernameChanged:) forControlEvents:UIControlEventEditingChanged];
    [self.view addSubview:self.usernameField];
    
    self.passwordField = [[UITextField alloc] initWithFrame:CGRectMake(20, 120, 280, 40)];
    self.passwordField.placeholder = @"密码";
    self.passwordField.secureTextEntry = YES;
    self.passwordField.borderStyle = UITextBorderStyleRoundedRect;
    [self.passwordField addTarget:self action:@selector(passwordChanged:) forControlEvents:UIControlEventEditingChanged];
    [self.view addSubview:self.passwordField];
    
    self.loginButton = [[UIButton alloc] initWithFrame:CGRectMake(20, 180, 280, 40)];
    [self.loginButton setTitle:@"登录" forState:UIControlStateNormal];
    [self.loginButton setBackgroundColor:[UIColor blueColor]];
    [self.loginButton addTarget:self action:@selector(loginButtonTapped) forControlEvents:UIControlEventTouchUpInside];
    self.loginButton.enabled = NO;
    [self.view addSubview:self.loginButton];
    
    self.loadingIndicator = [[UIActivityIndicatorView alloc] initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleGray];
    self.loadingIndicator.frame = CGRectMake(130, 230, 40, 40);
    self.loadingIndicator.hidden = YES;
    [self.view addSubview:self.loadingIndicator];
    
    self.errorLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 230, 280, 20)];
    self.errorLabel.textColor = [UIColor redColor];
    self.errorLabel.font = [UIFont systemFontOfSize:14];
    [self.view addSubview:self.errorLabel];
}

- (void)setupViewModel {
    self.viewModel = [[LoginViewModel alloc] init];
    
    __weak typeof(self) weakSelf = self;
    
    // 绑定：ViewModel → View
    self.viewModel.loginEnabledChanged = ^(BOOL enabled) {
        weakSelf.loginButton.enabled = enabled;
    };
    
    self.viewModel.loadingChanged = ^(BOOL loading) {
        weakSelf.loadingIndicator.hidden = !loading;
        weakSelf.loginButton.hidden = loading;
        if (loading) {
            [weakSelf.loadingIndicator startAnimating];
        } else {
            [weakSelf.loadingIndicator stopAnimating];
        }
    };
    
    self.viewModel.loginSuccess = ^{
        NSLog(@"登录成功");
    };
    
    self.viewModel.loginFailed = ^(NSString *errorMsg) {
        weakSelf.errorLabel.text = errorMsg;
    };
}

// View → ViewModel
- (void)usernameChanged:(UITextField *)textField {
    self.viewModel.username = textField.text;
}

- (void)passwordChanged:(UITextField *)textField {
    self.viewModel.password = textField.text;
}

- (void)loginButtonTapped {
    [self.viewModel login];
}

@end
```

## 【数据流向图】

```
┌─────────────────────────────────────────────────────┐
│  数据流向                                            │
├─────────────────────────────────────────────────────┤
│  View → ViewModel                                    │
│  ├── 用户输入 → viewModel.username = text            │
│  ├── 用户点击 → [viewModel login]                    │
│  └── 直接调用ViewModel的属性和方法                    │
├─────────────────────────────────────────────────────┤
│  ViewModel → View                                    │
│  ├── 状态变化 → Block回调                            │
│  ├── viewModel.loginEnabledChanged(enabled)         │
│  ├── viewModel.loadingChanged(loading)              │
│  └── ViewController在Block中更新UI                   │
├─────────────────────────────────────────────────────┤
│  ViewModel → Model                                   │
│  ├── 持有Model对象                                   │
│  ├── 处理业务逻辑                                    │
│  └── 数据转换（Model数据 → View可用数据）             │
└─────────────────────────────────────────────────────┘
```

## 【使用场景】

```
适合场景：
├── 中小型项目（不需要复杂的响应式框架）
├── 团队不熟悉ReactiveCocoa
├── 快速开发（代码量少）
├── 简单的业务页面
└── 面试官问"OC怎么实现MVVM"时的首选答案

不适合场景：
├── 非常复杂的页面（状态太多，Block写不过来）
├── 需要数据流操作（map/filter/combine等）
├── 团队已经在使用ReactiveCocoa
└── 需要统一的数据流管理
```

## 【面试话术】

> "OC中实现MVVM最简单常用的方式是用Block回调。
> ViewModel暴露若干个Block属性，ViewController在初始化时给这些Block赋值。
> 当ViewModel内部状态变化时，调用对应的Block通知ViewController更新UI。
> 这样比KVO简单很多，不需要手动管理观察者，也不容易出错。"
