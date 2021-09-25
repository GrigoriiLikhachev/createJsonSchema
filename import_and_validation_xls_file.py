import pandas
import sys


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
