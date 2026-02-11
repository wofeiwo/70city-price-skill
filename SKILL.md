---
name: 70city-price
description: 抓取并提取中国70个大中城市商品住宅销售价格数据，支持自动更新、数据查询、图表生成和一键分析。使用命令如/update-70city-price、/select-city-price、/gen-price-chart，或自然语言如"帮我更新房价数据"、"查询北京近10年房价"、"生成上海房价趋势图"等。
---

# 70城房价数据工具

本Skill提供中国70个大中城市商品住宅销售价格数据的抓取、提取、查询和分析功能。

## 功能特性

| 功能 | 描述 | 命令 |
|-----|------|-----|
| **数据更新** | 从国家统计局抓取最新房价数据（自动默认） | `/update-70city-price` |
| **数据提取** | 按城市、时间、指数类型提取数据 | `/select-city-price` |
| **图表生成** | 生成房价趋势图、对比图 | `/gen-price-chart` |
| **年度汇总** | 生成年度趋势汇总图表 | `/yearly-trend` |
| **一键分析** | 快速生成完整分析报告 | `/quick-select-price` |

## 使用方式

### 自然语言交互

直接用自然语言描述需求：

```
帮我更新房价数据
查询北京近10年房价
上海和广州哪个涨得多？
生成北京房价趋势图
分析广州深圳近5年对比
```

### 命令行调用

| 命令 | 功能 | 示例 |
|-----|------|-----|
| `/update-70city-price` | 更新数据（自动默认） | 直接运行即可自动搜索最新数据 |
| `/select-city-price` | 提取数据 | `/select-city-price --cities 北京 上海 --start 202401 --end 202412` |
| `/gen-price-chart` | 生成图表 | `/gen-price-chart --cities 北京 --type line` |
| `/yearly-trend` | 年度趋势汇总 | `/yearly-trend --cities 北京 上海 广州 深圳 --start 2016 --end 2025` |
| `/quick-select-price` | 一键分析 | `/quick-select-price --cities 北京 上海 --start 202001 --end 202412` |

## 详细用法

### 数据更新 `/update-70city-price`

**功能**：从国家统计局网站抓取最新房价数据

**参数**：
- 无需参数 - 默认自动搜索最新发布页
- `<URL>` - 可选，手动提供国家统计局发布页URL

**示例**：
```bash
# 默认方式（自动搜索最新发布页）
/update-70city-price

# 手动提供URL更新
/update-70city-price "https://www.stats.gov.cn/sj/zxfbhjd/202507/t20250715_1960403.html"
```

### 数据提取 `/select-city-price`

**功能**：按条件提取房价数据

**参数**：
- `--cities` - 城市列表（可多个）
- `--start` - 起始月份（YYYYMM格式）
- `--end` - 结束月份（YYYYMM格式）
- `--fixedbase` - 指数类型（同比/环比/定基比）
- `--output` - 输出文件名
- `--format` - 输出格式（csv/json/excel）

**子命令**：
- `month <start> <end>` - 按月份提取
- `city <城市1> <城市2>` - 按城市提取
- `filter` - 组合条件提取
- `list-cities` - 列出可用城市
- `list-dates` - 列出数据日期范围

**示例**：
```bash
# 按月份提取
/select-city-price month 202401 202412

# 按城市提取
/select-city-price city 北京 上海 广州 深圳

# 组合条件
/select-city-price filter --cities 北京 --start 202401 --end 202412 --fixedbase 同比

# 导出文件
/select-city-price city 成都 --output chengdu.xlsx
```

### 图表生成 `/gen-price-chart`

**功能**：生成房价趋势图表

**参数**：
- `--cities` - 城市列表（必填）
- `--start` - 起始月份
- `--end` - 结束月份
- `--type` - 图表类型（line/bar）
- `--fixedbase` - 指数类型
- `--output` - 输出文件路径
- `--width` - 图表宽度
- `--height` - 图表高度
- `--dpi` - 分辨率

**示例**：
```bash
# 趋势折线图
/gen-price-chart --cities 北京 上海 --start 202001 --end 202412

# 对比柱状图
/gen-price-chart --cities 北京 上海 广州 深圳 --type bar

# 自定义输出
/gen-price-chart --cities 成都 --output chengdu_trend.png --width 16 --height 8
```

