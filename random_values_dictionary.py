import pandas
import sys
import json
import random


def import_and_validation_dictionary_file(name_file_xls, name_sheet):
    df_import = pandas.read_excel(io=name_file_xls, sheet_name=name_sheet, dtype=str)
    name_list_df = list(df_import)
    if 'nameDictionary' not in name_list_df:
        print('Не найдены столбцы с названием словарей')
        sys.exit()
    elif 'valueDictionary' not in name_list_df:
        print('Не найдены столбцы со значениями словаря')
        sys.exit()
    df_import_whithout_nan = df_import.dropna(how='all')
    return df_import_whithout_nan


def create_dictionary_of_dictionary(df_import_whithout_nan):
    dictionary_of_dictionary = {}
    for i in df_import_whithout_nan.index:
        _, __ = df_import_whithout_nan.loc[i]['nameDictionary'], df_import_whithout_nan.loc[i]['valueDictionary']
        if _ in dictionary_of_dictionary:
            dictionary_of_dictionary[_].append(__)
        else:
            dictionary_of_dictionary[_] = []
            dictionary_of_dictionary[_].append(__)
    return dictionary_of_dictionary


def temp_create_random_dictionary_of_dictionary(df_import_whithout_nan):
    dictionary_of_dictionary = create_dictionary_of_dictionary(df_import_whithout_nan)
    random_dictionary_of_dictionary = {}
    for _ in dictionary_of_dictionary:
        __ = dictionary_of_dictionary[_]
        random_dictionary_of_dictionary[_] = __[random.randint(0, len(__) - 1)]
    return random_dictionary_of_dictionary


def create_random_dictionary_of_dictionary():
    with open('import.json', 'r') as read_file:
        dict_ = json.load(read_file)
    for _ in dict_['dictionary']['xls']:
        for __ in dict_['dictionary']['xls'][_]:
            df = import_and_validation_dictionary_file(_, __)
            random_dictionary_of_dictionary = temp_create_random_dictionary_of_dictionary(df)
    return random_dictionary_of_dictionary