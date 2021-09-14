import pandas
import sys
import json
import time


with open('config.json', 'r') as read_file:
    dict__ = json.load(read_file)
list_strings = dict__['data_types']['listStrings']
list_types_date = dict__['data_types']['listTypesDate']
list_integers = dict__['data_types']['listIntegers']
list_objects = dict__['data_types']['listObjects']
list_arrays = dict__['data_types']['listArrays']
list_booleans = dict__['data_types']['listBooleans']
list_reguired = dict__['arguments']['listReguired']


# import from xls and smoke tests import
def import_and_validation_xls_file(name_file_xls, name_sheet):
    df_import = pandas.read_excel(io=name_file_xls, sheet_name=name_sheet, dtype=str)
    name_list_df = list(df_import)
    if 'title' not in name_list_df and 'compositeTitle' not in name_list_df:
        print('Не найдены столбцы с заголовками')
        sys.exit()
    elif 'type' not in name_list_df and 'compositeType' not in name_list_df:
        print('Не найдены столбцы с типом данных')
        sys.exit()
    elif 'indexNumber' not in name_list_df and 'compositeTitle' not in name_list_df:
        print('Не найдены столбцы для создания структуры')
        sys.exit()
    df_import_whithout_nan = df_import.dropna(how='all')
    return df_import_whithout_nan


# Add zero level to schema JSON
def add_zero_level_to_schema(dictionary_for_json__):
    dictionary_for_json_ = {}
    dictionary_for_json_['$schema'] = 'version_' + str(time.time())
    dictionary_for_json_['type'] = 'object'
    dictionary_for_json_['properties'] = {}
    for i in dictionary_for_json__:
        dictionary_for_json_['properties'] = dictionary_for_json__[i]['properties']
    return dictionary_for_json_


# Validate dictionary
def validate_work_dictionary(work_dictionary_work_):
    keys_dictionary_work0 = list(work_dictionary_work_.keys())
    keys_dictionary_work0.sort(reverse=True)
    endkeys_dictionary_work0 = keys_dictionary_work0[-1]
    k_max = keys_dictionary_work0[0]
    lenDict = keys_dictionary_work0[0] - keys_dictionary_work0[-1]
    for _ in range(lenDict):
        for k in keys_dictionary_work0:
            if k != endkeys_dictionary_work0:
                if k - 1 not in work_dictionary_work_:
                    for _ in range(k, k_max):
                        if _ in work_dictionary_work_:
                            x = work_dictionary_work_.pop(k)
                            print('Не загрузились блоки', x, 'так предущей глубины нету')
                    k_max = k - 2
                    continue
                keys_dictionary_work_cycle = list(work_dictionary_work_[k].keys())
                keys_dictionary_work_cycle_last_ = list(work_dictionary_work_[k - 1].keys())
                dictkeys_dictionary_work_cycle_last = {}
                for j in keys_dictionary_work_cycle_last_:
                    for j_ in work_dictionary_work_[k - 1][j]:
                        dictkeys_dictionary_work_cycle_last[j_] = j
                for _ in keys_dictionary_work_cycle:
                    if _ not in dictkeys_dictionary_work_cycle_last:
                        x = work_dictionary_work_.pop(work_dictionary_work_[k][_])
                        print('Не загрузились блоки', x, 'так как нет родителя')
                        keys_dictionary_work_cycle.remove(_)
                        continue
                    else:
                        a = dictkeys_dictionary_work_cycle_last[_]
                        if (
                                work_dictionary_work_[k - 1][a][_][0] not in list_objects and
                                work_dictionary_work_[k - 1][a][_][0] not in list_arrays
                        ):
                            x = work_dictionary_work_.pop(work_dictionary_work_[k][_])
                            print('Не загрузились блоки', x, 'так как родитель не объект либо список')
                            keys_dictionary_work_cycle.remove(_)
                            continue
        keys_dictionary_work0 = list(work_dictionary_work_.keys())
    keys_dictionary_work0.sort(reverse=True)
    k_min = keys_dictionary_work0[-1]
    k_max = keys_dictionary_work0[0]
    return work_dictionary_work_, k_max, k_min


