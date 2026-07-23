# Category与Extension区别

## 【理论题】
**题目：** 请解释Category（分类）和Extension（扩展）的区别，各自的使用场景？
**答案：**

**Category（分类）和 Extension（扩展）的区别：**

| 特性 | Category（分类） | Extension（扩展） |
|------|-----------------|------------------|
| **语法** | `@interface Class (CatName)` | `@interface Class ()` |
| **位置** | 独立的.h/.m文件 | 写在.m文件顶部 |
| **添加方法** | ✅ 可以（公开方法） | ✅ 可以（私有方法） |
| **添加属性** | ❌ 不能加ivar | ✅ 可以加ivar（私有属性） |
| **添加实例变量** | ❌ 不能 | ✅ 可以 |
| **添加协议** | ✅ 可以 | ✅ 可以（私有协议） |
| **作用** | 扩展已有类功能 | 声明私有属性、私有方法、私有协议 |

**Extension能做的事：**
- 添加私有属性（ivar）
- 添加私有方法声明
- 遵循私有协议（不在.h中暴露）

**Category能做的事：**
- 添加公开方法
- 添加协议
- 拆分大类代码（模块化）

**一句话区别：**
> Category是"给类加方法"的，Extension是"给类加私有属性和方法"的。

## 【场景题】
**题目：** Category的实现原理是什么？

**答案：**

```
Category编译后：
┌─────────────────────────────────────────────────────┐
│  category_t 结构体                                   │
│  ├── name（类名）                                    │
│  ├── cls（关联的类）                                  │
│  ├── instance_methods（实例方法列表）                  │
│  ├── class_methods（类方法列表）                      │
│  └── protocols（协议列表）                           │
│                                                      │
│  在runtime加载时，把方法合并到类的方法列表前面         │
│  所以Category方法会"覆盖"原类同名方法                  │
└─────────────────────────────────────────────────────┘
```

**Category的特点：**
- 方法会合并到类的方法列表**前面**
- 消息查找时从前往后遍历，前面的先被找到
- 所以Category方法会"覆盖"原类同名方法（实际是优先调用）
- 多个Category有同名方法，编译顺序决定谁"覆盖"
- 不能添加ivar，因为类的内存布局在编译时已确定

```
方法列表（合并后）：
┌─────────────────────────────────────────┐
│ [0] Category方法A  ← 合并到前面，先被查到 │
│ [1] Category方法B                        │
│ [2] 原类方法A     ← 后被查到，被"覆盖"    │
│ [3] 原类方法B                            │
└─────────────────────────────────────────┘
查找methodA → 从[0]开始 → 先找到Category的 → 返回
```

## 【代码示例】
```objective-c
// 1. Category示例
// UIView+Custom.h
@interface UIView (Custom)
- (void)roundCornerWithRadius:(CGFloat)radius;
- (void)addBorderWithColor:(UIColor *)color width:(CGFloat)width;
@end

// UIView+Custom.m
@implementation UIView (Custom)
- (void)roundCornerWithRadius:(CGFloat)radius {
    self.layer.cornerRadius = radius;
    self.layer.masksToBounds = YES;
}
- (void)addBorderWithColor:(UIColor *)color width:(CGFloat)width {
    self.layer.borderColor = color.CGColor;
    self.layer.borderWidth = width;
}
@end

// 2. Extension示例（写在.m文件顶部）
// Person.m
#import "Person.h"

@interface Person ()
{
    NSString *_privateName;  // 私有实例变量
}
@property (nonatomic, strong) NSString *privateData;  // 私有属性
- (void)privateMethod;  // 私有方法声明
@end

@implementation Person
- (void)privateMethod {
    NSLog(@"这是私有方法");
}
@end

// 3. Category中用关联对象加属性
@interface NSObject (Tag)
@property (nonatomic, strong) NSString *tag;
@end

@implementation NSObject (Tag)
static const void *kTagKey = &kTagKey;
- (NSString *)tag {
    return objc_getAssociatedObject(self, kTagKey);
}
- (void)setTag:(NSString *)tag {
    objc_setAssociatedObject(self, kTagKey, tag, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
}
@end

// 4. 多个Category方法调用顺序
// 如果CatA和CatB都有methodA
// 编译顺序决定优先级（最后编译的优先）
// 配置方式：Build Phases → Compile Sources 顺序
```

## 【答题要点】
- Category用于扩展已有类的方法，不能加ivar
- Extension用于声明私有属性和方法，写在.m文件顶部
- Category编译后是category_t结构体，运行时合并到类的方法列表
- Category方法会"覆盖"原类同名方法（优先调用）
- 多个Category同名方法，编译顺序决定优先级
- Category不能加ivar的原因：类内存布局编译时已确定
- Category加属性需要用关联对象实现
- Extension可以加ivar，因为它在编译时就合并到类中
