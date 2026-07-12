# weak原理

## 【理论题】
**题目：** 请解释weak关键字的工作原理，以及为什么weak指针在对象释放后会自动置nil？
**答案：**

**weak关键字的工作原理：**

**weak是弱引用，不会增加引用计数！**

```objective-c
// weak属性的setter方法伪代码
- (void)setObject:(NSObject *)object {
    // weak不会retain！
    // 而是将指针注册到一个全局的"弱引用表"（side table）
    objc_storeWeak(&_object, object);
}
```

**弱引用表（Side Table）机制：**

每一个对象都有一个weak指针数组，记录所有指向它的weak指针：

1. 当对象引用计数变为0时
2. 遍历该对象的weak指针数组
3. 将所有weak指针设置为nil
4. 从weak指针数组中移除这些指针
5. 释放对象内存

**weak vs strong对比：**

| 特性 | weak | strong |
|------|------|--------|
| 引用计数 | 不增加 | +1 |
| 对象释放后 | 自动置nil | 变成野指针 |
| 使用场景 | 避免循环引用 | 持有对象 |

**为什么weak会自动置nil？**

这是通过**runtime的side table机制**实现的：
1. 每个对象都有一个对应的side table，存储weak指针列表
2. 对象dealloc时，runtime会遍历side table中的weak指针
3. 将所有weak指针置为nil，防止野指针访问

## 【场景题】
**题目：** 在ARC环境下，以下代码会输出什么？为什么？

```objective-c
@property (weak, nonatomic) NSObject *weakObj;
@property (strong, nonatomic) NSObject *strongObj;

- (void)test {
    NSObject *temp = [[NSObject alloc] init];
    self.weakObj = temp;
    self.strongObj = temp;
    
    NSLog(@"weakObj: %@", self.weakObj);  // ?
    NSLog(@"strongObj: %@", self.strongObj);  // ?
    
    self.strongObj = nil;
    
    NSLog(@"weakObj after strongObj = nil: %@", self.weakObj);  // ?
}
```

**答案：**

```
weakObj: <NSObject: 0x100600000>
strongObj: <NSObject: 0x100600000>
weakObj after strongObj = nil: (null)
```

**分析：**
1. `temp`创建后引用计数为1
2. `self.weakObj = temp`：weak不增加引用计数，引用计数仍为1
3. `self.strongObj = temp`：strong增加引用计数，引用计数变为2
4. 此时weak和strong都指向同一个对象
5. `self.strongObj = nil`：strong释放对象，引用计数减为1
6. `temp`超出作用域，ARC自动release，引用计数减为0
7. 对象dealloc，side table将所有weak指针置为nil

## 【代码示例】
```objective-c
// weak的正确使用场景：避免循环引用
@interface ViewController ()
@property (weak, nonatomic) UIButton *button;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    UIButton *btn = [[UIButton alloc] init];
    btn.backgroundColor = [UIColor redColor];
    
    // 使用weak避免循环引用（block场景）
    __weak typeof(self) weakSelf = self;
    btn.block = ^{
        // 在block内部使用weakSelf避免循环引用
        NSLog(@"button clicked: %@", weakSelf.button.titleLabel.text);
    };
    
    self.button = btn;  // weak引用，不增加引用计数
}

@end
```

## 【答题要点】
- weak是弱引用，不会增加引用计数
- weak通过side table机制实现自动置nil
- 对象dealloc时，runtime遍历side table将所有weak指针置为nil
- weak用于避免循环引用，strong用于持有对象
- weak指针在对象释放后自动置nil，不会变成野指针
