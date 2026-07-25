# MVVM设计模式详解

## 【概念题】
**题目：** 请简述MVVM设计模式与MVC的区别？

**答案：**

```
┌─────────────────────────────────────────────────────┐
│  MVVM模式组成与职责                                  │
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
│  ├── 通过数据绑定展示ViewModel的数据                 │
│  └── 通过命令（Command）调用ViewModel的方法           │
├─────────────────────────────────────────────────────┤
│  ViewModel（视图模型层）                              │
│  ├── 封装UI逻辑和业务逻辑                            │
│  ├── 暴露供View绑定的数据（属性）                    │
│  ├── 暴露供View调用的命令（方法）                    │
│  ├── 处理Model的数据，转换为View可用的格式            │
│  └── 不持有View引用，只负责数据转换                  │
├─────────────────────────────────────────────────────┤
│  Controller（控制层）                                 │
│  ├── 在MVVM中职责大大简化                            │
│  ├── 只负责创建ViewModel和View的绑定                 │
│  ├── 不处理业务逻辑                                 │
│  └── 相当于"接线员"角色                             │
└─────────────────────────────────────────────────────┘

MVVM与MVC的核心区别：
├── MVC：ViewController承担所有逻辑，容易臃肿
├── MVVM：ViewModel抽取业务逻辑，ViewController只做绑定
├── MVC：View通过Delegate/Target-Action与Controller通信
├── MVVM：View通过数据绑定与ViewModel通信
├── MVC：测试困难（业务逻辑在ViewController中）
├── MVVM：测试容易（ViewModel独立，可单元测试）

数据绑定方式（iOS中常用）：
├── KVO：监听ViewModel属性变化，更新View
├── Block：ViewModel通过Block回调更新View
├── RxSwift：响应式编程，自动绑定
└── ReactiveObjC：基于KVO的响应式框架
```

## 【场景题】
**题目：** 如何在iOS中正确实现MVVM模式？

**答案：**

