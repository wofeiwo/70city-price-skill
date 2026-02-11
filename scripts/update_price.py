# -*- coding: utf-8 -*-
"""
70城房价数据更新工具
"""

import sys
import os
import re

try:
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH, CITY_ADCODE, REQUIRED_COLUMNS, normalize_city_name, get_city_adcode, get_standard_city_name


def fetch_data_from_url(url):
    print(f"Fetching data from: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    tables = pd.read_html(response.text)
    print(f"Successfully read {len(tables)} tables")
    return tables


def parse_date_from_url(url):
    match = re.search(r't(\d{8})', url)
    if match:
        return int(match.group(1)[:4]), int(match.group(1)[4:6])
    return None, None


def parse_main_index_table(table, start_row=2, end_row=37, is_january=False):
    data = {}
    sample_row = table.iloc[start_row] if len(table) > start_row else None
    has_avg = sample_row is not None and (len(sample_row) > 6 or (not is_january and len(sample_row) > 4))
    
    for i in range(start_row, min(end_row, len(table))):
        row = table.iloc[i]
        city1 = normalize_city_name(str(row.iloc[0]))
        if city1 and city1 != 'nan':
            if has_avg:
                data[city1] = {'环比': row.iloc[1], '同比': row.iloc[2], '定基比': row.iloc[3]}
            else:
                tongbi_val = row.iloc[2]
                data[city1] = {'环比': row.iloc[1], '同比': tongbi_val, '定基比': tongbi_val}
        
        right_start = 4 if has_avg else 3
        if len(row) > right_start:
            city2 = normalize_city_name(str(row.iloc[right_start]))
            if city2 and city2 != 'nan':
                if has_avg:
                    data[city2] = {'环比': row.iloc[right_start + 1], '同比': row.iloc[right_start + 2], '定基比': row.iloc[right_start + 3]}
                else:
                    tongbi_val = row.iloc[right_start + 2]
                    data[city2] = {'环比': row.iloc[right_start + 1], '同比': tongbi_val, '定基比': tongbi_val}
    return data


def parse_size_index_table(table, start_row=3, end_row=38, is_january=False):
    data = {}
    sample_row = table.iloc[start_row] if len(table) > start_row else None
    has_avg = sample_row is not None and len(sample_row) >= 10
    
    for i in range(start_row, min(end_row, len(table))):
        row = table.iloc[i]
        city = normalize_city_name(str(row.iloc[0]))
        if city and city != 'nan':
            if has_avg:
                data[city] = {
                    'Below90': {'环比': row.iloc[1], '同比': row.iloc[2], '定基比': row.iloc[3]},
                    '144': {'环比': row.iloc[4], '同比': row.iloc[5], '定基比': row.iloc[6]},
                    'Above144': {'环比': row.iloc[7], '同比': row.iloc[8], '定基比': row.iloc[9]}
                }
    return data


def process_tables(tables, is_january=False):
    if len(tables) < 6:
        raise ValueError(f"Expected at least 6 tables, got {len(tables)}")
    commodity_main = parse_main_index_table(tables[0], is_january=is_january)
    secondhand_main = parse_main_index_table(tables[1], is_january=is_january)
    commodity_size = parse_size_index_table(tables[2], is_january=is_january)
    secondhand_size = parse_size_index_table(tables[4], is_january=is_january)
    return commodity_main, secondhand_main, commodity_size, secondhand_size


def create_records(date_str, commodity_main, secondhand_main, commodity_size, secondhand_size):
    records = []
    all_cities = set(commodity_main.keys()) | set(secondhand_main.keys())
    for city in all_cities:
        adcode = get_city_adcode(city)
        if not adcode:
            continue
        city_name = get_standard_city_name(city) or city
        for idx_type in ['同比', '环比', '定基比']:
            record = {col: '' for col in REQUIRED_COLUMNS}
            record['DATE'] = date_str
            record['ADCODE'] = adcode
            record['CITY'] = city_name
            record['FixedBase'] = idx_type
            if city in commodity_main and commodity_main[city].get(idx_type):
                record['CommodityHouseIDX'] = commodity_main[city][idx_type]
            if city in secondhand_main and secondhand_main[city].get(idx_type):
                record['SecondHandIDX'] = secondhand_main[city][idx_type]
            has_data = record['CommodityHouseIDX'] or record['SecondHandIDX']
            if has_data:
                records.append(record)
    return records


def update_csv(csv_path, new_records):
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path, dtype=str)
    else:
        existing_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    print(f"Existing data: {len(existing_df)} records")
    new_df = pd.DataFrame(new_records)
    if len(new_records) > 0:
        new_date = new_records[0]['DATE']
        if new_date in existing_df['DATE'].values:
            print(f"WARNING: Data for {new_date} already exists, will replace")
            existing_df = existing_df[existing_df['DATE'] != new_date]
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df = combined_df[REQUIRED_COLUMNS]
    combined_df['DATE_SORT'] = pd.to_datetime(combined_df['DATE'], format='%Y/%m/%d', errors='coerce')
    combined_df = combined_df.sort_values(['CITY', 'DATE_SORT', 'FixedBase']).drop('DATE_SORT', axis=1)
    combined_df.to_csv(csv_path, index=False, quoting=1)
    print(f"Updated data: {len(combined_df)} records")


def search_latest_url():
    print("Auto-search requires manual URL input")
    return None


def main():
    if not HAS_DEPS:
        print("ERROR: Missing dependencies. Run: pip install pandas requests beautifulsoup4 lxml")
        sys.exit(1)

    url = None
    auto_mode = False

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--auto':
            auto_mode = True
        else:
            url = sys.argv[1]
    elif len(sys.argv) == 1:
        auto_mode = True

    if auto_mode:
        print("Auto mode: Searching for latest data...")
        url = search_latest_url()

    if not url:
        print("Usage: python update_price.py <URL>")
        print("Example: python update_price.py 'https://www.stats.gov.cn/sj/zxfb/...'")
        sys.exit(1)

    try:
        tables = fetch_data_from_url(url)
        year, month = parse_date_from_url(url)
        if not year:
            print("ERROR: Cannot parse date")
            sys.exit(1)
        
        data_month = month - 1
        data_year = year
        if data_month == 0:
            data_month = 12
            data_year -= 1
        
        date_str = f"{data_year}/{data_month}/1"
        print(f"Data date: {date_str}")
        
        is_january = (data_month == 1)
        commodity_main, secondhand_main, commodity_size, secondhand_size = process_tables(tables, is_january)
        
        print(f"Parsed {len(commodity_main)} cities")
        records = create_records(date_str, commodity_main, secondhand_main, commodity_size, secondhand_size)
        print(f"Generated {len(records)} records")
        update_csv(CSV_PATH, records)
        print("[DONE] Data update complete!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
