import os
import pandas as pd
from find_address_in_excel import find_addres_in_excel
import time

HOME = os.getenv('HOME')
DIRECTORY = 'Downloads'
FILE_NAME = 'Copy of ASISTENCIA A TALLERES (respuestas).xlsx'
FILE_PATH = os.path.join(HOME, DIRECTORY, FILE_NAME)
COLUMN1 = 'Ingresa tu dirección y una referencia'
COLUMN2 = 'Ingresa el Barrio en que vives'
NEW_COLUMN_NAME = 'AGA'
NEW_FILE_NAME = f'AGA-{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'

PATTERN_DIRECTORY = 'Downloads'
PATTERN_FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
PATTERN_FILE_PATH = os.path.join(HOME, DIRECTORY, PATTERN_FILE_NAME)

df = pd.read_excel(FILE_PATH, engine='openpyxl')
# get sheet name
sheet_name = pd.ExcelFile(FILE_PATH).sheet_names[0]
# print(f"Sheet name: {sheet_name}")
data = df[[COLUMN1, COLUMN2]]
# print(f"Data: \n{data}")
# rows
rows = data.shape[0]
new_column_data = []
count = 0
# print(f"Rows: {rows}")

# Find the index of the existing column
existing_col_index = df.columns.get_loc(COLUMN1)
# print(f"Existing column index: {existing_col_index}")


# Save the modified DataFrame to a new Excel file
# df.to_excel(NEW_FILE_NAME, sheet_name=sheet_name, index=False)
# print(f"New Excel file saved as {NEW_FILE_NAME}")

for index, row in data.iterrows():
    address = row[COLUMN1]
    neighborhood = row[COLUMN2]
    print(f"Index: {index}")
    # print(f"Address: {address}")
    # print(f"Neighborhood: {neighborhood}")
    # print("\n")
    # Insert the new column to the left of the existing column
    # new_data = None
    new_data = find_addres_in_excel(PATTERN_FILE_PATH, address)

    if new_data is not None:
        # print(f"New column data: {new_data}")
        count += 1
    else:
        new_data = 'No coinciden'
        # print(f"New column data: {new_data}")
    # Check if the new column already exists
    new_column_data.append(new_data)
    # print(f"new_column_data: {new_column_data}")

# print(f"len of new_column_data: {len(new_column_data)}")    
print(f"Count of new data: {count}")
df.insert(existing_col_index, NEW_COLUMN_NAME, new_column_data)
df.to_excel(NEW_FILE_NAME, sheet_name=sheet_name, index=False)
