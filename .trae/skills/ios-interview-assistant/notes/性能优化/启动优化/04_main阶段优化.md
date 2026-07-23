# main阶段优化（异步初始化）

## 【理论题】
**题目：** 请解释main()阶段的优化方向，以及如何实现异步初始化？
**答案：**

**main()阶段时间线：**

```
T2 ─────────────────────────────── T3
│                                 │
main() → didLaunching → 首屏渲染   │
                                 │
优化目标：减少T2~T3的耗时          │
```

**优化方向：**

| 优化方向 | 具体方法 |
|---------|---------|
| **SDK异步初始化** | 非首屏必需的SDK放到后台线程 |
| **首屏必需SDK同步** | 首屏必需的SDK同步初始化 |
| **非首屏资源懒加载** | 图片、数据延迟加载 |
| **简化首屏VC** | 减少视图层级、简化逻辑 |
| **占位图** | 先用占位图，再异步加载真实内容 |

**为什么异步初始化能优化启动？**

```
同步初始化（不好）：
didLaunching:
├── SDK1初始化（100ms）
├── SDK2初始化（150ms）
├── SDK3初始化（80ms）
└── 总耗时：330ms

异步初始化（好）：
didLaunching:
├── 首屏必需SDK同步初始化（50ms）
└── 总耗时：50ms ✅

后台线程：
├── SDK1异步初始化（100ms）
├── SDK2异步初始化（150ms）
└── SDK3异步初始化（80ms）
```

## 【场景题】
**题目：** 如何判断哪些SDK需要同步初始化，哪些可以异步？

**答案：**

| SDK类型 | 初始化方式 | 原因 |
|---------|-----------|------|
| **核心SDK**（如登录、路由） | 同步 | 首屏需要立即使用 |
| **埋点SDK** | 异步 | 不影响首屏 |
| **崩溃上报SDK** | 异步 | 不影响首屏 |
| **推送SDK** | 异步 | 不影响首屏 |
| **图片缓存SDK**（如SDWebImage） | 异步 | 首屏图片可延迟加载 |
| **网络SDK**（如AFNetworking） | 可同步可异步 | 根据首屏是否需要网络请求 |

## 【代码示例】
```objective-c
// ✅ 异步初始化示例
- (BOOL)application:(UIApplication *)application 
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    
    // 1. 首屏必需的SDK同步初始化
    [CoreSDK initialize];
    [RouterSDK setup];
    
    // 2. 非首屏必需的SDK异步初始化
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        // 埋点SDK
        [AnalyticsSDK startWithConfig:config];
        
        // 崩溃上报SDK
        [CrashReportSDK start];
        
        // 推送SDK
        [PushSDK registerForRemoteNotifications];
        
        // 图片缓存SDK
        [[SDWebImageManager sharedManager] start];
    });
    
    // 3. 延迟初始化（首屏渲染后）
    [self setupDeferredInitialization];
    
    return YES;
}

- (void)setupDeferredInitialization {
    // 首屏渲染完成后1秒再初始化非关键模块
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1.0 * NSEC_PER_SEC)), 
                   dispatch_get_main_queue(), ^{
        [self loadNonCriticalModules];
    });
}

- (void)loadNonCriticalModules {
    // 非首屏页面的懒加载
    [self initializeSecondPageModules];
    [self initializeSettingsModules];
    [self initializeProfileModules];
}

// ✅ 使用Operation队列控制初始化顺序
- (void)setupWithOperations {
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];
    queue.maxConcurrentOperationCount = 2;
    
    // 依赖关系：CoreSDK完成后再初始化其他SDK
    NSBlockOperation *coreOp = [NSBlockOperation blockOperationWithBlock:^{
        [CoreSDK initialize];
    }];
    
    NSBlockOperation *analyticsOp = [NSBlockOperation blockOperationWithBlock:^{
        [AnalyticsSDK start];
    }];
    [analyticsOp addDependency:coreOp];
    
    NSBlockOperation *pushOp = [NSBlockOperation blockOperationWithBlock:^{
        [PushSDK register];
    }];
    [pushOp addDependency:coreOp];
    
    [queue addOperations:@[coreOp, analyticsOp, pushOp] waitUntilFinished:NO];
}

// ✅ 首屏优化：使用占位图
- (void)setupFirstPage {
    // 先用占位图
    self.imageView.image = [UIImage placeholderImage];
    
    // 异步加载真实图片
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        UIImage *image = [self downloadImageFromURL:url];
        dispatch_async(dispatch_get_main_queue(), ^{
            self.imageView.image = image;
        });
    });
    
    // 异步加载数据
    [self fetchDataAsync];
}

// ✅ 使用懒加载属性
@property (nonatomic, strong) DataManager *dataManager;

- (DataManager *)dataManager {
    if (!_dataManager) {
        _dataManager = [[DataManager alloc] init];
        [_dataManager loadData];
    }
    return _dataManager;
}

// 使用时才初始化
[self.dataManager fetchData];
```

## 【答题要点】
- main()阶段优化：异步初始化非首屏必需的SDK
- 判断标准：首屏是否需要立即使用该SDK
- 核心SDK同步初始化，非核心SDK异步初始化
- 使用dispatch_async放到后台线程
- 使用dispatch_after延迟到首屏渲染后
- 使用NSOperationQueue控制初始化顺序和并发数
- 首屏使用占位图，异步加载真实内容
- 使用懒加载属性延迟初始化对象
- 非首屏页面的模块完全懒加载
