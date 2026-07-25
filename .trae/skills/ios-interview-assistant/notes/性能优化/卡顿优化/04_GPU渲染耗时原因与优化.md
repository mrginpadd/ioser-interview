# GPU渲染耗时原因与优化（离屏渲染详解）

## 【概念题】
**题目：** 什么是离屏渲染？为什么离屏渲染会导致卡顿？

**答案：**

```
GPU渲染流程：
├── CPU准备数据 → GPU渲染 → 显示到屏幕
├── 正常渲染：直接在屏幕缓冲区绘制
├── 离屏渲染：先在屏幕外缓冲区绘制，再合成到屏幕

离屏渲染的触发条件：
├── layer.masksToBounds = YES + cornerRadius（非UIImageView）
├── layer.shadow（未设置shadowPath）
├── layer.mask
├── layer.shouldRasterize = YES（光栅化）
├── group opacity（UIViewGroupOpacity）
└── 复杂的layer变换

离屏渲染为什么慢：
├── 需要额外的缓冲区分配和管理
├── 需要多次渲染（离屏缓冲区→屏幕缓冲区）
├── 增加GPU负担，可能导致帧率下降
```

## 【场景题】
**题目：** 如何避免离屏渲染？

**答案：**

```objective-c
// 方案1：使用shadowPath避免阴影离屏渲染
// ❌ 不好的做法
self.view.layer.shadowColor = [UIColor blackColor].CGColor;
self.view.layer.shadowOpacity = 0.5;
self.view.layer.shadowRadius = 10;

// ✅ 好的做法
self.view.layer.shadowColor = [UIColor blackColor].CGColor;
self.view.layer.shadowOpacity = 0.5;
self.view.layer.shadowRadius = 10;
self.view.layer.shadowPath = [[UIBezierPath bezierPathWithRect:self.view.bounds] CGPath];

// 方案2：UIImageView圆角优化
// ❌ 不好的做法（会触发离屏渲染）
self.imageView.layer.cornerRadius = 20;
self.imageView.layer.masksToBounds = YES;

// ✅ 好的做法1：使用图片裁剪
UIImage *image = [UIImage imageNamed:@"avatar"];
self.imageView.image = [image imageWithRoundedCorners:CGSizeMake(20, 20)];

// ✅ 好的做法2：使用mask
CAShapeLayer *maskLayer = [CAShapeLayer layer];
maskLayer.path = [[UIBezierPath bezierPathWithRoundedRect:self.imageView.bounds
                                           byRoundingCorners:UIRectCornerAllCorners
                                                 cornerRadii:CGSizeMake(20, 20)] CGPath];
self.imageView.layer.mask = maskLayer;

// 方案3：使用光栅化优化（适用于静态内容）
self.staticView.layer.shouldRasterize = YES;
self.staticView.layer.rasterizationScale = [UIScreen mainScreen].scale;
```

## 【代码示例】
```objective-c
// UIImage圆角处理扩展
@implementation UIImage (RoundedCorners)

- (UIImage *)imageWithRoundedCorners:(CGSize)cornerSize {
    UIGraphicsBeginImageContextWithOptions(self.size, NO, [UIScreen mainScreen].scale);
    UIBezierPath *path = [UIBezierPath bezierPathWithRoundedRect:CGRectMake(0, 0, self.size.width, self.size.height)
                                                   byRoundingCorners:UIRectCornerAllCorners
                                                         cornerRadii:cornerSize];
    [path addClip];
    [self drawInRect:CGRectMake(0, 0, self.size.width, self.size.height)];
    UIImage *roundedImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return roundedImage;
}

@end

// 阴影优化
- (void)setupShadow {
    UIView *shadowView = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
    shadowView.backgroundColor = [UIColor whiteColor];
    
    // 设置shadowPath避免离屏渲染
    shadowView.layer.shadowColor = [UIColor blackColor].CGColor;
    shadowView.layer.shadowOpacity = 0.3;
    shadowView.layer.shadowRadius = 4;
    shadowView.layer.shadowOffset = CGSizeMake(0, 2);
    shadowView.layer.shadowPath = [[UIBezierPath bezierPathWithRect:shadowView.bounds] CGPath];
    
    [self.view addSubview:shadowView];
}

// 复杂圆角处理（不同角不同圆角）
- (void)setupComplexRoundedCorners {
    UIView *view = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 200, 100)];
    view.backgroundColor = [UIColor blueColor];
    
    CAShapeLayer *maskLayer = [CAShapeLayer layer];
    maskLayer.path = [[UIBezierPath bezierPathWithRoundedRect:view.bounds
                                               byRoundingCorners:UIRectCornerTopLeft | UIRectCornerBottomRight
                                                     cornerRadii:CGSizeMake(20, 20)] CGPath];
    view.layer.mask = maskLayer;
    
    [self.view addSubview:view];
}
```