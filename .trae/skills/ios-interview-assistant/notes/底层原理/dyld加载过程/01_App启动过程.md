# dyld加载过程

## 【理论题】
**题目：** 请简述App从点击到启动的大致过程？
**答案：**

**App启动过程（dyld加载）：**

**dyld是什么？**
> dyld = Dynamic Link Editor（动态链接器），是iOS系统的动态库加载器。
> 
> 简单说：**App的可执行文件就是被dyld"叫醒"的**。它负责把App运行需要的所有动态库（系统库、第三方库）加载到内存，链接好符号，然后把控制权交给App的main()函数。

```
点击App图标 → dyld加载 → main() → UIApplicationMain → 首屏渲染

┌─────────────────────────────────────────────────────┐
│  1. dyld加载动态库                                   │
│     - 加载可执行文件（如App叫MyDemo，编译产物就是MyDemo）│
│     - 加载所有依赖的动态库（UIKit、Foundation等系统库） │
│     - 链接、重定位符号（把代码里[UIView new]的调用接上│
│       UIKit动态库里的实现，让代码能找到对应方法）            │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. runtime初始化                                    │
│     - 注册所有类（把Person类、Dog类登记到内存，        │
│       因为后续调用方法时runtime需要通过类名找到对应    │
│       的isa指针、方法列表等元信息）                    │
│     - +load方法调用（此时main()还没执行，一般用于       │
│       Method Swizzle方法交换、埋点注册、初始化配置等）  │
│     - 初始化方法缓存（建好"方法速查表"加速后续调用）    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. main()函数                                       │
│     - 进入UIApplicationMain                          │
│     - 创建UIApplication对象                          │
│     - 设置AppDelegate                                │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  4. AppDelegate生命周期                               │
│     - application:didFinishLaunchingWithOptions:    │
│     - 配置根控制器、初始化SDK等                       │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  5. 首屏渲染                                         │
│     - 加载首屏控制器                                  │
│     - 计算布局、渲染视图                              │
│     - 用户可以看到首屏                                │
└─────────────────────────────────────────────────────┘
```

**启动时间划分：**

| 阶段 | 名称 | 关键点 |
|------|------|--------|
| **T0~T1** | dyld加载 | 动态库加载、链接 |
| **T1~T2** | runtime初始化 | +load方法、类注册 |
| **T2~T3** | main()到首屏渲染 | AppDelegate、首屏加载 |
| **T0~T3** | 总启动时间 | 冷启动 = T3 - T0 |

## 【场景题】
**题目：** 启动优化有哪些方向？

**答案：**

| 优化方向 | 具体方法 |
|---------|---------|
| **减少动态库** | 合并动态库、静态库化 |
| **+load优化** | 延迟到+initialize、减少+load |
| **首屏优化** | 异步加载非首屏资源、占位图 |
| **懒加载** | 非必需模块延迟初始化 |
| **二进制重排** | 减少Page Fault |

## 【代码示例】
```objective-c
// 1. main.m入口
int main(int argc, char * argv[]) {
    NSString *appDelegateClassName;
    @autoreleasepool {
        appDelegateClassName = NSStringFromClass([AppDelegate class]);
    }
    return UIApplicationMain(argc, argv, nil, appDelegateClassName);
}

// 2. AppDelegate启动回调
@interface AppDelegate : UIResponder <UIApplicationDelegate>
@property (strong, nonatomic) UIWindow *window;
@end

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application 
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    
    // 初始化根控制器
    self.window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
    ViewController *rootVC = [[ViewController alloc] init];
    self.window.rootViewController = rootVC;
    [self.window makeKeyAndVisible];
    
    return YES;
}

@end

// 3. +load方法（类加载时调用）
// 注意：+load在main()之前调用，启动优化时要减少+load中的代码
@implementation SomeClass

+ (void)load {
    NSLog(@"类被加载了，此时main()还没执行");
    // 尽量不要在这里写太多代码，会拖慢启动
}

+ (void)initialize {
    if (self == [SomeClass class]) {
        // 第一次使用类时调用，比+load更合适
    }
}

@end
```

## 【答题要点】
- 启动过程：dyld加载 → runtime初始化 → main() → AppDelegate → 首屏渲染
- dyld负责加载动态库和链接
- runtime负责注册类、调用+load
- UIApplicationMain创建UIApplication和AppDelegate
- didFinishLaunchingWithOptions是启动配置的入口
- 启动优化方向：减少动态库、减少+load、首屏懒加载、二进制重排
- +load在main()之前调用，+initialize在第一次使用类时调用
