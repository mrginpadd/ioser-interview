# CPU计算耗时原因与优化

## 【概念题】
**题目：** CPU计算耗时会导致哪些卡顿问题？

**答案：**

```
CPU负责的工作：
├── 布局计算（layoutSubviews）
├── 视图创建和销毁
├── 路径计算（UIBezierPath）
├── 文字渲染（UILabel、UITextView）
├── 图片解码（PNG/JPEG解码）
└── 动画计算

CPU耗时的常见原因：
├── AutoLayout约束过多（约束解析复杂）
├── 大量视图层级（递归遍历耗时）
├── 复杂路径计算（圆角、阴影路径）
├── 重复调用setNeedsLayout/layoutIfNeeded
├── 图片解码（大图解码耗时）
└── 文字排版（富文本、动态字体）
```

## 【场景题】
**题目：** 如何优化AutoLayout的性能问题？

**答案：**

```objective-c
// 方案1：减少约束数量
// ❌ 不好的做法：使用大量约束
[self.view addConstraints:[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-20-[view1]-20-[view2]-20-|" options:0 metrics:nil views:views]];
[self.view addConstraints:[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-20-[view3]-20-[view4]-20-|" options:0 metrics:nil views:views]];
// ... 更多约束

// ✅ 好的做法：合并视图或使用Frame
// 使用容器视图减少约束
[self.containerView addSubview:view1];
[self.containerView addSubview:view2];
[self.view addConstraints:[NSLayoutConstraint constraintsWithVisualFormat:@"H:|-20-[containerView]-20-|" options:0 metrics:nil views:views]];

// 方案2：缓存计算结果
@property (nonatomic, strong) NSMutableDictionary *layoutCache;

- (CGFloat)calculateWidthForText:(NSString *)text {
    NSString *key = [NSString stringWithFormat:@"%@_%ld", text, (long)self.font.pointSize];
    NSNumber *cachedWidth = self.layoutCache[key];
    if (cachedWidth) {
        return cachedWidth.floatValue;
    }
    CGFloat width = [text boundingRectWithSize:CGSizeMake(CGFLOAT_MAX, 30)
                                       options:NSStringDrawingUsesLineFragmentOrigin
                                    attributes:@{NSFontAttributeName: self.font}
                                       context:nil].size.width;
    self.layoutCache[key] = @(width);
    return width;
}

// 方案3：使用Frame替代AutoLayout（性能敏感场景）
- (void)layoutSubviews {
    [super layoutSubviews];
    self.subview.frame = CGRectMake(20, 20, self.bounds.size.width - 40, 40);
    self.anotherSubview.frame = CGRectMake(20, 70, self.bounds.size.width - 40, 40);
}
```

## 【代码示例】
```objective-c
// ❌ 不好的做法：频繁调用layoutIfNeeded
for (int i = 0; i < 100; i++) {
    self.view.frame = CGRectMake(0, i * 10, 100, 100);
    [self.view layoutIfNeeded]; // 每次都触发布局计算
}

// ✅ 好的做法：批量更新后统一布局
[self.view setNeedsLayout];
for (int i = 0; i < 100; i++) {
    self.view.frame = CGRectMake(0, i * 10, 100, 100);
}
[self.view layoutIfNeeded]; // 只计算一次

// ❌ 不好的做法：在滚动时计算
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    // ...
    cell.textLabel.attributedText = [self createAttributedText:self.data[indexPath.row]]; // 耗时操作
    return cell;
}

// ✅ 好的做法：预计算并缓存
- (void)precomputeAttributedTexts {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        for (NSString *text in self.data) {
            NSAttributedString *attrText = [self createAttributedText:text];
            [self.attributedTextCache setObject:attrText forKey:text];
        }
        dispatch_async(dispatch_get_main_queue(), ^{
            [self.tableView reloadData];
        });
    });
}
```