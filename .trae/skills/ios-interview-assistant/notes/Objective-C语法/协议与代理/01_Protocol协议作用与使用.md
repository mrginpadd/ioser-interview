# Protocol协议与代理

## 【理论题】
**题目：** 请解释Protocol（协议）的作用，以及和Category的区别？
**答案：**

**Protocol的作用：**
> 协议用来定义一组属性或方法的声明，遵循该协议的对象需要实现协议中的属性和方法。主要用于接口约束和代理模式。

**Protocol的两个核心作用：**

| 作用 | 说明 |
|------|------|
| **接口约束** | 规定遵循协议的类必须实现某些方法 |
| **代理模式** | 定义代理回调接口 |

**方法标识：**

```objective-c
@protocol MyProtocol <NSObject>
@required   // 必须实现（默认）
- (void)requiredMethod;

@optional   // 可选实现
- (void)optionalMethod;
@end
```

**Protocol和Category的区别：**

| 特性 | Protocol | Category |
|------|----------|----------|
| **本质** | 接口声明 | 方法实现 |
| **方法实现** | 不提供实现 | 提供实现 |
| **作用** | 接口约束 | 扩展功能 |
| **遵循方式** | `<Protocol>` | 无需遵循 |
| **多继承** | 一个类可遵循多个协议 | 一个类可有多个Category |

## 【场景题】
**题目：** Protocol在代理模式中如何使用？

**答案：**

```objective-c
// 1. 定义协议
@protocol TableViewCellDelegate <NSObject>
@optional
- (void)cellDidClick:(UITableViewCell *)cell;
- (void)cellDidLongPress:(UITableViewCell *)cell;
@end

// 2. 被代理对象声明delegate属性
@interface MyCell : UITableViewCell
@property (nonatomic, weak) id<TableViewCellDelegate> delegate;
@end

// 3. 调用代理方法
@implementation MyCell
- (void)touchesBegan:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event {
    if ([self.delegate respondsToSelector:@selector(cellDidClick:)]) {
        [self.delegate cellDidClick:self];
    }
}
@end

// 4. 代理方遵循协议并实现
@interface ViewController () <TableViewCellDelegate>
@end

@implementation ViewController
- (void)cellDidClick:(UITableViewCell *)cell {
    NSLog(@"Cell被点击了");
}
@end
```

## 【代码示例】
```objective-c
// 1. 协议定义
@protocol Drawable <NSObject>
@required
- (void)draw;
@property (nonatomic, strong) UIColor *color;

@optional
- (BOOL)canDraw;
@end

// 2. 遵循协议
@interface Circle : NSObject <Drawable>
@property (nonatomic, strong) UIColor *color;
@end

@implementation Circle
- (void)draw {
    NSLog(@"画圆，颜色：%@", self.color);
}
- (BOOL)canDraw {
    return YES;
}
@end

// 3. 多协议遵循
@interface Square : NSObject <Drawable, NSCopying>
@end

// 4. 协议作为类型约束
- (void)renderShape:(id<Drawable>)shape {
    if ([shape canDraw]) {
        [shape draw];
    }
}

// 5. 代理模式完整示例
@protocol NetworkManagerDelegate <NSObject>
@required
- (void)networkManagerDidFinish:(id)result;

@optional
- (void)networkManagerDidFail:(NSError *)error;
- (void)networkManagerDidStartRequest;
@end

@interface NetworkManager : NSObject
@property (nonatomic, weak) id<NetworkManagerDelegate> delegate;
- (void)startRequest;
@end

@implementation NetworkManager
- (void)startRequest {
    // 开始请求
    if ([self.delegate respondsToSelector:@selector(networkManagerDidStartRequest)]) {
        [self.delegate networkManagerDidStartRequest];
    }
    
    // 请求完成
    [self.delegate networkManagerDidFinish:@"数据"];
}
@end
```

## 【答题要点】
- Protocol是接口声明，不提供方法实现
- 两个核心作用：接口约束、代理模式
- @required：必须实现（默认）；@optional：可选实现
- 和Category区别：Protocol是声明，Category是实现
- 一个类可以遵循多个协议（OC的多继承替代方案）
- 代理模式中用weak修饰delegate避免循环引用
- 调用@optional方法前需要respondsToSelector检查
