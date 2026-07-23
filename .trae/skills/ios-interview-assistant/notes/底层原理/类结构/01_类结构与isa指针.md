# 类结构

## 【理论题】
**题目：** 请解释Objective-C中Class、Meta-Class、objc_class的关系？
**答案：**

**Objective-C类结构：**

```
┌─────────────────────────────────────────────────────┐
│                    对象（Instance）                   │
│  ┌─────────────────────────────────────────────┐   │
│  │  isa指针 ──────→ Class（类对象）             │   │
│  │  实例变量（ivar）                              │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    Class（类对象）                   │
│  ┌─────────────────────────────────────────────┐   │
│  │  isa指针 ──────→ Meta-Class（元类）           │   │
│  │  superclass指针 ─→ 父类                       │   │
│  │  方法列表（实例方法）                           │   │
│  │  属性列表、协议列表                            │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                Meta-Class（元类）                   │
│  ┌─────────────────────────────────────────────┐   │
│  │  isa指针 ──────→ NSObject的元类（根元类）     │   │
│  │  superclass指针 ─→ 父类的元类                  │   │
│  │  方法列表（类方法）                             │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**objc_class结构体：**

```objective-c
struct objc_class {
    Class _Nonnull isa  OBJC_ISA_AVAILABILITY;
    
#if !__OBJC2__
    Class _Nullable super_class                              OBJC2_UNAVAILABLE;
    const char * _Nonnull name                               OBJC2_UNAVAILABLE;
    long version                                             OBJC2_UNAVAILABLE;
    long info                                                OBJC2_UNAVAILABLE;
    long instance_size                                       OBJC2_UNAVAILABLE;
    struct objc_ivar_list * _Nullable ivars                  OBJC2_UNAVAILABLE;
    struct objc_method_list * _Nullable * _Nullable methodLists   OBJC2_UNAVAILABLE;
    struct objc_cache * _Nonnull cache                       OBJC2_UNAVAILABLE;
    struct objc_protocol_list * _Nullable protocols          OBJC2_UNAVAILABLE;
#endif
} OBJC2_UNAVAILABLE;
```

**关键点：**

| 概念 | 作用 | 包含内容 |
|------|------|---------|
| **Instance** | 对象实例 | isa指针 + 实例变量 |
| **Class** | 类对象 | 实例方法列表 + 属性 + 协议 |
| **Meta-Class** | 元类 | 类方法列表 |
| **isa** | 指向所属类/元类 | 对象→Class，Class→Meta-Class，Meta-Class→根元类 |

## 【场景题】
**题目：** 为什么类方法可以通过[NSObject alloc]调用？

**答案：**

```
[NSObject alloc]调用流程：
1. NSObject（Class）的isa指向Meta-Class
2. 查找alloc方法时，先在NSObject的方法列表（实例方法）找，没找到
3. 通过isa找到Meta-Class，在Meta-Class的方法列表（类方法）中找到alloc
4. 执行alloc方法
```

## 【代码示例】
```objective-c
// 1. 获取类对象
Class cls = [NSObject class];
Class cls2 = NSObject.class;
Class cls3 = object_getClass([NSObject alloc]);

// 2. 获取元类
Class metaCls = object_getClass(cls);

// 3. 验证isa指向
id obj = [[NSObject alloc] init];
Class objClass = object_getClass(obj);  // → NSObject
Class clsMetaClass = object_getClass(cls);  // → NSObject的元类

// 4. 判断是否为元类
BOOL isMetaClass = class_isMetaClass(metaCls);  // → YES
BOOL isClass = class_isMetaClass(cls);  // → NO

// 5. 获取方法列表（runtime API）
unsigned int methodCount = 0;
Method *methods = class_copyMethodList(cls, &methodCount);
for (int i = 0; i < methodCount; i++) {
    SEL sel = method_getName(methods[i]);
    NSLog(@"实例方法：%@", NSStringFromSelector(sel));
}
free(methods);

// 6. 获取类方法列表（从元类获取）
Method *classMethods = class_copyMethodList(metaCls, &methodCount);
for (int i = 0; i < methodCount; i++) {
    SEL sel = method_getName(classMethods[i]);
    NSLog(@"类方法：%@", NSStringFromSelector(sel));
}
free(classMethods);
```

## 【答题要点】
- 对象（Instance）通过isa指针指向Class（类对象）
- Class（类对象）通过isa指针指向Meta-Class（元类）
- Meta-Class（元类）通过isa指针指向NSObject的元类（根元类）
- Class包含实例方法列表，Meta-Class包含类方法列表
- objc_class是Class的底层结构体定义
- 类方法调用时，通过Class的isa找到Meta-Class中的方法
- superclass指针实现继承链
- runtime提供API操作类结构：object_getClass、class_copyMethodList等
