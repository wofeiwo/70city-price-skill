# -*- coding: utf-8 -*-
"""
Annual House Price Trend Chart Generator for Beijing, Shanghai, Guangzhou, Shenzhen
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

plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti SC', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found: {CSV_PATH}")
        sys.exit(1)
    print(f"Reading data file: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, dtype=str)
    print(f"Total records: {len(df)}")
    return df


def filter_data(df, cities, start_year, end_year, fixedbase):
    city_norms = {normalize_city_name(c) for c in cities}
    df = df[df['CITY'].apply(lambda x: normalize_city_name(x) in city_norms)]
    
    if fixedbase:
        df = df[df['FixedBase'] == fixedbase]
    
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y/%m/%d', errors='coerce')
    df = df.dropna(subset=['DATE'])
    df['YEAR'] = df['DATE'].dt.year
    
    df = df[(df['YEAR'] >= start_year) & (df['YEAR'] <= end_year)]
    
    return df


def calculate_yearly_avg(df, cities):
    df['CommodityHouseIDX'] = pd.to_numeric(df['CommodityHouseIDX'], errors='coerce')
    
    yearly_data = {}
    for city in cities:
        city_data = df[df['CITY'] == city]
        yearly_avg = city_data.groupby('YEAR')['CommodityHouseIDX'].mean()
        yearly_data[city] = yearly_avg
    
    return yearly_data


def create_yearly_trend_chart(yearly_data, cities, output_path, fixedbase):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    
    colors = {'北京': '#E53935', '上海': '#1E88E5', '广州': '#43A047', '深圳': '#FB8C00'}
    
    all_years = set()
    for city in cities:
        all_years.update(yearly_data[city].index)
    all_years = sorted(all_years)
    
    for city in cities:
        years = []
        values = []
        for year in all_years:
            if year in yearly_data[city].index:
                years.append(year)
                values.append(yearly_data[city][year])
        
        color = colors.get(city, plt.cm.tab10(cities.index(city) % 10))
        ax.plot(years, values, marker='o', linewidth=2.5, markersize=8, label=city, color=color)
        
        for x, y in zip(years, values):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", xytext=(0, 8), 
                       ha='center', fontsize=8, color=color)
    
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5, linewidth=1.5, label='Baseline (100)')
    
    ax.set_title(f'Beijing, Shanghai, Guangzhou, Shenzhen\nNew House Price Index ({fixedbase}) - 10 Year Trend', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel(f'Price Index ({fixedbase})', fontsize=12)
    
    ax.set_xticks(all_years)
    ax.set_xticklabels([str(y) for y in all_years], rotation=45, ha='right')
    
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    ax.text(0.02, 0.02, 'Data Source: National Bureau of Statistics of China', 
            transform=ax.transAxes, fontsize=9, color='gray', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')
    print(f"Chart saved: {output_path}")
    plt.close()


def main():
    if not HAS_DEPS:
        print("ERROR: Missing dependencies. Run: pip install pandas matplotlib")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Annual House Price Trend Chart Generator')
    parser.add_argument('--cities', '-c', nargs='+', default=['北京', '上海', '广州', '深圳'], help='City list')
    parser.add_argument('--start', '-s', type=int, default=2016, help='Start year')
    parser.add_argument('--end', '-e', type=int, default=2025, help='End year')
    parser.add_argument('--fixedbase', '-f', default='同比', choices=['同比', '环比', '定基比'], help='Index type')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--width', type=float, default=14)
    parser.add_argument('--height', type=float, default=8)
    parser.add_argument('--dpi', type=int, default=150)
    
    args = parser.parse_args()
    
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found")
        sys.exit(1)
    
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
    
    df = load_data()
    df_filtered = filter_data(df, cities, args.start, args.end, args.fixedbase)
    print(f"Filtered records: {len(df_filtered)}")
    
    if len(df_filtered) == 0:
        print("ERROR: No data found matching criteria")
        sys.exit(1)
    
    yearly_data = calculate_yearly_avg(df_filtered, cities)
    
    print("\n=== Annual Average Price Index ===")
    for city in cities:
        print(f"\n{city}:")
        for year in sorted(yearly_data[city].index):
            print(f"  {year}: {yearly_data[city][year]:.1f}")
    
    if args.output:
        output_path = args.output
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        cities_str = '_'.join(cities[:2]) + ('_etc' if len(cities) > 2 else '')
        output_path = os.path.join(OUTPUT_DIR, f"yearly_trend_{cities_str}_{args.fixedbase}.png")
    
    create_yearly_trend_chart(yearly_data, cities, output_path, args.fixedbase)
    
    print(f"\n[DONE] Chart generated successfully!")


if __name__ == '__main__':
    main()
