# Eepsite主动探测系统

主要目标是从floodfill节点中获取LeaseSets信息，将这个信息转换为域名，最后存到数据库中

大致的流程是

i2pd结点（生产者）--LeaseSets信息--> 后端代码（消费者）--域名--> 数据库

## mysql数据库字段

| 字段 | 含义 | 类型 |
| --- | --- | --- |
| id | 递增 | INT |
| domain | 域名 | VARCHAR(128) |
| fftime | 首次发现时间 | DATETIME |
| storage_typeupdatetime | 更新时间 | DATETIME |