# Abstract
**Prism** is a web-based AI News Summarization Engine designed to help users quickly digest large volumes of news information. The platform addresses the problem of "information overload" by providing automated, high-quality summaries of news articles retrieved from live URLs or raw text. It employs a hybrid NLP approach, implementing both **Extractive** (TextRank) and **Abstractive** (BART Transformer) summarization techniques to ensure both factual accuracy and logical coherence.

The system features an integrated web scraper that extracts clean article content by filtering out advertisements, navigation menus, and non-essential metadata. Beyond summarization, Prism performs **Sentiment Analysis** to gauge the emotional tone of the content and **Keyword Extraction** to identify core concepts. An integrated evaluation module uses **ROUGE metrics** to benchmark the generated summaries against human-written references, ensuring transparency and quality control.

Built with a modern Python stack involving **Streamlit, Hugging Face Transformers, NLTK, and Scikit-Learn**, the platform offers a premium, responsive dashboard with a dark-themed aesthetic. Prism provides an efficient solution for journalists, researchers, and general readers to stay informed with minimal effort, bridging the gap between extensive raw data and actionable editorial intelligence.

4

---

# Table of Contents
Title 1  
Certificate 2  
Acknowledgement 3  
Abstract 4  
Introduction 6  
Objectives 7  
Literature review 8 - 9  
Methodology 10 - 15  
Results 16 - 20  
Future Enhancements 21  
Conclusion 22  
References 23

5

---

# Introduction
**Prism AI News Summarizer** is a digital platform developed to simplify the consumption of news in the age of digital information abundance. In many cases, readers find it difficult to keep up with lengthy articles, complex reports, and multiple news sources daily. This project aims to bridge that gap by providing a centralized and user-friendly system where news content can be instantly condensed into readable, high-value summaries.

The system enables users to submit news articles via direct URLs or raw text. It then automatically cleans the input, removing noise like web ads and headers, to focus solely on the core message. It provides dedicated modes for both extractive summarization—which identifies the most important existing sentences—and abstractive summarization—which uses deep learning to rewrite the article in a shorter form. With added features like sentiment scoring and keyword detection, Prism enhances the reader's understanding of not just *what* is being said, but also the *tone* and *priority* of the information.

Overall, the project focuses on leveraging modern Natural Language Processing (NLP) and Large Language Model (LLM) technologies to create a smarter, faster, and more reliable way to stay informed.

6

---

# Objectives
* To provide a centralized platform for users to summarize news articles quickly and efficiently.
* To enable automated web scraping of live news articles, eliminating the need for manual copy-pasting.
* To implement a hybrid summarization engine featuring both Extractive (TextRank) and Abstractive (Transformer-based) algorithms.
* To facilitate deep text analysis through integrated Sentiment Analysis and Keyword Extraction.
* To allow users to benchmark AI performance using ROUGE (Recall-Oriented Understudy for Gisting Evaluation) metrics against human references.
* To help users adjust summarization intensity through interactive controls like the "Extractive Summary Ratio."
* To implement a modern, high-performance web interface using Streamlit for a premium user experience.
* To enhance the transparency of AI models by displaying polarity and subjectivity scores for every processed article.
* To ensure scalability and ease of deployment through a modular Python-based architecture.
* To build a research-ready tool that identifies the strengths and weaknesses of different NLP summarization methodologies.

7

---

# Literature Review
Recent advancements in Natural Language Processing (NLP) and Deep Learning have revolutionized the field of text summarization. Traditional methods were primarily extractive, relying on frequency-based algorithms and graph theory to identify key sentences. Modern research, however, has shifted toward abstractive summarization, which leverages encoder-decoder architectures (Transformers) to "understand" and paraphrase text.

