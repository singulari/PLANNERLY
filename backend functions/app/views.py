import pandas as pd
import numpy as np
import json
import os
import random
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FINAL_GRADE_MAP = {'A+': 5.0, 'A': 5.0, 'A-': 4.5, 'B+': 4.0, 'B': 3.5, 'CS': 0.0, 'CU': 0.0,
                   'B-': 3.0, 'C+': 2.5, 'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': '0.0'}

ENROLMENT_F = 'module_enrolment_updated.csv'
ENROLMENT_F = os.path.join(PATH, 'data', ENROLMENT_F)

MODULE_F = 'student feedback module.csv'
MODULE_F = os.path.join(PATH, 'data', MODULE_F)

TEACH_F = 'student feedback teaching.csv'
TEACH_F = os.path.join(PATH, 'data', TEACH_F)

RECOMM_F = 'Recommendation.csv'
RECOMM_F = os.path.join(PATH, 'data', RECOMM_F)

ALL_MODULE_CODES = []
STORE_MODULE_CODES = []


def transfer_cap_to_grade(cap):
    if cap > 5.0:
        grade = 'A+'
    elif cap > 4.5:
        grade = 'A'
    elif cap > 4.0:
        grade = 'A-'
    elif cap > 3.5:
        grade = 'B+'
    elif cap > 3.0:
        grade = 'B'
    elif cap > 2.5:
        grade = 'B-'
    elif cap > 2.0:
        grade = 'C+'
    elif cap > 1.5:
        grade = 'C'
    elif cap > 1.0:
        grade = 'D+'
    elif cap > 0.0:
        grade = 'D'
    else:
        grade = 'F'

    return grade


