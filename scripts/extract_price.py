# -*- coding: utf-8 -*-
"""
70城房价数据提取工具 / 70 City House Price Data Extraction Tool
"""

import sys
import os
import argparse

try:
    import pandas as pd
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH, OUTPUT_DIR, CITY_NAME_ALIASES, ALLOWED_FIXED_BASE, normalize_city_name


def parse_month_arg(month_str):
    month_str = month_str.replace('-', '').replace('/', '')
    if len(month_str) != 6:
        raise ValueError(f"Invalid month format: {month_str}")
    year, month = int(month_str[:4]), int(month_str[4:6])
    return year, month


def date_to_comparable(date_str):
    try:
        parts = date_str.split('/')
        return (int(parts[0]), int(parts[1]))
    except:
        return None


def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found: {CSV_PATH}")
        sys.exit(1)
    print(f"Reading data file: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, dtype=str)
    print(f"Total records: {len(df)}")
    return df


def extract_by_month(df, start_year, start_month, end_year, end_month):
    start_tuple, end_tuple = (start_year, start_month), (end_year, end_month)
    print(f"Extracting: {start_year}/{start_month} to {end_year}/{end_month}")
    mask = df['DATE'].apply(lambda x: start_tuple <= date_to_comparable(x) <= end_tuple if date_to_comparable(x) else False)
    return df[mask].copy()


def extract_by_city(df, cities):
    print(f"Extracting cities: {', '.join(cities)}")
    requested = {normalize_city_name(c) for c in cities}
    mask = df['CITY'].apply(lambda x: normalize_city_name(x) in requested)
    return df[mask].copy()


def extract_by_fixedbase(df, fixedbases):
    if not fixedbases:
        return df
    print(f"Filter by index type: {', '.join(sorted(fixedbases))}")
    mask = df['FixedBase'].isin(fixedbases)
    return df[mask].copy()


def parse_fixedbase_arg(arg):
    if not arg:
        return None
    parts = [p.strip() for p in str(arg).split(',') if p.strip()]
    invalid = sorted(set(parts) - ALLOWED_FIXED_BASE)
    if invalid:
        raise ValueError(f"Invalid index type: {', '.join(invalid)}")
    return set(parts) if parts else None


def print_stats(df, extracted_df):
    print(f"Extracted {len(extracted_df)} records")
    if len(extracted_df) > 0:
        months = sorted(set(date_to_comparable(d) for d in extracted_df['DATE'].dropna()))
        cities = extracted_df['CITY'].unique()
        print(f"Months: {len(months)}, Cities: {len(cities)}")


def save_data(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if output_path.endswith('.xlsx'):
        df.to_excel(output_path, index=False)
    elif output_path.endswith('.json'):
        df.to_json(output_path, orient='records', force_ascii=False, indent=2)
    else:
        df.to_csv(output_path, index=False, quoting=1)
    print(f"\nData saved to: {output_path}")


def get_output_path(filename):
    if os.path.sep in filename or '/' in filename:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', filename)
    return os.path.join(OUTPUT_DIR, filename)


def cmd_month(args):
    if not HAS_DEPS:
        print("Error: pandas is required")
        sys.exit(1)
    start_year, start_month = parse_month_arg(args.start)
    end_year, end_month = parse_month_arg(args.end)
    if (start_year, start_month) > (end_year, end_month):
        print("Error: start month must be before end month")
        sys.exit(1)
    df = load_data()
    extracted_df = extract_by_month(df, start_year, start_month, end_year, end_month)
    if args.fixedbase:
        extracted_df = extract_by_fixedbase(extracted_df, parse_fixedbase_arg(args.fixedbase))
    print_stats(df, extracted_df)
    if len(extracted_df) > 0:
        output = args.output or f"70cityprice_{start_year}{start_month:02d}_{end_year}{end_month:02d}.csv"
        save_data(extracted_df, get_output_path(output))
    return extracted_df


def cmd_city(args):
    if not HAS_DEPS:
        print("Error: pandas is required")
        sys.exit(1)
    if not args.cities:
        print("Error: please specify at least one city")
        sys.exit(1)
    df = load_data()
    extracted_df = extract_by_city(df, args.cities)
    if args.fixedbase:
        extracted_df = extract_by_fixedbase(extracted_df, parse_fixedbase_arg(args.fixedbase))
    print_stats(df, extracted_df)
    if len(extracted_df) > 0:
        cities_str = '_'.join(args.cities[:3]) + ('_etc' if len(args.cities) > 3 else '')
        output = args.output or f"70cityprice_{cities_str}.csv"
        save_data(extracted_df, get_output_path(output))
    return extracted_df


def cmd_list_cities(args):
    df = load_data()
    cities = sorted(df['CITY'].unique())
    print(f"\nAvailable cities ({len(cities)}):\n")
    for i in range(0, len(cities), 5):
        print("  " + "  ".join(f"{c:<8}" for c in cities[i:i+5]))


def cmd_list_dates(args):
    df = load_data()
    all_dates = sorted(set(date_to_comparable(d) for d in df['DATE'].dropna()))
    if all_dates:
        print(f"\nData date range: {all_dates[0][0]}/{all_dates[0][1]} to {all_dates[-1][0]}/{all_dates[-1][1]}")
        print(f"Total months: {len(all_dates)}")
    else:
        print("No valid date data found")


def main():
    if not HAS_DEPS:
        print("Error: pandas is required. Run: pip install pandas openpyxl")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='70 City House Price Data Extraction Tool')
    subparsers = parser.add_subparsers(dest='command')
    
    month_parser = subparsers.add_parser('month', help='Extract by month range')
    month_parser.add_argument('start')
    month_parser.add_argument('end')
    month_parser.add_argument('output', nargs='?')
    month_parser.add_argument('--fixedbase', '-f')
    month_parser.set_defaults(func=cmd_month)
    
    city_parser = subparsers.add_parser('city', help='Extract by city')
    city_parser.add_argument('cities', nargs='+')
    city_parser.add_argument('--output', '-o')
    city_parser.add_argument('--fixedbase', '-f')
    city_parser.set_defaults(func=cmd_city)
    
    subparsers.add_parser('list-cities', help='List available cities').set_defaults(func=cmd_list_cities)
    subparsers.add_parser('list-dates', help='List date range').set_defaults(func=cmd_list_dates)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
