# YYModel高性能JSON转Model

## 【理论题】
**题目：** 请简述YYModel的作用和核心原理？
**答案：**

**YYModel的作用：**
> YYModel是高性能的JSON转Model库，用于网络数据到模型的转换。

**核心原理（高性能原因）：**

| 优化点 | 说明 |
|------|------|
| **缓存元数据** | 首次转换时缓存类的属性信息，后续直接使用 |
| **避免KVC** | 直接通过指针访问实例变量，不走KVC |
| **避免消息转发** | 直接调用setter方法，绕过runtime消息机制 |
| **无协议约束** | 不需要实现任何协议方法 |

## 【场景题】
**题目：** 如何处理JSON字段名与Model属性名不一致的情况？

**答案：**

```objective-c
// 使用modelCustomPropertyMapper自定义映射
@interface User : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
@end

@implementation User
+ (NSDictionary<NSString *, id> *)modelCustomPropertyMapper {
    return @{
        @"name": @"user_name",        // JSON字段user_name → Model属性name
        @"age": @"user_age"           // JSON字段user_age → Model属性age
    };
}
@end
```

## 【代码示例】
```objective-c
// 1. 基础使用
@interface User : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
@property (nonatomic, copy) NSString *avatar;
@end

// JSON转Model
NSDictionary *json = @{
    @"name": @"张三",
    @"age": @25,
    @"avatar": @"https://example.com/img.jpg"
};
User *user = [User yy_modelWithJSON:json];

// Model转JSON
NSDictionary *jsonDict = [user yy_modelToJSONObject];

// 2. 数组转换
NSArray *jsonArray = @[json1, json2, json3];
NSArray *users = [NSArray yy_modelArrayWithClass:[User class] json:jsonArray];

// 3. 字段映射
@implementation User
+ (NSDictionary<NSString *, id> *)modelCustomPropertyMapper {
    return @{
        @"name": @"user_name",
        @"age": @"user_age"
    };
}
@end

// 4. 嵌套模型
@interface Order : NSObject
@property (nonatomic, copy) NSString *orderId;
@property (nonatomic, strong) User *user;  // 嵌套模型
@end

@implementation Order
+ (NSDictionary<NSString *, id> *)modelContainerPropertyGenericClass {
    return @{@"items": [Item class]};  // 数组中的元素类型
}
@end

// 5. 白名单/黑名单
@implementation User
// 只转换这些字段
+ (NSArray<NSString *> *)modelPropertyBlacklist {
    return @[@"password"];
}
// 忽略这些字段
+ (NSArray<NSString *> *)modelPropertyWhitelist {
    return @[@"name", @"age"];
}
@end

// 6. 自定义转换
@implementation User
+ (id)modelTransformJSONValue:(id)value property:(NSString *)property {
    if ([property isEqualToString:@"age"]) {
        return [value stringValue];
    }
    return value;
}
@end
```

## 【答题要点】
- YYModel是高性能的JSON转Model库
- 核心原理：缓存元数据、避免KVC、避免消息转发
- 不需要实现任何协议方法
- 支持字段映射（modelCustomPropertyMapper）
- 支持嵌套模型转换
- 支持白名单/黑名单过滤
- 支持自定义转换逻辑
- 性能优于JSONModel和Mantle
