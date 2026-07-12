# HTTP与HTTPS

## 【理论题】
**题目：** 请解释HTTP和HTTPS的区别，以及HTTPS是如何保证安全的？
**答案：**

**HTTP与HTTPS的区别：**

```
HTTP vs HTTPS：
┌─────────────────────────────────────────────────────┐
│ HTTP：明文传输，不安全                                │
│ 端口：80                                            │
│ 数据：明文，可被中间人窃取、篡改                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ HTTPS：加密传输，安全                                │
│ 端口：443                                           │
│ 数据：加密，需要SSL/TLS证书                           │
│ 额外开销：握手过程、加密解密                          │
└─────────────────────────────────────────────────────┘
```

**HTTP工作流程：**

```
HTTP请求过程：
┌─────────────────────────────────────────────────────┐
│ 1. 客户端建立TCP连接（三次握手）                        │
│ 2. 客户端发送HTTP请求（方法、路径、头部、正文）          │
│ 3. 服务器处理请求，返回HTTP响应（状态码、头部、正文）     │
│ 4. 客户端接收响应，处理数据                            │
│ 5. 可选：关闭TCP连接                                  │
└─────────────────────────────────────────────────────┘
```

**HTTPS工作流程：**

```
HTTPS握手过程：
┌─────────────────────────────────────────────────────┐
│ 1. 客户端建立TCP连接（三次握手） ← 同HTTP步骤1        │
│                                                    │
│ 【以下为HTTPS额外步骤（SSL/TLS握手）】                │
│ 2. 客户端发送支持的加密套件列表                        │
│ 3. 服务器返回SSL证书（包含公钥）        
               │
│ 4. 客户端验证证书有效性                               │
│ 5. 客户端生成随机密钥，用服务器公钥加密后发送      
      │
│ 6. 服务器用私钥解密，获取随机密钥                      │
│ 7. 双方用随机密钥进行对称加密通信                      │
│                                                    │
│ 【以下同HTTP，但数据经过加密】                        │
│ 8. 客户端用随机密钥加密HTTP请求，发送给服务器 ← 同HTTP步骤2 │
│ 9. 服务器用随机密钥解密请求，处理后加密响应 ← 同HTTP步骤3  │
│ 10. 客户端用随机密钥解密响应，处理数据 ← 同HTTP步骤4      │
└─────────────────────────────────────────────────────┘
```

**HTTP与HTTPS工作流程对比：**

| 步骤 | HTTP | HTTPS |
|------|------|-------|
| 1 | TCP三次握手 | TCP三次握手 |
| 2 | 发送HTTP请求 | 发送加密套件列表 |
| 3 | 服务器返回响应 | 服务器返回证书 |
| 4 | 处理响应 | 验证证书 |
| 5 | - | 密钥协商 |
| 6 | - | 对称加密通信 |
| 7 | - | 发送加密的HTTP请求 |
| 8 | - | 返回加密的HTTP响应 |

**核心区别：**

| 特性 | HTTP | HTTPS |
|------|------|-------|
| **端口** | 80 | 443 |
| **加密** | 明文 | SSL/TLS加密 |
| **证书** | 不需要 | 需要CA证书 |
| **安全性** | 低（可被窃取、篡改） | 高（防窃听、防篡改、防伪造） |
| **性能** | 快（无加密开销） | 略慢（握手+加密） |
| **SEO** | 无特殊优势 | 搜索引擎优先收录 |

**HTTPS如何保证安全：**

1. **数据加密**：通过SSL/TLS加密传输，防窃听
2. **身份认证**：通过CA证书验证服务器身份，防伪造
3. **完整性校验**：通过消息认证码（MAC）防止数据篡改

## 【场景题】
**题目：** 在iOS开发中，如何配置HTTPS请求？需要注意什么？

**答案：**

```objective-c
// iOS中配置HTTPS请求
@interface NetworkManager : NSObject
@end

@implementation NetworkManager

+ (void)requestWithURL:(NSString *)urlString {
    NSURL *url = [NSURL URLWithString:urlString];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    
    NSURLSessionDataTask *task = [[NSURLSession sharedSession] 
        dataTaskWithRequest:request 
        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
            if (!error) {
                // 处理响应数据
            }
        }];
    
    [task resume];
}

@end
```

**注意事项：**

| 事项 | 说明 |
|------|------|
| **ATS配置** | iOS 9+默认强制HTTPS，需在Info.plist配置NSAppTransportSecurity |
| **证书验证** | 默认验证服务器证书，可通过NSURLSessionDelegate自定义验证 |
| **证书类型** | 推荐使用EV SSL证书（绿色地址栏） |
| **证书过期** | 定期更新证书，避免请求失败 |

## 【代码示例】
```objective-c
// 1. 基本HTTPS请求
NSURL *url = [NSURL URLWithString:@"https://api.example.com/data"];
NSURLRequest *request = [NSURLRequest requestWithURL:url];

NSURLSessionDataTask *task = [[NSURLSession sharedSession]
    dataTaskWithRequest:request
    completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error) {
            NSLog(@"HTTPS请求失败: %@", error);
            return;
        }
        NSError *jsonError;
        NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data 
                                                             options:0 
                                                               error:&jsonError];
        NSLog(@"响应数据: %@", json);
    }];

[task resume];

// 2. ATS配置（Info.plist）
// <key>NSAppTransportSecurity</key>
// <dict>
//     <key>NSAllowsArbitraryLoads</key>
//     <false/>
//     <key>NSExceptionDomains</key>
//     <dict>
//         <key>example.com</key>
//         <dict>
//             <key>NSIncludesSubdomains</key>
//             <true/>
//             <key>NSExceptionAllowsInsecureHTTPLoads</key>
//             <false/>
//         </dict>
//     </dict>
// </dict>
```

## 【答题要点】
- HTTP是明文传输，HTTPS是加密传输
- HTTPS端口443，HTTP端口80
- HTTPS需要SSL/TLS证书
- HTTPS握手过程：证书交换→密钥协商→对称加密通信
- HTTPS保证安全的三个方面：数据加密、身份认证、完整性校验
- iOS开发中需配置ATS（App Transport Security）
- 默认验证服务器证书，可自定义验证逻辑
