# -*- coding: utf-8 -*-
"""
70城房价数据图表生成工具
"""

import sys
import os
import argparse

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH, OUTPUT_DIR, normalize_city_name, CITY_ADCODE

if HAS_DEPS:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti SC', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False


def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found: {CSV_PATH}")
        sys.exit(1)
    print(f"Reading data file: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, dtype=str)
    return df


def parse_month_arg(month_str):
    month_str = month_str.replace('-', '').replace('/', '')
    if len(month_str) != 6:
        raise ValueError(f"Invalid month format: {month_str}")
    return int(month_str[:4]), int(month_str[4:6])


def filter_data(df, cities, start_month, end_month, fixedbase):
    def date_in_range(date_str):
        try:
            parts = date_str.split('/')
            return (int(parts[0]), int(parts[1]))
        except:
            return None
    
    if start_month:
        sy, sm = parse_month_arg(start_month)
        df = df[df['DATE'].apply(lambda x: date_in_range(x) >= (sy, sm) if date_in_range(x) else False)]
    if end_month:
        ey, em = parse_month_arg(end_month)
        df = df[df['DATE'].apply(lambda x: date_in_range(x) <= (ey, em) if date_in_range(x) else False)]
    
    city_norms = {normalize_city_name(c) for c in cities}
    df = df[df['CITY'].apply(lambda x: normalize_city_name(x) in city_norms)]
    if fixedbase:
        df = df[df['FixedBase'] == fixedbase]
    return df


def create_trend_chart(df, cities, fixedbase, output_path):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    colors = {'北京': '#E53935', '上海': '#1E88E5', '广州': '#43A047', '深圳': '#FB8C00'}
    
    for city in cities:
        city_data = df[df['CITY'] == city].copy()
        city_data = city_data.sort_values('DATE')
        city_data['DATE_PARSED'] = pd.to_datetime(city_data['DATE'], format='%Y/%m/%d')
        color = colors.get(city, plt.cm.tab10(cities.index(city) % 10))
        ax.plot(city_data['DATE_PARSED'], city_data['CommodityHouseIDX'], label=city, linewidth=1.5, color=color)
    
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.set_title(f'新建商品住宅价格指数趋势（{fixedbase}）', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('时间', fontsize=11)
    ax.set_ylabel(f'价格指数', fontsize=11)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    ax.text(0.02, 0.02, '数据来源：国家统计局', transform=ax.transAxes, fontsize=9, color='gray', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')
    print(f'图表已保存至: {output_path}')
    plt.close()


def create_bar_chart(df, cities, fixedbase, output_path):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    latest_date = df['DATE'].max()
    latest_data = df[df['DATE'] == latest_date].copy()
    x, values = range(len(cities)), []
    
    for city in cities:
        cv = latest_data[latest_data['CITY'] == city]
        values.append(float(cv['CommodityHouseIDX'].iloc[0]) if len(cv) > 0 else 0)
    
    colors = ['#E53935' if v < 100 else '#43A047' for v in values]
    ax.bar(x, values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.7, linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(cities, fontsize=11)
    ax.set_ylabel(f'价格指数（{fixedbase}）', fontsize=11)
    ax.set_title(f'70城房价对比（{latest_date}，{fixedbase}）', fontsize=14, fontweight='bold', pad=15)
    for i, val in enumerate(values):
        ax.text(i, val + 0.5, f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    ax.set_ylim(85, max(values) + 5)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')
    print(f'图表已保存至: {output_path}')
    plt.close()


def main():
    if not HAS_DEPS:
        print("ERROR: Missing dependencies. Run: pip install pandas matplotlib")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='70 City House Price Chart Generator')
    parser.add_argument('--cities', '-c', required=True, nargs='+', help='City list')
    parser.add_argument('--start', '-s', help='Start month (YYYYMM)')
    parser.add_argument('--end', '-e', help='End month (YYYYMM)')
    parser.add_argument('--type', '-t', choices=['line', 'bar'], default='line', help='Chart type')
    parser.add_argument('--fixedbase', '-f', default='同比', choices=['同比', '环比', '定基比'], help='Index type')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--width', type=float, default=12)
    parser.add_argument('--height', type=float, default=6)
    parser.add_argument('--dpi', type=int, default=150)
    
    args = parser.parse_args()
    
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found")
        sys.exit(1)
    
    df = load_data()
    cities = []
    for city in args.cities:
        norm = normalize_city_name(city)
        if norm in CITY_ADCODE:
            cities.append(norm)
        else:
            print(f"WARNING: City '{city}' not found")
    
    if not cities:
        print("ERROR: No valid cities specified")
        sys.exit(1)
    
    plt.rcParams['figure.figsize'] = (args.width, args.height)
    plt.rcParams['figure.dpi'] = args.dpi
    
    df_filtered = filter_data(df, cities, args.start, args.end, args.fixedbase)
    print(f"Filtered records: {len(df_filtered)}")
    
    if len(df_filtered) == 0:
        print("ERROR: No data found matching criteria")
        sys.exit(1)
    
    if args.output:
        output_path = args.output
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        cities_str = '_'.join(cities[:2]) + ('_etc' if len(cities) > 2 else '')
        output_path = os.path.join(OUTPUT_DIR, f"chart_{cities_str}_{args.fixedbase}.png")
    
    if args.type == 'line':
        create_trend_chart(df_filtered, cities, args.fixedbase, output_path)
    else:
        create_bar_chart(df_filtered, cities, args.fixedbase, output_path)
    
    print("[DONE] Chart generation complete!")


if __name__ == '__main__':
    main()
