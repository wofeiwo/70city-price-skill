# 快速开始 | Getting Started

本指南将帮助你在5分钟内上手70城房价数据工具。

## 环境要求

- Python 3.8 或更高版本
- 稳定的网络连接
- 约10MB磁盘空间

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- pandas - 数据处理
- matplotlib - 图表生成
- requests - 网络请求
- beautifulsoup4 - HTML解析

### 2. 验证安装

```bash
python scripts/update_price.py
```

## 快速示例

### 示例1：更新数据

```bash
python scripts/update_price.py
```

### 示例2：查询数据

```bash
python scripts/extract_price.py month 202401 202412
python scripts/extract_price.py city 北京 上海
```

### 示例3：生成图表

```bash
python scripts/generate_chart.py --cities 北京 上海 --start 202001 --end 202412
```

### 示例4：年度趋势汇总

```bash
python scripts/yearly_trend.py --cities 北京 上海 广州 深圳 --start 2016 --end 2025
```

### 示例5：一键分析

```bash
python scripts/quick_analysis.py --cities 北京 上海 广州 深圳
```

## 下一步

1. 用户手册 - 了解所有命令的详细用法
2. 示例集合 - 学习更多实际用例
3. 数据参考 - 理解数据结构

祝你使用愉快！
