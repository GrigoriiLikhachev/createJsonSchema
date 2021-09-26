import json
import time
import create_and_validation_work_dictionary_for_json as cwdfj
import import_and_validation_xls_file as xls_file


with open('config.json', 'r') as read_file:
    dict__ = json.load(read_file)
list_strings = dict__['data_types']['listStrings']
list_types_date = dict__['data_types']['listTypesDate']
list_integers = dict__['data_types']['listIntegers']
list_objects = dict__['data_types']['listObjects']
list_arrays = dict__['data_types']['listArrays']
list_booleans = dict__['data_types']['listBooleans']
list_reguired = dict__['arguments']['listReguired']


# Create dictionary for JSON minimum or maximum
def create_dictionary_for_json_minimum_maximum(work_dictionary_work_, k_max, k_min, minimum_json=False):
    dictionary_for_json = {}
    for i in range(k_max, k_min - 1, -1):
        for k in work_dictionary_work_[i]:
            dictionary_for_json[k] = {}
            for j in work_dictionary_work_[i][k]:
                type_parametr = work_dictionary_work_[i][k][j][0]
                parametr_name = work_dictionary_work_[i][k][j][1]
                required_parametr = work_dictionary_work_[i][k][j][2]
                parametr_value = work_dictionary_work_[i][k][j][4]
                __ = 1
                if minimum_json:
                    if required_parametr in list_reguired:
                        __ = 1
                    else:
                        __ = 0
                if type_parametr not in list_arrays and type_parametr not in list_objects:
                    if __:
                        dictionary_for_json[k][parametr_name] = parametr_value
                else:
                    _ = dictionary_for_json.pop(j)
                    if __:
                        if type_parametr in list_arrays:
                            dictionary_for_json[k][parametr_name]= _
                        else:
                            dictionary_for_json[k][parametr_name] = [_]
    dictionary_for_json_ = {}
    for i in dictionary_for_json:
        for _ in dictionary_for_json[i]:
            dictionary_for_json_[_] = dictionary_for_json[i][_]
    return dictionary_for_json_


# Create dictionary for JSON schema
def create_dictionary_for_json_schema(work_dictionary_work_, k_max, k_min):
    dictionary_for_json = {}
    for i in range(k_max, k_min - 1, -1):
        for k in work_dictionary_work_[i]:
            if k not in dictionary_for_json:
                dictionary_for_json[k] = {'properties': {}, 'required': []}
            for j in work_dictionary_work_[i][k]:
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


# Add zero level to schema JSON
def add_zero_level_to_schema(dictionary_for_json__):
    dictionary_for_json_ = {}
    dictionary_for_json_['$schema'] = 'version_' + str(time.time())
    dictionary_for_json_['type'] = 'object'
    dictionary_for_json_['properties'] = {}
    for i in dictionary_for_json__:
        dictionary_for_json_['properties'] = dictionary_for_json__[i]['properties']
    return dictionary_for_json_


def create_json(json_schema=True, minimum_json=False, maximum_json=False):
    parametr = 0
    if json_schema:
        if minimum_json or maximum_json:
            parametr = 1
    else:
        parametr = 1
    with open('import.json', 'r') as read_file:
        dict_ = json.load(read_file)
    for _ in dict_['xls']:
        for __ in dict_['xls'][_]:
            file_name_, sheet_name_ = _, __
            ___ = 0
            try:
                df_import = xls_file.import_and_validation_xls_file(file_name_, sheet_name_)
                ___ = 1
            except FileNotFoundError:
                print('Не найден файл', file_name_)
            except:
                print('Не найден лист', __, 'в файле', _)
            if ___:
                work_dictionary_work = cwdfj.create_work_dictionary(df_import, parametr)
                work_dictionary_work, maximum_depth, minimum_depth = \
                    cwdfj.validate_work_dictionary(work_dictionary_work)
                if json_schema:
                    dictionary_for_json = create_dictionary_for_json_schema(work_dictionary_work,
                                                                            maximum_depth, minimum_depth)
                    file_name_json = 'json_schema_' + file_name_.replace('.', '_') + '_' + sheet_name_ + \
                                     '_' + str(time.time()) + '.json'
                    with open(file_name_json, 'w') as write_file:
                        json.dump(dictionary_for_json, write_file, ensure_ascii=False, indent=4)
                if minimum_json:
                    dictionary_for_json = create_dictionary_for_json_minimum_maximum(work_dictionary_work,
                                                                            maximum_depth, minimum_depth, True)
                    file_name_json = 'json_minimum_' + file_name_.replace('.', '_') + '_' + sheet_name_ + \
                                     '_' + str(time.time()) + '.json'
                    with open(file_name_json, 'w') as write_file:
                        json.dump(dictionary_for_json, write_file, ensure_ascii=False, indent=4)
                if maximum_json:
                    dictionary_for_json = create_dictionary_for_json_minimum_maximum(work_dictionary_work,
                                                                            maximum_depth, minimum_depth, False)
                    file_name_json = 'json_maximum_' + file_name_.replace('.', '_') + '_' + sheet_name_ + \
                                     '_' + str(time.time()) + '.json'
                    with open(file_name_json, 'w') as write_file:
                        json.dump(dictionary_for_json, write_file, ensure_ascii=False, indent=4)


create_json(True, True, True)