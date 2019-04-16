from django.test import TestCase

# Create your tests here.
import os
import pandas as pd
import numpy as np
from decimal import Decimal

FINAL_GRADE_MAP = {'A+': 5.0, 'A': 5.0, 'A-': 4.5, 'B+': 4.0, 'B': 3.5, 'CS': 0.0, 'CU': 0.0,
                   'B-': 3.0, 'C+': 2.5, 'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': '0.0'}


def read_csv(excel_filename, token_name):
    global FINAL_GRADE_MAP

    df = pd.read_csv(excel_filename)
    data = pd.DataFrame(df, columns=['token', 'module_code', 'module_credits', 'final_grade'])
    data = data[data['token'] == token_name]
    drop_values = [value for value in data['final_grade'].unique() if value not in FINAL_GRADE_MAP.keys()]
    data = data[~data['final_grade'].isin(drop_values)]
    data.dropna(axis=0, how='any', inplace=True)

    return data


def compute_cap_by_token_name(data):
    global FINAL_GRADE_MAP
    data['final_grade'] = data['final_grade'].map(lambda x: FINAL_GRADE_MAP[x])

    cap = np.sum(data['module_credits'] * data['final_grade']) / np.sum(data['module_credits'])
    return Decimal(cap).quantize(Decimal('0.00'))


def judge_module_code(excel_filename, module_code):
    df = pd.read_csv(excel_filename)
    df['module_code'] = df['module_code'].map(lambda x: x.upper())
    if module_code.upper() in df['module_code']:
        return True
    else:
        return False


def compute_cap_by_module_codes(excel_filename, module_codes):
    df = pd.read_csv(excel_filename)
    data = pd.DataFrame(df, columns=['module_code', 'module_credits', 'final_grade'])
    data = data[data['module_code'].isin(module_codes)]
    drop_values = [value for value in data['final_grade'].unique() if value not in FINAL_GRADE_MAP.keys()]
    data = data[~data['final_grade'].isin(drop_values)]
    data.dropna(axis=0, how='any', inplace=True)
    data['final_grade'] = data['final_grade'].map(lambda x: FINAL_GRADE_MAP[x])

    grade_points = 0.0
    credits = 0.0
    for module_code in module_codes:
        new_data = data[data['module_code'].isin([module_code])]
        grade_points += (np.sum(new_data['module_credits']) / len(new_data['module_credits'])) * \
                        (np.sum(new_data['final_grade']) / len(new_data['final_grade']))
        credits += np.sum(new_data['module_credits']) / len(new_data['module_credits'])

    cap = grade_points / credits
    cap = Decimal(cap).quantize(Decimal('0.00'))

    if cap >= 4.50:
        honours = 'Honours(Highest Distinction)'
    elif cap >= 4.00:
        honours = 'Honours(Distinction)'
    elif cap >= 3.50:
        honours = 'Honours(Merit)'
    elif cap >= 3.00:
        honours = 'Honours'
    else:
        honours = 'Pass'

    return honours


def get_average(model_excel, teaching_excel, token_name):
    model_df = pd.read_csv(model_excel)
    model_data = pd.DataFrame(model_df, columns=['token', 'm1', 'm3'])

    teaching_df = pd.read_csv(teaching_excel)
    teaching_data = pd.DataFrame(teaching_df, columns=['token', 't1', 't2', 't3'])

    model_data = model_data[model_data['token'] == token_name]
    model_data.dropna(axis=0, how='any', inplace=True)

    m1_ave = np.sum(model_data['m1']) / len(model_data['m1'])
    m1_ave = Decimal(m1_ave).quantize(Decimal('0.00'))
    m3_ave = np.sum(model_data['m3']) / len(model_data['m3'])
    m3_ave = Decimal(m3_ave).quantize(Decimal('0.00'))

    teaching_data = teaching_data[teaching_data['token'] == token_name]
    teaching_data.dropna(axis=0, how='any', inplace=True)

    t1_t2_t3_ave = np.sum([teaching_data['t1'], teaching_data['t2'], teaching_data['t3']]) / \
                   (len(teaching_data['t1']) + len(teaching_data['t2'].values) + len(teaching_data['t3'].values))
    t1_t2_t3_ave = Decimal(t1_t2_t3_ave).quantize(Decimal('0.00'))

    return m1_ave, m3_ave, t1_t2_t3_ave


if __name__ == '__main__':
    # token_name = '19700_2'
    # token_name = '40831_44'
    # path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # excel_filename = 'module enrolment.csv'
    # excel_filename = os.path.join(path, 'data', excel_filename)
    #
    # model_excel = 'student feedback module.csv'
    # model_excel = os.path.join(path, 'data', model_excel)
    #
    # teaching_excel = 'student feedback teaching.csv'
    # teaching_excel = os.path.join(path, 'data', teaching_excel)
    #
    # data = read_csv(excel_filename, token_name)
    # cap = compute_cap_by_token_name(data)
    # get_module_codes(data)
    #
    # token_name = '10013_789'
    # module_codes = ['ACC1002', 'ACC1006']
    # cap = compute_cap_by_module_codes(excel_filename, module_codes)
    # print(get_average(model_excel, teaching_excel, token_name))

    import requests

    url = 'http://127.0.0.1:9997/student/token_name/cap?token_name=40210_623'
    resp = requests.get(url)  # , params={'token_name': '40210_623'}
    print(resp.json())