### 一键分析 `/quick-select-price`

**功能**：组合提取、图表生成，快速得到分析结果

**参数**：
- `--cities` - 城市列表（必填）
- `--start` - 起始月份
- `--end` - 结束月份
- `--output` - 输出目录
- `--skip-charts` - 跳过图表生成

**示例**：
```bash
# 快速分析
/quick-select-price --cities 北京 上海

# 指定时间范围
/quick-select-price --cities 广州 深圳 --start 202001 --end 202412

# 只生成数据
/quick-select-price --cities 成都 --skip-charts
```

### 年度汇总 `/yearly-trend`

**功能**：生成年度平均房价趋势汇总图表，适合多年对比分析

**参数**：
- `--cities` - 城市列表（必填）
- `--start` - 起始年份
- `--end` - 结束年份
- `--fixedbase` - 指数类型（同比/环比/定基比）
- `--output` - 输出文件路径
- `--width` - 图表宽度
- `--height` - 图表高度
- `--dpi` - 分辨率

**示例**：
```bash
# 北上广深十年趋势
/yearly-trend --cities 北京 上海 广州 深圳 --start 2016 --end 2025

# 自定义输出
/yearly-trend --cities 北京 --start 2020 --end 2025 --output trend.png
```

## 数据说明

### 覆盖范围

- **城市数量**：70个大中城市
- **时间跨度**：2006年1月至今
- **更新频率**：每月15-17日更新上月数据
- **指数类型**：环比、同比、定基比

### 70城构成

| 类别 | 数量 | 包括 |
|-----|------|-----|
| 直辖市/省会 | 35 | 北京、上海、广州、深圳、重庆、成都、武汉、西安等 |
| 其他城市 | 35 | 唐山、秦皇岛、包头、烟台、洛阳、襄阳等 |

### 指数说明

| 指数 | 含义 | 解读 |
|-----|------|-----|
| **同比** | 与上年同月相比 | >100=上涨，<100=下跌 |
| **环比** | 与上月相比 | >100=上涨，<100=下跌 |
| **定基比** | 与固定基期相比 | 注意基期轮换问题 |

## 自然语言映射表

| 自然语言 | 解析结果 |
|---------|---------|
| "更新数据" | `/update-70city-price`（自动） |
| "更新房价" | `/update-70city-price`（自动） |
| "查询北京" | `/select-city-price --cities 北京` |
| "北京近10年" | `/select-city-price --cities 北京 --start 201501 --end 202412` |
| "房价对比" | `/select-city-price` + `/gen-price-chart --type bar` |
| "生成趋势图" | `/gen-price-chart --type line` |
| "生成年度趋势图" | `/yearly-trend --type line` |
| "十年房价对比" | `/yearly-trend --cities 北京 上海 广州 深圳 --start 2015 --end 2024` |
| "分析房价" | `/quick-select-price` |
| "广州深圳对比" | `/quick-select-price --cities 广州 深圳` |

## 数据来源

数据来源于**中华人民共和国国家统计局**公开发布的《70个大中城市商品住宅销售价格变动情况》。

官方发布页面：https://www.stats.gov.cn/sj/zxfb/

## 相关文档

- [快速开始](../docs/GETTING_STARTED.md) - 5分钟上手指南
- [用户手册](../docs/USER_GUIDE.md) - 完整命令参考
- [示例集合](../docs/EXAMPLES.md) - 20+使用示例
- [数据参考](../docs/DATA_REFERENCE.md) - 数据结构说明
- [常见问题](../docs/FAQ.md) - 常见问题解答

## 常见问题

**Q: 如何更新最新数据？**
A: 直接运行 `/update-70city-price`，无需参数，自动搜索最新发布页。

**Q: 支持导出Excel吗？**
A: 使用 `--output filename.xlsx` 参数即可导出Excel格式。

**Q: 图表显示乱码怎么办？**
A: 确保系统已安装中文字体（思源黑体、微软雅黑等）。

**Q: 城市名称怎么写？**
A: 支持"北京"、"北京市"、"成都市"等多种写法。
