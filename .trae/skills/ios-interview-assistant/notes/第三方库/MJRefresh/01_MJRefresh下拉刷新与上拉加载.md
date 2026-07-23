# MJRefresh下拉刷新与上拉加载

## 【理论题】
**题目：** 请简述MJRefresh的作用和基本使用方法？
**答案：**

**MJRefresh的作用：**
> MJRefresh是iOS下拉刷新和上拉加载更多的第三方库，提供多种刷新动画效果。

**核心类结构：**

| 类名 | 作用 |
|------|------|
| **MJRefreshHeader** | 下拉刷新基类 |
| **MJRefreshNormalHeader** | 默认下拉刷新（带箭头动画） |
| **MJRefreshGifHeader** | GIF动画下拉刷新 |
| **MJRefreshFooter** | 上拉加载更多基类 |
| **MJRefreshAutoNormalFooter** | 自动上拉加载 |
| **MJRefreshBackNormalFooter** | 点击触发上拉加载 |

## 【场景题】
**题目：** 如何自定义下拉刷新动画？

**答案：**

```objective-c
// 使用GIF动画作为下拉刷新
MJRefreshGifHeader *header = [MJRefreshGifHeader headerWithRefreshingBlock:^{
    [self loadNewData];
}];

// 设置普通状态动画
[header setImages:idleImages duration:1.0 forState:MJRefreshStateIdle];
// 设置刷新中动画
[header setImages:refreshingImages duration:1.0 forState:MJRefreshStateRefreshing];

self.tableView.mj_header = header;
```

## 【代码示例】
```objective-c
// 1. 基础下拉刷新
MJRefreshNormalHeader *header = [MJRefreshNormalHeader headerWithRefreshingBlock:^{
    [self loadNewData];
}];
self.tableView.mj_header = header;

// 2. 基础上拉加载
MJRefreshAutoNormalFooter *footer = [MJRefreshAutoNormalFooter footerWithRefreshingBlock:^{
    [self loadMoreData];
}];
self.tableView.mj_footer = footer;

// 3. 结束刷新
[self.tableView.mj_header endRefreshing];
[self.tableView.mj_footer endRefreshing];

// 4. 没有更多数据
[self.tableView.mj_footer endRefreshingWithNoMoreData];

// 5. 重置没有更多数据状态
[self.tableView.mj_footer resetNoMoreData];

// 6. 自定义文字
MJRefreshNormalHeader *header = [MJRefreshNormalHeader headerWithRefreshingBlock:^{
    [self loadNewData];
}];
[header setTitle:@"下拉刷新" forState:MJRefreshStateIdle];
[header setTitle:@"松开刷新" forState:MJRefreshStatePulling];
[header setTitle:@"正在刷新..." forState:MJRefreshStateRefreshing];
self.tableView.mj_header = header;

// 7. 自动隐藏footer（无数据时）
self.tableView.mj_footer.hidden = NO;

// 8. 使用Target-Action方式
MJRefreshNormalHeader *header = [MJRefreshNormalHeader headerWithRefreshingTarget:self refreshingAction:@selector(loadNewData)];
self.tableView.mj_header = header;
```

## 【答题要点】
- MJRefresh用于实现下拉刷新和上拉加载更多
- 核心类：MJRefreshHeader（下拉）、MJRefreshFooter（上拉）
- 通过分类方式添加到UITableView/UICollectionView
- 使用mj_header和mj_footer属性设置刷新控件
- 结束刷新调用endRefreshing
- 没有更多数据调用endRefreshingWithNoMoreData
- 支持自定义动画和文字
- 支持GIF动画刷新效果
