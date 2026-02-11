# -*- coding: utf-8 -*-
"""
70城房价数据一键分析工具
"""

import sys
import os
import argparse
from datetime import datetime

try:
    import pandas as pd
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH, OUTPUT_DIR, CITY_ADCODE, normalize_city_name


def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV file not found: {CSV_PATH}")
        sys.exit(1)
    print(f"Reading data file: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, dtype=str)
    print(f"Total records: {len(df)}")
    return df


def parse_month_arg(month_str):
    month_str = month_str.replace('-', '').replace('/', '')
    if len(month_str) != 6:
        raise ValueError(f"Invalid month format: {month_str}")
    return int(month_str[:4]), int(month_str[4:6])


def filter_data(df, cities, start_month, end_month):
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
    return df[df['CITY'].apply(lambda x: normalize_city_name(x) in city_norms)]


def extract_data(df, cities, start_month, end_month, output_dir):
    df_filtered = filter_data(df, cities, start_month, end_month)
    if len(df_filtered) == 0:
        print("WARNING: No data found matching criteria")
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, f"analysis_{'_'.join(cities[:2])}{'_etc' if len(cities) > 2 else ''}.csv")
    df_filtered.to_csv(output_csv, index=False)
    print(f"[OK] Data saved: {output_csv}")
    return df_filtered


def generate_summary(df, cities):
    print("\n" + "="*50)
    print("Analysis Summary")
    print("="*50)
    for city in cities:
        city_data = df[df['CITY'] == city]
        print(f"\n[{city}]")
        for fb in ['同比', '环比']:
            fb_data = city_data[city_data['FixedBase'] == fb]
            if len(fb_data) > 0:
                values = fb_data['CommodityHouseIDX'].dropna().astype(float)
                if len(values) > 0:
                    latest = values.iloc[-1]
                    avg = values.mean()
                    trend = "UP" if latest > 100 else ("DOWN" if latest < 100 else "FLAT")
                    print(f"  {fb}: latest={latest:.1f}({trend}) avg={avg:.1f}")


def generate_report(df, cities, start_month, end_month, output_dir):
    report_file = os.path.join(output_dir, f"report_{'_'.join(cities[:2])}{'_etc' if len(cities) > 2 else ''}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("70 City House Price Analysis Report\n")
        f.write("="*60 + "\n\n")
        f.write(f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Cities: {', '.join(cities)}\n")
        f.write(f"Time range: {start_month or 'start'} to {end_month or 'end'}\n")
        f.write(f"Total records: {len(df)}\n\n")
        for city in cities:
            city_data = df[df['CITY'] == city]
            f.write(f"[{city}]: {len(city_data)} records\n")
        f.write("\n" + "="*60 + "\n")
    print(f"[OK] Report saved: {report_file}")
    return report_file


def main():
    if not HAS_DEPS:
        print("ERROR: Missing pandas dependency")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='70 City House Price Quick Analysis Tool')
    parser.add_argument('--cities', '-c', required=True, nargs='+', help='City list')
    parser.add_argument('--start', '-s', help='Start month (YYYYMM)')
    parser.add_argument('--end', '-e', help='End month (YYYYMM)')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--skip-charts', action='store_true', help='Skip chart generation')
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

    output_dir = args.output or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    print("="*50)
    print("70 City House Price Quick Analysis")
    print("="*50)
    print(f"Cities: {', '.join(cities)}")
    print(f"Time range: {args.start or 'data start'} to {args.end or 'data end'}")
    print("="*50)

    df = load_data()

    df_filtered = extract_data(df, cities, args.start, args.end, output_dir)
    if df_filtered is None:
        sys.exit(1)

    if not args.skip_charts:
        print("\nGenerating charts...")
        chart_script = os.path.join(os.path.dirname(__file__), 'generate_chart.py')
        cmd = [sys.executable, chart_script, '--cities'] + cities + ['--output', os.path.join(output_dir, f"chart.png")]
        if args.start:
            cmd.extend(['--start', args.start])
        if args.end:
            cmd.extend(['--end', args.end])
        os.system(' '.join(cmd))

    generate_summary(df_filtered, cities)
    generate_report(df_filtered, cities, args.start, args.end, output_dir)

    print("\n" + "="*50)
    print("[DONE] Analysis complete!")
    print("="*50)
    print(f"Output directory: {output_dir}")


if __name__ == '__main__':
    main()