# Create dictionary for JSON
def create_dictionary_for_json(work_dictionary_work_, k_max, k_min):
    dictionary_for_json = {}
    for i in range(k_max, k_min - 1, -1):
        for k in work_dictionary_work_[i]:
            for j in work_dictionary_work_[i][k]:
                if k not in dictionary_for_json:
                    dictionary_for_json[k] = {'properties': {}, 'required': []}
                a0 = work_dictionary_work_[i][k][j][0]
                a1 = work_dictionary_work_[i][k][j][1]
                a2 = work_dictionary_work_[i][k][j][2]
                a3 = work_dictionary_work_[i][k][j][3]
                if a0 in list_arrays:
                    dictionary_for_json[k]['properties'][a1] = create_dictionary_for_json_array()
                    if j in dictionary_for_json:
                        dictionary_for_json[k]['properties'][a1]['items'][0]['properties'] =\
                            dictionary_for_json[j]['properties']
                        dictionary_for_json[k]['properties'][a1]['items'][0]['required'] = \
                            dictionary_for_json[j]['required']
                        dictionary_for_json.pop(j)
                elif a0 in list_objects:
                    dictionary_for_json[k]['properties'][a1] = create_dictionary_for_json_object()
                    if j in dictionary_for_json:
                        dictionary_for_json[k]['properties'][a1]['properties'] = \
                            dictionary_for_json[j]['properties']
                        dictionary_for_json[k]['properties'][a1]['required'] = \
                            dictionary_for_json[j]['required']
                        dictionary_for_json.pop(j)
                elif a0 in list_booleans:
                    dictionary_for_json[k]['properties'][a1] = create_dictionary_for_json_boolean()
                elif a0 in list_integers:
                    dictionary_for_json[k]['properties'][a1] = create_dictionary_for_json_number(a3)
                elif work_dictionary_work_[i][k][j][0] in list_strings:
                    dictionary_for_json[k]['properties'][a1] = create_dictionary_for_json_string(a3, a0)
                if a2 in list_reguired:
                    dictionary_for_json[k]['required'].append(a1)
    dictionary_for_json = add_zero_level_to_schema(dictionary_for_json)
    return  dictionary_for_json


def create_dictionary_for_json_object():
    dictionary_object = {}
    dictionary_object['type'] = 'object'
    dictionary_object['properties'] = {}
    dictionary_object['required'] = []
    return dictionary_object


def create_dictionary_for_json_array():
    dictionary_array = {}
    dictionary_array['type'] = 'array'
    dictionary_array['items'] = [create_dictionary_for_json_object()]
    return dictionary_array


def create_dictionary_for_json_number(max_length_):
    dictionary_number = {}
    dictionary_number['type'] = 'number'
    if max_length_:
        dictionary_number['maximum'] = 10 ** int(float(max_length_))
    return dictionary_number


def create_dictionary_for_json_string(max_length_, type_):
    dictionary_string = {}
    dictionary_string['type'] = 'string'
    if type_ in list_types_date:
        dictionary_string['format'] = type_
    if max_length_:
        dictionary_string['maxLength'] = int(float(max_length_))
    return dictionary_string


def create_dictionary_for_json_boolean():
    dictionary_number = {}
    dictionary_number['type'] = 'boolean'


# Search title
def search_title_to_dictionary(name_list_df, df_import, i):
    if 'title' in name_list_df:
        a = df_import.loc[i]['title'].strip().lower()
        return a
    else:
        a = df_import.loc[i]['compositeTitle'].strip().lower().split('.')
        return a[-1]


