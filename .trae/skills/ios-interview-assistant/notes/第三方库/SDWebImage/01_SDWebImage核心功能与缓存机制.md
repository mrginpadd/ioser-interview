# SDWebImage

## 【理论题】
**题目：** 请简述SDWebImage的核心功能和缓存机制？
**答案：**

**SDWebImage核心功能：**

```
┌─────────────────────────────────────────────────────┐
│              SDWebImage功能                          │
│                                                     │
│  1. 异步加载网络图片                                  │
│     - UIImageView+WebCache分类                        │
│     - [imageView sd_setImageWithURL:]                │
│                                                     │
│  2. 三级缓存机制                                      │
│     - 内存缓存（NSCache）→ 磁盘缓存（文件）→ 网络请求   │
│                                                     │
│  3. 图片解码优化                                      │
│     - 后台解码，避免主线程卡顿                         │
│                                                     │
│  4. 自动管理请求                                      │
│     - 取消重复请求、内存不足时自动清理                   │
│                                                     │
│  5. 动画支持                                          │
│     - GIF动图播放、WebP格式支持                       │
└─────────────────────────────────────────────────────┘
```

**三级缓存机制：**

| 层级 | 存储位置 | 特点 |
|------|---------|------|
| **内存缓存** | NSCache | 最快，App退出后失效 |
| **磁盘缓存** | 文件系统 | 较慢，App退出后保留 |
| **网络请求** | 服务器 | 最慢，首次加载使用 |

**缓存查找流程：**

```
加载图片
    │
    ▼
检查内存缓存（SDImageCache）
    │
  有缓存 ──────────────┬─────── 无缓存
    │                  │
    ▼                  ▼
直接返回           检查磁盘缓存
    │                  │
                 有缓存 ────────┬─────── 无缓存
                    │           │
                    ▼           ▼
              读取磁盘并      发起网络请求
              写入内存        下载完成后
                    │           │
                    └─────┬─────┘
                          ▼
                    显示图片
```

## 【场景题】
**题目：** 列表页大量图片加载如何优化？

**答案：**

```objective-c
// 1. 设置占位图和错误图
[imageView sd_setImageWithURL:url 
              placeholderImage:[UIImage imageNamed:@"placeholder"] 
                     completed:^(UIImage *image, NSError *error, SDImageCacheType cacheType, NSURL *imageURL) {
    if (error) {
        imageView.image = [UIImage imageNamed:@"error"];
    }
}];

// 2. 设置图片圆角
imageView.layer.cornerRadius = 10;
imageView.layer.masksToBounds = YES;

// 3. 取消滑动时的请求（UITableView/UICollectionView）
- (void)prepareForReuse {
    [super prepareForReuse];
    [self.imageView sd_cancelCurrentImageLoad];
}

// 4. 设置缓存大小限制
SDImageCache *cache = [SDImageCache sharedImageCache];
cache.maxMemoryCost = 100 * 1024 * 1024;  // 100MB内存缓存
cache.maxDiskSize = 500 * 1024 * 1024;     // 500MB磁盘缓存
```

## 【代码示例】
```objective-c
// 1. 基础使用（UIImageView）
UIImageView *imageView = [[UIImageView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
[imageView sd_setImageWithURL:[NSURL URLWithString:@"https://example.com/image.jpg"]];

// 2. 设置占位图
[imageView sd_setImageWithURL:url 
              placeholderImage:[UIImage imageNamed:@"placeholder"]];

// 3. 设置完成回调
[imageView sd_setImageWithURL:url 
              placeholderImage:nil 
                     completed:^(UIImage *image, NSError *error, SDImageCacheType cacheType, NSURL *imageURL) {
    if (image) {
        NSLog(@"图片加载成功，来源: %@", cacheType == SDImageCacheTypeMemory ? @"内存" : 
                                       cacheType == SDImageCacheTypeDisk ? @"磁盘" : @"网络");
    } else {
        NSLog(@"图片加载失败: %@", error);
    }
}];

// 4. 设置图片下载进度
[imageView sd_setImageWithURL:url 
              placeholderImage:nil 
                       options:SDWebImageProgressiveDownload 
                     progress:^(NSInteger receivedSize, NSInteger expectedSize) {
    CGFloat progress = receivedSize / (CGFloat)expectedSize;
    NSLog(@"下载进度: %.2f%%", progress * 100);
} completed:nil];

// 5. 取消当前请求
[imageView sd_cancelCurrentImageLoad];

// 6. 清理缓存
SDImageCache *cache = [SDImageCache sharedImageCache];
[cache clearMemory];           // 清理内存缓存
[cache clearDiskOnCompletion:nil];  // 清理磁盘缓存
[cache clearDisk];             // 清理磁盘缓存（异步）

// 7. 删除指定缓存
[cache removeImageForKey:@"https://example.com/image.jpg" withCompletion:nil];

// 8. 检查缓存是否存在
BOOL isCached = [cache diskImageExistsWithKey:@"https://example.com/image.jpg"];

// 9. 使用SDWebImageManager（高级用法）
SDWebImageManager *manager = [SDWebImageManager sharedManager];
[manager loadImageWithURL:url 
                  options:0 
                 progress:nil 
                completed:^(UIImage *image, NSData *data, NSError *error, SDImageCacheType cacheType, BOOL finished, NSURL *imageURL) {
    imageView.image = image;
}];

// 10. 设置缓存键自定义
SDWebImageManager.sharedManager.cacheKeyFilter = ^NSString *(NSURL *url) {
    return url.absoluteString;  // 默认使用URL作为缓存键
};

// 11. 设置下载器配置
SDWebImageDownloader *downloader = [SDWebImageDownloader sharedDownloader];
downloader.maxConcurrentDownloads = 4;  // 最大并发数
downloader.downloadTimeout = 15;         // 超时时间
[downloader setValue:@"MyApp/1.0" forHTTPHeaderField:@"User-Agent"];
```

## 【答题要点】
- SDWebImage是iOS最流行的图片加载库
- 核心功能：异步加载、三级缓存、图片解码、请求管理
- 三级缓存：内存缓存（NSCache）→ 磁盘缓存（文件）→ 网络请求
- 内存缓存最快，磁盘缓存较慢但持久，网络请求最慢
- 缓存键默认使用URL的MD5值
- 支持GIF动图、WebP格式
- 支持进度回调、完成回调
- 自动取消重复请求
- UITableView/UICollectionView中需要在prepareForReuse中取消请求
- SDImageCache管理缓存，SDWebImageDownloader管理下载
