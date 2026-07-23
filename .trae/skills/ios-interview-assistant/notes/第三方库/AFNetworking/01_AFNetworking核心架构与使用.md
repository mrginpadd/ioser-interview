# AFNetworking

## 【理论题】
**题目：** 请简述AFNetworking的核心架构和常用功能？
**答案：**

**AFNetworking核心架构：**

```
┌─────────────────────────────────────────────────────┐
│              AFNetworking架构                        │
│                                                     │
│  AFHTTPSessionManager                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  AFURLSessionManager（底层）                │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  NSURLSession（Apple原生）            │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────┘   │
│        │                                            │
│        ▼                                            │
│  AFHTTPRequestSerializer（请求序列化）                │
│  ┌─────────────────────────────────────────────┐   │
│  │  参数编码、Header设置、超时配置              │   │
│  └─────────────────────────────────────────────┘   │
│        │                                            │
│        ▼                                            │
│  AFHTTPResponseSerializer（响应序列化）              │
│  ┌─────────────────────────────────────────────┐   │
│  │  JSON解析、XML解析、图片解析、自定义解析     │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**常用功能：**

| 功能 | 说明 |
|------|------|
| **GET/POST请求** | 支持各种HTTP方法 |
| **文件上传** | 支持多文件、进度回调 |
| **文件下载** | 支持断点续传、后台下载 |
| **请求管理** | 取消、暂停、继续请求 |
| **缓存策略** | 支持NSURLCache |
| **安全认证** | HTTPS证书校验、身份认证 |
| **请求重试** | 自动重试失败请求 |

## 【场景题】
**题目：** 如何使用AFNetworking上传图片？

**答案：**

```objective-c
AFHTTPSessionManager *manager = [AFHTTPSessionManager manager];
manager.responseSerializer = [AFHTTPResponseSerializer serializer];

NSData *imageData = UIImageJPEGRepresentation(image, 0.8);

[manager POST:@"https://api.example.com/upload" 
    parameters:nil 
constructingBodyWithBlock:^(id<AFMultipartFormData> formData) {
    [formData appendPartWithFileData:imageData 
                                name:@"image" 
                            fileName:@"photo.jpg" 
                            mimeType:@"image/jpeg"];
} progress:^(NSProgress *uploadProgress) {
    NSLog(@"上传进度: %.2f%%", uploadProgress.fractionCompleted * 100);
} success:^(NSURLSessionDataTask *task, id responseObject) {
    NSLog(@"上传成功");
} failure:^(NSURLSessionDataTask *task, NSError *error) {
    NSLog(@"上传失败: %@", error);
}];
```

## 【代码示例】
```objective-c
// 1. 基础GET请求
AFHTTPSessionManager *manager = [AFHTTPSessionManager manager];
[manager GET:@"https://api.example.com/users" 
    parameters:@{@"page": @"1"} 
    progress:nil 
    success:^(NSURLSessionDataTask *task, id responseObject) {
    NSLog(@"GET成功: %@", responseObject);
} failure:^(NSURLSessionDataTask *task, NSError *error) {
    NSLog(@"GET失败: %@", error);
}];

// 2. 基础POST请求
[manager POST:@"https://api.example.com/login" 
    parameters:@{@"username": @"abc", @"password": @"123"} 
    progress:nil 
    success:^(NSURLSessionDataTask *task, id responseObject) {
    NSLog(@"POST成功: %@", responseObject);
} failure:^(NSURLSessionDataTask *task, NSError *error) {
    NSLog(@"POST失败: %@", error);
}];

// 3. 自定义Header
[manager.requestSerializer setValue:@"Bearer token" 
    forHTTPHeaderField:@"Authorization"];
[manager.requestSerializer setValue:@"MyApp/1.0" 
    forHTTPHeaderField:@"User-Agent"];

// 4. 自定义超时时间
manager.requestSerializer.timeoutInterval = 30;

// 5. 文件下载
NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"https://example.com/file.zip"]];
NSURLSessionDownloadTask *downloadTask = [manager downloadTaskWithRequest:request 
    progress:^(NSProgress *downloadProgress) {
    NSLog(@"下载进度: %.2f%%", downloadProgress.fractionCompleted * 100);
} destination:^NSURL *(NSURL *targetPath, NSURLResponse *response) {
    NSString *documentsPath = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0];
    NSString *filePath = [documentsPath stringByAppendingPathComponent:@"file.zip"];
    return [NSURL fileURLWithPath:filePath];
} completionHandler:^(NSURLResponse *response, NSURL *filePath, NSError *error) {
    NSLog(@"下载完成: %@", filePath);
}];
[downloadTask resume];

// 6. HTTPS证书校验（禁用校验，仅测试环境）
manager.securityPolicy.allowInvalidCertificates = YES;
manager.securityPolicy.validatesDomainName = NO;

// 7. 取消请求
[manager.tasks makeObjectsPerformSelector:@selector(cancel)];

// 8. 使用AFJSONResponseSerializer
manager.responseSerializer = [AFJSONResponseSerializer serializer];
// 设置可接受的Content-Type
manager.responseSerializer.acceptableContentTypes = [NSSet setWithObjects:@"application/json", @"text/json", @"text/javascript", nil];

// 9. 使用AFImageResponseSerializer（下载图片）
AFHTTPSessionManager *imageManager = [AFHTTPSessionManager manager];
imageManager.responseSerializer = [AFImageResponseSerializer serializer];
[imageManager GET:@"https://example.com/image.jpg" 
    parameters:nil 
    progress:nil 
    success:^(NSURLSessionDataTask *task, UIImage *image) {
    NSLog(@"图片下载成功");
} failure:^(NSURLSessionDataTask *task, NSError *error) {
    NSLog(@"图片下载失败");
}];
```

## 【答题要点】
- AFNetworking基于NSURLSession封装
- 核心组件：AFHTTPSessionManager、AFURLSessionManager
- 请求序列化：AFHTTPRequestSerializer负责参数编码
- 响应序列化：AFJSONResponseSerializer、AFXMLParserResponseSerializer等
- 支持文件上传、下载、进度回调
- 支持HTTPS安全认证
- 支持请求重试机制
- AFNetworking 3.0开始基于NSURLSession，废弃NSURLConnection
- 常用方法：GET、POST、PUT、DELETE、PATCH
- 支持取消单个请求或所有请求
