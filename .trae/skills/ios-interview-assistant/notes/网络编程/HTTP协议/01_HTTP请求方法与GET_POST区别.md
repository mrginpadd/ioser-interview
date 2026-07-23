# HTTP协议

## 【理论题】
**题目：** 请解释HTTP协议常用的请求方法有哪些？GET和POST的区别？
**答案：**

**HTTP常用请求方法：**

| 方法 | 作用 | 幂等性 | 使用场景 |
|------|------|--------|---------|
| **GET** | 获取资源 | 是 | 查询数据、拉取列表 |
| **POST** | 创建资源 | 否 | 提交表单、上传文件 |
| **PUT** | 完整更新资源 | 是 | 更新整个对象 |
| **PATCH** | 部分更新资源 | 否 | 只改某个字段 |
| **DELETE** | 删除资源 | 是 | 删除数据 |

> 幂等性：多次请求结果相同

**GET和POST区别：**

```
┌─────────────────────────────────────────────────────┐
│  GET                                                │
│  - 参数在URL拼接（?name=abc&age=18）                 │
│  - 明文传输，不安全                                  │
│  - URL长度有限制（浏览器约2KB）                       │
│  - 可被缓存、收藏、历史记录                          │
│  - 幂等（多次请求结果相同）                          │
│  - 只支持ASCII字符                                  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  POST                                               │
│  - 参数在请求体body中                               │
│  - 相对安全（仍可抓包，HTTPS才真正加密）              │
│  - 无大小限制（服务器可配置）                        │
│  - 不可缓存、不可收藏                              │
│  - 非幂等（多次请求可能创建多条数据）                │
│  - 支持二进制数据（文件上传）                        │
└─────────────────────────────────────────────────────┘
```

## 【场景题】
**题目：** 登录功能用GET还是POST？为什么？

**答案：** 用POST。
- 登录需要传输账号密码，GET会把密码拼在URL里（明文，不安全）
- POST放在body中，配合HTTPS加密传输
- 登录是非幂等操作（每次登录可能生成不同token）

## 【代码示例】
```objective-c
// 1. GET请求
NSString *urlStr = @"https://api.example.com/users?name=abc&age=18";
NSURL *url = [NSURL URLWithString:urlStr];
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
request.HTTPMethod = @"GET";

NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithURL:url 
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    NSLog(@"GET响应: %@", [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding]);
}];
[task resume];

// 2. POST请求（提交表单）
NSString *urlStr = @"https://api.example.com/login";
NSURL *url = [NSURL URLWithString:urlStr];
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
request.HTTPMethod = @"POST";
request.HTTPBody = [@"username=abc&password=123456" dataUsingEncoding:NSUTF8StringEncoding];
[request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];

NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithRequest:request 
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
    NSLog(@"POST响应: %@", [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding]);
}];
[task resume];

// 3. POST请求（JSON格式）
NSDictionary *params = @{@"username": @"abc", @"password": @"123456"};
NSData *bodyData = [NSJSONSerialization dataWithJSONObject:params options:0 error:nil];
request.HTTPBody = bodyData;
[request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];

// 4. DELETE请求
request.HTTPMethod = @"DELETE";

// 5. PUT请求
request.HTTPMethod = @"PUT";
request.HTTPBody = [NSJSONSerialization dataWithJSONObject:@{@"name": @"updated"} options:0 error:nil];
```

## 【答题要点】
- HTTP常用方法：GET、POST、PUT、PATCH、DELETE
- GET参数在URL拼接，POST参数在body中
- GET明文不安全，URL长度有限制，幂等
- POST相对安全，无大小限制，非幂等
- GET可缓存，POST不可缓存
- GET只支持ASCII，POST支持二进制数据
- 幂等性：GET、PUT、DELETE是幂等，POST、PATCH非幂等
- 登录、提交表单用POST，查询数据用GET
