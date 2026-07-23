# 视图系统

## 【理论题】
**题目：** 请解释UIView和CALayer的区别？它们各自负责什么？
**答案：**

**UIView和CALayer的区别：**

**通俗理解：UIView是"指挥官"，CALayer是"执行者"。**
- UIView管"交互"：处理触摸、手势、布局位置
- CALayer管"外观"：渲染颜色、圆角、动画、显示图片
- 每个UIView自带一个CALayer，指挥官说什么，执行者做什么。

```
┌─────────────────────────────────────────────────────┐
│                    UIView                           │
│  ┌─────────────────────────────────────────────┐   │
│  │  负责：事件响应、布局管理、视图层级关系        │   │
│  │  属性：frame、bounds、center、transform      │   │
│  │  方法：hitTest:、pointInside:、addSubview:   │   │
│  └─────────────────────────────────────────────┘   │
│                       │                            │
│                       │ backing layer              │
│                       ▼                            │
│  ┌─────────────────────────────────────────────┐   │
│  │                   CALayer                    │   │
│  │  负责：渲染、动画、显示内容                     │   │
│  │  属性：contents、opacity、cornerRadius       │   │
│  │  方法：addAnimation:、renderInContext:       │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**详细对比：**

| 特性 | UIView | CALayer |
|------|--------|---------|
| **职责** | 事件响应、布局、视图管理 | 渲染、动画、显示 |
| **坐标系** | 响应式坐标系 | 几何坐标系 |
| **事件处理** | 支持触摸事件 | 不支持触摸事件 |
| **层级关系** | UIView层级 | CALayer层级（shadow layer） |
| **动画** | UIKit动画（基于CALayer） | Core Animation |
| **性能** | 较高开销（事件+渲染） | 较低开销（仅渲染） |

## 【场景题】
**题目：** 什么时候用CALayer而不是UIView？

**答案：**

| 场景 | 选择 | 原因 |
|------|------|------|
| **复杂动画** | CALayer | Core Animation性能更好 |
| **阴影/圆角** | CALayer | cornerRadius、shadow属性 |
| **图片渲染** | CALayer | contents属性直接设置图片 |
| **粒子效果** | CALayer | CAEmitterLayer |
| **事件交互** | UIView | 需要触摸事件 |
| **AutoLayout** | UIView | CALayer不支持约束 |

## 【代码示例】
```objective-c
// 1. UIView基本操作
UIView *view = [[UIView alloc] initWithFrame:CGRectMake(50, 50, 200, 200)];
view.backgroundColor = [UIColor redColor];
view.layer.cornerRadius = 10;        // 通过layer设置圆角
view.layer.masksToBounds = YES;      // 裁剪子视图
view.layer.shadowColor = [UIColor blackColor].CGColor;
view.layer.shadowOpacity = 0.5;
view.layer.shadowOffset = CGSizeMake(5, 5);
[superView addSubview:view];

// 2. CALayer动画
CABasicAnimation *animation = [CABasicAnimation animationWithKeyPath:@"position"];
animation.fromValue = [NSValue valueWithCGPoint:view.layer.position];
animation.toValue = [NSValue valueWithCGPoint:CGPointMake(300, 300)];
animation.duration = 1.0;
animation.autoreverses = YES;
animation.repeatCount = HUGE_VALF;
[view.layer addAnimation:animation forKey:@"moveAnimation"];

// 3. 使用CALayer创建复杂效果
CALayer *gradientLayer = [CAGradientLayer layer];
gradientLayer.frame = view.bounds;
gradientLayer.colors = @[(id)[UIColor redColor].CGColor, 
                         (id)[UIColor blueColor].CGColor];
gradientLayer.startPoint = CGPointMake(0, 0);
gradientLayer.endPoint = CGPointMake(1, 1);
[view.layer addSublayer:gradientLayer];

// 4. 性能优化：使用CALayer替代UIView
// 不需要交互的静态内容可以直接用CALayer
CALayer *imageLayer = [CALayer layer];
imageLayer.frame = CGRectMake(0, 0, 100, 100);
imageLayer.contents = (__bridge id)[UIImage imageNamed:@"icon"].CGImage;
[view.layer addSublayer:imageLayer];
```

## 【答题要点】
- UIView负责事件响应、布局管理、视图层级关系
- CALayer负责渲染、动画、显示内容
- UIView内部有一个backing layer
- UIView通过layer设置圆角、阴影等视觉效果
- CALayer不支持触摸事件
- 复杂动画用CALayer性能更好
- 需要事件交互用UIView
