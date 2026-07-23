# JSPatch热修复框架

## 【理论题】
**题目：** 请简述JSPatch的作用和工作原理？
**答案：**
 
**JSPatch的作用：** 苹果2017年后禁止使用，了解原理即可
> JSPatch是iOS热修复框架，通过JavaScript调用Objective-C接口，实现动态下发代码修复线上Bug，无需重新发版。

**工作原理：**

```
┌─────────────────────────────────────────────────────┐
│              JSPatch工作流程                          │
│                                                     │
│  1. 服务器下发JS脚本                                   │
│         │                                           │
│         ▼                                           │
│  2. JavaScriptCore解析执行JS                          │
│         │                                           │
│         ▼                                           │
│  3. JS调用OC方法                                      │
│     - 通过runtime消息转发                              │
│     - JS字符串 → SEL → IMP                           │
│         │                                           │
│         ▼                                           │
│  4. 动态替换/新增OC方法                                  │
│     - method swizzling                              │
│     - 动态添加方法                                      │
└─────────────────────────────────────────────────────┘
```

## 【场景题】
**题目：** JSPatch为什么被苹果禁止？

**答案：**

| 原因 | 说明 |
|------|------|
| **违反审核条款** | 3.2.2条款禁止动态下发可执行代码 |
| **安全风险** | JS脚本可能被篡改，存在安全隐患 |
| **绕过审核** | 可动态修改App行为，绕过App Store审核 |
| **替代方案** | 使用苹果官方的bug修复机制 |

## 【代码示例】
```javascript
// 1. JSPatch基础语法
require('UIView')
var view = UIView.alloc().init()
view.setBackgroundColor(UIColor.redColor())

// 2. 替换方法
defineClass('ViewController', {
    viewDidLoad: function() {
        self.super().viewDidLoad()
        // 替换原有逻辑
        var label = UILabel.alloc().initWithFrame({x:0, y:0, width:100, height:30})
        label.setText("热修复后的内容")
        self.view().addSubview(label)
    }
})

// 3. 调用OC方法
defineClass('UserManager', {
    login: function(username, password) {
        if (username === "admin" && password === "123456") {
            return true
        }
        return false
    }
})

// 4. 属性操作
defineClass('UserModel', {
    setName: function(name) {
        self.setValue_forKey(name, "name")
    }
})
```

## 【答题要点】 苹果2017年后禁止使用，了解原理即可
- JSPatch是iOS热修复框架
- 通过JavaScript调用Objective-C接口
- 核心原理：JavaScriptCore + Runtime消息转发 + Method Swizzling
- 用于线上Bug修复，无需重新发版
- 苹果2017年后禁止使用，了解原理即可
- 替代方案：苹果官方的bug修复机制、Wax、AsyncDisplayKit
- 面试一般问原理，了解即可，不需要深入
