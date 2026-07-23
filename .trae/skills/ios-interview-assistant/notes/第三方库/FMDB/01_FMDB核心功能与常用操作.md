# FMDB

## 【理论题】
**题目：** 请简述FMDB的作用和常用操作？
**答案：**

**FMDB的作用：**
> FMDB是SQLite数据库的Objective-C封装库，简化了SQLite的使用，提供面向对象的API。

**FMDB核心类：**

| 类名 | 作用 |
|------|------|
| **FMDatabase** | 数据库连接，执行SQL语句 |
| **FMResultSet** | 查询结果集 |
| **FMDatabaseQueue** | 线程安全的数据库操作队列 |

**常用操作：**

| 操作 | 方法 |
|------|------|
| **打开数据库** | `[db open]` |
| **关闭数据库** | `[db close]` |
| **执行SQL** | `[db executeUpdate:@"INSERT INTO..."]` |
| **查询数据** | `[db executeQuery:@"SELECT * FROM..."]` |
| **事务** | `[db beginTransaction]` / `[db commit]` / `[db rollback]` |

**事务说明：**

```
事务 = 一组不可分割的数据库操作

┌─────────────────────────────────────────────────────┐
│              事务的ACID特性                           │
│                                                     │
│  A - Atomic（原子性）                                │
│      事务中的操作要么全部成功，要么全部失败回滚          │
│                                                     │
│  C - Consistent（一致性）                            │
│      事务前后数据库状态保持一致                        │
│                                                     │
│  I - Isolation（隔离性）                             │
│      多个事务之间相互隔离，互不影响                     │
│                                                     │
│  D - Durable（持久性）                               │
│      事务提交后，数据永久保存                          │
└─────────────────────────────────────────────────────┘
```

**事务使用场景：**
- 批量插入/更新数据，需要保证全部成功或全部失败
- 转账操作：扣款和收款必须同时成功
- 订单创建：创建订单和扣减库存必须同时成功

## 【场景题】
**题目：** 如何保证数据库操作的线程安全？

**答案：**

```objective-c
// 使用FMDatabaseQueue（线程安全）
FMDatabaseQueue *queue = [FMDatabaseQueue databaseQueueWithPath:path];

[queue inDatabase:^(FMDatabase *db) {
    [db executeUpdate:@"INSERT INTO users (name) VALUES (?)", @"张三"];
}];

// 使用事务
[queue inTransaction:^(FMDatabase *db, BOOL *rollback) {
    [db executeUpdate:@"INSERT INTO users (name) VALUES (?)", @"张三"];
    [db executeUpdate:@"INSERT INTO users (name) VALUES (?)", @"李四"];
    
    if (error) {
        *rollback = YES;  // 回滚事务
        return;
    }
}];
```

## 【代码示例】
```objective-c
// 1. 获取数据库路径
NSString *docsPath = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES)[0];
NSString *dbPath = [docsPath stringByAppendingPathComponent:@"mydb.sqlite"];

// 2. 创建数据库
FMDatabase *db = [FMDatabase databaseWithPath:dbPath];
if (![db open]) {
    NSLog(@"数据库打开失败");
    return;
}

// 3. 创建表
NSString *createSQL = @"CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)";
if (![db executeUpdate:createSQL]) {
    NSLog(@"创建表失败: %@", [db lastError]);
}

// 4. 插入数据
BOOL success = [db executeUpdate:@"INSERT INTO users (name, age) VALUES (?, ?)", @"张三", @25];
if (success) {
    NSLog(@"插入成功，ID: %lld", [db lastInsertRowId]);
}

// 5. 更新数据
[db executeUpdate:@"UPDATE users SET age = ? WHERE name = ?", @26, @"张三"];

// 6. 删除数据
[db executeUpdate:@"DELETE FROM users WHERE name = ?", @"张三"];

// 7. 查询数据
FMResultSet *rs = [db executeQuery:@"SELECT * FROM users"];
while ([rs next]) {
    NSInteger userId = [rs intForColumn:@"id"];
    NSString *name = [rs stringForColumn:@"name"];
    NSInteger age = [rs intForColumn:@"age"];
    NSLog(@"用户: %d, %@, %d", userId, name, age);
}
[rs close];

// 8. 事务操作
[db beginTransaction];
@try {
    [db executeUpdate:@"INSERT INTO users (name, age) VALUES (?, ?)", @"李四", @30];
    [db executeUpdate:@"INSERT INTO users (name, age) VALUES (?, ?)", @"王五", @28];
    [db commit];
    NSLog(@"事务提交成功");
}
@catch (NSException *exception) {
    [db rollback];
    NSLog(@"事务回滚: %@", exception);
}

// 9. 线程安全操作（推荐使用FMDatabaseQueue）
FMDatabaseQueue *queue = [FMDatabaseQueue databaseQueueWithPath:dbPath];

// 普通操作
[queue inDatabase:^(FMDatabase *db) {
    [db executeUpdate:@"INSERT INTO users (name) VALUES (?)", @"赵六"];
}];

// 事务操作
[queue inTransaction:^(FMDatabase *db, BOOL *rollback) {
    [db executeUpdate:@"INSERT INTO users (name) VALUES (?)", @"钱七"];
    
    if (someError) {
        *rollback = YES;
        return;
    }
}];

// 10. 查询操作
[queue inDatabase:^(FMDatabase *db) {
    FMResultSet *rs = [db executeQuery:@"SELECT * FROM users"];
    while ([rs next]) {
        NSLog(@"用户: %@", [rs stringForColumn:@"name"]);
    }
    [rs close];
}];

// 11. 关闭数据库
[db close];
```

## 【答题要点】
- FMDB是SQLite的Objective-C封装库
- 核心类：FMDatabase、FMResultSet、FMDatabaseQueue
- FMDatabaseQueue保证线程安全
- 使用executeUpdate执行增删改操作
- 使用executeQuery执行查询操作
- 使用事务保证数据一致性
- 查询结果通过FMResultSet遍历
- lastInsertRowId获取插入数据的ID
- lastError获取错误信息
- 推荐使用FMDatabaseQueue而非直接使用FMDatabase
- 数据库文件存储在Documents目录
