# 数据结构说明 | Data Schema

本文档详细说明70城房价数据的CSV结构。

## 文件概述

### 主数据文件

| 文件 | 位置 | 说明 |
|------|------|------|
| 70cityprice.csv | data/70cityprice.csv | 主数据文件 |

### 数据规模

| 指标 | 数值 |
|------|------|
| 总记录数 | 约45,000条 |
| 城市数量 | 70个 |
| 时间跨度 | 2006年1月 - 2025年12月 |

## CSV列定义

### 必需列（16列）

| 列名 | 数据类型 | 说明 |
|------|---------|------|
| DATE | string | 数据日期（YYYY/M/D格式） |
| ADCODE | string | 城市行政区划代码 |
| CITY | string | 城市名称 |
| FixedBase | string | 指数类型 |
| CommodityHouseIDX | float | 新建商品住宅销售价格指数 |
| SecondHandIDX | float | 二手住宅销售价格指数 |
| CommodityBelow90IDX | float | 新建商品住宅90平米以下 |
| Commodity144IDX | float | 新建商品住宅90-144平米 |
| CommodityAbove144IDX | float | 新建商品住宅144平米以上 |
| SecondHandBelow90IDX | float | 二手住宅90平米以下 |
| SecondHand144IDX | float | 二手住宅90-144平米 |
| SecondHandAbove144IDX | float | 二手住宅144平米以上 |

## 数据示例

```csv
DATE,CITY,ADCODE,FixedBase,CommodityHouseIDX,SecondHandIDX
2025/12/1,北京,110100,同比,97.6,91.5
2025/12/1,北京,110100,环比,100.1,99.8
2025/12/1,上海,310100,同比,104.8,93.9
```

## 索引结构

### 复合主键

(DATE, CITY, FixedBase) 组合唯一确定一条记录。

### 月度数据量

每月数据：70城市 × 3指数类型 = 210条记录

## 数据约束

### 约束规则

| 规则 | 说明 |
|------|------|
| 主键唯一 | (DATE, CITY, FixedBase) 必须唯一 |
| DATE格式 | 必须为 YYYY/M/1 |
| FixedBase | 只能是同比/环比/定基比 |
| CITY | 必须在70城列表中 |

### 城市覆盖要求

- 每月城市数：应等于70
- 指数覆盖：应包含同比和环比
