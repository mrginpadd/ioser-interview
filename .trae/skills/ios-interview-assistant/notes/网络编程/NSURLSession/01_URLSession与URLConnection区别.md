# NSURLSession

## 【理论题】
**题目：** 请解释NSURLSession的作用，以及和NSURLConnection的区别？
**答案：**

**NSURLSession的作用：**
> NSURLSession是iOS 7引入的网络请求API，替代了旧的NSURLConnection，负责发送HTTP请求、下载/上传文件、处理后台任务。

**NSURLSession vs NSURLConnection：**

```
┌─────────────────────────────────────────────────────┐
│              NSURLSession（iOS 7+）                  │
│  ┌─────────────────────────────────────────────┐   │
│  │  Session（会话） → Task（任务）               │   │
│  │  - 支持后台下载/上传                          │   │
│  │  - 支持配置（超时、缓存、Cookie）              │   │
│  │  - 多个Task共享同一个Session配置               │   │
│  │  - 支持断点续传                              │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           NSURLConnection（已废弃）                  │
│  ┌─────────────────────────────────────────────┐   │
│  │  - 一个请求对应一个Connection                 │   │
│  │  - 不支持后台任务                             │   │
│  │  - 配置分散，不统一                           │   │
│  │  - iOS 9后废弃                               │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**三种Task类型：**

| Task类型 | 作用 | 典型场景 |
|---------|------|---------|
| **DataTask** | 获取数据（NSData） | JSON请求、API调用 |
| **DownloadTask** | 下载文件到磁盘 | 图片下载、文件下载 |
| **UploadTask** | 上传文件 | 上传图片、文件 |

## 【场景题】
**题目：** AFNetworking 3.0为什么废弃了基于NSURLConnection的版本？

**答案：**
- NSURLConnection已废弃，Apple推荐用NSURLSession
- NSURLSession支持后台下载、断点续传
- NSURLSession配置更灵活（超时、缓存、Cookie统一管理）
- 性能更好，支持连接池复用

## 【代码示例】
```objective-c
// 1. 创建Session配置
NSURLSessionConfiguration *config = [NSURLSessionConfiguration defaultSessionConfiguration];
config.timeoutIntervalForRequest = 30;    // 请求超时
config.timeoutIntervalForResource = 60;    // 资源超时
config.allowsCellularAccess = YES;        // 允许蜂窝网络
config.HTTPAdditionalHeaders = @{@"User-Agent": @"MyApp/1.0"};

// 2. 创建Session
NSURLSession *session = [NSURLSession sessionWithConfiguration:config
                                                     delegate:nil
                                                delegateQueue:[NSOperationQueue mainQueue]];

// 3. DataTask（GET请求）
NSURLSessionDataTask *dataTask = [session dataTaskWithURL:[NSURL URLWithString:@"https://api.example.com/data"]
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    if (error) {
        NSLog(@"请求失败: %@", error);
        return;
    }
    NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
    NSLog(@"响应数据: %@", json);
}];
[dataTask resume];  // 启动任务

// 4. DataTask（POST请求）
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"https://api.example.com/login"]];
request.HTTPMethod = @"POST";
request.HTTPBody = [@"username=abc&password=123" dataUsingEncoding:NSUTF8StringEncoding];
[request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];

NSURLSessionDataTask *postTask = [session dataTaskWithRequest:request
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    NSLog(@"POST响应: %@", [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding]);
}];
[postTask resume];

// 5. DownloadTask（文件下载）
NSURLSessionDownloadTask *downloadTask = [session downloadTaskWithURL:[NSURL URLWithString:@"https://example.com/file.zip"]
    completionHandler:^(NSURL *location, NSURLResponse *response, NSError *error) {
    // location是临时文件路径，需要移动到永久位置
    NSString *documentsPath = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0];
    NSString *destPath = [documentsPath stringByAppendingPathComponent:@"file.zip"];
    [[NSFileManager defaultManager] moveItemAtURL:location toURL:[NSURL fileURLWithPath:destPath] error:nil];
}];
[downloadTask resume];

// 6. UploadTask（文件上传）
NSURL *fileURL = [NSURL fileURLWithPath:@"/path/to/image.jpg"];
NSURLSessionUploadTask *uploadTask = [session uploadTaskWithRequest:request
                                                            fromFile:fileURL
                                                   completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    NSLog(@"上传完成");
}];
[uploadTask resume];

// 7. 取消任务
[dataTask cancel];

// 8. 使用sharedSession（简单场景）
NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithURL:url
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    // 处理响应
}];
[task resume];
```

## 【答题要点】
- NSURLSession是iOS 7引入的，替代NSURLConnection
- Session + Task的设计：Session管配置，Task管执行
- 三种Task：DataTask、DownloadTask、UploadTask
- 支持后台下载、断点续传、配置统一管理
- defaultSessionConfiguration：默认配置
- ephemeralSessionConfiguration：无缓存（隐私模式）
- backgroundSessionConfiguration：后台下载
- task需要调用resume才会启动
- AFNetworking 3.0基于NSURLSession
