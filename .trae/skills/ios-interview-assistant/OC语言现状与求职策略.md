# OC语言现状与求职策略指导

## 【OC语言的现状】

```
┌─────────────────────────────────────────────────────┐
│  OC语言定位                                          │
├─────────────────────────────────────────────────────┤
│  设计年代：1984年，比响应式编程早20年                  │
│  当前定位：等待淘汰，但短期内不会死                    │
│  Apple战略：Swift是继任者，OC进入维护模式              │
├─────────────────────────────────────────────────────┤
│  为什么OC没有属性观察器语法糖？                       │
│  ├── 历史原因：设计时没有响应式编程概念               │
│  ├── Apple战略：语言创新精力都在Swift上               │
│  ├── 已有KVO：虽然难用，但"够用了"                   │
│  ├── 技术限制：C的超集，语法扩展受限                 │
│  └── 第三方库填补：ReactiveCocoa等已存在             │
├─────────────────────────────────────────────────────┤
│  OC不会"死"的原因                                    │
│  ├── 国内大厂核心项目大量OC代码（阿里、腾讯、字节）   │
│  ├── 老项目维护需要OC开发者                          │
│  ├── 面试仍会问OC底层原理                            │
│  └── OC岗位至少还能存在3-5年                         │
└─────────────────────────────────────────────────────┘
```

## 【OC vs Swift vs Flutter对比】

| 特性 | OC | Swift | Flutter |
|------|-----|-------|---------|
| 设计年代 | 1984 | 2014 | 2017 |
| 属性观察器 | ❌ 无 | ✅ willSet/didSet | ✅ .obs (GetX) |
| MVVM实现 | 繁琐（Block/KVO） | 简洁（Combine） | 极简（GetX） |
| 内存管理 | ARC + 手动__weak | ARC + [weak self] | GC自动管理 |
| 语法简洁度 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 学习成本 | 高（语法繁杂） | 中 | 低 |
| 未来趋势 | 维护模式 | Apple主推 | 跨平台主流 |

## 【求职策略：过渡期iOS开发者】

### 适用人群
- 毕业学的是OC，觉得OC繁杂
- 只会OC和Flutter，不会Swift/SwiftUI
- 目标是考编制，iOS只是过渡工作
- 不打算长期投入iOS技术栈

### 优先级排序

```
第一优先：考编制（真正目标）
第二优先：找到一份能养活自己的iOS工作（过渡）
第三优先：技术深度（够用就行）
```

### 精力分配

```
├── 80% → 考编准备
└── 20% → 面试准备
```

## 【面试准备：学什么 vs 不学什么】

### 学什么（性价比高）⭐⭐⭐⭐⭐

```
必学（面试高频考点）：
├── ✅ 内存管理
│   ├── ARC与MRC区别
│   ├── 引用计数机制
│   ├── 循环引用与解决
│   ├── AutoreleasePool原理
│   └── 内存修饰符（strong/weak/copy/assign）
├── ✅ Runtime
│   ├── 消息机制（发送+转发）
│   ├── 动态方法解析
│   ├── Method Swizzling
│   ├── 关联对象
│   └── isa指针
├── ✅ 多线程
│   ├── GCD（队列+sync/async）
│   ├── NSOperation
│   ├── 线程安全与锁
│   └── 死锁与避免
├── ✅ UI基础
│   ├── UIViewController生命周期
│   ├── 事件响应链
│   ├── UIView与CALayer
│   └── UITableView优化
├── ✅ 设计模式
│   ├── MVC vs MVVM
│   ├── 单例模式
│   ├── 代理模式
│   └── 观察者模式
└── ✅ 性能优化
    ├── 启动优化
    ├── 卡顿优化
    └── 内存优化
```

### 不用学（投入产出比低）⭐

```
不用深挖：
├── ❌ ReactiveCocoa深度使用（了解概念即可）
├── ❌ 复杂的OC黑魔法
├── ❌ 源码级别的底层实现（够面试用就行）
├── ❌ Swift/SwiftUI（过渡期没必要）
├── ❌ 架构设计深度（组件化、路由设计等）
└── ❌ 冷门第三方库的源码
```

## 【面试策略：80分 > 100分】

```
核心原则：
├── 核心80分 > 边缘100分
├── 面试准备到"能过面试"就停
├── 不追求100%掌握每个知识点
├── 找到工作后，重心全力转考编
└── OC是过渡工具，面试题是入场券
```

## 【不同语言实现MVVM的复杂度对比】

### Flutter GetX（极简）
```dart
// ViewModel
class CounterController extends GetxController {
  var count = 0.obs;          // 一行：响应式变量
  void increment() => count++;
}

// View
Obx(() => Text('${controller.count}'))  // 自动更新
```

### Swift（简洁）
```swift
class Counter {
    var count: Int = 0 {
        didSet {
            print("count changed: \(count)")
        }
    }
}
```

### OC Block版（繁琐但务实）
```objective-c
// ViewModel
@property (copy) void(^countChanged)(NSInteger);
@property (assign) NSInteger count;

- (void)setCount:(NSInteger)count {
    if (_count != count) {
        _count = count;
        if (self.countChanged) self.countChanged(count);
    }
}

// View
__weak typeof(self) weakSelf = self;
self.viewModel.countChanged = ^(NSInteger count) {
    weakSelf.label.text = [NSString stringWithFormat:@"%ld", count];
};
```

### OC复杂的原因
```
1. 语言层面缺少"属性观察器"
   ├── Flutter/Dart：.obs 一行搞定
   ├── Swift：willSet/didSet
   └── OC：没有，只能手动重写setter + Block/KVO

2. 没有自动内存管理语法糖
   ├── Swift：[weak self] in 闭包
   ├── Flutter：GC自动管理
   └── OC：__weak typeof(self) weakSelf = self; 啰嗦

3. 语言设计年代久远
   ├── OC：1984年设计，没有响应式编程概念
   └── Flutter/Dart：现代语言，天生支持响应式
```

## 【一句话总结】

> **"OC是过渡工具，面试题是入场券。学到能找到工作就够了，把主要精力放在考编上。"**

## 【面试话术：被问到"你觉得OC有什么缺点"】

> "OC作为30多年前的语言，确实有一些局限性：
> 1. 语法比较繁琐，比如实现MVVM需要手写Block或KVO，不如Swift的属性观察器简洁
> 2. 缺少现代语言的语法糖，如可选链、泛型等
> 3. 头文件机制增加了代码维护成本
> 
> 但OC也有优点：
> 1. Runtime动态性强大，适合做AOP、热修复等
> 2. 与C/C++无缝兼容，适合底层开发
> 3. 生态成熟，大量开源库支持
> 
> 如果是新项目，我会推荐用Swift；但维护老项目，OC仍然是必要的技能。"
