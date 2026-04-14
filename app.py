import streamlit as st
import scraper
import preprocessing
from summarizer import Summarizer
import evaluator

# Initialize session state and constants
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = Summarizer()

st.set_page_config(page_title="AI News Summarization", page_icon="📰", layout="wide")

st.title("📰 AI News Summarization Engine")
st.markdown("Extract and summarize news articles dynamically using Extractive (TextRank) and Abstractive (Transformers) NLP techniques.")

# Sidebar for controls
st.sidebar.header("Configuration")
input_method = st.sidebar.radio("Select Input Method", ("URL", "Raw Text"))

summary_ratio = st.sidebar.slider("Extractive Summary Ratio", min_value=0.1, max_value=0.5, value=0.3, step=0.05,
                               help="Percentage of the original text to keep for Extractive Summary.")
                               
st.sidebar.markdown("---")
st.sidebar.markdown("### Advanced Options")
run_abstractive = st.sidebar.checkbox("Run Abstractive Summarization", value=True, help="Uses a HuggingFace Transformer model. Might be slower initially as it downloads weights.")
run_sentiment = st.sidebar.checkbox("Analyze Sentiment", value=True, help="Perform sentiment analysis on the original text.")

# Main input area
article_text = ""
if input_method == "URL":
    url_input = st.text_input("Enter News Article URL:")
    if st.button("Fetch Article"):
        with st.spinner("Scraping content..."):
            fetched_text = scraper.fetch_article_text(url_input)
            st.session_state.fetched_text = fetched_text
            
    if 'fetched_text' in st.session_state:
        if st.session_state.fetched_text.startswith("Error"):
            st.error(st.session_state.fetched_text)
        else:
            st.success("Article fetched successfully!")
            with st.expander("Show Original Text"):
                st.write(st.session_state.fetched_text)
            article_text = st.session_state.fetched_text
            
elif input_method == "Raw Text":
    text_input = st.text_area("Paste Article Text Here:", height=250)
    if text_input:
        article_text = text_input

st.markdown("---")
reference_summary = st.text_area("Optional: Paste Reference/Human Summary (For ROUGE Evaluation)", height=100)

if st.button("Generate Summaries", type="primary"):
    if not article_text or article_text.startswith("Error"):
        st.warning("Please provide valid text or a working URL first.")
    else:
        with st.spinner("Preprocessing text..."):
            orig_sents, clean_sents = preprocessing.preprocess_text(article_text)
            keywords = preprocessing.extract_keywords(clean_sents)
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔑 Extracted Keywords")
            st.info(", ".join(keywords))
            
        with col2:
            if run_sentiment:
                st.subheader("💡 Sentiment Analysis")
                sentiment = evaluator.analyze_sentiment(article_text)
                st.write(f"**Label:** {sentiment['label']}")
                st.write(f"**Polarity:** {sentiment['polarity']} | **Subjectivity:** {sentiment['subjectivity']}")
                
        st.markdown("---")
        
        sum_col1, sum_col2 = st.columns(2)
        
        extractive_summary = ""
        with sum_col1:
            st.subheader("📝 Extractive Summary (TextRank)")
            with st.spinner("Generating..."):
                extractive_summary = st.session_state.summarizer.extractive_summarization(orig_sents, clean_sents, ratio=summary_ratio)
                st.write(extractive_summary)
                
        abstractive_summary = ""
        with sum_col2:
            if run_abstractive:
                st.subheader("🤖 Abstractive Summary (BART)")
                with st.spinner("Generating... (This may take a moment mapping the Transformer model)"):
                    abstractive_summary = st.session_state.summarizer.abstractive_summarization(article_text)
                    st.write(abstractive_summary)
            else:
                st.subheader("🤖 Abstractive Summary")
                st.info("Abstractive summarization is disabled in the sidebar.")
                
        # ROUGE Evaluation
        if reference_summary and reference_summary.strip():
            st.markdown("---")
            st.subheader("📊 ROUGE Evaluation (vs Reference)")
            
            e_col1, e_col2 = st.columns(2)
            
            ext_scores = evaluator.calculate_rouge(extractive_summary, reference_summary)
            if ext_scores:
                with e_col1:
                    st.write("#### Extractive Score")
                    st.json(ext_scores)
                    
            if run_abstractive and abstractive_summary:
                abs_scores = evaluator.calculate_rouge(abstractive_summary, reference_summary)
                if abs_scores:
                    with e_col2:
                         st.write("#### Abstractive Score")
                         st.json(abs_scores)
