# runtime API

## 【理论题】
**题目：** 请列举常用的runtime API，并说明它们的用途？
**答案：**

**常用runtime API分类：**

### 1. 类相关API

| API | 用途 |
|-----|------|
| `class_addMethod` | 为类添加方法 |
| `class_replaceMethod` | 替换类的方法实现 |
| `class_copyMethodList` | 获取类的所有方法列表 |
| `class_getInstanceMethod` | 获取实例方法 |
| `class_getClassMethod` | 获取类方法 |
| `class_addProperty` | 为类添加属性 |
| `class_copyPropertyList` | 获取类的所有属性列表 |
| `class_getProperty` | 获取指定属性 |
| `class_addProtocol` | 为类添加协议 |
| `class_conformsToProtocol` | 检查类是否遵循协议 |
| `class_getSuperclass` | 获取父类 |
| `class_getInstanceSize` | 获取实例大小 |

### 2. 对象相关API

| API | 用途 |
|-----|------|
| `object_getClass` | 获取对象的类 |
| `object_getIvar` | 获取对象的实例变量 |
| `object_setIvar` | 设置对象的实例变量 |
| `object_copy` | 复制对象 |
| `object_dispose` | 释放对象 |

### 3. 方法相关API

| API | 用途 |
|-----|------|
| `method_getName` | 获取方法名（SEL） |
| `method_getImplementation` | 获取方法实现（IMP） |
| `method_setImplementation` | 设置方法实现 |
| `method_getTypeEncoding` | 获取方法类型编码 |
| `method_exchangeImplementations` | 交换两个方法的实现 |

### 4. 属性相关API

| API | 用途 |
|-----|------|
| `property_getName` | 获取属性名 |
| `property_getAttributes` | 获取属性描述字符串 |
| `property_copyAttributeList` | 获取属性的所有属性列表 |

### 5. 关联对象API

| API | 用途 |
|-----|------|
| `objc_setAssociatedObject` | 设置关联对象 |
| `objc_getAssociatedObject` | 获取关联对象 |
| `objc_removeAssociatedObjects` | 移除所有关联对象 |

### 6. SEL相关API

| API | 用途 |
|-----|------|
| `sel_registerName` | 注册一个SEL |
| `sel_getName` | 获取SEL的字符串 |
| `sel_isEqual` | 比较两个SEL是否相等 |

## 【场景题】
**题目：** 如何用runtime实现一个通用的字典转模型？

**答案：**

```objective-c
#import <objc/runtime.h>

+ (instancetype)modelWithDict:(NSDictionary *)dict {
    id obj = [[self alloc] init];
    
    unsigned int count = 0;
    objc_property_t *properties = class_copyPropertyList([self class], &count);
    
    for (int i = 0; i < count; i++) {
        objc_property_t property = properties[i];
        const char *propertyName = property_getName(property);
        NSString *name = [NSString stringWithUTF8String:propertyName];
        
        id value = dict[name];
        if (value) {
            [obj setValue:value forKey:name];
        }
    }
    
    free(properties);
    return obj;
}
```

## 【代码示例】
```objective-c
#import <objc/runtime.h>

// 1. 获取类的所有方法
unsigned int methodCount = 0;
Method *methods = class_copyMethodList([Person class], &methodCount);
for (int i = 0; i < methodCount; i++) {
    SEL sel = method_getName(methods[i]);
    NSString *methodName = NSStringFromSelector(sel);
    NSLog(@"方法：%@", methodName);
}
free(methods);

// 2. 获取类的所有属性
unsigned int propertyCount = 0;
objc_property_t *properties = class_copyPropertyList([Person class], &propertyCount);
for (int i = 0; i < propertyCount; i++) {
    const char *name = property_getName(properties[i]);
    const char *attrs = property_getAttributes(properties[i]);
    NSLog(@"属性：%s，描述：%s", name, attrs);
}
free(properties);

// 3. 添加方法
void dynamicMethod(id self, SEL _cmd) {
    NSLog(@"动态方法");
}
class_addMethod([Person class], 
               @selector(dynamicMethod), 
               (IMP)dynamicMethod, 
               "v@:");

// 4. 交换方法实现
Method original = class_getInstanceMethod([Person class], @selector(originalMethod));
Method swizzled = class_getInstanceMethod([Person class], @selector(swizzledMethod));
method_exchangeImplementations(original, swizzled);

// 5. 关联对象
static const void *kAssociatedKey = &kAssociatedKey;
objc_setAssociatedObject(self, kAssociatedKey, value, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
id associatedValue = objc_getAssociatedObject(self, kAssociatedKey);

// 6. 获取对象的ivar
Ivar ivar = class_getInstanceVariable([Person class], "_name");
id value = object_getIvar(person, ivar);

// 7. 获取实例大小
size_t size = class_getInstanceSize([Person class]);

// 8. 检查协议
BOOL conforms = class_conformsToProtocol([Person class], @protocol(NSCopying));

// 9. 获取方法实现
IMP imp = class_getMethodImplementation([Person class], @selector(doSomething));
((void(*)(id, SEL))imp)(self, @selector(doSomething));
```

## 【答题要点】
- runtime API用于在运行时操作类、对象、方法、属性
- 类相关API：class_addMethod、class_copyMethodList、class_copyPropertyList
- 对象相关API：object_getClass、object_getIvar
- 方法相关API：method_exchangeImplementations、method_getImplementation
- 关联对象API：objc_setAssociatedObject、objc_getAssociatedObject
- SEL相关API：sel_registerName、sel_getName
- 使用完需要free释放内存（class_copyMethodList等返回的数组）
- 常用场景：字典转模型、方法交换、动态添加属性
