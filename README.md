

# YouTube-Web-Summarizer

An AI-powered content summarization application that transforms lengthy YouTube videos and website articles into concise, meaningful summaries using **LangChain and Hugging Face LLMs**.

## 🚀 Features

- 🎥 **YouTube Summarization:** Extracts video transcripts and generates summaries.
- 🌐 **Website Summarization:** Extracts and summarizes content from web pages.
- 🤖 **Hugging Face Integration:** Uses the Mistral-7B-Instruct-v0.3 model.
- 🔗 **LangChain:** Implements an LLM-based summarization pipeline.
- ⚡ **Interactive UI:** Built with Streamlit and custom CSS.
- 🔐 **API Authentication:** Secure Hugging Face API token input.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Hugging Face
- Mistral-7B-Instruct-v0.3
- Unstructured
- YouTube Transcript API

## 📂 Project Structure

```text
InsightAI-Content-Summarizer/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/InsightAI-Content-Summarizer.git
cd InsightAI-Content-Summarizer
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment**

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the application**

```bash
streamlit run app.py
```

## 🔑 Hugging Face API Setup

1. Create an account on [Hugging Face](https://huggingface.co/).
2. Generate an API token from [Access Tokens](https://huggingface.co/settings/tokens).
3. Launch the application.
4. Enter your Hugging Face API token in the sidebar.
5. Paste a YouTube or website URL and generate your summary.

## 📸 How It Works

1. Enter a YouTube video or website URL.
2. The application extracts the available content.
3. LangChain processes the extracted documents.
4. The Hugging Face Mistral model generates a summary.
5. View the generated summary in the Streamlit interface.

## 🎯 Learning Outcomes

- Working with Large Language Models (LLMs).
- Building summarization chains using LangChain.
- Integrating Hugging Face models through API endpoints.
- Extracting content from YouTube videos and websites.
- Developing interactive AI applications using Streamlit.

## 👨‍💻 Author

**Sharique Sabeeh**

B.Tech Computer Science & Engineering

---

⭐ If you find this project useful, consider giving it a star!
