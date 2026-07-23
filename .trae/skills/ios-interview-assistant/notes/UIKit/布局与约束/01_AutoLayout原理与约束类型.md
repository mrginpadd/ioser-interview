# 布局与约束

## 【理论题】
**题目：** 请解释AutoLayout的原理，以及常用的约束类型有哪些？
**答案：**

**AutoLayout原理：**

```
AutoLayout = 约束系统 + 布局引擎

┌─────────────────────────────────────────────────────┐
│  开发者设置约束（如：左边距20、宽度100）               │
│                        │                            │
│                        ▼                            │
│  布局引擎（Cassowary算法）解算约束方程                 │
│                        │                            │
│                        ▼                            │
│  自动计算每个视图的frame，适配不同屏幕                 │
└─────────────────────────────────────────────────────┘
```

**常用约束类型：**

| 约束类型 | 作用 | 代码示例 |
|---------|------|---------|
| **Leading** | 左边缘距离 | `leading = superview.leading + 20` |
| **Trailing** | 右边缘距离 | `trailing = superview.trailing - 20` |
| **Top** | 顶部距离 | `top = superview.top + 20` |
| **Bottom** | 底部距离 | `bottom = superview.bottom - 20` |
| **Width** | 宽度固定 | `width = 100` |
| **Height** | 高度固定 | `height = 50` |
| **CenterX** | 水平居中 | `centerX = superview.centerX` |
| **CenterY** | 垂直居中 | `centerY = superview.centerY` |
| **AspectRatio** | 宽高比 | `width:height = 16:9` |

## 【场景题】
**题目：** 如何用AutoLayout实现一个正方形视图，宽度是父视图的一半，居中显示？

**答案：**

```objective-c
UIView *squareView = [[UIView alloc] init];
squareView.backgroundColor = [UIColor redColor];
squareView.translatesAutoresizingMaskIntoConstraints = NO;
[self.view addSubview:squareView];

// 约束：宽度是父视图的一半
[squareView.widthAnchor constraintEqualToAnchor:self.view.widthAnchor 
                                        multiplier:0.5].active = YES;
// 约束：宽高比1:1（正方形）
[squareView.heightAnchor constraintEqualToAnchor:squareView.widthAnchor].active = YES;
// 约束：水平居中
[squareView.centerXAnchor constraintEqualToAnchor:self.view.centerXAnchor].active = YES;
// 约束：垂直居中
[squareView.centerYAnchor constraintEqualToAnchor:self.view.centerYAnchor].active = YES;
```

## 【代码示例】
```objective-c
// 1. 创建视图并关闭自动转换
UIView *redView = [[UIView alloc] init];
redView.backgroundColor = [UIColor redColor];
redView.translatesAutoresizingMaskIntoConstraints = NO;
[self.view addSubview:redView];

// 2. 使用NSLayoutConstraint创建约束
NSArray *constraints = [NSLayoutConstraint constraintsWithVisualFormat:@"H:|-20-[redView]-20-|" 
                                                               options:0 
                                                               metrics:nil 
                                                                 views:NSDictionaryOfVariableBindings(redView)];
[self.view addConstraints:constraints];

// 3. 使用Anchor API创建约束（推荐）
[redView.topAnchor constraintEqualToAnchor:self.view.topAnchor constant:100].active = YES;
[redView.heightAnchor constraintEqualToConstant:50].active = YES;

// 4. Masonry第三方库（链式调用）
#import "Masonry.h"
[redView mas_makeConstraints:^(MASConstraintMaker *make) {
    make.top.equalTo(self.view).offset(100);
    make.left.equalTo(self.view).offset(20);
    make.right.equalTo(self.view).offset(-20);
    make.height.mas_equalTo(50);
}];

// 5. 约束优先级
UILayoutPriority highPriority = UILayoutPriorityRequired;
UILayoutPriority lowPriority = UILayoutPriorityDefaultLow;
[redView.widthAnchor constraintEqualToConstant:200].priority = highPriority;
[redView.widthAnchor constraintEqualToConstant:100].priority = lowPriority;
```

## 【答题要点】
- AutoLayout通过约束系统和布局引擎自动计算frame
- 布局引擎使用Cassowary算法解算约束方程
- 常用约束：Leading、Trailing、Top、Bottom、Width、Height、CenterX、CenterY、AspectRatio
- 设置约束前需关闭translatesAutoresizingMaskIntoConstraints
- Anchor API是推荐的约束方式
- Masonry提供链式调用简化约束编写
- 约束优先级：UILayoutPriorityRequired > UILayoutPriorityDefaultHigh > UILayoutPriorityDefaultLow
