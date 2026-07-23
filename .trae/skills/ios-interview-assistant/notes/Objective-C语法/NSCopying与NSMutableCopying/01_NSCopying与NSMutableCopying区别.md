# NSCopying与NSMutableCopying

## 【理论题】
**题目：** 请解释NSCopying和NSMutableCopying协议的作用，以及copy与mutableCopy的区别？
**答案：**

**两个协议的作用：**

| 协议 | 方法 | 返回类型 |
|------|------|---------|
| **NSCopying** | -copy | 返回不可变副本 |
| **NSMutableCopying** | -mutableCopy | 返回可变副本 |

**copy与mutableCopy的区别：**

```
原对象类型    copy结果        mutableCopy结果
─────────    ───────        ──────────────
NSString      NSString（副本）  NSMutableString
NSMutableString NSString（副本）  NSMutableString
NSArray       NSArray（副本）   NSMutableArray
NSMutableArray NSArray（副本）   NSMutableArray
```

**核心规则：**
- copy：**返回不可变类型**的副本
- mutableCopy：**返回可变类型**的副本
- 不管原对象是可变还是不可变，返回类型由调用的方法决定

## 【场景题】
**题目：** 自定义类如何实现深拷贝？

**答案：**

```objective-c
@interface Person : NSObject <NSCopying>
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
@end

@implementation Person
- (id)copyWithZone:(NSZone *)zone {
    Person *copy = [[[self class] allocWithZone:zone] init];
    copy.name = [self.name copy];      // 深拷贝字符串
    copy.age = self.age;
    return copy;
}
@end
```

## 【代码示例】
```objective-c
// 1. NSString的copy和mutableCopy
NSString *str = @"hello";
NSString *copyStr = [str copy];           // NSString
NSMutableString *mutableStr = [str mutableCopy];  // NSMutableString

// 2. NSMutableString的copy和mutableCopy
NSMutableString *mStr = [NSMutableString stringWithString:@"world"];
NSString *copyMStr = [mStr copy];        // NSString（不可变）
NSMutableString *mutableMStr = [mStr mutableCopy];  // NSMutableString

// 3. NSArray的copy和mutableCopy
NSArray *arr = @[@1, @2];
NSArray *copyArr = [arr copy];           // NSArray
NSMutableArray *mutableArr = [arr mutableCopy];  // NSMutableArray

// 4. NSMutableArray的copy和mutableCopy
NSMutableArray *mArr = [NSMutableArray arrayWithObjects:@1, @2, nil];
NSArray *copyMArr = [mArr copy];         // NSArray（不可变）
NSMutableArray *mutableMArr = [mArr mutableCopy];  // NSMutableArray

// 5. 自定义类实现NSCopying
@interface Student : NSObject <NSCopying>
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger score;
@property (nonatomic, strong) NSArray *courses;
@end

@implementation Student
- (id)copyWithZone:(NSZone *)zone {
    Student *copy = [[Student allocWithZone:zone] init];
    copy.name = [self.name copy];
    copy.score = self.score;
    copy.courses = [[NSArray alloc] initWithArray:self.courses copyItems:YES];
    return copy;
}
@end

// 使用
Student *stu1 = [[Student alloc] init];
stu1.name = @"张三";
stu1.score = 90;

Student *stu2 = [stu1 copy];
stu2.name = @"李四";  // 修改副本不影响原对象
NSLog(@"%@", stu1.name);  // 张三
NSLog(@"%@", stu2.name);  // 李四

// 6. @property的copy修饰
@interface MyClass : NSObject
@property (nonatomic, copy) NSString *name;  // copy修饰，自动调用copy
@end

// 7. 深拷贝vs浅拷贝
// 浅拷贝：只拷贝指针，共享数据
// 深拷贝：拷贝数据，各自独立

// NSArray的深拷贝（每个元素都拷贝）
NSArray *deepCopy = [[NSArray alloc] initWithArray:originalArray copyItems:YES];
```

## 【答题要点】
- NSCopying协议实现-copy方法，返回不可变副本
- NSMutableCopying协议实现-mutableCopy方法，返回可变副本
- copy：返回不可变类型，mutableCopy：返回可变类型
- 不管原对象是可变还是不可变，返回类型由调用的方法决定
- NSString调用copy：如果是字面量，可能是同一个对象（优化）
- 自定义类实现NSCopying需要实现-copyWithZone:方法
- @property的copy修饰会自动调用copy方法
- 深拷贝需要递归拷贝所有成员变量
- 浅拷贝只拷贝指针，共享数据
