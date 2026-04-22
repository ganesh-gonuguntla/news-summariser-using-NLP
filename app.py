# import streamlit as st
# import scraper
# import preprocessing
# from summarizer import Summarizer
# import evaluator

# # Initialize session state and constants
# if 'summarizer' not in st.session_state:
#     st.session_state.summarizer = Summarizer()

# st.set_page_config(page_title="AI News Summarization", page_icon="📰", layout="wide")

# st.title("📰 AI News Summarization Engine")
# st.markdown("Extract and summarize news articles dynamically using Extractive (TextRank) and Abstractive (Transformers) NLP techniques.")

# # Sidebar for controls
# st.sidebar.header("Configuration")
# input_method = st.sidebar.radio("Select Input Method", ("URL", "Raw Text"))

# summary_ratio = st.sidebar.slider("Extractive Summary Ratio", min_value=0.1, max_value=0.5, value=0.3, step=0.05,
#                                help="Percentage of the original text to keep for Extractive Summary.")
                               
# st.sidebar.markdown("---")
# st.sidebar.markdown("### Advanced Options")
# run_abstractive = st.sidebar.checkbox("Run Abstractive Summarization", value=True, help="Uses a HuggingFace Transformer model. Might be slower initially as it downloads weights.")
# run_sentiment = st.sidebar.checkbox("Analyze Sentiment", value=True, help="Perform sentiment analysis on the original text.")

# # Main input area
# article_text = ""
# if input_method == "URL":
#     url_input = st.text_input("Enter News Article URL:")
#     if st.button("Fetch Article"):
#         with st.spinner("Scraping content..."):
#             fetched_text = scraper.fetch_article_text(url_input)
#             st.session_state.fetched_text = fetched_text
            
#     if 'fetched_text' in st.session_state:
#         if st.session_state.fetched_text.startswith("Error"):
#             st.error(st.session_state.fetched_text)
#         else:
#             st.success("Article fetched successfully!")
#             with st.expander("Show Original Text"):
#                 st.write(st.session_state.fetched_text)
#             article_text = st.session_state.fetched_text
            
# elif input_method == "Raw Text":
#     text_input = st.text_area("Paste Article Text Here:", height=250)
#     if text_input:
#         article_text = text_input

# st.markdown("---")
# reference_summary = st.text_area("Optional: Paste Reference/Human Summary (For ROUGE Evaluation)", height=100)

# if st.button("Generate Summaries", type="primary"):
#     if not article_text or article_text.startswith("Error"):
#         st.warning("Please provide valid text or a working URL first.")
#     else:
#         with st.spinner("Preprocessing text..."):
#             orig_sents, clean_sents = preprocessing.preprocess_text(article_text)
#             keywords = preprocessing.extract_keywords(clean_sents)
            
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("🔑 Extracted Keywords")
#             st.info(", ".join(keywords))
            
#         with col2:
#             if run_sentiment:
#                 st.subheader("💡 Sentiment Analysis")
#                 sentiment = evaluator.analyze_sentiment(article_text)
#                 st.write(f"**Label:** {sentiment['label']}")
#                 st.write(f"**Polarity:** {sentiment['polarity']} | **Subjectivity:** {sentiment['subjectivity']}")
                
#         st.markdown("---")
        
#         sum_col1, sum_col2 = st.columns(2)
        
#         extractive_summary = ""
#         with sum_col1:
#             st.subheader("📝 Extractive Summary (TextRank)")
#             with st.spinner("Generating..."):
#                 extractive_summary = st.session_state.summarizer.extractive_summarization(orig_sents, clean_sents, ratio=summary_ratio)
#                 st.write(extractive_summary)
                
#         abstractive_summary = ""
#         with sum_col2:
#             if run_abstractive:
#                 st.subheader("🤖 Abstractive Summary (BART)")
#                 with st.spinner("Generating... (This may take a moment mapping the Transformer model)"):
#                     abstractive_summary = st.session_state.summarizer.abstractive_summarization(article_text)
#                     st.write(abstractive_summary)
#             else:
#                 st.subheader("🤖 Abstractive Summary")
#                 st.info("Abstractive summarization is disabled in the sidebar.")
                
