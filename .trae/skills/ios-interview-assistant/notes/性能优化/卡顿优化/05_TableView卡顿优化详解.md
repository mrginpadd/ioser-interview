# TableView卡顿优化详解

## 【概念题】
**题目：** TableView卡顿的常见原因有哪些？

**答案：**

```
TableView卡顿的常见原因：
├── cell复用不当（每次都创建新cell）
├── 高度计算耗时（动态高度计算）
├── 图片加载阻塞（主线程加载图片）
├── 复杂布局（AutoLayout约束过多）
├── 子视图过多（cell层级深）
├── 重复计算（每次scroll都重新计算）
└── 主线程阻塞（网络请求、数据库操作）

TableView优化策略：
├── 使用cell复用机制
├── 缓存cell高度
├── 异步加载图片
├── 简化cell布局
├── 减少子视图数量
├── 预计算数据
└── 优化数据源方法
```

## 【场景题】
**题目：** 如何优化TableView的滚动性能？

**答案：**

```objective-c
// 方案1：使用cell复用
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"CustomCell";
    CustomCell *cell = [tableView dequeueReusableCellWithIdentifier:identifier];
    if (!cell) {
        cell = [[CustomCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:identifier];
    }
    [self configureCell:cell atIndexPath:indexPath];
    return cell;
}

// 方案2：缓存cell高度
@property (nonatomic, strong) NSMutableDictionary *heightCache;

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    NSNumber *height = self.heightCache[indexPath.row];
    if (height) {
        return height.floatValue;
    }
    CGFloat height = [self calculateHeightForRowAtIndexPath:indexPath];
    self.heightCache[indexPath.row] = @(height);
    return height;
}

// 方案3：异步加载图片
- (void)configureCell:(CustomCell *)cell atIndexPath:(NSIndexPath *)indexPath {
    cell.titleLabel.text = self.data[indexPath.row].title;
    [cell.imageView sd_setImageWithURL:[NSURL URLWithString:self.data[indexPath.row].imageURL]
                      placeholderImage:[UIImage imageNamed:@"placeholder"]];
}

// 方案4：使用estimatedHeight减少计算
self.tableView.estimatedRowHeight = 100;
self.tableView.rowHeight = UITableViewAutomaticDimension;

// 方案5：预取数据（iOS 10+）
- (void)tableView:(UITableView *)tableView prefetchRowsAtIndexPaths:(NSArray<NSIndexPath *> *)indexPaths {
    for (NSIndexPath *indexPath in indexPaths) {
        [self preloadDataForIndexPath:indexPath];
    }
}
```

## 【代码示例】
```objective-c
// 自定义cell优化
@interface CustomCell : UITableViewCell
@property (nonatomic, strong) UILabel *titleLabel;
@property (nonatomic, strong) UIImageView *iconImageView;
@end

@implementation CustomCell

- (instancetype)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier {
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        [self setupSubviews];
    }
    return self;
}

- (void)setupSubviews {
    // 使用Frame替代AutoLayout提升性能
    self.titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(60, 10, 200, 20)];
    self.titleLabel.font = [UIFont systemFontOfSize:16];
    [self.contentView addSubview:self.titleLabel];
    
    self.iconImageView = [[UIImageView alloc] initWithFrame:CGRectMake(10, 10, 40, 40)];
    self.iconImageView.contentMode = UIViewContentModeScaleAspectFill;
    self.iconImageView.clipsToBounds = YES;
    [self.contentView addSubview:self.iconImageView];
}

@end

// 数据源优化
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.dataArray.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"CustomCell";
    CustomCell *cell = [tableView dequeueReusableCellWithIdentifier:identifier];
    if (!cell) {
        cell = [[CustomCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:identifier];
    }
    
    // 避免在cellForRow中做耗时操作
    cell.titleLabel.text = self.dataArray[indexPath.row].title;
    
    // 异步加载图片并取消之前的请求
    // 原因：
    // 1. cell被复用时，之前的图片请求可能还在进行中
    // 2. 网络请求完成顺序不确定，慢速的旧请求可能后完成
    // 3. 如果不取消，会出现图片错位（cell显示错误的图片）
    // 4. 取消后可以节省网络带宽和内存
    [cell.iconImageView sd_cancelCurrentImageLoad];
    [cell.iconImageView sd_setImageWithURL:[NSURL URLWithString:self.dataArray[indexPath.row].imageURL]
                          placeholderImage:[UIImage imageNamed:@"placeholder"]];
    
    return cell;
}

// 高度计算缓存
- (CGFloat)calculateHeightForRowAtIndexPath:(NSIndexPath *)indexPath {
    NSString *text = self.dataArray[indexPath.row].title;
    CGSize size = [text boundingRectWithSize:CGSizeMake([UIScreen mainScreen].bounds.size.width - 70, CGFLOAT_MAX)
                                     options:NSStringDrawingUsesLineFragmentOrigin
                                  attributes:@{NSFontAttributeName: [UIFont systemFontOfSize:16]}
                                     context:nil].size;
    return MAX(size.height + 20, 60);
}
```