```objective-c
// Model
@interface UserModel : NSObject

@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;

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

// ViewModel
@interface LoginViewModel : NSObject

@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *password;
@property (nonatomic, assign) BOOL isLoading;
@property (nonatomic, assign) BOOL isLoginEnabled;
@property (nonatomic, copy) NSString *errorMessage;

@property (nonatomic, strong) UserModel *userModel;

- (void)loginWithCompletion:(void(^)(BOOL success))completion;

@end

@implementation LoginViewModel

- (instancetype)init {
    self = [super init];
    if (self) {
        _userModel = [[UserModel alloc] init];
    }
    return self;
}

- (void)setUsername:(NSString *)username {
    _username = [username copy];
    _userModel.username = username;
    [self updateLoginEnabled];
}

- (void)setPassword:(NSString *)password {
    _password = [password copy];
    _userModel.password = password;
    [self updateLoginEnabled];
}

- (void)updateLoginEnabled {
    self.isLoginEnabled = [_userModel validateUsername] && [_userModel validatePassword];
}

- (void)loginWithCompletion:(void(^)(BOOL success))completion {
    self.isLoading = YES;
    self.errorMessage = nil;
    
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 1.0 * NSEC_PER_SEC), dispatch_get_main_queue(), ^{
        BOOL success = [self.userModel validateUsername] && [self.userModel validatePassword];
        self.isLoading = NO;
        
        if (!success) {
            self.errorMessage = @"用户名或密码格式错误";
        }
        
        completion(success);
    });
}

@end

// View（ViewController）
@interface LoginViewController : UIViewController

@property (nonatomic, strong) UITextField *usernameField;
@property (nonatomic, strong) UITextField *passwordField;
@property (nonatomic, strong) UIButton *loginButton;
@property (nonatomic, strong) UIActivityIndicatorView *loadingIndicator;
@property (nonatomic, strong) UILabel *errorLabel;

@property (nonatomic, strong) LoginViewModel *viewModel;

@end

@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self setupSubviews];
    [self setupViewModel];
    [self setupBindings];
}

- (void)setupSubviews {
    self.view.backgroundColor = [UIColor whiteColor];
    
    self.usernameField = [[UITextField alloc] initWithFrame:CGRectMake(20, 60, 280, 40)];
    self.usernameField.placeholder = @"用户名";
    self.usernameField.borderStyle = UITextBorderStyleRoundedRect;
    [self.view addSubview:self.usernameField];
    
    self.passwordField = [[UITextField alloc] initWithFrame:CGRectMake(20, 120, 280, 40)];
    self.passwordField.placeholder = @"密码";
    self.passwordField.secureTextEntry = YES;
    self.passwordField.borderStyle = UITextBorderStyleRoundedRect;
    [self.view addSubview:self.passwordField];
    
    self.loginButton = [[UIButton alloc] initWithFrame:CGRectMake(20, 180, 280, 40)];
    [self.loginButton setTitle:@"登录" forState:UIControlStateNormal];
    [self.loginButton setBackgroundColor:[UIColor blueColor]];
    [self.loginButton addTarget:self action:@selector(loginButtonTapped) forControlEvents:UIControlEventTouchUpInside];
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
}

- (void)setupBindings {
    // View → ViewModel（用户输入）
    [self.usernameField addTarget:self action:@selector(usernameChanged:) forControlEvents:UIControlEventEditingChanged];
    [self.passwordField addTarget:self action:@selector(passwordChanged:) forControlEvents:UIControlEventEditingChanged];
    
    // ViewModel → View（数据绑定，使用KVO）
    [self.viewModel addObserver:self forKeyPath:@"isLoginEnabled" options:NSKeyValueObservingOptionNew context:nil];
    [self.viewModel addObserver:self forKeyPath:@"isLoading" options:NSKeyValueObservingOptionNew context:nil];
    [self.viewModel addObserver:self forKeyPath:@"errorMessage" options:NSKeyValueObservingOptionNew context:nil];
}

- (void)usernameChanged:(UITextField *)textField {
    self.viewModel.username = textField.text;
}

- (void)passwordChanged:(UITextField *)textField {
    self.viewModel.password = textField.text;
}

- (void)loginButtonTapped {
    [self.viewModel loginWithCompletion:^(BOOL success) {
        if (success) {
            NSLog(@"登录成功");
        }
    }];
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary<NSKeyValueChangeKey,id> *)change context:(void *)context {
    if ([keyPath isEqualToString:@"isLoginEnabled"]) {
        self.loginButton.enabled = [change[NSKeyValueChangeNewKey] boolValue];
    } else if ([keyPath isEqualToString:@"isLoading"]) {
        BOOL isLoading = [change[NSKeyValueChangeNewKey] boolValue];
        self.loadingIndicator.hidden = !isLoading;
        self.loginButton.hidden = isLoading;
        if (isLoading) {
            [self.loadingIndicator startAnimating];
        } else {
            [self.loadingIndicator stopAnimating];
        }
    } else if ([keyPath isEqualToString:@"errorMessage"]) {
        self.errorLabel.text = change[NSKeyValueChangeNewKey];
    }
}

- (void)dealloc {
    [self.viewModel removeObserver:self forKeyPath:@"isLoginEnabled"];
    [self.viewModel removeObserver:self forKeyPath:@"isLoading"];
    [self.viewModel removeObserver:self forKeyPath:@"errorMessage"];
}

@end
```

## 【代码示例】
```objective-c
// MVVM中数据流转示例
// 用户输入 → ViewModel处理 → 更新View

// View → ViewModel（用户输入）
- (void)usernameChanged:(UITextField *)textField {
    self.viewModel.username = textField.text;
}

// ViewModel处理（自动更新属性）
- (void)setUsername:(NSString *)username {
    _username = [username copy];
    [self updateLoginEnabled]; // 自动更新登录按钮状态
}

// ViewModel → View（KVO绑定）
- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    if ([keyPath isEqualToString:@"isLoginEnabled"]) {
        self.loginButton.enabled = [change[NSKeyValueChangeNewKey] boolValue];
    }
}

// MVVM的优点：
// 1. ViewController代码简洁，只负责绑定
// 2. ViewModel独立，可进行单元测试
// 3. 数据流向清晰（View → ViewModel → Model）
// 4. 易于维护和扩展
```