# MVC设计模式详解

## 【概念题】
**题目：** 请简述MVC设计模式的组成和职责？

**答案：**

```
┌─────────────────────────────────────────────────────┐
│  MVC模式组成与职责                                   │
├─────────────────────────────────────────────────────┤
│  Model（模型层）                                      │
│  ├── 封装数据（属性、关系）                          │
│  ├── 数据处理逻辑（计算、验证）                      │
│  ├── 数据持久化（CoreData、SQLite）                  │
│  └── 不关心UI，只关心数据                            │
├─────────────────────────────────────────────────────┤
│  View（视图层）                                       │
│  ├── 展示数据（界面渲染）                            │
│  ├── 用户交互（触摸、手势）                          │
│  ├── 不关心数据来源，只负责展示                      │
│  └── 通过Delegate/Target-Action与Controller通信       │
├─────────────────────────────────────────────────────┤
│  Controller（控制层）                                 │
│  ├── 协调Model和View                                │
│  ├── 处理业务逻辑                                    │
│  ├── 响应用户交互，更新Model或View                    │
│  └── iOS中ViewController既是View又是Controller        │
├─────────────────────────────────────────────────────┤
│  组件之间的关系                                       │
│  ├── View ↔ Controller（直接通信）                   │
│  ├── Controller ↔ Model（直接通信）                  │
│  ├── View ↔ Model（禁止直接通信）                    │
│  └── 数据流向：Model → Controller → View             │
└─────────────────────────────────────────────────────┘

iOS中的MVC特殊实现：
├── ViewController继承UIViewController
├── 内部包含view属性（View层）
├── 自身承担Controller职责
├── 导致ViewController容易臃肿（MVC的缺点）

解决方案：
├── MVVM：抽取ViewModel处理业务逻辑
├── MVP：引入Presenter层
└── VIPER：更清晰的分层架构
```

## 【场景题】
**题目：** 如何在iOS中正确实现MVC模式？

**答案：**

```objective-c
// Model
@interface UserModel : NSObject

@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;
@property (nonatomic, assign) NSInteger age;

- (BOOL)validateUsername;
- (BOOL)validatePassword;

@end

@implementation UserModel

- (BOOL)validateUsername {
    return self.username.length >= 6;
}

- (BOOL)validatePassword {
    return self.password.length >= 8;
}

@end

// View（自定义View）
@protocol LoginViewDelegate <NSObject>

- (void)loginButtonTappedWithUsername:(NSString *)username password:(NSString *)password;

@end

@interface LoginView : UIView

@property (nonatomic, weak) id<LoginViewDelegate> delegate;
@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;
@property (nonatomic, strong) UIButton *loginButton;

@end

@implementation LoginView

- (instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        [self setupSubviews];
    }
    return self;
}

- (void)setupSubviews {
    self.usernameField = [[UITextField alloc] initWithFrame:CGRectMake(20, 60, 280, 40)];
    self.usernameField.placeholder = @"用户名";
    [self addSubview:self.usernameField];
    
    self.passwordField = [[UITextField alloc] initWithFrame:CGRectMake(20, 120, 280, 40)];
    self.passwordField.placeholder = @"密码";
    self.passwordField.secureTextEntry = YES;
    [self addSubview:self.passwordField];
    
    self.loginButton = [[UIButton alloc] initWithFrame:CGRectMake(20, 180, 280, 40)];
    [self.loginButton setTitle:@"登录" forState:UIControlStateNormal];
    [self.loginButton setBackgroundColor:[UIColor blueColor]];
    [self.loginButton addTarget:self action:@selector(loginButtonTapped) forControlEvents:UIControlEventTouchUpInside];
    [self addSubview:self.loginButton];
}

- (void)loginButtonTapped {
    if ([self.delegate respondsToSelector:@selector(loginButtonTappedWithUsername:password:)]) {
        [self.delegate loginButtonTappedWithUsername:self.usernameField.text password:self.passwordField.text];
    }
}

@end

// Controller
@interface LoginViewController : UIViewController <LoginViewDelegate>

@property (nonatomic, strong) LoginView *loginView;
@property (nonatomic, strong) UserModel *userModel;

@end

@implementation LoginViewController

- (void)loadView {
    self.loginView = [[LoginView alloc] initWithFrame:[UIScreen mainScreen].bounds];
    self.loginView.delegate = self;
    self.view = self.loginView;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    self.userModel = [[UserModel alloc] init];
}

- (void)loginButtonTappedWithUsername:(NSString *)username password:(NSString *)password {
    // 更新Model
    self.userModel.username = username;
    self.userModel.password = password;
    
    // 验证数据
    if ([self.userModel validateUsername] && [self.userModel validatePassword]) {
        [self performLogin];
    } else {
        [self showError];
    }
}

- (void)performLogin {
    // 网络请求等业务逻辑
    NSLog(@"登录中...");
}

- (void)showError {
    // 更新View
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"错误" message:@"用户名或密码格式错误" preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:YES completion:nil];
}

@end
```

## 【代码示例】
```objective-c
// MVC中数据流转示例
// 用户点击按钮 → Controller处理 → 更新Model → 更新View

// View触发事件（通过Delegate/Target-Action）
- (void)loginButtonTapped {
    [self.delegate loginButtonTapped];
}

// Controller处理事件
- (void)loginButtonTapped {
    // 1. 获取View的数据
    NSString *username = self.loginView.usernameField.text;
    
    // 2. 更新Model
    self.userModel.username = username;
    
    // 3. 更新View
    [self.loginView showLoading];
    
    // 4. 业务逻辑处理
    [self.userModel save];
}

// Model数据变化通知Controller（通过KVO/Block/Delegate）
// Controller再更新View
```