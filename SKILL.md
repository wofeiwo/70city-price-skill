---
name: 70city-price
description: 中国70个大中城市商品住宅销售价格数据工具。支持数据更新、提取、图表生成和一键分析。命令：/update-70city-price（更新）、/select-city-price（提取）、/gen-price-chart（图表）、/yearly-trend（年度汇总）、/quick-select-price（一键分析）。
---

# Commands

| Command | Function | Example |
|---------|----------|---------|
| `/update-70city-price` | Fetch latest data from NBS | Run directly |
| `/select-city-price` | Extract data by city/month | `--cities 北京 上海 --start 202401 --end 202412` |
| `/gen-price-chart` | Generate trend/bar charts | `--cities 北京 上海 --type line` |
| `/yearly-trend` | Annual summary charts | `--cities 北京 上海 广州 深圳 --start 2016 --end 2025` |
| `/quick-select-price` | Full analysis | `--cities 北京 上海 --start 202001 --end 202412` |

# Parameters

## Common
- `--cities` - City list (required for most)
- `--start` - Start month/year (YYYYMM or YYYY)
- `--end` - End month/year (YYYYMM or YYYY)
- `--fixedbase` - Index type (同比/环比/定基比)
- `--output` - Output file path

## gen-price-chart only
- `--type` - Chart type (line/bar, default: line)
- `--width` - Chart width (default: 12)
- `--height` - Chart height (default: 6)
- `--dpi` - Resolution (default: 150)

## yearly-trend only
- `--type` - Ignored, always generates summary

# Data

- **Cities**: 70 major Chinese cities
- **Range**: 2006-01 to 2025-12
- **Index**: >100=up, <100=down
- **Source**: stats.gov.cn

# References

- [USER_GUIDE.md](references/USER_GUIDE.md) - Detailed command reference
- [EXAMPLES.md](references/EXAMPLES.md) - Usage examples
- [DATA_SCHEMA.md](references/DATA_SCHEMA.md) - Data structure
- [CITY_LIST.md](references/CITY_LIST.md) - City codes
