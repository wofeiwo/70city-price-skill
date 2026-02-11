# 用户手册 | User Guide

本手册提供所有命令的详细用法说明。

## 命令概述

| 命令 | 功能 |
|------|------|
| /update-70city-price | 更新房价数据（自动默认） |
| /select-city-price | 提取房价数据 |
| /gen-price-chart | 生成房价图表 |
| /yearly-trend | 年度趋势汇总 |
| /quick-select-price | 一键分析 |

## update_price - 更新数据

### 命令语法

```bash
python scripts/update_price.py [URL] [选项]
```

### 参数选项

| 参数 | 说明 |
|------|------|
| URL | 国家统计局发布页URL（可选） |

### 使用示例

```bash
# 自动搜索并更新
python scripts/update_price.py

# 从URL更新
python scripts/update_price.py "https://www.stats.gov.cn/sj/zxfbhjd/..."
```

## extract_price - 提取数据

### 命令语法

```bash
python scripts/extract_price.py month <start> <end> [选项]
python scripts/extract_price.py city <城市1> [城市2] ... [选项]
```

### 使用示例

```bash
# 按月份提取
python scripts/extract_price.py month 202401 202412

# 按城市提取
python scripts/extract_price.py city 北京 上海

# 组合条件
python scripts/extract_price.py filter --cities 北京 --start 202401 --end 202412
```

## generate_chart - 生成图表

### 命令语法

```bash
python scripts/generate_chart.py --cities <城市列表> [选项]
```

### 使用示例

```bash
# 趋势折线图
python scripts/generate_chart.py --cities 北京 上海

# 柱状图
python scripts/generate_chart.py --cities 北京 上海 --type bar
```

## yearly_trend - 年度趋势汇总

### 命令语法

```bash
python scripts/yearly_trend.py --cities <城市列表> [选项]
```

### 使用示例

```bash
# 北上广深十年趋势
python scripts/yearly_trend.py --cities 北京 上海 广州 深圳 --start 2016 --end 2025

# 自定义输出
python scripts/yearly_trend.py --cities 北京 --start 2020 --end 2025 --output trend.png
```

## quick_analysis - 一键分析

```bash
python scripts/quick_analysis.py --cities 北京 上海
```

## 自然语言支持

| 自然语言 | 对应命令 |
|---------|---------|
| 更新房价数据 | /update-70city-price |
| 查询北京房价 | /select-city-price --cities 北京 |
| 生成趋势图 | /gen-price-chart --cities 北京 |

如需更多帮助，请查看示例集合或FAQ。
