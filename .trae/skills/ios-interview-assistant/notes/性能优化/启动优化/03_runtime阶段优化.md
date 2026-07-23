# runtime阶段优化（+load方法优化）

## 【理论题】
**题目：** 请解释+load方法的执行时机，以及为什么过多的+load会拖慢启动？
**答案：**

**+load方法执行时机：**

```
App启动流程：
T0 → dyld加载动态库 → runtime初始化 → +load → T1 → main()

+load执行顺序：
1. 父类的+load先于子类
2. Category的+load在主类之后
3. 所有+load在main()之前执行

+load特点：
┌─────────────────────────────────────────────────────┐
│  - 在main()之前调用                                  │
│  - 每个类的+load只会调用一次                          │
│  - 父类先于子类执行                                  │
│  - Category的+load在主类之后                        │
│  - 不能手动调用（系统自动调用）                        │
└─────────────────────────────────────────────────────┘
```

**为什么+load会拖慢启动？**

```
+load在main()之前执行，是串行执行的：
类A的+load → 类B的+load → 类C的+load → ... → main()

如果某个+load中有耗时操作：
+load总耗时 = 类A耗时 + 类B耗时 + 类C耗时 + ...

示例：
类A的+load：读取配置文件（50ms）
类B的+load：网络请求（200ms）❌ 严重拖慢启动
类C的+load：初始化SDK（100ms）

总+load耗时：350ms，这350ms都会加到启动时间里！
```

**+load vs +initialize：**

| 特性 | +load | +initialize |
|------|-------|-------------|
| 执行时机 | main()之前 | 类第一次使用时 |
| 执行次数 | 只一次 | 只一次（懒加载） |
| 父类子类 | 父类先执行 | 子类没实现会调用父类 |
| **阻塞启动** | ✅ 阻塞 | ❌ 不阻塞（懒加载） |
| **适用场景** | Method Swizzling | 懒加载初始化 |

**必须在+load中执行的场景：**

```
┌─────────────────────────────────────────────────────┐
│  1. Method Swizzling（方法交换）                       │
│                                                      │
│  原因：需要在main()之前完成hook                        │
│  如果等到+initialize，可能已经有代码调用了原方法         │
│  示例：hook UIViewController的viewWillAppear:          │
│  必须在+load中执行，否则首屏的viewWillAppear不会被hook   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  2. 全局配置（必须在App运行前完成）                     │
│                                                      │
│  原因：某些配置需要在所有代码执行前生效                  │
│  示例：设置全局日志级别、配置全局异常捕获                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  3. 注册通知（必须在main()之前注册）                    │
│                                                      │
│  原因：某些系统通知在main()之前就会发出                  │
│  示例：UIApplicationDidFinishLaunchingNotification    │
│        不需要在+load中（在didLaunching中注册即可）        │
│        但某些底层通知可能需要在+load中注册               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  4. 初始化顺序依赖（必须保证执行顺序）                   │
│                                                      │
│  原因：+load的执行顺序是确定的（父类→子类→Category）     │
│        +initialize的执行顺序不确定（懒加载）             │
│  如果你的初始化依赖特定的执行顺序，必须用+load           │
└─────────────────────────────────────────────────────┘
```

**可以延迟到+initialize的场景：**

| 场景 | 说明 |
|------|------|
| **SDK初始化** | 第一次使用时才初始化 |
| **配置加载** | 第一次使用时才加载 |
| **数据缓存** | 第一次使用时才读取 |
| **工具类初始化** | 第一次使用时才初始化 |

**总结：**
> 必须在+load中：Method Swizzling、全局配置、初始化顺序依赖
> 可以延迟到+initialize：SDK初始化、配置加载、数据缓存等非紧急操作

## 【场景题】
**题目：** 如何优化+load方法？

**答案：**

| 优化方法 | 说明 |
|---------|------|
| **移除耗时操作** | 网络请求、文件读写移到+initialize |
| **延迟到+initialize** | 懒加载，第一次使用时才执行 |
| **合并+load** | 多个小+load合并成一个 |
| **使用dispatch_once** | 在+initialize中懒加载 |
| **使用懒加载单例** | 第一次使用时才初始化 |

## 【代码示例】
```objective-c
// ❌ 不好的做法：在+load中做耗时操作
@implementation BadClass
+ (void)load {
    // ❌ 网络请求 - 严重拖慢启动
    [self fetchConfigFromServer];
    
    // ❌ 大量计算
    [self heavyComputation];
}
@end

// ✅ 好的做法：延迟到+initialize
@implementation GoodClass
+ (void)load {
    // 只做Method Swizzling等必须在main()之前执行的操作
    [self swizzleMethods];
}

+ (void)initialize {
    if (self == [GoodClass class]) {
        // ✅ 懒加载：第一次使用时才初始化
        [self loadConfig];
        [self initializeSDK];
    }
}
@end

// ✅ 使用dispatch_once延迟初始化
@implementation LazyInitClass
+ (void)initialize {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        // 初始化代码，只执行一次
        [self setup];
    });
}
@end

// ✅ 使用懒加载单例
@interface ConfigManager : NSObject
+ (instancetype)sharedManager;
@end

@implementation ConfigManager
+ (instancetype)sharedManager {
    static ConfigManager *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
        [instance loadConfig];  // 第一次使用时才加载
    });
    return instance;
}
@end

// ✅ 检测+load耗时（在+load中埋点）
// 在AppDelegate中记录所有+load的总耗时
// T1 = runtime初始化完成时间（所有+load执行完）
```

## 【答题要点】
- +load在main()之前执行，阻塞启动流程
- +load执行顺序：父类→子类→Category
- +load只执行一次，+initialize懒加载执行
- 优化策略：移除耗时操作、延迟到+initialize、合并+load
- Method Swizzling必须在+load中执行（需要在main()之前hook）
- +initialize注意：子类没实现会调用父类的，需要判断self == [Class class]
- 使用dispatch_once保证初始化只执行一次
- 懒加载单例是最常用的延迟初始化方式