@api_view(('GET',))
@permission_classes((AllowAny,))
def compute_caps_by_token_name(request):
    """ 
	Compute CAP over semesters based on a token_name
	store semester name and CAP obtained in a dictionary

    :param token_name: token is the primary key to identify a student
    :return: type of json, judge based on the value of status 
             status: 200 - successful，400 - failed ，405 token_name not found
    """

    token_name = request.GET.get('token_name', None)

    term_caps = {}
    message = 'success'
    results = {}
    if not token_name:
        message = "No params token_name"
        status = 400
    else:
        global FINAL_GRADE_MAP
        global ENROLMENT_F

        try:
            df = pd.read_csv(ENROLMENT_F)
            data = pd.DataFrame(df, columns=['token', 'term', 'module_credits', 'final_grade'])
            data = data[data['token'] == token_name]
            if len(data.index) > 0:
                drop_values = [value for value in data['final_grade'].unique() if value not in FINAL_GRADE_MAP.keys()]
                data = data[~data['final_grade'].isin(drop_values)]
                data.dropna(axis=0, how='any', inplace=True)
                data['final_grade'] = data['final_grade'].map(lambda x: FINAL_GRADE_MAP[x])
                for term in data['term'].unique():
                    new_data = data[data['term'].isin([term])]
                    if np.sum(new_data['module_credits']) > 0:
                        cap = np.sum(new_data['module_credits'] * new_data['final_grade']) / np.sum(new_data['module_credits'])
                        cap = Decimal(cap).quantize(Decimal('0.00'))
                        term_caps[str(term)] = cap
                    else:
                        term_caps[str(term)] = 0.0

                status = 200
            else:
                message = "token_name '{}' is not exist".format(token_name)
                status = 405
        except Exception as e:
            message = "token_name '{}' is Exception, {}".format(token_name, str(e))
            status = 405

    results['term_caps'] = term_caps
    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def judge_module_code(request):
    """ 
    Judge if a module_code exists, if yes, the module can be added into the module planner
    
    :param module_code
    :return: type of json, judge based on the value of status 
             status: 200 - successful，400 - failed ，405 token_name not found
    """

    module_code = request.GET.get('module_code', None)

    message = 'success'
    results = {}
    if not module_code:
        message = "No params module_code"
        status = 400
    else:
        global ENROLMENT_F

        df = pd.read_csv(ENROLMENT_F)
        df['module_code'] = df['module_code'].map(lambda x: x.upper())

        if module_code.upper() in df['module_code'].values:
            global ALL_MODULE_CODES
            ALL_MODULE_CODES.append(module_code.upper())
            if len(ALL_MODULE_CODES) > 5:
                ALL_MODULE_CODES.pop(0)

            status = 200
        else:
            message = "module_code '{}' is not exist".format(module_code)
            status = 405

    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def compute_honours_by_module_codes(request):
    """ Based on the table of intended modules, predict the degree range

    :param module_codes: type of json，json stores the list of module codes
    :return: type of json, judge based on the value of status 
             status: 200 - successful，400 - failed ，405 token_name not found
    """

    module_codes = request.GET.get('module_codes', None)

    message = 'success'
    results = {}
    if not module_codes:
        message = "No params module_codes"
        status = 400
    else:
        global ENROLMENT_F

        module_codes = json.loads(module_codes)
        df = pd.read_csv(ENROLMENT_F)
        data = pd.DataFrame(df, columns=['module_code', 'module_credits', 'final_grade'])
        data = data[data['module_code'].isin(module_codes)]
        if len(data.index) > 0:
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

            results['honours'] = honours
            status = 200
        else:
            message = "module_codes '{}' is not exist".format(module_codes)
            status = 405

    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_average_by_mod_class_id(request):
    """ Based on the mod_class_id, obtain the three average values of m1, m3, t1_t2_t3 

    :param mod_class_id
    :return: type of json, judge based on the value of status 
             status: 200 - successful，400 - failed ，405 mod_class_id not found
    """

    mod_class_id = request.GET.get('mod_class_id', None)

    message = 'success'
    results = {}
    if not mod_class_id:
        message = "No params mod_class_id"
        status = 400
    else:
        global MODULE_F, TEACH_F

        model_df = pd.read_csv(MODULE_F)
        model_data = pd.DataFrame(model_df, columns=['mod_class_id', 'm1', 'm3'])

        teaching_df = pd.read_csv(TEACH_F)
        teaching_data = pd.DataFrame(teaching_df, columns=['mod_class_id', 't1', 't2', 't3'])

        model_data = model_data[model_data['mod_class_id'] == mod_class_id]
        if len(model_data.index) > 0:
            model_data.dropna(axis=0, how='any', inplace=True)
            m1_ave = np.sum(model_data['m1']) / len(model_data['m1'])
            m1_ave = Decimal(m1_ave).quantize(Decimal('0.00'))
            m3_ave = np.sum(model_data['m3']) / len(model_data['m3'])
            m3_ave = Decimal(m3_ave).quantize(Decimal('0.00'))
            results['m1_ave'] = m1_ave
            results['m3_ave'] = m3_ave

            teaching_data = teaching_data[teaching_data['mod_class_id'] == mod_class_id]
            if len(teaching_data.index) > 0:
                teaching_data.dropna(axis=0, how='any', inplace=True)
                t1_t2_t3_ave = np.sum([teaching_data['t1'], teaching_data['t2'], teaching_data['t3']]) / \
                               (len(teaching_data['t1']) + len(teaching_data['t2'].values) +
                                len(teaching_data['t3'].values))
                t1_t2_t3_ave = Decimal(t1_t2_t3_ave).quantize(Decimal('0.00'))
                results['t1_t2_t3_ave'] = t1_t2_t3_ave
                status = 200
            else:
                message = "mod_class_id '{}' is not exist in student 'student feedback teaching.csv'".format(mod_class_id)
                status = 405
        else:
            message = "mod_class_id '{}' is not exist in student 'feedback module.csv'".format(mod_class_id)
            status = 405

    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def compute_caps_by_module_codes(request):
    """ Compute and predict the CAP of a module code that a student intends to take in the module planner

    :return: type of json, judge based on the value of status 
             status: 200 - successful，400 - failed ，405 module_codes not found
    """

    message = 'success'
    results = {}
    status = 200
    global ENROLMENT_F

    module_codes = STORE_MODULE_CODES
    df = pd.read_csv(ENROLMENT_F)
    data = pd.DataFrame(df, columns=['module_code', 'module_credits', 'final_grade'])
    data = data[data['module_code'].isin(module_codes)]
    if len(data.index) > 0:
        drop_values = [value for value in data['final_grade'].unique() if value not in FINAL_GRADE_MAP.keys()]
        data = data[~data['final_grade'].isin(drop_values)]
        data.dropna(axis=0, how='any', inplace=True)
        data['final_grade'] = data['final_grade'].map(lambda x: FINAL_GRADE_MAP[x])

        for module_code in module_codes:
            new_data = data[data['module_code'].isin([module_code])]
            if len(new_data.index) > 0:
                values = new_data['final_grade'].values
                values = [float(value) for value in values]
                cap = np.sum(values) / len(values)
                cap = Decimal(cap).quantize(Decimal('0.0'))
                results[module_code] = transfer_cap_to_grade(cap)
            else:
                results[module_code] = transfer_cap_to_grade(0.0)

    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_recent_courses_title(request):
    """ Obtain the most recent five searched module information and the list contains at most 5 module code, store in time sequence;
    dictionary stores the module code and module name

    :return: type of json，judge based on the value of status 
             status: 200 is successful
    """

    global ALL_MODULE_CODES
    global ENROLMENT_F

    results = {}
    message = 'success'
    module_codes_tile = {}
    module_codes = []
    if len(ALL_MODULE_CODES) > 0:
        module_codes = ALL_MODULE_CODES[::-1]
        df = pd.read_csv(ENROLMENT_F)
        data = pd.DataFrame(df, columns=['module_code', 'course_title'])
        data.drop_duplicates(keep='first', inplace=True)

        data = data[data['module_code'].isin(module_codes)]
        print(data)
        for module_code in module_codes:
            new_data = data[data['module_code'].isin([module_code])]
            module_codes_tile[module_code] = new_data['course_title'].values[0]

    if len(module_codes) == 0:
        module_codes_tile['CS1231'] = 'Nation-Building in Singapore'
        module_codes_tile['EC1301'] = 'Financial Accounting'
        module_codes_tile['CS2106'] = 'Econometrics I'
        module_codes_tile['ST2131'] = 'Cell Biology'
        module_codes_tile['CS3241'] = 'Digital Design'
        module_codes = module_codes_tile.keys()

    status = 200
    results['message'] = message
    results['module_codes'] = module_codes
    results['module_codes_tile'] = module_codes_tile
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_module_codes_by_token_name(request):
    """ Based on token_name to retrieve all a list of all the modules the students have previously taken

    :param token_name: student token，primary key of identifying a student
    :return: type of json，judge based on the value of status 
             status: 200 is successful，400 is failed, 405 token_name not found
    """

    token_name = request.GET.get('token_name', None)

    module_codes = []
    message = 'success'
    results = {}
    if not token_name:
        message = "No params token_name"
        status = 400
    else:
        global FINAL_GRADE_MAP
        global ENROLMENT_F

        try:
            df = pd.read_csv(ENROLMENT_F)
            data = pd.DataFrame(df, columns=['token', 'module_code'])
            data = data[data['token'] == token_name]
            if len(data.index) > 0:
                data.dropna(axis=0, how='any', inplace=True)
                module_codes = data['module_code'].unique()
                status = 200
            else:
                message = "token_name '{}' is not exist".format(token_name)
                status = 405
        except Exception as e:
            message = "token_name '{}' is Exception, {}".format(token_name, str(e))
            status = 405

    results['module_codes'] = module_codes
    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_final_marks_by_module_code(request):
    """ Obtain all the final marks obtained for a module code
	
    :param module_code
    :return: type of json，judge based on the value of status 
             status: 200 is successful，400 is failed, 405 module_code not found
    """

    module_code = request.GET.get('module_code', None)

    y = [0 for _ in range(7)]
    x = [35, 50, 60, 70, 80, 90, 100]
    message = 'success'
    results = {}
    if not module_code:
        message = "No params module_code"
        status = 400
    else:
        global FINAL_GRADE_MAP
        global ENROLMENT_F

        try:
            data = pd.read_csv(ENROLMENT_F)
            data = data[data['module_code'].isin([module_code])]
            if len(data.index) > 0:
                data.dropna(axis=0, how='any', inplace=True, subset=['final_marks'])
                final_marks = data['final_marks']
                for final_mark in final_marks:
                    if final_mark >= 90:
                        y[6] += 1
                    elif final_mark >= 80:
                        y[5] += 1
                    elif final_mark >= 70:
                        y[4] += 1
                    elif final_mark >= 60:
                        y[3] += 1
                    elif final_mark >= 50:
                        y[2] += 1
                    elif final_mark >= 35:
                        y[1] += 1
                    else:
                        if y[0] != 0:
                            y[0] += 1
                status = 200
            else:
                message = "module_code '{}' is not exist".format(module_code)
                status = 405
        except Exception as e:
            message = "module_code '{}' is Exception, {}".format(module_code, str(e))
            status = 405

    results['final_marks_y'] = y
    results['final_marks_x'] = x
    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_core_ue_ge_modules(request):
    """ Obtain the number of Core/UE/GE modules and return modules randomly from the modules list

	:param number1: type os int
    :param number2: type os int
    :param number3: type os int
	:return: type of json，judge based on the value of status 
             status: 200 is successful
             size: the number of modules returned
    		 modules: the list of module code and module name
    """
    number1 = request.GET.get('number1', None)
    number2 = request.GET.get('number2', None)
    number3 = request.GET.get('number3', None)

    number1 = int(number1)
    number2 = int(number2)
    number3 = int(number3)

    global RECOMM_F
    data = pd.read_csv(RECOMM_F)
    core_modules = data['Core Modules'].values
    ue_modules = data['UE Modules'].values
    ge_modules = data['GE Modules'].values

    random.shuffle(core_modules)
    random.shuffle(ue_modules)
    random.shuffle(ge_modules)

    results = {
        'core': {'size': number1, 'modules': core_modules[:number1 % 8]},
        'ue': {'size': number2, 'modules': ue_modules[:number2 % 8]},
        'ge': {'size': number3, 'modules': ge_modules[:number3 % 8]}
    }
    return Response(data=results, status=200)


