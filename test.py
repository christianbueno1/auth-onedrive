import nltk
import uuid
import time
# run once to download the NLTK data
# nltk.download('popular')
# nltk.download('punkt_tab')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import unidecode

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
    print(f"Address1: {address1}")
    print(f"Address2: {address2}")

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
    return phrase

# Test the function
# address1 = "Calle de la Paz, 12, 28001 Madrid, Spain"
address1 = "MONTE SINAHÍ BARRIO 1 SECTOR 7"
# address2 = "Calle de la Paz, 12, 28001 Madrid, Spain"
# address2 = "Calle de la Paz, 12, 28001 Madrid, España"
address2 = "BARRIO MONTE SINAHÍ"
similarity = compare_address_similarity(address1, address2)
print(f"Similarity between the addresses: {similarity}")
# Output: Similarity between the addresses: 0.9999999999999998
# unique_name = f'AGA-{uuid.uuid4()}.xlsx'
# add date and time to the unique name
unique_name = f'AGA-{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
print(f"Unique name: {unique_name}")