# 部署文档

## 部署步骤

1. 修改`docker-compose.yml`文件，包括以下几个部分：
    1. mysql服务中的密码，数据库名称
    2. mysql服务中映射出来的端口
    3. backend_leaseset服务中挂载的目录，需要将bushu/config目录挂载在/app/config中
2. 修改`config/config.ini`文件，包括以下几个部分：
    1. mysql的password，database
3. 部署docker服务，执行

```bash
docker-compose up -d
```

4. 进入backend_leaseset容器

```bash
docker exec -it backend_leaseset bash
```

5. 执行程序

```bash
cd src
python3 -m active_leaseSet.main.main
```

6. 检验数据库中是否有数据

## 数据库字段

| 字段 | 含义 | 类型 |
| --- | --- | --- |
| id | 递增 | INT |
| domain | 域名 | VARCHAR(128) |
| fftime | 首次发现时间 | DATETIME |
| updatetime | 更新时间 | DATETIME |