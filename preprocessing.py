import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocess the text for extractive summarization.
    Returns original sentences and heavily cleaned sentences (no stopwords/punctuation).
    """
    if not text or text.startswith("Error:"):
        return [], []
        
    # Sentence tokenization
    sentences = sent_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    cleaned_sentences = []
    
    for sentence in sentences:
        # Remove special characters and digits
        clean_s = re.sub(r'[^a-zA-Z\s]', '', sentence)
        # Word tokenization and lowercasing
        words = word_tokenize(clean_s.lower())
        # Remove stop words and short words
        words = [w for w in words if w not in stop_words and len(w) > 1]
        cleaned_sentences.append(" ".join(words))
        
    return sentences, cleaned_sentences

def extract_keywords(cleaned_sentences, top_n=5):
    """
    Extract simple keywords based on word frequencies.
    """
    if not cleaned_sentences:
        return []
        
    all_words = []
    for s in cleaned_sentences:
        all_words.extend(s.split())
        
    freq_dist = nltk.FreqDist(all_words)
    return [word for word, freq in freq_dist.most_common(top_n)]
