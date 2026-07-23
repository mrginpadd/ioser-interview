# isa指针

## 【理论题】
**题目：** 请解释isa指针的作用，以及在64位系统中isa指针的结构？
**答案：**

**isa的全称：**

> **isa = "is a"** 的缩写，表示"是什么"。

**isa指针的作用：**

```
对象的isa指针指向它所属的类，回答"我是什么类型？"这个问题。

Person *p = [[Person alloc] init];
p->isa → Person类对象（告诉系统p是Person类型）

[Person alloc];
Person->isa → Person元类（告诉系统Person类对象的类型）
```

**isa指向链：**

```
对象（Instance）→ isa → Class（类对象）→ isa → Meta-Class（元类）→ isa → 根元类 → isa → 自己
```

**64位系统中的isa结构：**

在64位系统中，isa不再是单纯的指针，而是一个**union（联合体）**，包含更多信息：

```c
union isa_t {
    Class cls;  // 类指针（普通指针模式）
    
    struct {
        uintptr_t nonpointer : 1;  // 是否开启非指针模式（0=纯指针，1=非指针）
        uintptr_t has_assoc : 1;   // 是否有关联对象
        uintptr_t has_cxx_dtor : 1; // 是否有C++析构函数
        uintptr_t shiftcls : 33;   // 类指针（非指针模式下，高33位）
        uintptr_t magic : 6;       // 调试用的魔数
        uintptr_t weakly_referenced : 1;  // 是否被weak引用
        uintptr_t deallocating : 1;       // 是否正在dealloc
        uintptr_t has_sidetable_rc : 1;   // 是否需要使用sidetable引用计数
        uintptr_t extra_rc : 19;          // 额外的引用计数
    };
};
```

**非指针模式（nonpointer=1）：**
- 节省内存：把类指针和其他信息打包在8字节中
- shiftcls：高33位存储类指针（掩码后得到）
- extra_rc：低19位存储引用计数

**纯指针模式（nonpointer=0）：**
- isa直接存储类指针
- 用于一些特殊场景（如Tagged Pointer对象）

## 【场景题】
**题目：** 为什么64位系统要把isa设计成union？

**答案：**

| 原因 | 说明 |
|------|------|
| **节省内存** | 把类指针和引用计数等信息打包在8字节中，不额外占用内存 |
| **提高性能** | 引用计数等信息可以直接从isa中读取，不需要访问其他数据结构 |
| **兼容性** | 保持8字节大小，兼容旧代码 |

## 【代码示例】
```objective-c
#import <objc/runtime.h>

// 1. 获取对象的isa
id obj = [[Person alloc] init];
Class cls = object_getClass(obj);  // 等价于obj->isa

// 2. 获取类对象的isa（元类）
Class metaCls = object_getClass(cls);

// 3. 验证isa链
Class rootMetaCls = object_getClass(metaCls);  // → 根元类
Class rootRootMetaCls = object_getClass(rootMetaCls);  // → 根元类（指向自己）

// 4. 判断对象类型
if ([obj isKindOfClass:[Person class]]) {
    NSLog(@"obj是Person类型");
}

// 5. 判断类对象类型
if (class_isMetaClass(metaCls)) {
    NSLog(@"metaCls是元类");
}

// 6. 获取isa中的引用计数信息（runtime内部使用）
// 通过object_getIvar获取，但实际中不需要直接访问

// 7. isa与消息查找
// [obj doSomething]的查找流程：
// 1. 通过obj->isa找到Class
// 2. 在Class的方法列表中查找doSomething
// 3. 如果没找到，通过Class->isa找到Meta-Class
// 4. 在Meta-Class中查找（类方法）

// 8. KVO中的isa-swizzling
// KVO会修改对象的isa，指向动态创建的子类
// NSKVONotifying_Person
```

## 【答题要点】
- isa = "is a"，表示"是什么类型"
- 对象的isa指向类对象，类对象的isa指向元类
- isa链：对象→类对象→元类→根元类→根元类（指向自己）
- 64位系统中isa是union结构
- 非指针模式（nonpointer=1）：把类指针和引用计数等信息打包
- 纯指针模式（nonpointer=0）：isa直接存储类指针
- shiftcls：非指针模式下的类指针（高33位）
- extra_rc：额外的引用计数（低19位）
- has_assoc：是否有关联对象
- has_cxx_dtor：是否有C++析构函数
- KVO通过修改isa实现监听
