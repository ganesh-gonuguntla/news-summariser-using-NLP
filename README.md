# 📰 AI News Summarization Engine

An efficient, dynamic Natural Language Processing (NLP) tool that automatically extracts, cleans, and summarizes the content of long news articles.

This project combats information overload by running both **Extractive** algorithms (TextRank) and **Abstractive** deep learning models (Hugging Face BART) side by side. Wrapped in a beautiful Streamlit dashboard, users can scrape live web pages or paste raw text to quickly digest the world's news.

## ✨ Key Features
* 🕷️ **Live Web Scraping:** Point to a URL and automatically extract the main article text (filters out ads, navbars, etc.).
* 📝 **Extractive Summarization:** Uses TF-IDF and NetworkX to algorithmically identify and pull the most critical sentences from the text.
* 🤖 **Abstractive Summarization:** Employs a pre-trained **BART Transformer** (`sshleifer/distilbart-cnn-12-6`) to rewrite and condense stories logically, just like a human reader would.
* 📊 **Sentiment Analysis:** Analyzes the tone of the article via TextBlob, returning Polarity and Subjectivity metrics.
* 🔑 **Keyword Extraction:** Automatically detects the 5 most heavily focused concepts using NLTK frequency distribution.
* 📈 **ROUGE Evaluation:** Test the accuracy of your models against a human-written "reference" summary. 

---

## 🚀 Installation & Setup Steps

Follow these steps to get the project running on your local machine:

**1. Clone the repository**
```bash
git clone https://github.com/ganesh-gonuguntla/news-summariser-using-NLP.git
cd news-summariser-using-NLP
```

**2. Install Python Dependencies**
Make sure you have Python 3 installed. Run the following command to grab all the required packages:
```bash
pip install -r requirements.txt
```

*(Note: NLTK language corpus files like `punkt_tab` and `stopwords` will download automatically the first time you run the script).*

**3. Run the Application!**
Launch the interactive dashboard with Streamlit:
```bash
streamlit run app.py
```

*(This command will automatically open a browser window to `http://localhost:8501`. If it's your first time running an Abstractive Summary, it may take a minute to download the Transformer weights.)*

---

## 🎮 How to Use

1. **Select Input Method:** Use the left sidebar to toggle between providing a live **URL** or pasting **Raw Text**. 
2. **Fetch Article:** If using a URL, click "Fetch Article" and verify that the text was retrieved properly.
3. **Configure Options:** 
   * Adjust the **Extractive Summary Ratio** (e.g., 0.3 leaves exactly 30% of the sentences).
   * Check or uncheck **Sentiment Analysis** and **Abstractive Summarization** toggles. 
4. **Generate!** Click the primary **"Generate Summaries"** button.
5. *(Optional)* Scroll down and paste a reference summary to instantly benchmark the models and receive a **ROUGE** score.

## 🛠️ Built With
* **Language:** Python
* **Frontend:** Streamlit 
* **Deep Learning:** HuggingFace `transformers`, PyTorch
* **Data Processing/NLP:** NLTK, TextBlob, Scikit-Learn, NetworkX
* **Scraping:** BeautifulSoup4, Requests
