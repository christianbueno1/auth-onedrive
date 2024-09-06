import pandas as pd
import unidecode
import os


HOME = os.getenv('HOME')
DIRECTORY = 'Downloads'
FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
FILE_PATH = os.path.join(HOME, DIRECTORY, FILE_NAME)
# print(f"File path: {FILE_PATH}")

# read the file
data = pd.read_excel(FILE_PATH, engine='openpyxl')
# print(f"Data: {data}")
# class ExcelFile, file is a DataFrame
file = pd.ExcelFile(FILE_PATH)
sheet_names = file.sheet_names
# print(f"Sheet names: {sheet_names}")

# in a phrase remove spanish accents, special characters, and convert to lowercasephrase
phrase = "MONTE SINAHÍ - BARRIO 1 - SECTOR 7"
# phrase = "Café con leche y azúcar"
def remove_special_characters(phrase):
    # convert to lowercase
    phrase = phrase.lower()
    # remove accents
    phrase = unidecode.unidecode(phrase)
    # remove special characters
    phrase = ''.join(e for e in phrase if e.isalnum() or e.isspace())
    return phrase
phrase = remove_special_characters(phrase)
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
result = search_substring(substring, string)
print(f"Substring '{substring}' found in '{string}': {result}")