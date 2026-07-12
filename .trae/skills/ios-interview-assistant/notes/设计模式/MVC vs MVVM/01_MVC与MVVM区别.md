# MVC与MVVM

## 【理论题】
**题目：** 请解释MVC和MVVM的区别，以及在iOS开发中如何选择使用？
**答案：**

**MVC架构：**

```
┌─────────────────────────────────────────────────────┐
│                      View                           │
│              (UI界面，展示数据)                       │
│                      │                              │
│                      ▼                              │
│              Controller                            │
│         (逻辑处理，协调Model和View)                  │
│                      │                              │
│                      ▼                              │
│                      Model                          │
│              (数据模型，业务逻辑)                     │
└─────────────────────────────────────────────────────┘
```

**MVVM架构：**

```
┌─────────────────────────────────────────────────────┐
│                      View                           │
│              (UI界面，展示数据)                       │
│                      │                              │
│            双向绑定（数据绑定）                        │
│                      ▼                              │
│              ViewModel                              │
│         (视图模型，处理UI逻辑，转化数据)               │
│                      │                              │
│                      ▼                              │
│                      Model                          │
│              (数据模型，业务逻辑)                     │
└─────────────────────────────────────────────────────┘
```

**核心区别：**

| 特性 | MVC | MVVM |
|------|-----|------|
| **核心层** | Controller | ViewModel |
| **数据流向** | 单向（Model→Controller→View） | 双向绑定 |
| **View与Model关系** | 通过Controller间接关联 | 完全解耦 |
| **可测试性** | Controller难测试 | ViewModel易测试（纯逻辑） |
| **代码复用** | 较差 | 较好（ViewModel可复用） |
| **学习成本** | 低 | 较高（需要理解绑定机制） |

**选择建议：**

| 场景 | 推荐架构 |
|------|---------|
| 小型项目、快速开发 | MVC |
| 大型项目、复杂UI | MVVM |
| 需要高度可测试 | MVVM |
| 团队成员水平不一 | MVC |
| 使用SwiftUI/Combine | MVVM（天然支持） |

## 【场景题】
**题目：** 在实际项目中，什么时候应该从MVC迁移到MVVM？

**答案：**

当出现以下情况时，应该考虑迁移到MVVM：

1. **ViewController过于臃肿**（超过500行代码）
2. **UI逻辑无法复用**（多个页面有相似的展示逻辑）
3. **测试困难**（无法单独测试UI逻辑）
4. **团队协作困难**（多人修改同一个ViewController冲突频繁）
5. **需要响应式编程**（使用RxSwift、Combine等）

## 【代码示例】

### MVC：登录页面（Controller处理所有逻辑）

```objective-c
// LoginViewController.h
@interface LoginViewController : UIViewController
@property (weak, nonatomic) IBOutlet UITextField *usernameField;
@property (weak, nonatomic) IBOutlet UITextField *passwordField;
@property (weak, nonatomic) IBOutlet UIButton *loginButton;
@property (weak, nonatomic) IBOutlet UILabel *errorLabel;
@end

// LoginViewController.m
@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [self loginButton].enabled = NO;
    // Controller监听文本变化
    [self.usernameField addTarget:self 
                           action:@selector(textFieldDidChange:) 
                 forControlEvents:UIControlEventEditingChanged];
    [self.passwordField addTarget:self 
                           action:@selector(textFieldDidChange:) 
                 forControlEvents:UIControlEventEditingChanged];
}

// Controller处理UI逻辑（验证、状态更新）
- (void)textFieldDidChange:(UITextField *)textField {
    BOOL isValid = [self validateUsername:self.usernameField.text 
                                password:self.passwordField.text];
    self.loginButton.enabled = isValid;
    self.loginButton.alpha = isValid ? 1.0 : 0.5;
}

// Controller处理业务逻辑（数据验证）
- (BOOL)validateUsername:(NSString *)username password:(NSString *)password {
    BOOL usernameValid = username.length >= 6;
    BOOL passwordValid = password.length >= 8;
    return usernameValid && passwordValid;
}

// Controller处理登录请求
- (IBAction)loginButtonTapped:(UIButton *)sender {
    [self errorLabel].text = @"";
    NSString *username = self.usernameField.text;
    NSString *password = self.passwordField.text;
    
    // Controller处理网络请求和回调
    [[NetworkManager sharedManager] loginWithUsername:username 
                                             password:password 
                                            completion:^(BOOL success, NSString *message) {
        if (success) {
            [self navigateToHomePage];
        } else {
            self.errorLabel.text = message;
        }
    }];
}

- (void)navigateToHomePage {
    // Controller处理页面跳转
    HomeViewController *homeVC = [[HomeViewController alloc] init];
    [self.navigationController pushViewController:homeVC animated:YES];
}

@end
```

### MVVM：登录页面（ViewModel处理UI逻辑，ViewController只负责绑定）