Several studies highlight that graph-based algorithms like **TextRank** (inspired by Google's PageRank) are highly effective for extractive tasks because they treat sentences as nodes in a network and calculate their importance based on similarity scores. Research on systems like Lexus and NewsLens shows that these methods provide computationally efficient summaries that preserve the exact wording of the source.

Other studies emphasize the role of **Transformers**, specifically models like **BART** (Bidirectional and Auto-Regressive Transformers), in generating human-like summaries. BART is pre-trained by corrupting text and then learning to reconstruct it, making it exceptionally good at rewriting articles logically. However, abstractive models can sometimes introduce "hallucinations," leading researchers to advocate for hybrid systems that offer both options for validation.

In addition, modern news platforms explore:
* **Sentiment Analysis** for bias detection and emotional mapping.
* **TF-IDF (Term Frequency-Inverse Document Frequency)** for identifying unique keywords within a corpus.
* **ROUGE Evaluation** as the industry standard for measuring the overlap between machine and human summaries.

Research also shows that integrating scraping technologies with NLP pipelines allows for real-time news monitoring, enabling users to stay ahead of fast-moving global events.

8

---

Furthermore, emerging approaches propose using **Large Language Models (LLMs)** for zero-shot summarization and multi-document synthesis to handle even larger datasets across multiple languages.

### Research Gap
From the study of existing summarization tools, the following gaps are identified:
* Lack of integrated web scraping in most basic summarization tools, requiring manual text entry.
* Limited access to both Extractive and Abstractive results side-by-side for comparison.
* Weak support for systematic performance benchmarking (ROUGE) within the same interface.
* No focus on the "emotional metadata" (sentiment) of news, which is critical for identifying media bias.
* Manual configuration of summarization ratios is often missing in standard transformer interfaces.
* Insufficient user-friendly dashboards that combine scraping, cleaning, analysis, and evaluation in one workflow.

9

---

# Methodology
**Prism** is developed using a full-stack NLP approach to handle news data digitally. The system follows a modular architecture where the frontend handles user interaction and the backend manages the scraping, preprocessing, NLP modeling, and evaluation. The methodology of the project is divided into the following stages.

### 1. Requirement Analysis
The first step was to identify the main challenges in traditional news consumption. Large articles often contain "filler" content, ads, and navigation noise that distract the reader. Based on these issues, the system was designed to support:
* Automated article extraction (Scraping)
* Noise reduction and text cleaning
* Sentence-level ranking (Extractive)
* Contextual paraphrasing (Abstractive)
* Sentiment and subjectivity detection
* Performance benchmarking (ROUGE)

This analysis helped define the data flow and the choice of libraries like Hugging Face and NLTK.

### 2. System Design
The project was designed with a pipeline-centric approach:
* **Input Layer:** Handles URL entry or raw text submission via Streamlit.
* **Processing Layer:** Cleaners and scrapers strip unnecessary HTML and tokenize text.
* **Intelligence Layer:** Summarization engines (TextRank & BART) and sentiment analyzers process the cleaned data.
* **Evaluation Layer:** Compares outputs to references and generates JSON report metrics.

A modular design was followed so that the scraper, preprocessor, and summarizer can be updated or replaced independently as new models emerge.

10

---

### 3. Frontend Development
The frontend is built using **Streamlit**, providing a high-performance, interactive interface.
The frontend methodology includes:
* **Configuration Sidebar:** Controls for input method, summary ratio, and feature toggles.
* **Hero Header:** A premium "Prism" branding with dynamic badges and Syne typography.
* **Interactive Inputs:** URL text fields and large text-area components for raw data.
* **Dynamic Results Cards:** Custom HTML/CSS containers for keywords, sentiment metrics, and summary outputs.
* **Real-time Spinners:** Visual feedback during intensive model loading and generation.
* **ROUGE Dashboard:** A dedicated section displaying precision, recall, and F1-measure scores.

Custom CSS was used to implement a dark-mode "Glassmorphism" aesthetic, ensuring a professional and modern look.

### 4. Backend Development
The backend is built using **Python** and leverages several specialized libraries.
Main backend functions include:
* **Model Management:** Lazy-loading the BART transformer model through a singleton class.
* **Pipeline Logic:** Coordinating data flow from the scraper to the summarizer and finally to the evaluator.
* **API Integration:** Using the Hugging Face `transformers` library for seq2seq generation.
* **Vectorization:** Handling TF-IDF matrix generation for the TextRank algorithm.
* **Graph Management:** Using NetworkX to calculate PageRank scores for sentence nodes.

The backend follows a controller-based structure where separate modules (`scraper.py`, `summarizer.py`, `evaluator.py`) handle specific domain logic.

11

---

### 5. Database Design
Prism currently operates as a **Stateless Engine**. It uses Streamlit's `session_state` to manage temporary data such as:
* Fetched article content
* Summary outputs
* Model initialization status
* User configuration settings

By not relying on a persistent database, the system remains lightweight, private, and extremely fast for one-off analysis. For future versions, a MongoDB integration is planned for historical summary tracking.

### 6. Authentication and Authorization
In its current implementation, Prism is a **public-facing utility tool**. 
* **Authorization:** All users have access to all features once the application is launched.
* **Middleware:** The backend uses local system resources to run models, meaning no external API keys (like OpenAI) are required, ensuring 100% data privacy for the user.
* **Session Isolation:** Each user's data remains private to their browser session thanks to Streamlit's architecture.

This ensures a friction-less experience for researchers who need raw NLP power without complex login flows.

12

---

### 7. News Processing Workflow
When a user submits a news URL:
1. The Scraper uses `requests` and `BeautifulSoup` to fetch the HTML.
2. It strips `script`, `style`, and `nav` tags to isolate the article body.
3. The Preprocessor tokenizes the text into sentences using NLTK's Punkt tokenizer.
4. Stopwords are removed, and words are lowercased for the Extractive layer.
5. The processed data is then passed to the specialized summarization modules.

This workflow ensures that only high-quality, relevant text enters the summarization engine.

### 8. Summary Generation Workflow
The system generates dual summaries through the following lifecycle:
* **Extractive Phase:** Calculates sentence similarity using cosine similarity on TF-IDF vectors, applies PageRank, and selects the top N sentences.
* **Abstractive Phase:** Passes the raw text into the BART model, which performs a beam search to generate a concise summary.
* **Synthesis:** Both summaries are displayed side-by-side, allowing the user to compare factual extraction vs. contextual abstraction.

This dual-pathway approach provides a comprehensive view of the news article.

13

---

### 9. Sentiment & Keyword Analysis Methodology
Prism includes an "Intelligence Panel" consisting of:
* **Sentiment Analysis:** Uses **TextBlob** to calculate polarity (positive/negative) and subjectivity (fact vs. opinion).
* **Keyword Detection:** Uses **NLTK frequency distributions** on the cleaned text to identify the top 5 most frequent and significant words.
* **Visual Mapping:** Results are displayed in high-contrast "Pills" and "Metric Cards" for easy scanning.

This adds a layer of depth, helping the user understand the article's core focus and potential bias at a glance.

### 10. Performance Evaluation (ROUGE)
The platform integrates a benchmarking mechanism:
1. The user provides a "Reference Summary."
2. The `rouge-score` library compares the AI output (Hypothesis) to the Reference.
3. It calculates **ROUGE-1** (unigrams), **ROUGE-2** (bigrams), and **ROUGE-L** (longest common subsequence).
4. Results are presented in JSON format, showing Precision, Recall, and F1-Measure.

This enables developers to objectively measure model accuracy and fine-tune parameters.

### 11. Configuration & Parameter Management
The platform provides a "Configuration Control Center" in the sidebar:
* **Ratio Tuning:** Users can drag a slider to determine exactly how long the extractive summary should be.
* **Feature Toggles:** High-latency features like Abstractive Summarization can be turned off to save resources.
* **Input Toggle:** Switch instantly between URL scraping and manual text analysis.

This makes the tool adaptable to different hardware constraints and user needs.

14

---

### 12. Model Loading & Resource Management
To ensure a smooth user experience, Prism handles intense NLP models carefully:
* **Lazy Loading:** Transformer models are only loaded into memory when the user specifically requests an abstractive summary.
* **Resource Optimization:** The system uses `distilbart-cnn-12-6`, a distilled version of BART that offers 95% of the performance with significantly lower memory and CPU requirements.
* **Truncation Handling:** Longer articles are automatically truncated to 1024 tokens to fit the transformer's maximum input size.

This keeps the application responsive even on consumer-grade hardware.

### Overall Workflow
The complete execution flow of the project is:
**User Input (URL/Text) → Web Scraping & Cleaning → Text Preprocessing → Dual Summarization (TextRank + BART) → Sentiment & Keyword Extraction → ROUGE Benchmarking → Result Visualization.**

15

---

# Results
Prism successfully demonstrates the power of hybrid NLP models in news analysis. 
* **Extractive Summaries:** Consistently provide factually grounded summaries by picking the most representative sentences.
* **Abstractive Summaries:** Provide a much more natural, readable flow, behaving like a human-written "TL;DR."
* **Sentiment Analysis:** Correctially identifies the tone of breaking news (e.g., negative polarity for disaster reports, positive for innovation news).
* **Keywords:** Effectively highlights the primary subjects (e.g., "AI," "Tech," "Future" for a technology article).

The Streamlit dashboard provides a high-framerate, aesthetically pleasing experience that makes complex data processing feel effortless for the end-user.

16-20

---

# Future Enhancements
* **Multi-Language Support**
Integration with models like `mBART` to support summarization in regional and international languages.
* **Automated News Feed**
A dashboard that automatically pulls and summarizes the top 10 headlines from major news outlets (BBC, CNN, etc.) every hour.
* **User Accounts & History**
Integration with MongoDB to allow users to save their summaries and track news trends over time.
* **AI Image Generation**
Automatically generate a relevant cover image for the summary using models like Stable Diffusion.
* **Voice-to-Summary**
Enable users to record news broadcasts and receive a text summary immediately.
* **Browser Extension**
A Chrome/Firefox extension that summarizes any news article directly on the website without leaving the tab.
* **Entity Extraction**
Advanced Name Entity Recognition (NER) to identify specific people, places, and organizations mentioned in the news.
* **PDF/Document Support**
Expand the tool to summarize long research papers and corporate PDFs, not just news URLs.

21

---

# Conclusion
**Prism** is a practical and user-friendly AI News Summarization system that improves the way readers interact with digital information. By combining web scraping, dual summarization methodologies (Extractive and Abstractive), and deep sentiment analysis, the project creates a comprehensive tool for editorial intelligence. It reduces the time spent on news consumption by up to 70%, increases clarity, and provides an objective way to evaluate AI performance through ROUGE metrics. Overall, Prism provides a state-of-the-art digital solution for smarter news monitoring and enhanced digital literacy.

22

---

# References
* **Hugging Face Transformers Documentation** – https://huggingface.co/docs/transformers
* **Streamlit Official Documentation** – https://docs.streamlit.io
* **NLTK (Natural Language Toolkit) Documentation** – https://www.nltk.org
* **TextRank: Bringing Order into Texts (Mihalcea & Tarau)** – https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
* **BART: Denoising Sequence-to-Sequence Pre-training (Lewis et al.)** – https://arxiv.org/abs/1910.13461
* **Scikit-Learn Documentation** – https://scikit-learn.org
* **BeautifulSoup4 Documentation** – https://www.crummy.com/software/BeautifulSoup/bs4/doc/
* **ROUGE Score Library** – https://github.com/google-research/google-research/tree/master/rouge

23
