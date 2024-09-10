import pandas as pd
import unidecode
import os


HOME = os.getenv('HOME')
DIRECTORY = 'Downloads'
FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
FILE_PATH = os.path.join(HOME, DIRECTORY, FILE_NAME)
# print(f"File path: {FILE_PATH}")

# start and end sheet names
start_sheet_name = 'A-01 - BARRIOS'
end_sheet_name = 'A-18 - BARRIOS'
column_name = 'B'
row = 2

# read the file, DataFrame
# data = pd.read_excel(FILE_PATH, engine='openpyxl')
# print(f"Data: {data}")
# class ExcelFile, file is a DataFrame
file = pd.ExcelFile(FILE_PATH)
sheet_names = file.sheet_names
# print(f"Sheet names: {sheet_names}")


# data = pd.read_excel(file, sheet_name=sheet_name)
# print(f"Data: \n{data}")

# get the indices of the start and end sheet name
start_index = sheet_names.index(start_sheet_name)
end_index = sheet_names.index(end_sheet_name)


# Loop through the sheets within the specified range
for sheet_name in sheet_names[start_index:end_index+1]:
    data = pd.read_excel(FILE_PATH, sheet_name=sheet_name, usecols=column_name, skiprows=row)
    # data = pd.read_excel(file, sheet_name=sheet_name)
    # Slice the DataFrame to get the column of interest
    # data = data[column_name]
    print(f"Sheet name: {sheet_name}")
    print(f"Data: \n{data}")
    columns = data.columns
    # print(f"Columns: {columns}")


# in a phrase remove spanish accents, special characters, and convert to lowercasephrase
def remove_special_characters(phrase):
    # convert to lowercase
    phrase = phrase.lower()
    # remove accents
    phrase = unidecode.unidecode(phrase)
    # remove special characters
    phrase = ''.join(e for e in phrase if e.isalnum() or e.isspace())
    return phrase

phrase = "MONTE SINAHÍ - BARRIO 1 - SECTOR 7"
# phrase = "Café con leche y azúcar"
# phrase = remove_special_characters(phrase)
# print(f"Processed phrase: {phrase}")

# bollean function to search a substring in a string
def search_substring(substring, string):
    string = remove_special_characters(string)
    print(f"Processed string: {string}")
    print(f"Processed substring: {substring}")
    return substring in string
# search a substring in a string
substring = 'barrio monte sinahi'
string = 'MONTE SINAHÍ - BARRIO 1 - SECTOR 7'
# result = search_substring(substring, string)
# print(f"Substring '{substring}' found in '{string}': {result}")