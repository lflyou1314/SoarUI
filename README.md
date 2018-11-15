# **[SoarUI](https://github.com/lflyou1314/SoarUI)**
* [SOAR](https://github.com/xiaomi/soar)(SQL Optimizer And Rewriter)是一个对SQL进行优化和改写的自动化工具。
* [SoarUI](http://soarui.xxx.xhceis.cn)(An open source user interface for SOAR)
-------
## 语法检查工具

```bash
$ echo "select * from tb" | soar -only-syntax-check
$ echo $?
0

$ echo "select * fromtb" | soar -only-syntax-check
At SQL 0 : syntax error at position 16 near 'fromtb'
$ echo $?
1
```

## SQL指纹
```bash
$ echo "select * from film where col='abc'" | soar -report-type=fingerprint
$ select * from film where col=?
```

## 合并多条ALTER语句

```bash
$ echo "alter table tb add column a int; alter table tb add column b int;" | soar -report-type rewrite -rewrite-rules mergealter
$ ALTER TABLE `tb` add column a int, add column b int ;
```

## SQL美化
```bash
$ echo "select * from tbl where col = 'val'" | ./soar -report-type=pretty
$ SELECT
    *
  FROM
    tbl
  WHERE
    col  = 'val';
```

## EXPLAIN信息分析报告
```bash
$ soar -report-type explain-digest << EOF
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
|  1 | SIMPLE      | film  | ALL  | NULL          | NULL | NULL    | NULL | 1131 |       |
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
EOF
```
```text
##  Explain信息

| id | select\_type | table | partitions | type | possible_keys | key | key\_len | ref | rows | filtered | scalability | Extra |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1  | SIMPLE | *film* | NULL | ALL | NULL | NULL | NULL | NULL | 0 | 0.00% | ☠️ **O(n)** |  |

### Explain信息解读

#### SelectType信息解读

* **SIMPLE**: 简单SELECT(不使用UNION或子查询等).

#### Type信息解读

* ☠️ **ALL**: 最坏的情况, 从头到尾全表扫描.
```
## SQL评分

不同类型的建议指定的Severity不同，严重程度数字由低到高依次排序。满分100分，扣到0分为止。L0不扣分只给出建议，L1扣5分，L2扣10分，每级多扣5分以此类推。当由时给出L1, L2两要建议时扣分叠加，即扣15分。

注意：目前只有`markdown`和`html`两种`-report-type`支持评分输出显示，其他输出格式如有评分需求可以按上述规则自行计算。

### 命令行参数配置DSN

> 账号密码中如包含特殊符号(如：'@',':','/'等)可在配置文件中设置，存在特殊字符的情况不适合在命令行中使用。目前`soar`只支持tcp协议的MySQL数据库连接方式，如需要配置本机MySQL环境建议将`localhost`修改为'127.0.0.1'，并检查对应的'user'@'127.0.0.1'账号是否存在。

```bash
$ soar -online-dsn "user:password@ip:port/database"

$ soar -test-dsn "user:password@ip:port/database"
```

#### DSN格式支持
* "user:password@127.0.0.1:3307/database"
* "user:password@127.0.0.1:3307"
* "user:password@127.0.0.1:/database"
* "user:password@:3307/database"
* "user:password@"
* "127.0.0.1:3307/database"
* "@127.0.0.1:3307/database"
* "@127.0.0.1"
* "127.0.0.1"
* "@/database"
* "@127.0.0.1:3307"
* "@:3307/database"
* ":3307/database"
* "/database"
-----------------

![SoarUI](https://github.com/lflyou1314/SoarUI/blob/master/images/soarui.png)
