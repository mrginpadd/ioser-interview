# ARC与MRC

## 【理论题】
**题目：** 请解释ARC和MRC的区别，以及ARC的工作原理是什么？
**答案：**

**ARC（Automatic Reference Counting）：**
- **自动管理引用计数**，编译器在编译时自动插入`retain`、`release`、`autorelease`代码
- **编译时特性**，不是运行时垃圾回收
- **开发者无需手动管理**内存，但仍需注意循环引用

**MRC（Manual Reference Counting）：**
- **手动管理引用计数**，需要开发者手动调用`retain`、`release`、`autorelease`
- **繁琐且容易出错**，容易导致内存泄漏或野指针

**核心区别：**

| 特性 | ARC | MRC |
|------|-----|-----|
| 引用计数管理 | 自动 | 手动 |
| retain/release | 编译器自动插入 | 开发者手动调用 |
| autorelease | 编译器自动管理 | 开发者手动管理 |
| 循环引用 | 仍需手动处理 | 仍需手动处理 |
| 性能 | 与MRC相当（编译器优化） | 取决于开发者水平 |

**ARC的工作原理：**
1. **强引用**：对象赋值给`strong`指针时，自动`retain`
2. **指针作用域结束**：自动`release`
3. **弱引用**：对象赋值给`weak`指针时，不`retain`，对象释放后自动置`nil`

**ARC不管理的对象：**
- **C语言指针**：`malloc/free`分配的内存
- **Core Foundation对象**：需要使用`CFRetain/CFRelease`

## 【场景题】
**题目：** 在ARC环境下，以下代码是否会导致内存泄漏？为什么？

```objective-c
@property (strong, nonatomic) NSObject *obj;

- (void)test {
    self.obj = [[NSObject alloc] init];
    self.obj = nil;
}
```

**答案：**

不会导致内存泄漏。

**分析：**
```objective-c
self.obj = [[NSObject alloc] init];
// ARC自动插入：[newObject retain]
// 此时引用计数：1

self.obj = nil;
// ARC自动插入：[oldObject release]
// 引用计数减为0，对象被释放
```

**关键要点：**
- ARC会在赋值时自动`release`旧对象
- `self.obj = nil`会触发setter方法，ARC会自动释放之前的对象
- 只有循环引用才会导致ARC无法释放对象

## 【代码示例】
```objective-c
// ARC环境下的代码
@interface Person : NSObject
@property (strong, nonatomic) NSString *name;
@property (weak, nonatomic) Person *friend;  // 避免循环引用
@end

@implementation Person
- (instancetype)init {
    self = [super init];
    if (self) {
        _name = @"Unknown";
    }
    return self;
}
// ARC会自动生成dealloc方法，无需手动释放
@end

// MRC环境下的代码（需手动管理）
@implementation Person
- (instancetype)init {
    self = [super init];
    if (self) {
        _name = [[NSString alloc] initWithString:@"Unknown"];
    }
    return self;
}

- (void)dealloc {
    [_name release];  // 手动释放
    [super dealloc];
}
@end
```

## 【答题要点】
- ARC是编译时特性，不是运行时垃圾回收
- ARC自动插入retain/release/autorelease代码
- ARC仍需注意循环引用问题
- ARC不管理C语言指针和Core Foundation对象
- MRC需要开发者手动调用retain/release/autorelease
- ARC与MRC的性能相当，因为编译器优化
