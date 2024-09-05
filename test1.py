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
# compare the similairty of the 2 addresses, the language used in the addresses is spanish.

def preprocess_text(text):
    """
    Preprocesses the input text by tokenizing and removing stopwords.
    """
    stop_words = set(stopwords.words(LANGUAGE))
    # Extend the stop words with additional words
    additional_stop_words = {
        'calle', 'avenida', 'plaza', 'carrera', 'camino', 'paseo', 'barrio', 'ciudad', 'provincia', 'pais', 'numero'
    }
    stop_words.update(additional_stop_words)
    print(f"Stop words in {LANGUAGE}: {stop_words}")

    word_tokens = word_tokenize(text.lower())
    filtered_text = [word for word in word_tokens if word.isalnum() and word not in stop_words]

    return " ".join(filtered_text)

def calculate_similarity(text1, text2):
    """
    Calculates the cosine similarity between two input texts.
    """
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([preprocessed_text1, preprocessed_text2])

    return cosine_similarity(tfidf_matrix)[0][1]
    
def main():
    address1 = "Calle de la Princesa, 1, 28008 Madrid, Spain"
    address2 = "Calle Princesa, 1, 28008 Madrid, España"

    similarity = calculate_similarity(address1, address2)
    print(f"Similarity between the addresses: {similarity}")

if __name__ == "__main__":
    main()