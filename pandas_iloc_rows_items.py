import os
import pandas as pd
from find_address_in_excel import find_address_in_excel
import time

HOME = os.getenv('HOME')
FILE_NAME = 'Copy of ASISTENCIA A TALLERES (respuestas).xlsx'
DOWNLOADS_PATH = os.path.join(HOME, 'Downloads')
FILE_PATH = os.path.join(DOWNLOADS_PATH, FILE_NAME)
SHEET_NAME = 'Sheet1'
# from 0
SHEET_INDEX = 1
COLUMN1 = 'Ingresa el Barrio en que vives'
COLUMN2 = 'Ingresa tu dirección y una referencia'
NEW_COLUMN_NAME = 'AGA'
NEW_FILE_NAME = f'{FILE_NAME}-{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'

PATTERN_FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
PATTERN_FILE_PATH = os.path.join(DOWNLOADS_PATH, PATTERN_FILE_NAME)

# read the file
def read_file(file_path=FILE_PATH, sheet_name=SHEET_INDEX, columns=None):
    """
    Read the file
    Atributes:
    file_path: str, path to the file
    sheet_name: str, name of the sheet
    columns: list, columns to read
    """
    new_columns_data = []
    positive_new_value_inserted_count = 0
    
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    # count of rows
    row_count = df.shape[0]
    if columns:
        # store in existing_col_index the index of the first value in columns
        existing_col_index = df.columns.get_loc(columns[0])
        df = df[columns]
    else:
        existing_col_index = 0
    for index, row in df.iterrows():
        print(f"Index: {index}")
        new_row = {}
        for header, value in row.items():
            sheet_name_founded = None
            sheet_name_founded = f"{str(value)} checked"
            new_header_name = f"similarity {header}"
            new_row[new_header_name] = sheet_name_founded
            # print(f"Header: {header}, Value: {value}")
            search_address = value
            # Insert the new column to the left of the existing column
            # sheet_name_founded = find_address_in_excel(PATTERN_FILE_PATH, search_address)
            if sheet_name_founded is not None:
                positive_new_value_inserted_count += 1
            else:
                sheet_name_founded = 'No existe'
            
        
        new_columns_data.append(new_row)
        # print(f"new_columns_data: {new_columns_data}")
    print(f"len of new_columns_data: {len(new_columns_data)}")
    print(f"Count of new data: {positive_new_value_inserted_count}")    
    print(f"the number of rows excluding the header or column names: {row_count}")

    return new_columns_data

# Insert the new column to the left of the existing column
# df.insert(existing_col_index, NEW_COLUMN_NAME, new_column_data)
# df.to_excel(NEW_FILE_NAME, sheet_name=sheet_name, index=False)

def make_unique_headers(headers):
    """
    Make headers unique by appending a suffix to duplicate column names.
    """
    seen = {}
    for i, header in enumerate(headers):
        if header in seen:
            seen[header] += 1
            headers[i] = f"{header}_{seen[header]}"
        else:
            seen[header] = 0
    return headers

if __name__ == "__main__":
    print(f"from main: {__name__}")
    # sheet_name = pd.ExcelFile(FILE_PATH).sheet_names[0]
    # sheet_name = pd.ExcelFile(FILE_PATH).sheet_names
    # print(f"Sheet name: {sheet_name}, type: {type(sheet_name)}")

    # df = pd.read_excel(FILE_PATH, sheet_name=1)
    # # count of rows
    # row_count = df.shape[0]
    # print(f"Row count: {row_count}")
    # columns = [COLUMN1, COLUMN2]
    # df = df[columns]
    # for index, row in df.iterrows():
    #     print(f"Index: {index}")
    #     # print(f"Row: {row}, type: {type(row)}\n")
    # #     # column1 = row.iloc[0]
    # #     # column1 = row.iloc[1]
    # #     # print(f"Column1: {column1}")
    # #     # ask for typing enter to continue
    #     for header, value in row.items():
    #         print(f"Header: {header}, Value: {value}")
    #     print("\n")
    #     input("Press Enter to continue...")

    new_column_data = read_file(file_path=FILE_PATH, sheet_name=SHEET_INDEX, columns=[COLUMN1, COLUMN2])
    # ask for typing enter to continue
    input("Press Enter to continue...")
    # create a new dataframe with new_column_data
    df = pd.DataFrame(new_column_data)
    print(f"df: {df}")

    # test make_unique_headers
    # headers = ['a', 'b', 'a', 'b', 'a', 'b']
    # print(make_unique_headers(headers))