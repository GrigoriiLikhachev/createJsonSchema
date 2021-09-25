import json
import boolean_random
import number_random
import russian_random
import random_values_dictionary
import date_random


with open('config.json', 'r') as read_file:
    dict__ = json.load(read_file)
list_strings = dict__['data_types']['listStrings']
list_types_date = dict__['data_types']['listTypesDate']
list_integers = dict__['data_types']['listIntegers']
list_objects = dict__['data_types']['listObjects']
list_arrays = dict__['data_types']['listArrays']
list_booleans = dict__['data_types']['listBooleans']
list_reguired = dict__['arguments']['listReguired']


def create_work_dictionary(df_import, parametr = 0, default_value_maximum_string = 10,
                           default_value_maximum_number = 5):
    name_list_df = list(df_import)
    index_df_import = df_import.index
    work_dictionary = {}
    if parametr != 0:
        random_dictionary_of_dictionary = random_values_dictionary.create_random_dictionary_of_dictionary()
    for i in index_df_import:
        title_dict = search_title_to_dictionary(name_list_df, df_import, i)
        now_key_dict, last_key_dict, len_now_key_dict = search_keys_to_dictionary(name_list_df, df_import, i)
        reguired_dict = search_reguired_to_dictionary(name_list_df, df_import, i)
        type_dict, max_length_dict = search_type_and_max_length_to_dictionary(name_list_df, df_import, i)
        if parametr == 0:
            random_value_of_parametr = None
        else:
            name_of_dictionary = search_name_of_dictionary(name_list_df, df_import, i)
            if name_of_dictionary is not None and name_of_dictionary in random_dictionary_of_dictionary:
                random_value_of_parametr = random_dictionary_of_dictionary[name_of_dictionary]
            elif type_dict in list_strings:
                if type_dict in list_types_date:
                    random_value_of_parametr = date_random.random_date()
                else:
                    if max_length_dict is not None and max_length_dict != '':
                        random_value_of_parametr = russian_random.random_russian_word(int(float(max_length_dict)))
                    else:
                        random_value_of_parametr = russian_random.random_russian_word(default_value_maximum_string)
            elif type_dict in list_booleans:
                random_value_of_parametr = boolean_random.random_boolean_value()
            elif type_dict in list_integers:
                if max_length_dict is not None and max_length_dict != '':
                    _ = int(float(max_length_dict))
                    if _ == max_length_dict:
                        __ = 0
                    else:
                        __ = int((float(max_length_dict) - _) * 10)
                    random_value_of_parametr = number_random.number_random(_, __)
                else:
                    random_value_of_parametr = number_random.number_random(default_value_maximum_number, 0)
            else:
                random_value_of_parametr = None
        if len_now_key_dict in work_dictionary:
            if last_key_dict in work_dictionary[len_now_key_dict]:
                work_dictionary[len_now_key_dict][last_key_dict][now_key_dict] = [type_dict, title_dict, reguired_dict,
                                                                          max_length_dict, random_value_of_parametr]
            else:
                work_dictionary[len_now_key_dict][last_key_dict] = {
                    now_key_dict: [type_dict, title_dict, reguired_dict, max_length_dict, random_value_of_parametr]}
        else:
            work_dictionary[len_now_key_dict] = {
                last_key_dict: {now_key_dict: [type_dict, title_dict, reguired_dict,
                                               max_length_dict, random_value_of_parametr]}}
    return work_dictionary


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


# Search title
def search_title_to_dictionary(name_list_df, df_import, i):
    if 'title' in name_list_df:
        a = df_import.loc[i]['title'].strip().lower()
        return a
    else:
        a = df_import.loc[i]['compositeTitle'].strip().lower().split('.')
        return a[-1]


# Search required
def search_reguired_to_dictionary(name_list_df, df_import, i):
    if 'reguired' in name_list_df:
        return df_import.loc[i]['reguired'].strip().lower()


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


# Search name of dictionary
def search_name_of_dictionary(name_list_df, df_import, i):
    if 'nameDictionary' in name_list_df:
        return str(df_import.loc[i]['nameDictionary']).strip().lower()
    else:
        return None