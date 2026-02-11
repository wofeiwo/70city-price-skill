# -*- coding: utf-8 -*-
"""
70城房价数据工具 - 配置模块
"""

import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(REPO_ROOT, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'outputs')
CSV_PATH = os.path.join(DATA_DIR, '70cityprice.csv')

os.makedirs(OUTPUT_DIR, exist_ok=True)

CITY_ADCODE = {
    '北京': '110100', '天津': '120100', '石家庄': '130100', '太原': '140100',
    '呼和浩特': '150100', '沈阳': '210100', '大连': '210200', '长春': '220100',
    '哈尔滨': '230100', '上海': '310100', '南京': '320100', '杭州': '330100',
    '宁波': '330200', '合肥': '340100', '福州': '350100', '厦门': '350200',
    '南昌': '360100', '济南': '370100', '青岛': '370200', '郑州': '410100',
    '武汉': '420100', '长沙': '430100', '广州': '440100', '深圳': '440300',
    '南宁': '450100', '海口': '460100', '重庆': '500100', '成都': '510100',
    '贵阳': '520100', '昆明': '530100', '西安': '610100', '兰州': '620100',
    '西宁': '630100', '银川': '640100', '乌鲁木齐': '650100',
    '唐山': '130200', '秦皇岛': '130300', '包头': '150200', '丹东': '210600',
    '锦州': '210700', '吉林': '220200', '牡丹江': '231000', '无锡': '320200',
    '徐州': '320300', '扬州': '321000', '温州': '330300', '金华': '330700',
    '蚌埠': '340300', '安庆': '340800', '泉州': '350500', '九江': '360400',
    '赣州': '360700', '烟台': '370600', '济宁': '370800', '洛阳': '410300',
    '平顶山': '410400', '宜昌': '420500', '襄阳': '420600', '岳阳': '430600',
    '常德': '430700', '韶关': '440200', '湛江': '440800', '惠州': '441300',
    '桂林': '450300', '北海': '450500', '三亚': '460200', '泸州': '510500',
    '南充': '511300', '遵义': '520300', '大理': '532900'
}

CITY_NAME_ALIASES = {
    '大理白族自治州': '大理', '大理市': '大理',
    '北京市': '北京', '上海市': '上海', '天津市': '天津', '重庆市': '重庆',
}

CITY_STANDARD_NAME = {city: city for city in CITY_ADCODE}

REQUIRED_COLUMNS = [
    'DATE', 'ADCODE', 'CITY', 'FixedBase', 'HouseIDX', 'ResidentIDX',
    'CommodityHouseIDX', 'SecondHandIDX', 'ResidentBelow90IDX',
    'CommonResidentBelow90IDX', 'CommodityBelow90IDX', 'Commodity144IDX',
    'CommodityAbove144IDX', 'SecondHandBelow90IDX', 'SecondHand144IDX',
    'SecondHandAbove144IDX'
]

ALLOWED_FIXED_BASE = {'同比', '环比', '定基比'}
REQUIRED_FIXED_BASE = {'同比', '环比'}

EXPECTED_CITY_COUNT = len(CITY_ADCODE)


def normalize_city_name(name):
    if pd.isna(name):
        return None
    name = str(name).replace(' ', '').replace('\u3000', '').strip()
    if name in CITY_NAME_ALIASES:
        return CITY_NAME_ALIASES[name]
    if name.endswith('市'):
        name = name[:-1]
    return name if name else None


def get_city_adcode(city_name):
    normalized = normalize_city_name(city_name)
    if normalized and normalized in CITY_ADCODE:
        return CITY_ADCODE[normalized]
    return None


def get_standard_city_name(city_name):
    normalized = normalize_city_name(city_name)
    if normalized and normalized in CITY_STANDARD_NAME:
        return CITY_STANDARD_NAME[normalized]
    return city_name
