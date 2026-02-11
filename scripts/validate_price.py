# -*- coding: utf-8 -*-
"""
70城房价数据质量校验工具
"""

import sys
import os
import argparse
from typing import List

try:
    import pandas as pd
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CSV_PATH, REQUIRED_COLUMNS, ALLOWED_FIXED_BASE, REQUIRED_FIXED_BASE, EXPECTED_CITY_COUNT, normalize_city_name


def limit_join(items: List[str], max_items: int = 8) -> str:
    if not items:
        return ''
    shown = items[:max_items]
    suffix = '' if len(items) <= max_items else f' ... total {len(items)} items'
    return ', '.join(shown) + suffix


def non_empty_mask(series):
    return series.notna() & (series.astype(str).str.strip() != '')


def validate_csv(csv_path: str, max_details: int = 8) -> int:
    issues: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(csv_path):
        print(f'ERROR: CSV file not found: {csv_path}')
        return 1

    print(f'Starting validation: {csv_path}')
    df = pd.read_csv(csv_path, dtype=str)
    print(f'Records: {len(df)}')

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        issues.append(f"Missing required columns: {', '.join(missing_columns)}")
    if missing_columns:
        return print_report(issues, warnings)

    date_parsed = pd.to_datetime(df['DATE'], format='%Y/%m/%d', errors='coerce')
    invalid_dates = sorted(df.loc[date_parsed.isna(), 'DATE'].dropna().astype(str).unique().tolist())
    if invalid_dates:
        issues.append(f"Invalid DATE values: {limit_join(invalid_dates, max_details)}")

    month_series = date_parsed.dt.to_period('M')
    valid_months = sorted(month_series.dropna().unique())
    if not valid_months:
        issues.append('No usable month data detected')
    else:
        gaps = []
        for prev, curr in zip(valid_months[:-1], valid_months[1:]):
            month_delta = (curr.year - prev.year) * 12 + (curr.month - prev.month)
            if month_delta != 1:
                gaps.append(f'{prev}->{curr}')
        if gaps:
            issues.append(f"Non-continuous months: {limit_join(gaps, max_details)}")

    fixed_base_series = df['FixedBase'].astype(str).str.strip()
    invalid_fixed_base = sorted((set(fixed_base_series.unique()) - ALLOWED_FIXED_BASE) - {'nan'})
    if invalid_fixed_base:
        issues.append(f"Invalid FixedBase values: {', '.join(invalid_fixed_base)}")

    city_std = df['CITY'].apply(normalize_city_name)
    city_set = set(city_std.dropna().astype(str).str.strip().tolist())
    if len(city_set) != EXPECTED_CITY_COUNT:
        issues.append(f"Abnormal city count after standardization: actual={len(city_set)}, expected={EXPECTED_CITY_COUNT}")

    key_df = pd.DataFrame({'DATE': df['DATE'].astype(str), 'CITY_STD': city_std.astype(str), 'FixedBase': fixed_base_series})
    duplicated = key_df.duplicated(['DATE', 'CITY_STD', 'FixedBase'], keep=False)
    if duplicated.any():
        sample_text = ', '.join(f"{r.DATE}|{r.CITY_STD}|{r.FixedBase}" for r in key_df.loc[duplicated].head(max_details).itertuples(index=False))
        issues.append(f"Duplicate primary keys: {sample_text}")

    return print_report(issues, warnings)


def print_report(issues: List[str], warnings: List[str]) -> int:
    print('\n================ VALIDATION RESULTS ================')
    if issues:
        print(f'[FAIL] Found {len(issues)} issues')
        for idx, text in enumerate(issues, start=1):
            print(f'{idx}. {text}')
    else:
        print('[PASS] No blocking issues found')

    if warnings:
        print(f'\n[WARN] {len(warnings)} items')
        for idx, text in enumerate(warnings, start=1):
            print(f'W{idx}. {text}')

    return 1 if issues else 0


def main() -> int:
    if not HAS_DEPS:
        print("ERROR: Missing pandas dependency")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='70 City House Price Data Validation Tool')
    parser.add_argument('--csv', default=CSV_PATH, help='CSV file path')
    parser.add_argument('--max-details', type=int, default=8)
    args = parser.parse_args()

    return validate_csv(args.csv, max_details=args.max_details)


if __name__ == '__main__':
    sys.exit(main())