```objective-c
// LoginViewModel.h
@interface LoginViewModel : NSObject
@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;
@property (nonatomic, assign, readonly) BOOL isLoginEnabled;
@property (nonatomic, copy, readonly) NSString *loginButtonAlpha;
@property (nonatomic, copy) NSString *errorMessage;
@property (nonatomic, copy) void (^loginSuccess)(void);
@property (nonatomic, copy) void (^loginFailure)(NSString *error);

- (void)login;
@end

// LoginViewModel.m
@implementation LoginViewModel

// ViewModel处理UI逻辑（数据转换、验证）
- (BOOL)isLoginEnabled {
    BOOL usernameValid = self.username.length >= 6;
    BOOL passwordValid = self.password.length >= 8;
    return usernameValid && passwordValid;
}

- (NSString *)loginButtonAlpha {
    return [NSString stringWithFormat:@"%f", self.isLoginEnabled ? 1.0 : 0.5];
}

// ViewModel处理业务逻辑（网络请求）
- (void)login {
    [[NetworkManager sharedManager] loginWithUsername:self.username 
                                             password:self.password 
                                            completion:^(BOOL success, NSString *message) {
        if (success) {
            if (self.loginSuccess) {
                self.loginSuccess();
            }
        } else {
            self.errorMessage = message;
            if (self.loginFailure) {
                self.loginFailure(message);
            }
        }
    }];
}

@end

// LoginViewController.h
@interface LoginViewController : UIViewController
@property (weak, nonatomic) IBOutlet UITextField *usernameField;
@property (weak, nonatomic) IBOutlet UITextField *passwordField;
@property (weak, nonatomic) IBOutlet UIButton *loginButton;
@property (weak, nonatomic) IBOutlet UILabel *errorLabel;
@property (strong, nonatomic) LoginViewModel *viewModel;
@end

// LoginViewController.m
@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.viewModel = [[LoginViewModel alloc] init];
    
    // ViewController只负责绑定，不处理逻辑
    [self bindViewModel];
}

// ViewController只负责数据绑定
- (void)bindViewModel {
    // 文本变化绑定到ViewModel
    [self.usernameField addTarget:self 
                           action:@selector(updateViewModel) 
                 forControlEvents:UIControlEventEditingChanged];
    [self.passwordField addTarget:self 
                           action:@selector(updateViewModel) 
                 forControlEvents:UIControlEventEditingChanged];
    
    // 按钮状态绑定到ViewModel
    self.loginButton.enabled = self.viewModel.isLoginEnabled;
    self.loginButton.alpha = self.viewModel.isLoginEnabled ? 1.0 : 0.5;
    
    // 登录成功回调
    self.viewModel.loginSuccess = ^{
        [self navigateToHomePage];
    };
    
    // 登录失败回调
    self.viewModel.loginFailure = ^(NSString *error) {
        self.errorLabel.text = error;
    };
}

- (void)updateViewModel {
    self.viewModel.username = self.usernameField.text;
    self.viewModel.password = self.passwordField.text;
    self.loginButton.enabled = self.viewModel.isLoginEnabled;
    self.loginButton.alpha = self.viewModel.isLoginEnabled ? 1.0 : 0.5;
}

- (IBAction)loginButtonTapped:(UIButton *)sender {
    // ViewController只负责调用，不处理逻辑
    [self.viewModel login];
}

- (void)navigateToHomePage {
    HomeViewController *homeVC = [[HomeViewController alloc] init];
    [self.navigationController pushViewController:homeVC animated:YES];
}

@end
```

### MVC vs MVVM 代码对比

| 职责 | MVC | MVVM |
|------|-----|------|
| **UI验证逻辑** | Controller处理 | ViewModel处理 |
| **数据转换** | Controller处理 | ViewModel处理 |
| **网络请求** | Controller处理 | ViewModel处理 |
| **按钮状态更新** | Controller处理 | ViewModel处理 |
| **ViewController职责** | 处理所有逻辑 | 只负责绑定和页面跳转 |
| **可测试性** | Controller难测试（依赖UI） | ViewModel易测试（纯逻辑） |

## 【核心总结】

**iOS中MVC的实际情况：**

```
MVC（iOS实际情况）：
┌─────────────────────────────────────────────────────┐
│              ViewController                         │
│  ┌───────────────┬─────────────────────────────┐   │
│  │     View      │        Controller           │   │
│  │ （界面展示）  │ （业务逻辑、数据处理）       │   │
│  └───────────────┴─────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

MVVM：
┌─────────────────────────────────────────────────────┐
│              ViewController                         │
│  ┌───────────────┐                                 │
│  │     View      │   ← 只负责绑定和调用              │
│  │ （界面展示）  │                                 │
│  └───────────────┘                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              ViewModel                              │
│  ┌─────────────────────────────────────────────┐    │
│  │   业务逻辑、数据处理、UI状态管理             │    │
│  │   （从ViewController中抽离出来）             │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**一句话总结：**
> **MVC** = ViewController又当爹又当妈（既管界面又管逻辑）
> **MVVM** = ViewController只当"接线员"（只负责绑定和调用），ViewModel当"工程师"（负责所有逻辑）

## 【答题要点】
- MVC：Model-View-Controller，Controller协调数据和视图
- MVVM：Model-View-ViewModel，ViewModel处理UI逻辑，双向绑定
- MVC是单向数据流，MVVM是双向绑定
- MVVM中View和Model完全解耦
- ViewModel是纯逻辑，易于测试和复用
- 小型项目用MVC，大型复杂项目用MVVM
- 当ViewController过于臃肿时考虑迁移到MVVM
