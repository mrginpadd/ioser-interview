# KVO实现原理

## 【理论题】
**题目：** 请解释KVO的实现原理，以及它是如何监听属性变化的？
**答案：**

**KVO实现原理：**

**KVO的本质是Runtime动态生成子类，重写setter方法来监听属性变化。**
KVO实现流程:
┌─────────────────────────────────────────────────────┐
│  1. 添加观察者                                       │
│     [obj addObserver:self forKeyPath:@"property"    │
│              options:NSKeyValueObservingOptionNew   │
│              context:NULL];                         │
│                                                     │
│  2. Runtime动态生成子类 NSKVONotifying_ClassName     │
│     并重写setter方法:                                │
│     - (void)setProperty:(id)value {                 │
│         [self willChangeValueForKey:@"property"];    │
│         [super setProperty:value];                   │
│         [self didChangeValueForKey:@"property"];     │
│     }                                               │
│                                                     │
│  3. 将对象的isa指针指向动态子类                       │
│                                                     │
│  4. 修改属性时，调用重写的setter方法                   │
│     didChangeValueForKey内部触发回调                  │
│                                                     │
│  5. 回调方法:                                      │
│     - (void)observeValueForKeyPath:(NSString *)keyPath│
│                           ofObject:(id)object       │
│                             change:(NSDictionary *)change│
│                            context:(void *)context   │
│     {                                               │
│         // 处理属性变化                              │
│     }                                               │
└─────────────────────────────────────────────────────┘

工作流程：
1. 添加观察者时，Runtime动态生成子类`NSKVONotifying_ClassName`
2. 动态子类重写setter方法，调用`willChangeValueForKey:`和`didChangeValueForKey:`
3. 将对象的isa指针指向动态子类
4. 修改属性时，调用重写的setter方法，`didChangeValueForKey:`内部触发回调
5. 回调`observeValueForKeyPath:ofObject:change:context:`方法

```objective-c
// 动态子类重写的setter方法伪代码
- (void)setProperty:(id)value {
    [self willChangeValueForKey:@"property"];
    [super setProperty:value];
    [self didChangeValueForKey:@"property"];
}
```

**关键要点：**

| 特性 | 说明 |
|------|------|
| **动态子类** | Runtime生成`NSKVONotifying_ClassName`子类 |
| **isa指针** | 对象的isa指向动态子类 |
| **setter重写** | 动态子类重写setter方法 |
| **通知机制** | 通过`willChangeValueForKey:`和`didChangeValueForKey:`通知 |
| **手动触发** | 可手动调用willChange/didChange触发KVO |

**手动触发KVO：**

```objective-c
- (void)updateProperty {
    [self willChangeValueForKey:@"property"];
    _property = newValue;  // 直接修改实例变量，不走setter
    [self didChangeValueForKey:@"property"];
}
```

## 【场景题】
**题目：** 直接修改实例变量`_property`会触发KVO吗？为什么？

**答案：**

不会触发KVO。

**原因：**

KVO是通过重写setter方法实现的，直接修改实例变量不走setter方法，所以不会触发KVO。

**解决方法：**

```objective-c
// 方法1：使用setter方法（推荐）
self.property = newValue;

// 方法2：手动触发KVO
[self willChangeValueForKey:@"property"];
_property = newValue;
[self didChangeValueForKey:@"property"];
```

## 【代码示例】
```objective-c
// 添加观察者
@interface ViewController ()
@property (nonatomic, strong) Person *person;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.person = [[Person alloc] init];
    
    // 添加KVO观察者
    [self.person addObserver:self 
                  forKeyPath:@"name" 
                     options:NSKeyValueObservingOptionNew | NSKeyValueObservingOptionOld
                     context:NULL];
    
    // 修改属性，触发KVO
    self.person.name = @"New Name";
}

// KVO回调
- (void)observeValueForKeyPath:(NSString *)keyPath 
                      ofObject:(id)object 
                        change:(NSDictionary<NSString *,id> *)change 
                       context:(void *)context {
    if ([keyPath isEqualToString:@"name"]) {
        NSString *newValue = change[NSKeyValueChangeNewKey];
        NSString *oldValue = change[NSKeyValueChangeOldKey];
        NSLog(@"name changed from %@ to %@", oldValue, newValue);
    }
}

- (void)dealloc {
    // 移除观察者
    [self.person removeObserver:self forKeyPath:@"name"];
}

@end
```

## 【答题要点】
- KVO的本质是Runtime动态生成子类
- 动态子类重写setter方法，调用willChange/didChange
- 对象的isa指针指向动态子类
- 必须通过setter方法或KVC修改值才能触发KVO
- 直接修改实例变量不会触发KVO
- 需要手动移除观察者，防止内存泄漏
