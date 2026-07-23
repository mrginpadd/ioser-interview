# SEL与IMP区别

## 【理论题】
**题目：** 请解释SEL和IMP的区别，以及它们在Runtime中的作用？
**答案：**

**SEL和IMP的关系：**

```
[obj doSomething]
        │
        ▼
   @selector(doSomething)
        │
        │  SEL = 方法名（字符串哈希）
        ▼
   方法列表查找
   ┌──────────────────────────┐
   │ SEL ──→ IMP              │
   │ doSomething ──→ 函数指针   │
   └──────────────────────────┘
        │
        ▼
   执行函数指针指向的代码
```

| 概念 | 全称 | 本质 | 作用 |
|------|------|------|------|
| **SEL** | Selector | 方法名的哈希值 | 方法标识 |
| **IMP** | Implementation | 函数指针 | 方法实现 |

**底层结构（method_t）：**

```c
struct method_t {
    SEL name;           // 方法名
    const char *types; // 类型编码
    IMP imp;            // 函数指针
};
```

## 【场景题】
**题目：** SEL和IMP在实际开发中的应用？

**答案：**

| 应用 | API | 说明 |
|------|-----|------|
| **Method Swizzling** | method_exchangeImplementations | 交换两个IMP |
| **动态添加方法** | class_addMethod | 添加SEL→IMP映射 |
| **获取方法实现** | method_getImplementation | 获取IMP |
| **替换方法实现** | method_setImplementation | 替换IMP |
| **直接调用IMP** | imp_implementationWithBlock | 获取Block的IMP |

## 【代码示例】
```objective-c
#import <objc/runtime.h>

// 1. 获取SEL
SEL sel = @selector(viewDidLoad);
SEL sel2 = NSSelectorFromString(@"viewDidLoad");

// 2. SEL转字符串
NSString *selStr = NSStringFromSelector(sel);

// 3. 获取Method（SEL + types + IMP）
Method method = class_getInstanceMethod([UIViewController class], sel);

// 4. 从Method获取IMP
IMP imp = method_getImplementation(method);

// 5. 获取SEL对应的IMP
IMP imp2 = class_getMethodImplementation([UIViewController class], sel);

// 6. 直接调用IMP（少走消息查找，性能更高）
// imp的函数签名: id (id self, SEL _cmd, ...)
id result = ((id(*)(id, SEL))imp)(self, sel);

// 7. 动态添加方法
void dynamicMethodIMP(id self, SEL _cmd) {
    NSLog(@"动态方法被调用");
}
class_addMethod([self class], @selector(dynamicMethod), (IMP)dynamicMethodIMP, "v@:");

// 8. 替换方法实现
Method original = class_getInstanceMethod([self class], @selector(originalMethod));
Method newMethod = class_getInstanceMethod([self class], @selector(newMethod));
method_setImplementation(original, method_getImplementation(newMethod));

// 9. SEL比较
if (sel == @selector(viewDidLoad)) {
    NSLog(@"是viewDidLoad方法");
}

// 10. 检查是否能响应SEL
if ([self respondsToSelector:sel]) {
    [self performSelector:sel];
}
```

## 【答题要点】
- SEL是方法选择子，本质是方法名的哈希值
- IMP是方法实现，本质是函数指针
- SEL → IMP 是映射关系（通过方法列表查找）
- method_t结构体包含：SEL name + types + IMP imp
- Method Swizzling本质是交换两个SEL对应的IMP
- 直接调用IMP可以绕过消息查找，性能更高
- 动态添加方法：class_addMethod添加SEL→IMP映射
- SEL是全局唯一的（相同方法名在不同类中是同一个SEL）
