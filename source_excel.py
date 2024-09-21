import os
import pandas as pd
from find_address_in_excel import find_address_in_excel
import time

HOME = os.getenv('HOME')
FILE_NAME = 'Copy of ASISTENCIA A TALLERES (respuestas).xlsx'
DOWNLOADS_PATH = os.path.join(HOME, 'Downloads')
FILE_PATH = os.path.join(DOWNLOADS_PATH, FILE_NAME)
SHEET_NAME = 'Sheet2'
# from 0
SHEET_INDEX = 1
COLUMN1 = 'Ingresa el Barrio en que vives'
COLUMN2 = 'Ingresa tu dirección y una referencia'
COLUMN3 = 'Ingresa la Parroquia a la que pertenece tu Sector'
NEW_COLUMNS_NAME = ['AGA', 'address']

NEW_FILE_NAME = f'{FILE_NAME}-{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
NEW_FILE_NAME_PATH = os.path.join(DOWNLOADS_PATH, NEW_FILE_NAME)

PATTERN_FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
PATTERN_FILE_PATH = os.path.join(DOWNLOADS_PATH, PATTERN_FILE_NAME)

# read the file
def read_file(file_path=FILE_PATH, sheet_name=SHEET_INDEX, columns=[COLUMN1, COLUMN2, COLUMN3], new_columns_name=NEW_COLUMNS_NAME) -> list:
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
        sheet_name_founded = None
        address_pattern = None
        print(f"Index: {index}")
        new_row = {}
        county = row.values[2]
        # print(f"county: {county}")
        # ask to type enter
        # input("Press Enter to continue...")
        for header, value in row.items():
            # if header == columns[2] break
            if header == columns[2]:
                continue
            # sheet_name_founded = None
            # sheet_name_founded = f"{str(value)} checked"
            # new_header_name = f"similarity {header}"
            # new_row[new_header_name] = sheet_name_founded
            # print(f"Header: {header}, Value: {value}")
            search_address = value
            # Insert the new column to the left of the existing column
            sheet_name_founded, address_pattern = find_address_in_excel(PATTERN_FILE_PATH, search_address, county)
            # ask to type enter
            # input("Press Enter to continue...*")
            if sheet_name_founded is not None:
                positive_new_value_inserted_count += 1
                if sheet_name_founded:
                    break
            else:
                sheet_name_founded = 'No coincide'    
                address_pattern = 'No coincide'
        new_row[new_columns_name[0]] = sheet_name_founded
        new_row[new_columns_name[1]] = address_pattern
        new_columns_data.append(new_row)
        print(f"new_columns_data: {new_columns_data}")
        # ask to type enter to continue
        # input("Press Enter to continue...*")
    print(f"len of new_columns_data: {len(new_columns_data)}")
    print(f"Count of new data: {positive_new_value_inserted_count}")    
    print(f"the number of rows excluding the header or column names: {row_count}")
    # ask to type enter
    # input("Press Enter to continue...*")

    return new_columns_data

# function to insert columns new_columns_data in a excel file, but create a new file
def insert_column_in_excel(file_path, sheet_name, col_index, new_columns_data) -> pd.DataFrame:
    """
    Insert the new column in the excel file
    Attributes:
    file_path: str, path to the file
    sheet_name: str, name of the sheet
    col_index: str, name of the column
    new_columns_data: list, data to insert
    new_columns_name: list, name of the new columns
    """
    try:
       # Creating a new DataFrame from the list of dictionaries
        new_df = pd.DataFrame(new_columns_data)
        # read the file
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        # Insert the new column to the left of the existing column
        existing_col_index = df.columns.get_loc(col_index)
        # Insert the new column to the left of the existing column
        df = pd.concat([df.iloc[:, :existing_col_index], new_df, df.iloc[:, existing_col_index:]], axis=1)
        # print df NEW_COLUMNS_NAME and 2 columns before
        # print(f"df: {df[df.columns[existing_col_index-2:]]}")
        # print columsn 9, 10, 11
        # print(f"df: {df[df.columns[8:12]]}")
        return df
    except Exception as e:
        print(f"Error: {e}")

# function to create a new excel file from pd.DataFrame
def create_new_excel_file(df: pd.DataFrame, new_file_name=NEW_FILE_NAME, sheet_name=SHEET_NAME):
    """
    Create a new excel file from pd.DataFrame
    Atributes:
    df: pd.DataFrame, data to insert
    new_file_name: str, name of the new file
    sheet_name: str, name of the sheet
    """
    try:
        df.to_excel(new_file_name, sheet_name=sheet_name, index=False)
        # print a success message
        print(f"New file created: {new_file_name}")
    except Exception as e:
        print(f"Error: {e}")

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

    new_columns_data = read_file(file_path=FILE_PATH, sheet_name=SHEET_INDEX)
    # len of new_column_data
    # print(f"len of new_column_data: {len(new_column_data)}")
    # create a new excel file with new_columns_data
    df: pd.DataFrame = insert_column_in_excel(file_path=FILE_PATH, sheet_name=SHEET_INDEX, col_index=COLUMN2, new_columns_data=new_columns_data)
    # print df only NEW_COLUMNS_NAME
    # print(f"df: {df[NEW_COLUMNS_NAME]}")
    # create a new excel file
    create_new_excel_file(df, new_file_name=NEW_FILE_NAME_PATH, sheet_name=SHEET_NAME)
    # ask for typing enter to continue
    # input("Press Enter to continue...")
    # create a new dataframe with new_column_data
    # df = pd.DataFrame(new_column_data)
    # print(f"df: {df}")