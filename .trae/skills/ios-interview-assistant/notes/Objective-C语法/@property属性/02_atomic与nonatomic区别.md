# atomic与nonatomic

## 【理论题】
**题目：** 请解释atomic和nonatomic的区别，以及在实际开发中应该如何选择？
**答案：**

**atomic（原子属性）：**
- 编译器生成的getter/setter会保证**原子性操作**
- 通过**自旋锁（spinlock）**实现，确保读写操作的完整性
- **注意**：atomic**不保证绝对的线程安全**！它只保证单个属性的读写完整，不能保证多个属性操作的原子性

**nonatomic（非原子属性）：**
- 编译器生成的getter/setter**不做原子性保证**
- 性能比atomic**高20-30%**
- 需要开发者**手动保证线程安全**

**核心区别：**

| 特性 | atomic | nonatomic |
|------|--------|-----------|
| 原子性 | 保证 | 不保证 |
| 线程安全 | 部分保证（不绝对） | 不保证 |
| 性能 | 较低 | 较高 |
| 适用场景 | 多线程共享属性 | 单线程属性 |

## 【场景题】
**题目：** 在实际项目中，为什么我们通常使用`nonatomic`而不是`atomic`？
**答案：**
1. **性能考虑**：atomic需要加锁解锁，带来20-30%的性能开销
2. **atomic不保证真正的线程安全**：
   ```objective-c
   // 即使使用atomic，以下代码仍然不是线程安全的
   @property (atomic, strong) NSString *name;
   
   // 线程A
   self.name = @"Alice";
   // 线程B
   self.name = @"Bob";
   // 线程C
   NSString *temp = self.name; // 可能获取到中间状态
   ```
3. **需要线程安全时，应使用更高级的锁机制**：
   - `@synchronized`
   - `dispatch_queue`（串行队列）
   - `NSLock`等

**最佳实践：**
- 默认使用`nonatomic`
- 需要线程安全时，手动加锁或使用串行队列

## 【代码示例】
```objective-c
// 正确：默认使用nonatomic
@property (nonatomic, strong) NSString *userName;
@property (nonatomic, weak) UIView *containerView;

// 需要线程安全时，手动实现
@interface DataManager : NSObject
@property (nonatomic, strong) NSString *sharedData;
@end

@implementation DataManager {
    dispatch_queue_t _syncQueue;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _syncQueue = dispatch_queue_create("com.example.sync", DISPATCH_QUEUE_SERIAL);
    }
    return self;
}

- (NSString *)sharedData {
    __block NSString *data;
    dispatch_sync(_syncQueue, ^{
        data = _sharedData;
    });
    return data;
}

- (void)setSharedData:(NSString *)sharedData {
    dispatch_sync(_syncQueue, ^{
        _sharedData = sharedData;
    });
}
@end
```

## 【答题要点】
- atomic通过自旋锁保证原子性，但不保证线程安全
- nonatomic性能更高，是实际开发的默认选择
- 需要线程安全时应使用串行队列或锁，而不是依赖atomic
- 多属性操作需要手动保证原子性
