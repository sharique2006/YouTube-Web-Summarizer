
import validators
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import (
    YoutubeLoader,
    UnstructuredURLLoader
)
from langchain_huggingface import HuggingFaceEndpoint


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Content Summarizer",
    page_icon="✨",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, #25204b 0%, transparent 30%),
        radial-gradient(circle at 90% 90%, #142b49 0%, transparent 30%),
        #0b1020;
    color: #f8fafc;
}

/* Main container */
.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Header */
.hero {
    text-align: center;
    padding: 35px 20px 25px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.3);
    color: #c4b5fd;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin: 22px 0 12px;
    background: linear-gradient(90deg, #ffffff, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a5b4cc;
    font-size: 16px;
}

/* Content card */
.main-card {
    background: rgba(22, 30, 52, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 22px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

/* Input */
.stTextInput input {
    background: #111a30 !important;
    color: #ffffff !important;
    border: 1px solid #34415f !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

.stTextInput input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.2) !important;
}

.stTextInput label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    color: white;
    font-size: 16px;
    font-weight: 700;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #8b5cf6, #6366f1);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(124,58,237,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10182b;
    border-right: 1px solid #26334d;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* Summary */
.summary-card {
    background: linear-gradient(135deg, rgba(30,41,75,0.95), rgba(24,35,61,0.95));
    border: 1px solid rgba(139,92,246,0.35);
    border-radius: 18px;
    padding: 28px;
    margin-top: 25px;
    line-height: 1.8;
}

.summary-heading {
    color: #c4b5fd;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ✨ AI Summarizer")
    st.caption("Your personal content assistant")

    st.markdown("---")

    st.markdown("### 🔑 Configuration")

    hf_api_key = st.text_input(
        "Hugging Face API Token",
        type="password",
        placeholder="Enter your HF token..."
    )

    st.markdown("---")
    st.markdown("### 📌 Supported Sources")
    st.markdown("▶️ YouTube videos")
    st.markdown("🌐 Websites")

    st.markdown("---")
    st.caption("Powered by LangChain & Hugging Face")


# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">✨ AI POWERED SUMMARIZATION</div>
    <h1>Content Summarizer</h1>
    <p>Turn lengthy videos and articles into clear, meaningful summaries.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- MAIN INPUT CARD ----------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown("### 🔗 Enter Your Content URL")
st.caption("Paste a YouTube video link or website URL below.")

generic_url = st.text_input(
    "Content URL",
    placeholder="https://www.youtube.com/watch?v=... or https://example.com",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

summarize_button = st.button(
    "✨  Generate Summary",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- PROMPT & MODEL ----------------
prompt_template = """
Provide a clear, informative and well-structured summary
of the following content in approximately 300 words.

Focus on:
- Main ideas and important points
- Key information and explanations
- Important conclusions

Content:
{text}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["text"]
)


# ---------------- SUMMARIZATION ----------------
if summarize_button:

    if not hf_api_key.strip() or not generic_url.strip():
        st.error("⚠️ Please provide both your Hugging Face API token and URL.")

    elif not validators.url(generic_url):
        st.error("⚠️ Please enter a valid URL.")

    else:
        try:
            with st.spinner("✨ Reading content and generating your summary..."):

                repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

                llm = HuggingFaceEndpoint(
                    repo_id=repo_id,
                    max_new_tokens=512,
                    temperature=0.7,
                    huggingfacehub_api_token=hf_api_key
                )

                # Load content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=True
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0"
                        }
                    )

                docs = loader.load()

                if not docs:
                    st.warning("No content could be extracted from this URL.")
                else:
                    # Summarization chain
                    chain = load_summarize_chain(
                        llm,
                        chain_type="stuff",
                        prompt=prompt
                    )

                    output_summary = chain.invoke({"input_documents": docs})
                    summary = output_summary["output_text"]

                    st.markdown("""
                    <div class="summary-card">
                        <div class="summary-heading">
                            ✨ Your AI Generated Summary
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(summary)

                    st.success("Summary generated successfully!")

        except Exception as e:
            st.error("Something went wrong while generating the summary.")
            st.exception(e)


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit, LangChain & Hugging Face
</div>
""", unsafe_allow_html=True)
