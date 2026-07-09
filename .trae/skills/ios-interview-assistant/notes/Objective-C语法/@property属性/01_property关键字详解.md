# @property属性

## 【理论题】
**题目：** 请解释Objective-C中@property的作用，以及它的完整写法包含哪些关键字？
**答案：**

`@property` 是Objective-C的属性声明语法，编译器会自动生成：
1. **实例变量（ivar）**：默认以下划线开头
2. **getter方法**：获取属性值
3. **setter方法**：设置属性值

**关键字分类：**

| 分类 | 关键字 | 作用 |
|------|--------|------|
| **原子性** | `atomic` | 原子属性，保证读写完整性，线程安全（但不是绝对安全） |
| | `nonatomic` | 非原子属性，性能更高，需手动保证线程安全 |
| **内存管理** | `strong` | 强引用，增加引用计数，ARC默认 |
| | `weak` | 弱引用，不增加引用计数，对象释放后自动置nil |
| | `assign` | 简单赋值，不改变引用计数，用于基本数据类型 |
| **拷贝语义** | `copy` | 拷贝属性，创建副本，用于NSString、NSArray等可变对象 |

## 【场景题】
**题目：** 在实际开发中，NSString属性应该用`strong`还是`copy`？为什么？
**答案：**

应该使用`copy`。

**原因：**
```objective-c
// 假设有如下代码：
NSMutableString *mutableStr = [NSMutableString stringWithString:@"hello"];
self.name = mutableStr;  // 如果用strong，name指向同一个对象
[mutableStr appendString:@" world"];  // 修改mutableStr会影响self.name
// self.name 现在变成了 @"hello world"，这不是我们想要的！

// 使用copy的话：
self.name = mutableStr;  // copy会创建一个不可变副本
[mutableStr appendString:@" world"];  // 修改原对象不影响副本
// self.name 仍然是 @"hello"，符合预期
```

**总结：**
- 对于`NSString`、`NSArray`、`NSDictionary`等不可变类型的属性，应该使用`copy`
- 防止外部可变对象修改导致属性值意外变化

## 【代码示例】
```objective-c
@interface Person : NSObject
@property (nonatomic, strong) NSString *name;      // 错误！应该用copy
@property (nonatomic, copy) NSString *address;     // 正确
@property (nonatomic, weak) UIView *containerView; // 避免循环引用
@property (nonatomic, assign) NSInteger age;       // 基本数据类型用assign
@end
```

## 【答题要点】
- @property自动生成ivar + getter + setter
- atomic保证原子性但不保证线程安全
- copy用于可变对象类型防止外部修改
- weak用于避免循环引用
- assign用于基本数据类型（int、float、NSInteger等）