# Search keys
def search_keys_to_dictionary(name_list_df, df_import, i):
    if 'indexNumber' in name_list_df:
        now_key_dict = df_import.loc[i]['indexNumber'].strip().lower()
        c = '.'
    else:
        now_key_dict = df_import.loc[i]['compositeTitle'].strip().lower()
        c = '/'
    a = now_key_dict.split(c)
    b = len(a)
    if b == 1:
        return now_key_dict, 'root', b
    else:
        last_key_dict = ''
        for i in range(b - 1):
            if i == b - 2:
                last_key_dict += a[i]
            else:
                last_key_dict += a[i] + c
        return now_key_dict, last_key_dict, b


# Search type and max length
def search_type_and_max_length_to_dictionary(name_list_df, df_import, i):
    if 'type' in name_list_df and 'maxLength' in name_list_df:
        a = df_import.loc[i]['type'].strip().lower()
        b = str(df_import.loc[i]['maxLength']).strip().lower().replace(',', '.')
        if b == 'nan':
            return a, ''
        else:
            return a, b
    elif 'type' in name_list_df and 'compositeType' not in name_list_df:
        a = df_import.loc[i]['type'].strip().lower()
        return a, None
    else:
        a_ = df_import.loc[i]['compositeType'].strip().lower()
        if a_.find('(') == -1:
            return a_, None
        else:
            a_1, a_2 = a_.find('('), a_.find(')')
            a, b_ = a_[:a_1], a_[a_1 + 1, a_2]
            b = b_.replace(',', '.')
            if b == 'nan':
                return a, ''
            else:
                return a, b


# Search required
def search_reguired_to_dictionary(name_list_df, df_import, i):
    if 'reguired' in name_list_df:
        return df_import.loc[i]['reguired'].strip().lower()


# Create work dictionary from import
def create_work_dictionary(df_import):
    name_list_df = list(df_import)
    index_df_import = df_import.index
    work_dictionary = {}
    for i in index_df_import:
        title_dict = search_title_to_dictionary(name_list_df, df_import, i)
        now_key_dict, last_key_dict, len_now_key_dict = search_keys_to_dictionary(name_list_df, df_import, i)
        reguired_dict = search_reguired_to_dictionary(name_list_df, df_import, i)
        type_dict, max_length_dict = search_type_and_max_length_to_dictionary(name_list_df, df_import, i)
        if len_now_key_dict in work_dictionary:
            if last_key_dict in work_dictionary[len_now_key_dict]:
                work_dictionary[len_now_key_dict][last_key_dict][now_key_dict] = [type_dict, title_dict, reguired_dict,
                                                                          max_length_dict]
            else:
                work_dictionary[len_now_key_dict][last_key_dict] = {
                    now_key_dict: [type_dict, title_dict, reguired_dict, max_length_dict]}
        else:
            work_dictionary[len_now_key_dict] = {
                last_key_dict: {now_key_dict: [type_dict, title_dict, reguired_dict, max_length_dict]}}
    return work_dictionary



with open('import.json', 'r') as read_file:
    dict_ = json.load(read_file)
for _ in dict_['xls']:
    for __ in dict_['xls'][_]:
        file_name_, sheet_name_ = _, __
        ___ = 0
        try:
            df_import = import_and_validation_xls_file(file_name_, sheet_name_)
            ___ = 1
        except FileNotFoundError:
            print('Не найден файл', file_name_)
        except:
            print('Не найден лист', __, 'в файле', _)
        if ___:
            work_dictionary_work = create_work_dictionary(df_import)
            work_dictionary_work, maximum_depth, minimum_depth = validate_work_dictionary(work_dictionary_work)
            dictionary_for_json = create_dictionary_for_json(work_dictionary_work, maximum_depth, minimum_depth)
            file_name_json = file_name_.replace('.', '_') + '_' + sheet_name_ + '_' + str(time.time()) + '.json'
            with open(file_name_json, 'w') as write_file:
                json.dump(dictionary_for_json, write_file, ensure_ascii=False, indent=4)
