import pandas
import sys
import json
import random


def importAndValidationDictionaryFile(nameFileXls, nameSheet):
    df_import = pandas.read_excel(io=nameFileXls, sheet_name=nameSheet, dtype=str)
    nameListDf = list(df_import)
    if 'nameDictionary' not in nameListDf:
        print('Не найдены столбцы с названием словарей')
        sys.exit()
    elif 'valueDictionary' not in nameListDf:
        print('Не найдены столбцы со значениями словаря')
        sys.exit()
    df_import_whithout_nan = df_import.dropna(how='all')
    return df_import_whithout_nan


def createDictionaryOfDictionary(df_import_whithout_nan):
    DictionaryOfDictionary = {}
    for i in df_import_whithout_nan.index:
        _, __ = df_import_whithout_nan.loc[i]['nameDictionary'], df_import_whithout_nan.loc[i]['valueDictionary']
        if _ in DictionaryOfDictionary:
            DictionaryOfDictionary[_].append(__)
        else:
            DictionaryOfDictionary[_] = []
            DictionaryOfDictionary[_].append(__)
    return DictionaryOfDictionary


def createRandomDictionaryOfDictionary(df_import_whithout_nan):
    DictionaryOfDictionary = createDictionaryOfDictionary(df_import_whithout_nan)
    RandomDictionaryOfDictionary = {}
    for _ in DictionaryOfDictionary:
        __ = DictionaryOfDictionary[_]
        RandomDictionaryOfDictionary[_] = __[random.randint(0, len(__) - 1)]
    return RandomDictionaryOfDictionary


#for testing
with open('import.json', 'r') as read_file:
    dict_ = json.load(read_file)


for _ in dict_['dictionary']['xls']:
    for __ in dict_['dictionary']['xls'][_]:
        df= importAndValidationDictionaryFile(_, __)
        RandomDictionaryOfDictionary = createRandomDictionaryOfDictionary(df)