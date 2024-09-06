import nltk

# run once to download the NLTK data
# nltk.download('popular')
# nltk.download('punkt_tab')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# edit for spanish words of address
LANGUAGE = 'spanish'
# LANGUAGE = 'english'
def compare_address_similarity(address1, address2, language=LANGUAGE):
    """
    Compares the similarity between two addresses using TF-IDF and cosine similarity.
    """
    # Tokenize the addresses
    stop_words = list(stopwords.words(language))
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    address1 = word_tokenize(address1)
    address2 = word_tokenize(address2)

    # Combine the tokens back into strings
    address1 = ' '.join(address1)
    address2 = ' '.join(address2)

    # Create a matrix of TF-IDF features
    matrix = vectorizer.fit_transform([address1, address2])

    # Calculate the cosine similarity between the vectors
    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]
    return similarity

# Test the function
address1 = "Calle de la Paz, 12, 28001 Madrid, Spain"
address2 = "Calle de la Paz, 12, 28001 Madrid, Spain"
# address2 = "Calle de la Paz, 12, 28001 Madrid, España"
similarity = compare_address_similarity(address1, address2)
print(f"Similarity between the addresses: {similarity}")
# Output: Similarity between the addresses: 0.9999999999999998