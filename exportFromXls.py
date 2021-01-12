import pandas
import sys
import json
import time


with open('config.json', 'r') as read_file:
    dict__ = json.load(read_file)
listStrings = dict__['data_types']['listStrings']
listTypesDate = dict__['data_types']['listTypesDate']
listIntegers = dict__['data_types']['listIntegers']
listObjects = dict__['data_types']['listObjects']
listArrays = dict__['data_types']['listArrays']
listBooleans = dict__['data_types']['listBooleans']
listReguired = dict__['arguments']['listReguired']


# import from xls and smoke tests import
def importAndValidationXlsFile(nameFileXls, nameSheet):
    df_import = pandas.read_excel(io=nameFileXls, sheet_name=nameSheet, dtype=str)
    nameListDf = list(df_import)
    if 'title' not in nameListDf and 'compositeTitle' not in nameListDf:
        print('Не найдены столбцы с заголовками')
        sys.exit()
    elif 'type' not in nameListDf and 'compositeType' not in nameListDf:
        print('Не найдены столбцы с типом данных')
        sys.exit()
    elif 'indexNumber' not in nameListDf and 'compositeTitle' not in nameListDf:
        print('Не найдены столбцы для создания структуры')
        sys.exit()
    df_import_whithout_nan = df_import.dropna(how='all')
    return df_import_whithout_nan


# Validate dictionary
def validateWorkDictionray(workDictionaryWork_):
    keysDictionaryWork0 = list(workDictionaryWork_.keys())
    keysDictionaryWork0.sort(reverse=True)
    endKeysDictionaryWork0 = keysDictionaryWork0[-1]
    kMax = keysDictionaryWork0[0]
    lenDict = keysDictionaryWork0[0] - keysDictionaryWork0[-1]
    for _ in range(lenDict):
        for k in keysDictionaryWork0:
            if k != endKeysDictionaryWork0:
                if k - 1 not in workDictionaryWork_:
                    for _ in range(k, kMax):
                        if _ in workDictionaryWork_:
                            x = workDictionaryWork_.pop(k)
                            print('Не загрузились блоки', x, 'так предущей глубины нету')
                    kMax = k - 2
                    continue
                keysDictionaryWorkCycle = list(workDictionaryWork_[k].keys())
                keysDictionaryWorkCycleLast_ = list(workDictionaryWork_[k - 1].keys())
                dictKeysDictionaryWorkCycleLast = {}
                for j in keysDictionaryWorkCycleLast_:
                    for j_ in workDictionaryWork_[k - 1][j]:
                        dictKeysDictionaryWorkCycleLast[j_] = j
                for _ in keysDictionaryWorkCycle:
                    if _ not in dictKeysDictionaryWorkCycleLast:
                        x = workDictionaryWork_.pop(workDictionaryWork_[k][_])
                        print('Не загрузились блоки', x, 'так как нет родителя')
                        keysDictionaryWorkCycle.remove(_)
                        continue
                    else:
                        a = dictKeysDictionaryWorkCycleLast[_]
                        if (
                                workDictionaryWork_[k - 1][a][_][0] not in listObjects and
                                workDictionaryWork_[k - 1][a][_][0] not in listArrays
                        ):
                            x = workDictionaryWork_.pop(workDictionaryWork_[k][_])
                            print('Не загрузились блоки', x, 'так как родитель не объект либо список')
                            keysDictionaryWorkCycle.remove(_)
                            continue
        keysDictionaryWork0 = list(workDictionaryWork_.keys())
    keysDictionaryWork0.sort(reverse=True)
    kMin = keysDictionaryWork0[-1]
    kMax = keysDictionaryWork0[0]
    return workDictionaryWork_, kMax, kMin


# Add zero level to schema JSON
def addZeroLevelToSchema(dictionaryForJson__):
    dictionaryForJson_ = {}
    dictionaryForJson_['$schema'] = 'version_' + str(time.time())
    dictionaryForJson_['type'] = 'object'
    dictionaryForJson_['properties'] = {}
    for i in dictionaryForJson__:
        dictionaryForJson_['properties'] = dictionaryForJson__[i]['properties']
    return dictionaryForJson_


# Create dictionary for JSON
def createDictionaryForJSON(workDictionaryWork_, kMax, kMin):
    dictionaryForJson = {}
    for i in range(kMax, kMin - 1, -1):
        for k in workDictionaryWork_[i]:
            for j in workDictionaryWork_[i][k]:
                if k not in dictionaryForJson:
                    dictionaryForJson[k] = {'properties': {}, 'required': []}
                a0 = workDictionaryWork_[i][k][j][0]
                a1 = workDictionaryWork_[i][k][j][1]
                a2 = workDictionaryWork_[i][k][j][2]
                a3 = workDictionaryWork_[i][k][j][3]
                if a0 in listArrays:
                    dictionaryForJson[k]['properties'][a1] = createDictionaryForJsonArray()
                    if j in dictionaryForJson:
                        dictionaryForJson[k]['properties'][a1]['items'][0]['properties'] =\
                            dictionaryForJson[j]['properties']
                        dictionaryForJson[k]['properties'][a1]['items'][0]['required'] = \
                            dictionaryForJson[j]['required']
                        dictionaryForJson.pop(j)
                elif a0 in listObjects:
                    dictionaryForJson[k]['properties'][a1] = createDictionaryForJsonObject()
                    if j in dictionaryForJson:
                        dictionaryForJson[k]['properties'][a1]['properties'] = \
                            dictionaryForJson[j]['properties']
                        dictionaryForJson[k]['properties'][a1]['required'] = \
                            dictionaryForJson[j]['required']
                        dictionaryForJson.pop(j)
                elif a0 in listBooleans:
                    dictionaryForJson[k]['properties'][a1] = createDictionaryForJsonBoolean()
                elif a0 in listIntegers:
                    dictionaryForJson[k]['properties'][a1] = createDictionaryForJsonNumber(a3)
                elif workDictionaryWork_[i][k][j][0] in listStrings:
                    dictionaryForJson[k]['properties'][a1] = createDictionaryForJsonString(a3, a0)
                if a2 in listReguired:
                    dictionaryForJson[k]['required'].append(a1)
    dictionaryForJson = addZeroLevelToSchema(dictionaryForJson)
    return  dictionaryForJson


