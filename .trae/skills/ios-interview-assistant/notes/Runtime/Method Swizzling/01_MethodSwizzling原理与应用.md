# Method Swizzling方法交换

## 【理论题】
**题目：** 请解释Method Swizzling的作用和实现原理？
**答案：**

**Method Swizzling的作用：**
> 在运行时交换两个方法的实现（IMP），用于hook系统方法或第三方库方法，添加自定义逻辑。

**实现原理：**

```
交换前：
selector A ──────► IMP_A（原实现）
selector B ──────► IMP_B（自定义实现）

交换后：
selector A ──────► IMP_B（自定义实现）
selector B ──────► IMP_A（原实现）

调用 [obj methodA] → 实际执行 IMP_B
```

**核心API：**
```objective-c
class_getInstanceMethod()   // 获取方法
method_exchangeImplementations()  // 交换IMP
```

**与消息转发的区别：**

| 特性 | Method Swizzling | 消息转发 |
|------|-----------------|---------|
| **原理** | 直接交换IMP | 通过消息转发机制 |
| **性能** | 高（直接调用） | 较低（多走几个阶段） |
| **改动** | 修改类的方法列表 | 不修改方法列表 |
| **适用** | 全局hook | 单个对象转发 |

## 【Hook流程与时机】

**Hook一个方法的完整流程：**

```
┌─────────────────────────────────────────────────────┐
│  Step 1：确定要hook的类和方法                         │
│     - 目标类：UIViewController                       │
│     - 目标方法：viewWillAppear:                       │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Step 2：创建Category，编写自定义方法                  │
│     - 方法名：track_viewWillAppear:                  │
│     - 在方法内写自定义逻辑                             │
│     - Category的作用：给改不了源码的类添加方法          │
│     - 自己写的类可以直接在类里写，不需要Category        │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Step 3：在+load中执行交换                            │
│     - 用dispatch_once保证只执行一次                   │
│     - class_getInstanceMethod获取两个方法             │
│     - method_exchangeImplementations交换IMP           │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Step 4：调用原方法                                   │
│     - 调用swizzled方法名 = 调用原方法                  │
│     - [self track_viewWillAppear:] 实际执行原方法     │
└─────────────────────────────────────────────────────┘
```

**Hook时机对比：**

| 时机 | 方法 | 特点 | 是否推荐 |
|------|------|------|---------|
| **+load** | 类加载时调用 | main()之前，只调用一次 | ✅ 推荐 |
| **+initialize** | 类第一次使用时调用 | 懒加载，可能子类也触发 | ⚠️ 不推荐 |
| **main()之后** | AppDelegate中手动调用 | 需要手动触发 | ⚠️ 不推荐 |
| **首次使用时** | dispatch_once | 延迟加载 | ❌ 不推荐 |

**为什么用+load？**

```objective-c
// +load 的执行时机
// App启动时（main()之前）：
//   dyld加载 → runtime初始化 → +load → main()

// +load特点：
// 1. 在main()之前调用，保证hook在App运行前就生效
// 2. 每个类的+load只会调用一次
// 3. 父类的+load先于子类
// 4. 不需要手动触发

// +initialize 的执行时机
// 类第一次接收到消息时（懒加载）：
//   [Person alloc] → 触发+initialize → 然后执行alloc

// +initialize特点：
// 1. 懒加载，第一次使用时才调用
// 2. 子类没实现会调用父类的
// 3. 可能被多次调用（子类触发时父类也会触发）
// 4. 不适合做Swizzling，时机不可控
```

**Hook流程代码示例：**