@api_view(('GET',))
@permission_classes((AllowAny,))
def add_module(request):
    """ add module code

    :param module_code: module code
    :return: type of json，judge based on the value of status
             status: 200 is successful，400 is failed, 405 module_code not found
    """

    module_code = request.GET.get('module_code', None)

    message = 'success'
    results = {}
    if not module_code:
        message = "No params module_code"
        status = 400
    else:
        global ENROLMENT_F

        df = pd.read_csv(ENROLMENT_F)
        df['module_code'] = df['module_code'].map(lambda x: x.upper())

        if module_code.upper() in df['module_code'].values:
            global STORE_MODULE_CODES
            if module_code.upper() not in STORE_MODULE_CODES:
                STORE_MODULE_CODES.append(module_code.upper())

            status = 200
        else:
            message = "module_code '{}' is not exist".format(module_code)
            status = 405

    results['message'] = message
    return Response(data=results, status=status)


@api_view(('GET',))
@permission_classes((AllowAny,))
def delete_module(request):
    """ delete module code

    :param module_code: module code
    :return: type of json，judge based on the value of status
             status: 200 is successful，400 is failed, 405 module_code not found
    """

    module_code = request.GET.get('module_code', None)

    message = 'success'
    results = {}
    if not module_code:
        message = "No params module_code"
        status = 400
    else:
        global STORE_MODULE_CODES
        if module_code.upper() in STORE_MODULE_CODES:
            STORE_MODULE_CODES.remove(module_code.upper())
            status = 200
        else:
            status = 405
            message = "module_code '{}' is not exist".format(module_code)

    results['message'] = message
    return Response(data=results, status=status)
