import nltk
import re

def prepare_stopwords():
    """Download stopwords and create stemmer for data preprocessing."""
    nltk.download('stopwords')
    stemmer = nltk.stem.PorterStemmer()
    all_stopwords = nltk.corpus.stopwords.words('english')
    all_stopwords.remove('not')
    return stemmer, all_stopwords

def preprocess_data(review, stemmer, words_to_remove):
    """Preprocess data by removing stopwords and punctuation,
       and lower-casing + stemming the words.
    """
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower().split()
    review = [stemmer.stem(w) for w in review if w not in set(words_to_remove)]
    review = ' '.join(review)
    return review