import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Summarizer:
    def __init__(self):
        self.ab_model = None
        self.tokenizer = None
        
    def load_abstractive_model(self):
        if self.ab_model is None:
            model_name = "sshleifer/distilbart-cnn-12-6"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.ab_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def extractive_summarization(self, original_sentences, cleaned_sentences, ratio=0.3):
        """
        Extractive summarization using TextRank algorithm.
        """
        if not original_sentences or not cleaned_sentences:
            return ""
            
        num_sentences = max(1, int(len(original_sentences) * ratio))
        
        # If there are very few sentences, return the whole text
        if len(original_sentences) <= num_sentences or len(original_sentences) <= 1:
            return " ".join(original_sentences)
            
        # Create TF-IDF matrix for the cleaned sentences
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
        except ValueError:
            return " ".join(original_sentences[:num_sentences])
            
        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Create a graph and apply PageRank
        nx_graph = nx.from_numpy_array(similarity_matrix)
        try:
            scores = nx.pagerank(nx_graph)
        except nx.PowerIterationFailedConvergence:
            scores = {i: 1.0 for i in range(len(original_sentences))}
            
        # Rank sentences
        ranked_sentences = sorted(((scores[i], s, i) for i, s in enumerate(original_sentences)), reverse=True)
        
        # Select top N sentences and sort them by original order
        top_sentences = sorted(ranked_sentences[:num_sentences], key=lambda x: x[2])
        
        summary = " ".join([s[1] for s in top_sentences])
        return summary
        
    def abstractive_summarization(self, text, min_length=30, max_length=130):
        """
        Abstractive summarization using Hugging Face transformers.
        """
        self.load_abstractive_model()
        
        try:
            inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = self.ab_model.generate(
                inputs["input_ids"], 
                max_length=max_length, 
                min_length=min_length, 
                num_beams=4, 
                early_stopping=True
            )
            return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error generating abstractive summary: {str(e)}"
