# iOS Objective-C 面试助手 - 简化方案

## 一、需求分析

### 用户核心需求
1. **iOS Objective-C核心面试题与高频考点**：通过对话直接提供
2. **知识图谱系统**：记录在本地文件中，支持"点亮"标记和掌握程度查询
3. **交互式面试模拟**：用户随时请求出题，我进行打分和点评

### 用户明确要求
- ❌ 不需要实现网页或复杂的Skill工程
- ❌ 不需要创建对话窗口功能
- ✅ 通过Trae对话窗口直接交互
- ✅ 知识图谱和进度记录在一个本地文件中

---

## 二、简化方案

### 2.1 文件结构
```
.trae/skills/ios-interview-assistant/
└── progress.json              # 知识图谱 + 掌握程度记录
```

### 2.2 数据结构 (progress.json)
```json
{
  "knowledge_graph": {
    "Objective-C语法": {
      "mastery": 0.0,
      "topics": {
        "@property属性": { "mastery": 0.0, "status": "pending" },
        "atomic与nonatomic": { "mastery": 0.0, "status": "pending" },
        "Block与循环引用": { "mastery": 0.0, "status": "pending" },
        "分类与扩展": { "mastery": 0.0, "status": "pending" },
        "协议与代理": { "mastery": 0.0, "status": "pending" },
        "消息机制": { "mastery": 0.0, "status": "pending" }
      }
    },
    "Runtime": { ... },
    "内存管理": { ... },
    "多线程": { ... },
    "UIKit": { ... },
    "设计模式": { ... },
    "网络编程": { ... },
    "性能优化": { ... },
    "底层原理": { ... },
    "架构设计": { ... }
  },
  "wrong_questions": [],
  "total_answered": 0,
  "total_correct": 0
}
```

---

## 三、知识点覆盖范围

### 核心知识体系（10大模块，50+知识点）

| 模块 | 知识点 | 高频考点 |
|------|--------|----------|
| **Objective-C语法** | @property、atomic/nonatomic、Block、分类、协议、消息机制 | @property完整写法、Block循环引用、消息发送流程 |
| **Runtime** | 消息转发、动态方法解析、关联对象、Method Swizzling | 消息转发三阶段、Method Swizzling应用场景 |
| **内存管理** | ARC/MRC、引用计数、AutoreleasePool、weak原理 | 引用计数机制、weak底层实现、循环引用解决 |
| **多线程** | GCD、NSOperation、线程安全、各种锁 | GCD队列类型、死锁场景、锁的性能对比 |
| **UIKit** | 视图层级、AutoLayout、事件响应链、TableView | 事件响应链、TableView性能优化、Cell复用原理 |
| **设计模式** | MVC/MVVM、单例、代理、观察者、工厂模式 | MVC vs MVVM、单例线程安全实现 |
| **网络编程** | HTTP/HTTPS、NSURLSession、缓存策略 | HTTPS原理、缓存机制、网络层封装 |
| **性能优化** | 启动优化、内存优化、卡顿优化 | 启动时间优化、内存泄漏检测、卡顿监控 |
| **底层原理** | 类结构、对象内存布局、KVO/KVC、RunLoop | KVO实现原理、RunLoop机制、对象内存布局 |
| **架构设计** | 模块化、组件化、路由设计 | 组件化方案、路由设计、解耦策略 |

---

## 四、交互方式

### 4.1 用户可用命令
- **查看知识图谱**：输入"查看图谱"或"查看进度"
- **点亮知识点**：输入"点亮 [知识点名称]"
- **请求出题**：输入"出题"或"出一道 [模块名] 的题"
- **查看错题本**：输入"查看错题"或"复习错题"
- **查看统计**：输入"查看统计"

### 4.2 答题流程
```
用户: "出题"
我: 给出面试题（包含难度、类型）
用户: 回答内容
我: 评分 + 点评 + 标准答案 + 更新掌握程度
```

---

## 五、实施步骤

### Step 1：创建进度文件
创建 `progress.json`，包含完整的知识图谱结构

### Step 2：准备题库
整理100+道精选面试题（概念题+场景题+代码题）

### Step 3：开始服务
用户可以直接通过对话窗口使用各项功能

---

## 六、预期成果

- ✅ 本地进度文件 `progress.json`（知识图谱 + 掌握程度）
- ✅ 支持对话交互的面试指导服务
- ✅ 100+道精选面试题
- ✅ 答题评分和点评功能
- ✅ 错题本功能
