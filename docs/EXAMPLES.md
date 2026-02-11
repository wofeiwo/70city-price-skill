# 示例集合 | Examples

本文档提供20+实际使用示例。

## 📈 典型案例：北上广深十年房价趋势分析

### 案例背景
分析北京、上海、广州、深圳四个一线城市2016-2025年新建商品住宅价格同比指数的十年变化趋势。

### 命令
```bash
python scripts/yearly_trend.py --cities 北京 上海 广州 深圳 --start 2016 --end 2025 --fixedbase 同比
```

### 输出效果

![Beijing Shanghai Guangzhou Shenzhen 10-Year Trend](./assets/yearly_trend_preview.png)

**年度平均同比指数汇总：**

| 年份 | 北京 | 上海 | 广州 | 深圳 |
|------|------|------|------|------|
| 2016 | 122.8 | 132.8 | 119.1 | 144.6 |
| 2017 | 110.9 | 110.2 | 115.7 | 103.4 |
| 2018 | 100.2 | 99.8 | 103.0 | 98.8 |
| 2019 | 104.0 | 102.0 | 109.9 | 101.4 |
| 2020 | 103.5 | 103.6 | 102.2 | 105.0 |
| 2021 | 104.5 | 104.5 | 108.6 | 103.6 |
| 2022 | 105.8 | 103.8 | 101.4 | 102.4 |
| 2023 | 103.5 | 104.4 | 98.8 | 97.7 |
| 2024 | 97.6 | 104.6 | 91.8 | 93.1 |
| 2025 | 96.1 | 105.7 | 94.4 | 96.8 |

### 关键洞察
- **深圳**：2016年达到峰值（144.6），之后持续调整
- **上海**：最为稳健，2025年仍保持105.7的增长
- **北京/广州**：自2023年起进入调整期
- **2024-2025**：多数城市低于100基准线，显示价格回调

## 基础查询

### 1. 查询单个城市

```bash
python scripts/extract_price.py city 北京
```

### 2. 查询多个城市

```bash
python scripts/extract_price.py city 北京 上海 广州 深圳
```

### 3. 按时间范围查询

```bash
python scripts/extract_price.py month 202401 202412
```

### 4. 导出到文件

```bash
python scripts/extract_price.py month 202401 202412 -o 2024_data.csv
```

## 进阶用法

### 5. 城市对比分析

```bash
python scripts/extract_price.py filter --cities 北京 上海 --start 202401 --end 202412 -o comparison.csv
```

### 6. 生成趋势图

```bash
python scripts/generate_chart.py --cities 北京 上海 --start 202001 --end 202412 -o trend.png
```

### 7. 批量导出

```bash
for city in 北京 上海 广州 深圳; do
    python scripts/extract_price.py city $city -o ${city}_data.csv
done
```

## 自然语言示例

### 8. 更新数据

```bash
python scripts/update_price.py
```

### 9. 查询北京房价

```bash
python scripts/extract_price.py city 北京
```

### 10. 生成趋势图

```bash
python scripts/generate_chart.py --cities 北京
```

### 11. 一键分析

```bash
python scripts/quick_analysis.py --cities 北京 上海
```

### 12. 年度趋势汇总

```bash
python scripts/yearly_trend.py --cities 北京 上海 广州 深圳 --start 2016 --end 2025
```

## 完整工作流

### 新数据发布后

```bash
# 1. 更新数据
python scripts/update_price.py

# 2. 生成图表
python scripts/generate_chart.py --cities 北京 上海 --start 202301 --end 202412 -o latest.png

# 3. 导出数据
python scripts/extract_price.py month 202401 202412 -o data_2024.csv
```

## 常见组合

| 需求 | 命令组合 |
|------|---------|
| 城市近N年趋势 | extract + generate_chart |
| 月度数据对比 | extract month + generate_chart --type bar |
| **年度趋势汇总** | **yearly_trend.py** |

## 更多示例

### 13. 生成月度趋势折线图

```bash
python scripts/generate_chart.py --cities 北京 上海 广州 深圳 --start 202001 --end 202412 --type line
```

### 14. 生成城市对比柱状图

```bash
python scripts/generate_chart.py --cities 北京 上海 广州 深圳 --type bar --fixedbase 同比
```

### 15. 查看可用城市列表

```bash
python scripts/extract_price.py list-cities
```

### 16. 查看数据时间范围

```bash
python scripts/extract_price.py list-dates
```

### 17. 按特定指数类型提取

```bash
python scripts/extract_price.py city 北京 上海 --fixedbase 环比
```

### 18. 一键完整分析

```bash
python scripts/quick_analysis.py --cities 北京 上海 广州 深圳 --start 201601 --end 202512
```

### 19. 导出为Excel格式

```bash
python scripts/extract_price.py city 北京 上海 广州 深圳 -o cities.xlsx
```

### 20. 导出为JSON格式

```bash
python scripts/extract_price.py month 202401 202412 -o data.json
```

## 高级用法

### 自定义图表尺寸

```bash
python scripts/generate_chart.py --cities 北京 --start 202001 --end 202412 --width 16 --height 9 --dpi 200
```

### 跳过图表生成（仅分析）

```bash
python scripts/quick_analysis.py --cities 北京 上海 --skip-charts
```

### 指定输出目录

```bash
python scripts/quick_analysis.py --cities 北京 上海 --output ./my_analysis
```

---

如需更多帮助，请查看用户手册或FAQ。
