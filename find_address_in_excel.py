import pandas as pd
import unidecode
import os
# run once to download the NLTK data
# import nltk
# nltk.download('popular')
# nltk.download('punkt_tab')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import unidecode


# patterns
HOME = os.getenv('HOME')
DOWNLOADS_PATH = os.path.join(HOME, 'Downloads')
FILE_NAME = 'AGA - LIM_POB_PARR_BARR 07-2024.xlsx'
FILE_PATH = os.path.join(DOWNLOADS_PATH, FILE_NAME)
# print(f"File path: {FILE_PATH}")

# start and end sheet names
START_SHEET_NAME = 'A-01 - BARRIOS'
END_SHEET_NAME = 'A-18 - BARRIOS'
COLUMN_NAME = 'B'
# remove the first row
ROW_START = 1
BASE_PERCENTAGE_SIMILARITY = 0.6
BOOST = 0.2

def find_address_in_excel(file_name, search_address, start_sheet_name=START_SHEET_NAME, end_sheet_name=END_SHEET_NAME, column_name=COLUMN_NAME, row_start=ROW_START, base_percentage_similarity=BASE_PERCENTAGE_SIMILARITY):
    """
    Find the address in the excel file
    """
    header = 'Unnamed: 1'
    max_similarity = base_percentage_similarity
    address_find = None
    sheet_name_find = None

    sheets_dict = pd.read_excel(file_name, sheet_name=None, usecols=column_name)
    for sheet_name, df in sheets_dict.items():
        if sheet_name < start_sheet_name or sheet_name > end_sheet_name:
            continue
        print(f"Sheet namee: {sheet_name}")
        # remove the first row
        df = df.iloc[row_start:]
        # apply compare_address_similarity function to the data
        count_rows = len(df)
        count_rowss = 0
        for index, row in df.iterrows():
            # address to str
            address = str(row.values[0])
            if not pd.isna(address):
                # similarity = compare_address_similarity(search_address, address)
                # exists_in = is_address_in_address(search_address, address)
                # if exists_in:
                #     similarity = 1
                # else:
                #     # similarity = compare_address_similarity(search_address, address)
                #     similarity = 0.6
                # if similarity > max_similarity:
                #     max_similarity = similarity
                #     address_find = address
                #     sheet_name_find = sheet_name
                    # print(f"Sheet name: {sheet_name}")
                    # print(f"Similarity: {similarity}")
                    # print(f"Found address: {address}\n")
                pass
            count_rowss += 1
        #     if similarity == 1:
        #         break
        # if max_similarity == 1:
        #     break
        if count_rowss == count_rows:
            print(f"row variables are equal")
        else:
            print(f"row variables are not equal")
        print(f"count_rows: {count_rows}, count_rowss: {count_rowss}\n")
        # ask for typing enter
        input("Press Enter to continue...")


    
    print(f"Max similarity: {max_similarity}")
    print(f"address: {search_address}")
    print(f"Found address: {address_find}\n")
    # print(f"Sheet name: {sheet_name_find}")

    return sheet_name_find




# edit for spanish words of address
LANGUAGE = 'spanish'
# LANGUAGE = 'english'
# function using TF-IDF and cosine similarity
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

# function using in operator
def is_address_in_address(address1, address2):
    """
    Check if address1 is in address2 or vice versa
    """
    return address1.lower() in address2.lower() or address2.lower() in address1.lower()

# test the function
# search_address = "PRE-COOP. UNION DE BANANEROS BLOQUE 4"
# search_address = "Isla trinitaria coop luz de América "
# search_address = "La 14 y 4 de noviembre "
# search_address = "barrio lindo"
# sheet_name = find_address_in_excel(FILE_PATH, search_address)
# print(f"Sheet name: {sheet_name}")

if __name__=="__main__":
    
    search_address = "flor de bastion bloque 119"
    sheet_name = find_address_in_excel(FILE_PATH, search_address)
    print(f"Sheet name: {sheet_name}")
    # search_address = "maria auxiliadora"
    # search_address = "paraiso de la flor"
    # name = 'christian'
    # name2 = name.join(['a', 'b'])
    # print(f"Name2: {name2}")
    # search_address = "balerio estacio 7"
    # search_address1 = "balerio estacio"
    # search_address1 = "Ciudad"
    # search_address2 = "COOP. BALERIO ESTACIO BLOQUE 3 LÁMINA 1"
    

    # search_address = "Isla trinitaria coop luz de América "
    # sheet_name = find_address_in_excel(FILE_PATH, search_address)
    # print(f"Sheet name: {sheet_name}")

    # search_address = "La 14 y 4 de noviembre "
    # sheet_name = find_address_in_excel(FILE_PATH, search_address)
    # print(f"Sheet name: {sheet_name}")

    # search_address = "barrio lindo"
    # sheet_name = find_address_in_excel(FILE_PATH, search_address)
    # print(f"Sheet name: {sheet_name}")