```objective-c
#import <objc/runtime.h>

// ============================================
// 完整的Hook流程示例
// ============================================

// 1. 创建Category
@interface UIViewController (Tracking)
// 不需要声明，track_viewWillAppear只在内部使用
@end

@implementation UIViewController (Tracking)

// 2. 在+load中执行交换（Hook时机）
+ (void)load {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        // Step 1：确定类和方法
        Class class = [self class];
        SEL originalSelector = @selector(viewWillAppear:);
        SEL swizzledSelector = @selector(track_viewWillAppear:);
        
        // Step 2：获取方法
        Method originalMethod = class_getInstanceMethod(class, originalSelector);
        Method swizzledMethod = class_getInstanceMethod(class, swizzledSelector);
        
        // Step 3：先尝试添加（防止父类方法没被找到）
        BOOL didAddMethod = class_addMethod(class,
                                            originalSelector,
                                            method_getImplementation(swizzledMethod),
                                            method_getTypeEncoding(swizzledMethod));
        
        if (didAddMethod) {
            // 添加成功：原方法不存在，用swizzled方法替换原selector
            class_replaceMethod(class,
                               swizzledSelector,
                               method_getImplementation(originalMethod),
                               method_getTypeEncoding(originalMethod));
        } else {
            // 添加失败：原方法已存在，直接交换IMP
            method_exchangeImplementations(originalMethod, swizzledMethod);
        }
        
        NSLog(@"✅ Hook完成：UIViewController.viewWillAppear: 已被交换");
    });
}

// 3. 自定义方法（hook后的逻辑）
- (void)track_viewWillAppear:(BOOL)animated {
    // 自定义逻辑：埋点
    NSLog(@"📊 页面埋点：%@", NSStringFromClass([self class]));
    
    // 调用原方法（注意：调用自己的方法名，因为已经交换了）
    // 看起来像递归，实际上IMP已交换，调用的是原viewWillAppear:
    [self track_viewWillAppear:animated];
}

@end

// ============================================
// 为什么调用[self track_viewWillAppear:]是调用原方法？
// ============================================
// 交换前：
//   @selector(viewWillAppear:) → IMP_viewWillAppear（原方法）
//   @selector(track_viewWillAppear:) → IMP_track（自定义方法）
//
// 交换后：
//   @selector(viewWillAppear:) → IMP_track（自定义方法）
//   @selector(track_viewWillAppear:) → IMP_viewWillAppear（原方法）
//
// 所以：
//   [self viewWillAppear:] → 执行IMP_track（自定义逻辑）
//   [self track_viewWillAppear:] → 执行IMP_viewWillAppear（原方法）
// ============================================
```

## 【场景题】
**题目：** Method Swizzling有哪些实际应用场景？

**答案：**

| 场景 | 说明 |
|------|------|
| **页面埋点** | hook viewDidAppear: 自动统计页面访问 |
| **崩溃防护** | hook容器类方法（如NSArray的objectAtIndex:） |
| **性能监控** | hook消息发送，统计方法耗时 |
| **AOP编程** | 在方法前后插入统一逻辑 |
| **热修复** | JSPatch底层使用Method Swizzling |

## 【代码示例】
```objective-c
#import <objc/runtime.h>

@interface UIViewController (Tracking)
@end

@implementation UIViewController (Tracking)

+ (void)load {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        Class class = [self class];
        
        // 原方法
        SEL originalSelector = @selector(viewWillAppear:);
        Method originalMethod = class_getInstanceMethod(class, originalSelector);
        
        // 自定义方法
        SEL swizzledSelector = @selector(track_viewWillAppear:);
        Method swizzledMethod = class_getInstanceMethod(class, swizzledSelector);
        
        // 尝试添加方法（如果类中没有该方法）
        BOOL didAddMethod = class_addMethod(class,
                                            originalSelector,
                                            method_getImplementation(swizzledMethod),
                                            method_getTypeEncoding(swizzledMethod));
        
        if (didAddMethod) {
            // 添加成功，说明原方法不存在，替换swizzled方法的实现
            class_replaceMethod(class,
                               swizzledSelector,
                               method_getImplementation(originalMethod),
                               method_getTypeEncoding(originalMethod));
        } else {
            // 添加失败，说明原方法已存在，直接交换
            method_exchangeImplementations(originalMethod, swizzledMethod);
        }
    });
}

- (void)track_viewWillAppear:(BOOL)animated {
    // 自定义逻辑：埋点
    NSLog(@"页面即将显示: %@", NSStringFromClass([self class]));
    
    // 调用原方法（看起来像递归，实际上已交换）
    [self track_viewWillAppear:animated];
}

@end

// 2. 崩溃防护示例
@implementation NSArray (Safe)

+ (void)load {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        // NSArray是类簇，实际类是__NSArrayI
        Class cls = NSClassFromString(@"__NSArrayI");
        SEL originalSel = @selector(objectAtIndex:);
        SEL swizzledSel = @selector(safe_objectAtIndex:);
        
        Method originalMethod = class_getInstanceMethod(cls, originalSel);
        Method swizzledMethod = class_getInstanceMethod(cls, swizzledSel);
        
        method_exchangeImplementations(originalMethod, swizzledMethod);
    });
}

- (id)safe_objectAtIndex:(NSUInteger)index {
    if (index >= self.count) {
        NSLog(@"数组越界防护: index=%lu, count=%lu", (unsigned long)index, (unsigned long)self.count);
        return nil;
    }
    return [self safe_objectAtIndex:index];
}

@end
```

## 【答题要点】
- Method Swizzling是方法交换，直接交换IMP
- 作用：hook方法，添加自定义逻辑（埋点、崩溃防护、AOP）
- 原理：交换方法列表中两个selector对应的IMP指针
- 不是通过消息转发，是直接修改方法列表
- 在+load方法中执行，用dispatch_once保证只执行一次
- 需要注意：类簇（如NSArray、NSDictionary）要找实际类名
- 调用原方法时，调用自己的swizzled方法名（已交换）
