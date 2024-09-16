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
COLUMNS = 'B, C'
# remove the first row
ROW_START = 1
BASE_PERCENTAGE_SIMILARITY = 0.6
BOOST = 0.2
LEVEL = 0
HEADER_ROW = 1

def find_address_in_excel(file_name, search_address, search_county, start_sheet_name=START_SHEET_NAME, end_sheet_name=END_SHEET_NAME, columns=COLUMNS, header_row=HEADER_ROW, row_start=ROW_START, base_percentage_similarity=BASE_PERCENTAGE_SIMILARITY, level=LEVEL):
    """
    Find the address in the excel file
    """
    header = 'Unnamed: 1'
    max_similarity = base_percentage_similarity
    address_find = None
    county_find = None
    sheet_name_find = None
    count_all_sheet_coincidences = 0
    sheets_dict = pd.read_excel(file_name, sheet_name=None, header=header_row, usecols=columns)
    for sheet_name, df in sheets_dict.items():
        if sheet_name < start_sheet_name or sheet_name > end_sheet_name:
            continue
        print(f"Sheet namee: {sheet_name}")
        # remove the first row
        # print(f"df: {df}")
        df = df.iloc[row_start:]
        # apply compare_address_similarity function to the data
        # count_rows = len(df)
        for index, row in df.iterrows():
            # address to str
            # print(f"Row: {row} row.values: {row.values}")
            address = str(row.values[0])
            # parroquias
            county = str(row.values[1])
            if not pd.isna(address):
                match level:
                    case 0:
                        address_in_address = is_address_in_address(search_address, address)
                        county_eq = is_county_equals(search_county, county)
                        similarity = address_in_address and county_eq
                        if similarity:
                            if not(is_both_address_one_word(search_address, address)) and not(is_both_address_more_than_one_word(search_address, address)):
                                similarity = False
                    case 1:
                        similarity = compare_address_similarity(search_address, address)
                # use equal to know if there is a match                        
                if similarity >= max_similarity:
                    count_all_sheet_coincidences += 1
                    max_similarity = similarity
                    address_find = address
                    county_find = county
                    sheet_name_find = sheet_name
                    # print(f"Sheet name: {sheet_name}")
                    # print(f"Similarity: {similarity}")
                    print(f"Found address: {address}, county: {county}")
                    # print(f"max_similarity: {max_similarity}")
                    # ask to type enter
                    # input("Press Enter to continue...")
        #     if similarity == 1:
        #         break
        # if max_similarity == 1:
        #     break


    
    print(f"\nMax similarity: {max_similarity}")
    print(f"address: {search_address}")
    print(f"Found address(pattern): {address_find}")
    print(f"Found county(pattern): {search_county}")
    print(f"Sheet name: {sheet_name_find}")
    print(f"Count of all coincidences: {count_all_sheet_coincidences}")
    # ask for typing enter
    input("Press Enter to continue...\n")

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

# remove special characters and convert to lowercase
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

# check if counties are equals
def is_county_equals(county1, county2) -> bool:
    """
    Check if county1 is equals to county2
    """
    county1 = remove_special_characters(county1)
    county2 = remove_special_characters(county2)
    return county1 == county2

# function using in operator
def is_address_in_address(address1, address2) -> bool:
    """
    Check if address1 is in address2 or vice versa
    """
    result = False
    # remove special characters and convert to lowercase
    address1 = remove_special_characters(address1)
    address2 = remove_special_characters(address2)
    return address1 in address2 or address2 in address1    
    

# check if address1 and address2 have both one word
def is_both_address_one_word(address1, address2) -> bool:
    """
    Check if address1 and address2 have both one word
    """
    address1 = address1.split()
    address2 = address2.split()
    return len(address1) == 1 and len(address2) == 1

# check if address1 and address2 have both more than one word
def is_both_address_more_than_one_word(address1, address2) -> bool:
    """
    Check if address1 and address2 have both more than one word
    """
    address1 = address1.split()
    address2 = address2.split()
    return len(address1) > 1 and len(address2) > 1


if __name__=="__main__":
    
    # search_address = "guayacanes"
    search_address = "los ángeles"
    # search_address = "Coop los ángeles mz 487 sl 6"
    # search_address = "Coop los ángeles"
    county = "parroquia ximena"
    # county = "parroquia tarqui"
    # address2 = "COOP. FLOR DE BASTIÓN BLOQUE 13"
    # similarity = is_address_in_address(search_address, address2)
    # print(f"Similarity: {similarity}")
    sheet_name = find_address_in_excel(FILE_PATH, search_address, county)
    print(f"Sheet name: {sheet_name}")

    # sheets_dict = pd.read_excel(FILE_PATH, sheet_name=None, header=HEADER_ROW, usecols='B, C')
    # print(f"Sheet dict: {sheets_dict}")

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