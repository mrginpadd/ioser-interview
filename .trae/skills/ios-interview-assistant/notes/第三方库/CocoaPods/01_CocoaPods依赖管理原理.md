# CocoaPods依赖管理工具

## 【理论题】
**题目：** 请简述CocoaPods的作用和工作原理？
**答案：**

**CocoaPods的作用：**
> CocoaPods是iOS的依赖管理工具，用于统一管理第三方库的安装、版本和更新。

**工作原理：**

```
┌─────────────────────────────────────────────────────┐
│              CocoaPods工作流程                        │
│                                                     │
│  1. Podfile（声明依赖）                               │
│     pod 'AFNetworking', '~> 3.0'                    │
│         │                                           │
│         ▼                                           │
│  2. pod install（解析依赖）                           │
│     - 下载库到Pods目录                                │
│     - 生成Podfile.lock（锁定版本）                    │
│     - 创建workspace                                  │
│         │                                           │
│         ▼                                           │
│  3. Pods.xcodeproj（编译库）                         │
│     - 所有依赖库编译为静态库/动态库                     │
│         │                                           │
│         ▼                                           │
│  4. AppDelegate + Pod导入                           │
│     #import <AFNetworking/AFNetworking.h>           │
└─────────────────────────────────────────────────────┘
```

**常用命令对比：**

| 命令 | 作用 |
|------|------|
| `pod install` | 安装Podfile中的库，生成workspace |
| `pod update` | 更新库到最新版本，更新Podfile.lock |
| `pod install --no-repo-update` | 跳过仓库更新，加快安装 |
| `pod search` | 搜索可用的库 |
| `pod repo update` | 更新本地仓库索引 |

## 【场景题】
**题目：** pod install和pod update的区别？

**答案：**

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `pod install` | 按Podfile.lock锁定的版本安装 | 团队协作、新增库 |
| `pod update` | 忽略lock文件，更新到最新版本 | 需要升级库版本 |

**团队协作规则：**
- 提交Podfile和Podfile.lock到Git
- 不提交Pods目录
- 拉取代码后执行`pod install`

## 【代码示例】
```ruby
# Podfile示例

platform :ios, '13.0'
use_frameworks!

target 'MyApp' do
  # 网络请求
  pod 'AFNetworking', '~> 3.0'
  
  # 图片加载
  pod 'SDWebImage', '~> 5.0'
  
  # 数据库
  pod 'FMDB'
  
  # 刷新控件
  pod 'MJRefresh'
  
  # JSON转Model
  pod 'YYModel'
  
  # 布局
  pod 'Masonry'
  
  target 'MyAppTests' do
    inherit! :search_paths
    pod 'Quick'
    pod 'Nimble'
  end
end

# 版本控制符号说明
# '~> 3.0' = 3.x 最新版本（不包含4.0）
# '~> 3.2.1' = 3.2.x 最新版本（不包含3.3）
# '3.0' = 精确版本3.0
# '> 3.0' = 大于3.0的任何版本
```

## 【答题要点】
- CocoaPods是iOS依赖管理工具
- 通过Podfile声明依赖库
- pod install安装，pod update更新
- Podfile.lock锁定版本，保证团队版本一致
- 生成workspace（.xcworkspace）管理项目
- Pods目录不需要提交到Git
- 常用版本控制符号：~>、>、>=、精确版本
- use_frameworks!使用动态库，不写使用静态库
