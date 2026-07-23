# KVO与KVC

## 【理论题】
**题目：** 请解释KVO（键值观察）和KVC（键值编码）的作用，以及它们的区别？
**答案：**

**KVO和KVC的作用：**

| 概念 | 全称 | 作用 |
|------|------|------|
| **KVO** | Key-Value Observing | 监听对象属性值的变化 |
| **KVC** | Key-Value Coding | 通过key访问对象属性（包括私有属性） |

**一句话区别：**
> KVO是"监听变化"，KVC是"通过key读写属性"。

## 【常见误解纠正】

**错误理解：**
> "KVO修改的是SET方法，KVC修改的是GET方法"

**正确理解：**
- **KVO原理**：通过**isa-swizzling**动态创建子类，不是修改原类的SET方法
- **KVC原理**：一套查找链，不是修改GET方法

## 【KVO原理 - isa-swizzling】

```
正常情况：
Person对象 → isa → Person类

KVO监听后：
Person对象 → isa → NSKVONotifying_Person（动态创建的子类）
                           │
                           ├─ setName:（重写，通知观察者）
                           ├─ class（伪装成原类）
                           └─ dealloc（清理）

当调用person.name = @"新值"时：
1. 调用子类的setName:
2. 子类setName:内部调用原类的setName:
3. 发送通知给所有观察者
```

## 【KVC查找链】

**setValue:forKey: 查找顺序：**

```
setValue:forKey:@"name"
        │
        ▼
1. 查找 setName:
        │
        ▼ (没找到)
2. 查找 _setName:
        │
        ▼ (没找到)
3. 检查 accessInstanceVariablesDirectly（默认YES）
        │
        ▼
4. 查找 _name（带下划线的ivar）
        │
        ▼ (没找到)
5. 查找 name（不带下划线的ivar）
        │
        ▼ (没找到)
6. 查找 _isName
        │
        ▼ (没找到)
7. 查找 isName
        │
        ▼ (没找到)
8. 抛出 NSUnknownKeyException
```

**valueForKey: 查找顺序：**

```
valueForKey:@"name"
        │
        ▼
1. 查找 getName
        │
        ▼ (没找到)
2. 查找 name
        │
        ▼ (没找到)
3. 查找 isName
        │
        ▼ (没找到)
4. 查找 _getName
        │
        ▼ (没找到)
5. 查找 _name（带下划线的ivar）
        │
        ▼ (没找到)
6. 查找 _isName
        │
        ▼ (没找到)
7. 抛出 NSUnknownKeyException
```

## 【场景题】
**题目：** KVO和代理模式的区别？

**答案：**

| 特性 | KVO | 代理模式 |
|------|-----|---------|
| **通信方向** | 一对多 | 一对一 |
| **关注点** | 属性变化 | 事件回调 |
| **实现方式** | isa-swizzling | 协议+委托 |
| **性能** | 较低（运行时动态） | 较高（直接调用） |
| **灵活性** | 高（动态添加观察者） | 低（编译时确定） |

## 【代码示例】
```objective-c
// 1. KVO基本使用
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
@end

@implementation Person
@end

// 观察者
@interface Observer : NSObject
@property (nonatomic, strong) Person *person;
@end

@implementation Observer
- (instancetype)init {
    self = [super init];
    if (self) {
        _person = [[Person alloc] init];
        // 添加观察者
        [_person addObserver:self 
                  forKeyPath:@"name" 
                     options:NSKeyValueObservingOptionNew | NSKeyValueObservingOptionOld
                     context:@"nameChange"];
        [_person addObserver:self 
                  forKeyPath:@"age" 
                     options:NSKeyValueObservingOptionNew
                     context:@"ageChange"];
    }
    return self;
}

// 监听回调
- (void)observeValueForKeyPath:(NSString *)keyPath 
                      ofObject:(id)object 
                        change:(NSDictionary<NSKeyValueChangeKey,id> *)change 
                       context:(void *)context {
    if ([(NSString *)context isEqualToString:@"nameChange"]) {
        NSLog(@"name变化: %@ → %@", 
              change[NSKeyValueChangeOldKey], 
              change[NSKeyValueChangeNewKey]);
    } else if ([(NSString *)context isEqualToString:@"ageChange"]) {
        NSLog(@"age变化: %@", change[NSKeyValueChangeNewKey]);
    }
}

- (void)dealloc {
    // 移除观察者（重要！否则会崩溃）
    [_person removeObserver:self forKeyPath:@"name"];
    [_person removeObserver:self forKeyPath:@"age"];
}
@end

// 使用
Person *p = [[Person alloc] init];
p.name = @"张三";  // 触发KVO
p.age = 25;       // 触发KVO

// 2. KVC基本使用
// 通过key访问属性
[p setValue:@"李四" forKey:@"name"];  // 等价于 p.name = @"李四"
NSString *name = [p valueForKey:@"name"];  // 等价于 p.name

// 通过key访问私有属性
@interface PrivateClass : NSObject {
    NSString *_secret;
}
@end
PrivateClass *pc = [[PrivateClass alloc] init];
[pc setValue:@"秘密" forKey:@"secret"];  // KVC可以访问私有ivar
NSString *secret = [pc valueForKey:@"secret"];

// 3. KVC路径访问
@interface Department : NSObject
@property (nonatomic, copy) NSString *deptName;
@end

@interface Employee : NSObject
@property (nonatomic, strong) Department *dept;
@end

Employee *emp = [[Employee alloc] init];
emp.dept = [[Department alloc] init];
emp.dept.deptName = @"研发部";

// 通过路径访问
NSString *deptName = [emp valueForKeyPath:@"dept.deptName"];
[emp setValue:@"市场部" forKeyPath:@"dept.deptName"];

// 4. KVC集合操作
NSArray *employees = @[emp1, emp2, emp3];
NSNumber *maxSalary = [employees valueForKeyPath:@"@max.salary"];
NSNumber *avgSalary = [employees valueForKeyPath:@"@avg.salary"];
NSArray *names = [employees valueForKeyPath:@"name"];

// 5. KVO手动触发
// 默认KVO自动触发（通过setter或KVC）
// 如果需要手动控制，重写以下方法
+ (BOOL)automaticallyNotifiesObserversForKey:(NSString *)key {
    if ([key isEqualToString:@"customProperty"]) {
        return NO;  // 关闭自动通知
    }
    return [super automaticallyNotifiesObserversForKey:key];
}

- (void)updateCustomProperty {
    [self willChangeValueForKey:@"customProperty"];
    // 修改属性
    [self didChangeValueForKey:@"customProperty"];
}
```

## 【答题要点】
- KVO是键值观察，监听属性变化；KVC是键值编码，通过key访问属性
- KVO原理：isa-swizzling动态创建子类（NSKVONotifying_XXX）
- KVC查找链：setValue→setKey→_setKey→_key→key→_isKey→isKey
- KVO需要手动removeObserver，否则会崩溃
- KVC可以访问私有属性（绕过访问控制）
- KVO是一对多通信，代理是一对一
- KVC支持路径访问：valueForKeyPath:@"dept.name"
- KVC支持集合操作：@max、@avg、@sum等
- 手动KVO：willChangeValueForKey: + didChangeValueForKey:
- 常见误解：KVO不是修改SET方法，而是isa-swizzling
