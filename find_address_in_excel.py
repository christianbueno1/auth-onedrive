import pandas as pd
import unidecode
import os
# import nltk

# run once to download the NLTK data
# nltk.download('popular')
# nltk.download('punkt_tab')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import unidecode



HOME = os.getenv('HOME')
DIRECTORY = 'Downloads'
FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
FILE_PATH = os.path.join(HOME, DIRECTORY, FILE_NAME)
# print(f"File path: {FILE_PATH}")

# start and end sheet names
START_SHEET_NAME = 'A-01 - BARRIOS'
END_SHEET_NAME = 'A-18 - BARRIOS'
COLUMN_NAME = 'B'
# remove the first row
ROW_START = 1
BASE_PERCENTAGE_SIMILARITY = 0.6

def find_addres_in_excel(file_name, search_address, start_sheet_name=START_SHEET_NAME, end_sheet_name=END_SHEET_NAME, column_name=COLUMN_NAME, row_start=ROW_START, base_percentage_similarity=BASE_PERCENTAGE_SIMILARITY):
    """
    Find the address in the excel file
    """
    header = 'Unnamed: 1'
    max_similarity = base_percentage_similarity
    address_find = None
    sheet_name_find = None
    # class ExcelFile, file is a DataFrame
    file = pd.ExcelFile(file_name)
    sheet_names = file.sheet_names

    # get the indices of the start and end sheet name
    start_index = sheet_names.index(start_sheet_name)
    end_index = sheet_names.index(end_sheet_name)

    # Loop through the sheets in the column column_name, skip the row row, within the specified range
    for sheet_name in sheet_names[start_index:end_index+1]:
        data = pd.read_excel(file_name, sheet_name=sheet_name, usecols=column_name)
        # print(f"Sheet name: {sheet_name}")
        data = data.iloc[row_start: , :]
        # rows = data.shape[0]
        # columns = data.columns
        # print(f"Rows: {rows}")
        # apply compare_address_similarity function to the data
        for index, row in data.iterrows():
            address = row[header]
            # print(f"Address: {address}")
            if not pd.isna(address):
                similarity = compare_address_similarity(search_address, address)
                if similarity >= max_similarity:
                    # print(f"index: {index}")
                    max_similarity = similarity
                    address_find = address
                    sheet_name_find = sheet_name
                    # print(f"Similarity: {similarity}")
                    # print(f"Found address: {address}")
                    if similarity == 1:
                        break
        if max_similarity == 1:
            break



    
    # print(f"Max similarity: {max_similarity}")
    # print(f"address: {search_address}")
    # print(f"Found address: {address_find}")
    # print(f"Sheet name: {sheet_name_find}")

    return sheet_name_find


    

# edit for spanish words of address
LANGUAGE = 'spanish'
# LANGUAGE = 'english'
def compare_address_similarity(address1, address2, language=LANGUAGE):
    """
    Compares the similarity between two addresses using TF-IDF and cosine similarity.
    """
    # print(f"Address1: {address1}")
    # print(f"Address2: {address2}")
    
    # Tokenize the addresses
    stop_words = list(stopwords.words(language))
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    address1 = word_tokenize(address1)
    address2 = word_tokenize(address2)
    # print(f"Address1: {address1}")
    # print(f"Address2: {address2}")

    # Remove special characters
    address1 = [remove_special_characters(word) for word in address1]
    address2 = [remove_special_characters(word) for word in address2]
    # print(f"Address1: {address1}")
    # print(f"Address2: {address2}")

    # Combine the tokens back into strings
    address1 = ' '.join(address1)
    address2 = ' '.join(address2)

    # Create a matrix of TF-IDF features
    matrix = vectorizer.fit_transform([address1, address2])

    # Calculate the cosine similarity between the vectors
    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]
    return similarity

def remove_special_characters(phrase):
    # convert to lowercase
    phrase = phrase.lower()
    # remove accents
    phrase = unidecode.unidecode(phrase)
    # remove special characters
    phrase = ''.join(e for e in phrase if e.isalnum() or e.isspace())
    # remove leading and trailing whitespaces
    phrase = phrase.strip()
    return phrase

# test the function
# search_address = "PRE-COOP. UNION DE BANANEROS BLOQUE 4"
# search_address = "Isla trinitaria coop luz de América "
# search_address = "La 14 y 4 de noviembre "
# search_address = "barrio lindo"
# sheet_name = find_addres_in_excel(FILE_PATH, search_address)
# print(f"Sheet name: {sheet_name}")