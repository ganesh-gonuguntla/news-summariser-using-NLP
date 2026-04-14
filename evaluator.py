from rouge_score import rouge_scorer
from textblob import TextBlob

def calculate_rouge(hypothesis, reference):
    """
    Calculates ROUGE-1, ROUGE-2, and ROUGE-L scores between a hypothesis (generated summary)
    and a reference (ground truth summary).
    """
    if not hypothesis or not reference:
        return None
        
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    
    return {
        key: {
            'precision': round(value.precision, 4),
            'recall': round(value.recall, 4),
            'fmeasure': round(value.fmeasure, 4)
        }
        for key, value in scores.items()
    }

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the text using TextBlob.
    Returns polarity (-1 to +1) and subjectivity (0 to 1), along with a descriptive label.
    """
    if not text:
        return {"label": "Neutral", "polarity": 0.0, "subjectivity": 0.0}
        
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        label = "Positive 😊"
    elif polarity < -0.1:
        label = "Negative 😞"
    else:
        label = "Neutral 😐"
        
    return {
        "label": label,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2)
    }