def createDictionaryForJsonObject():
    dictionaryObject = {}
    dictionaryObject['type'] = 'object'
    dictionaryObject['properties'] = {}
    dictionaryObject['required'] = []
    return dictionaryObject


def createDictionaryForJsonArray():
    dictionaryArray = {}
    dictionaryArray['type'] = 'array'
    dictionaryArray['items'] = [createDictionaryForJsonObject()]
    return dictionaryArray


def createDictionaryForJsonNumber(maxLength_):
    dictionaryNumber = {}
    dictionaryNumber['type'] = 'number'
    if maxLength_:
        dictionaryNumber['maximum'] = 10 ** int(float(maxLength_))
    return dictionaryNumber


def createDictionaryForJsonString(maxLength_, type_):
    dictionaryString = {}
    dictionaryString['type'] = 'string'
    if type_ in listTypesDate:
        dictionaryString['format'] = type_
    if maxLength_:
        dictionaryString['maxLength'] = int(float(maxLength_))
    return dictionaryString


def createDictionaryForJsonBoolean():
    dictionaryNumber = {}
    dictionaryNumber['type'] = 'boolean'


# Search title
def searchTitleToDictionary(nameListDf, df_import, i):
    if 'title' in nameListDf:
        a = df_import.loc[i]['title'].strip().lower()
        return a
    else:
        a = df_import.loc[i]['compositeTitle'].strip().lower().split('.')
        return a[-1]


# Search keys
def searchKeysToDictionary(nameListDf, df_import, i):
    if 'indexNumber' in nameListDf:
        nowKeyDict = df_import.loc[i]['indexNumber'].strip().lower()
        c = '.'
    else:
        nowKeyDict = df_import.loc[i]['compositeTitle'].strip().lower()
        c = '/'
    a = nowKeyDict.split(c)
    b = len(a)
    if b == 1:
        return nowKeyDict, 'root', b
    else:
        lastKeyDict = ''
        for i in range(b - 1):
            if i == b - 2:
                lastKeyDict += a[i]
            else:
                lastKeyDict += a[i] + c
        return nowKeyDict, lastKeyDict, b


# Search type and max length
def searchTypeAndMaxLengthToDictionary(nameListDf, df_import, i):
    if 'type' in nameListDf and 'maxLength' in nameListDf:
        a = df_import.loc[i]['type'].strip().lower()
        b = str(df_import.loc[i]['maxLength']).strip().lower().replace(',', '.')
        if b == 'nan':
            return a, ''
        else:
            return a, b
    elif 'type' in nameListDf and 'compositeType' not in nameListDf:
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
def searchReguiredToDictionary(nameListDf, df_import, i):
    if 'reguired' in nameListDf:
        return df_import.loc[i]['reguired'].strip().lower()


# Create work dictionary from import
def createWorkDictionary(df_import):
    nameListDf = list(df_import)
    indexDfImport = df_import.index
    workDictionary = {}
    for i in indexDfImport:
        titleDict = searchTitleToDictionary(nameListDf, df_import, i)
        nowKeyDict, lastKeyDict, lenNowKeyDict = searchKeysToDictionary(nameListDf, df_import, i)
        reguiredDict = searchReguiredToDictionary(nameListDf, df_import, i)
        typeDict, maxLengthDict = searchTypeAndMaxLengthToDictionary(nameListDf, df_import, i)
        if lenNowKeyDict in workDictionary:
            if lastKeyDict in workDictionary[lenNowKeyDict]:
                workDictionary[lenNowKeyDict][lastKeyDict][nowKeyDict] = [typeDict, titleDict, reguiredDict,
                                                                          maxLengthDict]
            else:
                workDictionary[lenNowKeyDict][lastKeyDict] = {
                    nowKeyDict: [typeDict, titleDict, reguiredDict, maxLengthDict]}
        else:
            workDictionary[lenNowKeyDict] = {
                lastKeyDict: {nowKeyDict: [typeDict, titleDict, reguiredDict, maxLengthDict]}}
    return workDictionary



with open('import.json', 'r') as read_file:
    dict_ = json.load(read_file)
for _ in dict_['xls']:
    for __ in dict_['xls'][_]:
        fileName_, sheetName_ = _, __
        ___ = 0
        try:
            df_import = importAndValidationXlsFile(fileName_, sheetName_)
            ___ = 1
        except FileNotFoundError:
            print('Не найден файл', fileName_)
        except:
            print('Не найден лист', __, 'в файле', _)
        if ___:
            workDictionaryWork = createWorkDictionary(df_import)
            workDictionaryWork, maximumDepth, minimumDepth = validateWorkDictionray(workDictionaryWork)
            dictionaryForJson = createDictionaryForJSON(workDictionaryWork, maximumDepth, minimumDepth)
            fileNameJson = fileName_.replace('.', '_') + '_' + sheetName_ + '_' + str(time.time()) + '.json'
            with open(fileNameJson, 'w') as write_file:
                json.dump(dictionaryForJson, write_file, ensure_ascii=False, indent=4)
