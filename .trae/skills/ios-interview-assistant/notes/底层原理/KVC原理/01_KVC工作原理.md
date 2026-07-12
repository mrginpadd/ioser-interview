# KVC原理

## 【理论题】
**题目：** 请解释KVC（Key-Value Coding）的原理，以及它是如何通过字符串访问属性的？
**答案：**

**KVC原理：**

**KVC（Key-Value Coding）是通过字符串key来访问对象属性的机制，核心是按照固定顺序查找方法或实例变量。**

**取值流程 (valueForKey:):**
1. 查找get方法：`getKey`、`key`、`isKey`
2. 查找实例变量：`_key`、`_isKey`、`key`、`isKey`
3. 调用`accessInstanceVariablesDirectly`（默认返回YES）
4. 调用`valueForUndefinedKey:`（默认抛异常）

**赋值流程 (setValue:forKey:):**
1. 查找set方法：`setKey:`
2. 查找实例变量：`_key`、`_isKey`、`key`、`isKey`
3. 调用`accessInstanceVariablesDirectly`（默认返回YES）
4. 调用`setValue:forUndefinedKey:`（默认抛异常）

**KVC与KVO的关系：**

| 特性 | KVC | KVO |
|------|-----|-----|
| 作用 | 通过key访问属性 | 监听属性变化 |
| 实现 | 方法/变量查找 | 动态子类+重写setter |
| 触发 | 手动调用valueForKey/setValue | 属性变化自动触发 |
| 关系 | KVC赋值会触发KVO | KVO依赖KVC的setter |

**注意：** 通过KVC的`setValue:forKey:`修改属性，**会触发KVO**，因为KVC最终会调用setter方法或直接访问变量，但会触发KVO通知。

## 【场景题】
**题目：** KVC可以修改私有属性吗？为什么？有什么应用场景？

**答案：**

**可以修改私有属性。**

**原因：** KVC会查找实例变量`_key`，即使属性是私有的（.m文件中声明），KVC也能找到并修改。

```objective-c
// Person.h
@interface Person : NSObject
@end

// Person.m
@interface Person ()
@property (nonatomic, copy) NSString *privateName;  // 私有属性
@end

@implementation Person
@end

// 外部使用KVC修改私有属性
Person *p = [[Person alloc] init];
[p setValue:@"newName" forKey:@"privateName"];  // 可以修改私有属性！
NSString *name = [p valueForKey:@"privateName"];  // 可以读取私有属性！
```

**应用场景：**
1. **修改系统控件私有属性**：如修改UITextField的占位文字颜色
2. **字典转模型**：利用KVC快速设置模型属性
3. **数据绑定**：通过key路径访问嵌套属性

## 【代码示例】
```objective-c
// KVC基本使用
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
@property (nonatomic, strong) Person *friend;
@end

@implementation Person
@end

// 1. 基本使用
Person *p = [[Person alloc] init];
[p setValue:@"Tom" forKey:@"name"];
[p setValue:@25 forKey:@"age"];
NSLog(@"name: %@", [p valueForKey:@"name"]);
NSLog(@"age: %@", [p valueForKey:@"age"]);

// 2. 键路径（Key Path）
Person *friend = [[Person alloc] init];
friend.name = @"Jerry";
p.friend = friend;
NSLog(@"friend name: %@", [p valueForKeyPath:@"friend.name"]);
[p setValue:@"Jack" forKeyPath:@"friend.name"];

// 3. 字典转模型
NSDictionary *dict = @{@"name": @"Bob", @"age": @30};
Person *p2 = [[Person alloc] init];
[p2 setValuesForKeysWithDictionary:dict];

// 4. 防止undefined key崩溃
- (void)setValue:(id)value forUndefinedKey:(NSString *)key {
    NSLog(@"undefined key: %@", key);
    // 不调用super，避免崩溃
}
```

## 【答题要点】
- KVC通过字符串key访问属性
- 取值顺序：get方法 → 实例变量 → undefinedKey
- 赋值顺序：set方法 → 实例变量 → undefinedKey
- 可以访问和修改私有属性
- KVC赋值会触发KVO
- 常用API：valueForKey:、setValue:forKey:、valueForKeyPath:
- 键路径用点语法访问嵌套属性
