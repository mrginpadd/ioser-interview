# UIViewController生命周期

## 【理论题】
**题目：** 请按照执行顺序列出UIViewController的生命周期方法，并说明每个方法的作用？
**答案：**

**UIViewController生命周期完整顺序：**

```
┌─────────────────────────────────────────────────────┐
│  完整生命周期顺序（首次加载）：                        │
│                                                     │
│  1. init                 ← 创建对象                   │
│  2. loadView             ← 创建视图（手动创建view时用） │
│  3. viewDidLoad          ← 视图加载完成               │
│  4. viewWillAppear       ← 视图即将显示               │
│  5. viewWillLayoutSubviews ← 即将布局子视图           │
│  6. viewDidLayoutSubviews  ← 布局完成                 │
│  7. viewDidAppear        ← 视图已经显示               │
│                                                     │
│  ═════════ 进入后台/切换页面 ═════════                │
│                                                     │
│  8. viewWillDisappear    ← 视图即将消失               │
│  9. viewDidDisappear     ← 视图已经消失               │
│                                                     │
│  ═════════ 释放 ═════════                          │
│                                                     │
│  10. dealloc             ← 对象释放                   │
└─────────────────────────────────────────────────────┘
```

**各方法作用：**

| 方法 | 作用 | 调用次数 |
|------|------|---------|
| **init** | 创建对象，初始化数据 | 1次 |
| **loadView** | 手动创建view（不使用xib/storyboard时） | 1次 |
| **viewDidLoad** | 视图加载完成，初始化UI | 1次 |
| **viewWillAppear** | 视图即将显示，准备数据 | 多次 |
| **viewWillLayoutSubviews** | 即将布局子视图 | 多次 |
| **viewDidLayoutSubviews** | 布局完成，调整frame | 多次 |
| **viewDidAppear** | 视图已经显示，开始动画/网络请求 | 多次 |
| **viewWillDisappear** | 视图即将消失，保存状态 | 多次 |
| **viewDidDisappear** | 视图已经消失，清理资源 | 多次 |
| **dealloc** | 对象释放，清理内存 | 1次 |

## 【场景题】
**题目：** viewDidLoad和viewDidAppear的区别？什么时候用哪个？

**答案：**

| 特性 | viewDidLoad | viewDidAppear |
|------|------------|---------------|
| **调用时机** | 视图首次加载完成 | 视图每次显示时 |
| **调用次数** | 仅一次 | 可多次 |
| **UI状态** | view已创建但未显示 | view已显示在屏幕上 |
| **使用场景** | 初始化UI、设置约束 | 开始动画、网络请求 |

**选择建议：**
- 一次性初始化（如创建子视图）→ viewDidLoad
- 需要每次显示都执行（如刷新数据）→ viewDidAppear
- 动画、定位等需要屏幕显示后才能执行的操作 → viewDidAppear

## 【代码示例】
```objective-c
@interface ViewController : UIViewController
@property (strong, nonatomic) UILabel *titleLabel;
@property (strong, nonatomic) NSArray *data;
@end

@implementation ViewController

// 1. 创建对象
- (instancetype)init {
    if (self = [super init]) {
        // 初始化数据
        _data = @[@"item1", @"item2", @"item3"];
    }
    return self;
}

// 2. 手动创建视图（不使用xib时）
- (void)loadView {
    self.view = [[UIView alloc] initWithFrame:[UIScreen mainScreen].bounds];
    self.view.backgroundColor = [UIColor whiteColor];
}

// 3. 视图加载完成，初始化UI
- (void)viewDidLoad {
    [super viewDidLoad];
    // 创建子视图（一次性操作）
    self.titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 100, 200, 30)];
    self.titleLabel.text = @"标题";
    [self.view addSubview:self.titleLabel];
}

// 4. 视图即将显示，准备数据
- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    // 更新导航栏
    self.navigationItem.title = @"首页";
}

// 5. 即将布局子视图
- (void)viewWillLayoutSubviews {
    [super viewWillLayoutSubviews];
    // 调整视图布局前的准备
}

// 6. 布局完成，调整frame
- (void)viewDidLayoutSubviews {
    [super viewDidLayoutSubviews];
    // 根据父视图大小调整子视图位置
    self.titleLabel.center = CGPointMake(self.view.center.x, 100);
}

// 7. 视图已经显示，开始动画/网络请求
- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    // 开始动画
    [UIView animateWithDuration:0.3 animations:^{
        self.titleLabel.alpha = 1.0;
    }];
    // 发起网络请求
    [self fetchData];
}

// 8. 视图即将消失，保存状态
- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    // 保存用户输入
}

// 9. 视图已经消失，清理资源
- (void)viewDidDisappear:(BOOL)animated {
    [super viewDidDisappear:animated];
    // 停止动画、定时器等
}

// 10. 对象释放，清理内存
- (void)dealloc {
    // 释放资源（ARC自动管理大部分）
}

@end
```

## 【答题要点】
- 生命周期顺序：init → loadView → viewDidLoad → viewWillAppear → viewWillLayoutSubviews → viewDidLayoutSubviews → viewDidAppear → viewWillDisappear → viewDidDisappear → dealloc
- viewDidLoad仅调用一次，用于初始化UI
- viewWillAppear/viewDidAppear会多次调用，用于准备数据和开始动画
- viewWillDisappear/viewDidDisappear用于保存状态和清理资源
- viewDidLayoutSubviews在布局完成后调用，用于调整frame
- loadView仅在手动创建view时使用