#         # ROUGE Evaluation
#         if reference_summary and reference_summary.strip():
#             st.markdown("---")
#             st.subheader("📊 ROUGE Evaluation (vs Reference)")
            
#             e_col1, e_col2 = st.columns(2)
            
#             ext_scores = evaluator.calculate_rouge(extractive_summary, reference_summary)
#             if ext_scores:
#                 with e_col1:
#                     st.write("#### Extractive Score")
#                     st.json(ext_scores)
                    
#             if run_abstractive and abstractive_summary:
#                 abs_scores = evaluator.calculate_rouge(abstractive_summary, reference_summary)
#                 if abs_scores:
#                     with e_col2:
#                          st.write("#### Abstractive Score")
#                          st.json(abs_scores)


import streamlit as st
import scraper
import preprocessing
from summarizer import Summarizer
import evaluator

# ── Session state ──────────────────────────────────────────────────────────────
if "summarizer" not in st.session_state:
    st.session_state.summarizer = Summarizer()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prism — AI News Summarizer",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Root palette ── */
    :root {
        --bg:        #0a0d12;
        --surface:   #111622;
        --border:    #1e2840;
        --accent:    #00e5ff;
        --accent2:   #7b61ff;
        --muted:     #4a5568;
        --text:      #e2e8f0;
        --text-dim:  #8896ab;
        --success:   #00e5b4;
        --warn:      #ff6b6b;
        --radius:    12px;
    }

    /* ── Base reset ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }

    /* ── Remove Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2.5rem 3rem 4rem !important; max-width: 1400px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    .sidebar-logo {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--accent) !important;
        padding: 0 1rem 1.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }

    .sidebar-section {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--muted) !important;
        padding: 0 1rem;
        margin-bottom: 0.6rem;
        margin-top: 1.4rem;
    }

    /* ── Radio / checkboxes ── */
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        font-size: 0.88rem !important;
        color: var(--text-dim) !important;
    }
    [data-testid="stRadio"] [data-checked="true"] label,
    [data-testid="stCheckbox"] [data-checked="true"] label {
        color: var(--accent) !important;
    }

    /* ── Slider ── */
    [data-testid="stSlider"] .stSlider { accent-color: var(--accent); }

    /* ── Hero header ── */
    .hero {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        padding-bottom: 2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2.5rem;
        gap: 1rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.4rem, 5vw, 3.6rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -0.02em;
        margin: 0;
        background: linear-gradient(135deg, var(--text) 40%, var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-dim);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(0,229,255,0.07);
        border: 1px solid rgba(0,229,255,0.25);
        border-radius: 999px;
        padding: 0.35rem 0.9rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent);
        letter-spacing: 0.1em;
        white-space: nowrap;
    }
    .hero-badge::before {
        content: '';
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 8px var(--accent);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* ── Section label ── */
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.6rem;
    }

    /* ── Card ── */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
    }
    .card-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--text-dim);
        margin-bottom: 1rem;
    }

    /* ── Inputs ── */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background: #0d1117 !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.2s;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(0,229,255,0.1) !important;
    }

    /* ── Primary button ── */
    [data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #000 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 2rem !important;
        transition: opacity 0.2s, transform 0.1s !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stButton"] button[kind="secondary"] {
        background: transparent !important;
        color: var(--accent) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.8rem !important;
        border: 1px solid rgba(0,229,255,0.35) !important;
        border-radius: 8px !important;
        letter-spacing: 0.08em !important;
        transition: background 0.2s !important;
    }
    [data-testid="stButton"] button[kind="secondary"]:hover {
        background: rgba(0,229,255,0.07) !important;
    }

    /* ── Success / error / info ── */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #0d1117 !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.8rem !important;
        color: var(--text-dim) !important;
        letter-spacing: 0.08em !important;
    }

    /* ── Stat pill ── */
    .stat-row {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 0.5rem;
    }
    .stat-pill {
        background: rgba(0,229,255,0.07);
        border: 1px solid rgba(0,229,255,0.2);
        border-radius: 999px;
        padding: 0.3rem 0.9rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: var(--accent);
    }
    .stat-pill span { color: var(--text-dim); }

    /* ── Summary output ── */
    .summary-body {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        line-height: 1.75;
        color: var(--text);
        border-left: 2px solid var(--accent);
        padding-left: 1.2rem;
        margin-top: 0.5rem;
    }

    /* ── Keywords ── */
    .kw-wrap { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
    .kw-tag {
        background: rgba(123,97,255,0.12);
        border: 1px solid rgba(123,97,255,0.3);
        border-radius: 6px;
        padding: 0.25rem 0.7rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: #b8a8ff;
    }

    /* ── Sentiment ── */
    .sentiment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin-top: 0.8rem;
    }
    .sentiment-item {
        background: #0d1117;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem 1rem;
        text-align: center;
    }
    .sentiment-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--accent);
    }
    .sentiment-key {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin-top: 0.2rem;
    }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

    /* ── JSON ── */
    [data-testid="stJson"] {
        background: #0d1117 !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    /* ── Spinner ── */
    [data-testid="stSpinner"] { color: var(--accent) !important; }

    /* ── Sub-header override ── */
    h1,h2,h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        color: var(--text) !important;
    }

    /* ── Columns gap ── */
    [data-testid="column"] { gap: 0; }

    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⬡ PRISM</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Input Source</div>', unsafe_allow_html=True)
    input_method = st.radio("", ("URL", "Raw Text"), label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">Extraction</div>', unsafe_allow_html=True)
    summary_ratio = st.slider(
        "Extractive Ratio",
        min_value=0.1, max_value=0.5, value=0.3, step=0.05,
        help="Fraction of original sentences to retain.",
    )

    st.markdown('<div class="sidebar-section">Features</div>', unsafe_allow_html=True)
    run_abstractive = st.checkbox("Abstractive (BART)", value=True)
    run_sentiment   = st.checkbox("Sentiment Analysis", value=True)

    st.markdown(
        """
        <div style='position:absolute;bottom:2rem;left:1rem;right:1rem;
                    font-family:"DM Mono",monospace;font-size:0.65rem;
                    color:#2d3d55;letter-spacing:0.06em;line-height:1.6;'>
            PRISM v2.0<br>TextRank · BART · ROUGE
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <div>
        <p class="hero-sub">⬡ AI-Powered Editorial Intelligence</p>
        <h1 class="hero-title">News<br>Summarizer</h1>
      </div>
      <div class="hero-badge">NLP Engine Active</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Input area ─────────────────────────────────────────────────────────────────
article_text = ""

if input_method == "URL":
    st.markdown('<p class="section-label">Article URL</p>', unsafe_allow_html=True)
    url_input = st.text_input("", placeholder="https://example.com/news-article", label_visibility="collapsed")

    if st.button("Fetch Article →", key="fetch_btn"):
        with st.spinner("Fetching content…"):
            fetched = scraper.fetch_article_text(url_input)
            st.session_state.fetched_text = fetched

    if "fetched_text" in st.session_state:
        if st.session_state.fetched_text.startswith("Error"):
            st.error(st.session_state.fetched_text)
        else:
            st.success("Article fetched successfully.")
            with st.expander("Preview original text"):
                st.write(st.session_state.fetched_text)
            article_text = st.session_state.fetched_text

else:
    st.markdown('<p class="section-label">Raw Article Text</p>', unsafe_allow_html=True)
    text_input = st.text_area("", placeholder="Paste your article here…", height=220, label_visibility="collapsed")
    if text_input:
        article_text = text_input

st.markdown('<p class="section-label" style="margin-top:1.4rem;">Reference Summary <span style="color:#2d3d55;font-size:0.6rem;">(Optional — for ROUGE evaluation)</span></p>', unsafe_allow_html=True)
reference_summary = st.text_area("", placeholder="Paste a human-written summary to evaluate against…", height=100, label_visibility="collapsed", key="ref")

st.markdown("")
run_btn = st.button("Generate Summaries", type="primary", use_container_width=False)

# ── Generation ─────────────────────────────────────────────────────────────────
if run_btn:
    if not article_text or article_text.startswith("Error"):
        st.warning("Provide valid article text or a working URL first.")
    else:
        # Preprocessing
        with st.spinner("Preprocessing…"):
            orig_sents, clean_sents = preprocessing.preprocess_text(article_text)
            keywords = preprocessing.extract_keywords(clean_sents)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Keywords + Sentiment row
        kw_col, sent_col = st.columns([1, 1], gap="large")

        with kw_col:
            st.markdown(
                f"""
                <div class="card">
                  <div class="card-title">🔑 Keywords</div>
                  <div class="kw-wrap">
                    {''.join(f'<span class="kw-tag">{k}</span>' for k in keywords)}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with sent_col:
            if run_sentiment:
                with st.spinner("Analysing sentiment…"):
                    sentiment = evaluator.analyze_sentiment(article_text)

                label_color = {
                    "POSITIVE": "#00e5b4",
                    "NEGATIVE": "#ff6b6b",
                    "NEUTRAL":  "#8896ab",
                }.get(sentiment["label"].upper(), "#8896ab")

                st.markdown(
                    f"""
                    <div class="card">
                      <div class="card-title">💡 Sentiment</div>
                      <div class="sentiment-grid">
                        <div class="sentiment-item">
                          <div class="sentiment-value" style="color:{label_color};">{sentiment['label']}</div>
                          <div class="sentiment-key">Label</div>
                        </div>
                        <div class="sentiment-item">
                          <div class="sentiment-value">{sentiment['polarity']}</div>
                          <div class="sentiment-key">Polarity</div>
                        </div>
                        <div class="sentiment-item">
                          <div class="sentiment-value">{sentiment['subjectivity']}</div>
                          <div class="sentiment-key">Subjectivity</div>
                        </div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="card" style="opacity:0.45;"><div class="card-title">💡 Sentiment</div><p style="font-size:0.85rem;color:var(--text-dim);">Disabled in sidebar.</p></div>',
                    unsafe_allow_html=True,
                )

        # Summaries
        st.markdown("<hr>", unsafe_allow_html=True)
        ex_col, ab_col = st.columns(2, gap="large")

        extractive_summary  = ""
        abstractive_summary = ""

        with ex_col:
            st.markdown(
                '<div class="section-label">📝 Extractive Summary — TextRank</div>',
                unsafe_allow_html=True,
            )
            with st.spinner("Running TextRank…"):
                extractive_summary = st.session_state.summarizer.extractive_summarization(
                    orig_sents, clean_sents, ratio=summary_ratio
                )
            st.markdown(
                f'<div class="card"><div class="summary-body">{extractive_summary}</div></div>',
                unsafe_allow_html=True,
            )

        with ab_col:
            if run_abstractive:
                st.markdown(
                    '<div class="section-label">🤖 Abstractive Summary — BART</div>',
                    unsafe_allow_html=True,
                )
                with st.spinner("Loading transformer model…"):
                    abstractive_summary = st.session_state.summarizer.abstractive_summarization(article_text)
                st.markdown(
                    f'<div class="card"><div class="summary-body">{abstractive_summary}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="card" style="opacity:0.45;"><div class="section-label">🤖 Abstractive Summary</div><p style="font-size:0.85rem;color:var(--text-dim);">Disabled in sidebar.</p></div>',
                    unsafe_allow_html=True,
                )

        # ROUGE
        if reference_summary and reference_summary.strip():
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(
                '<div class="section-label">📊 ROUGE Evaluation vs Reference</div>',
                unsafe_allow_html=True,
            )

            r_col1, r_col2 = st.columns(2, gap="large")

            ext_scores = evaluator.calculate_rouge(extractive_summary, reference_summary)
            if ext_scores:
                with r_col1:
                    st.markdown(
                        '<div class="card"><div class="card-title">Extractive Scores</div>',
                        unsafe_allow_html=True,
                    )
                    st.json(ext_scores)
                    st.markdown("</div>", unsafe_allow_html=True)

            if run_abstractive and abstractive_summary:
                abs_scores = evaluator.calculate_rouge(abstractive_summary, reference_summary)
                if abs_scores:
                    with r_col2:
                        st.markdown(
                            '<div class="card"><div class="card-title">Abstractive Scores</div>',
                            unsafe_allow_html=True,
                        )
                        st.json(abs_scores)
                        st.markdown("</div>", unsafe_allow_html=True)