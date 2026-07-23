# Masonry布局约束封装

## 【理论题】
**题目：** 请简述Masonry的作用和基本使用方法？
**答案：**

**Masonry的作用：**
> Masonry是AutoLayout的链式语法封装库，用更简洁的语法替代原生繁琐的约束代码。

**三个核心方法区别：**

| 方法 | 作用 | 使用场景 |
|------|------|---------|
| `makeConstraints` | **添加**约束 | 首次设置约束 |
| `updateConstraints` | **更新**约束 | 修改已有约束的值 |
| `remakeConstraints` | **移除并重新添加**约束 | 完全重新布局 |

## 【场景题】
**题目：** makeConstraints、updateConstraints、remakeConstraints的区别？

**答案：**

```objective-c
// makeConstraints：添加约束（首次设置）
[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.top.equalTo(self.view).offset(100);
    make.left.equalTo(self.view).offset(20);
    make.size.mas_equalTo(CGSizeMake(100, 100));
}];

// updateConstraints：更新已有约束的值（只改值，不改结构）
[view mas_updateConstraints:^(MASConstraintMaker *make) {
    make.top.equalTo(self.view).offset(200);  // 只改了offset
}];

// remakeConstraints：清除所有旧约束，重新设置
[view mas_remakeConstraints:^(MASConstraintMaker *make) {
    make.bottom.equalTo(self.view).offset(-20);
    make.right.equalTo(self.view).offset(-20);
    make.size.mas_equalTo(CGSizeMake(200, 200));
}];
```

## 【代码示例】
```objective-c
// 1. 基础使用
UIView *view = [[UIView alloc] init];
view.backgroundColor = [UIColor redColor];
[self.view addSubview:view];

[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.top.equalTo(self.view).offset(100);
    make.left.equalTo(self.view).offset(20);
    make.right.equalTo(self.view).offset(-20);
    make.height.mas_equalTo(50);
}];

// 2. 居中
[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.center.equalTo(self.view);
    make.size.mas_equalTo(CGSizeMake(200, 200));
}];

// 3. 充满父视图
[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.edges.equalTo(self.view).insets(UIEdgeInsetsMake(20, 20, 20, 20));
}];

// 4. 等比例布局
[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.width.height.equalTo(@100);  // 等价于 mas_equalTo(100)
    make.center.equalTo(self.view);
}];

// 5. 相对其他视图
[view1 mas_makeConstraints:^(MASConstraintMaker *make) {
    make.top.left.equalTo(self.view).offset(20);
    make.right.equalTo(view2.mas_left).offset(-20);
    make.height.equalTo(view2);  // 高度等于view2
}];

// 6. 优先级
[view mas_makeConstraints:^(MASConstraintMaker *make) {
    make.width.equalTo(@100).priorityHigh();      // 高优先级
    make.width.equalTo(@200).priorityMedium();    // 中优先级
    make.width.equalTo(@300).priorityLow();        // 低优先级
}];

// 7. ScrollView中的约束
[scrollView mas_makeConstraints:^(MASConstraintMaker *make) {
    make.edges.equalTo(self.view);
}];

[contentView mas_makeConstraints:^(MASConstraintMaker *make) {
    make.edges.equalTo(scrollView);
    make.width.equalTo(scrollView);  // 垂直滚动
}];

// 8. 动画更新约束
[view mas_updateConstraints:^(MASConstraintMaker *make) {
    make.height.equalTo(@200);
}];

[self.view setNeedsUpdateConstraints];
[self.view updateConstraintsIfNeeded];
[UIView animateWithDuration:0.3 animations:^{
    [self.view layoutIfNeeded];
}];
```

## 【答题要点】
- Masonry是AutoLayout的链式语法封装库
- 核心方法：makeConstraints（添加）、updateConstraints（更新）、remakeConstraints（重置）
- makeConstraints：首次设置约束，不能重复调用
- updateConstraints：只更新已有约束的值，不改变约束结构
- remakeConstraints：清除所有旧约束，重新设置
- equalTo和mas_equalTo的区别：前者可以传UIView，后者可以传数值
- 支持优先级设置：priorityHigh、priorityMedium、priorityLow
- 支持动画：updateConstraints + layoutIfNeeded
