# 🧠 SmartText AI

### NLP-Based Text Analysis System

SmartText AI is a Python-based Natural Language Processing (NLP) application designed to analyze text and extract meaningful information using different NLP techniques. It provides an interactive interface for text analysis, semantic exploration, summarization, sentiment analysis, and document processing.

## 🚀 Features

- **Document Upload:** Upload PDF and TXT files for text analysis.
- **N-Gram Analysis:** Analyze unigrams, bigrams, and trigrams to identify frequently occurring words and phrases.
- **Semantic Analysis:** Explore word definitions, synonyms, and antonyms using WordNet.
- **Word Sense Disambiguation (WSD):** Get a basic context-based hint to understand the meaning of a word.
- **Text Summarization:** Generate concise summaries using extractive summarization.
- **Sentiment Analysis:** Classify text as Positive, Negative, or Neutral using TextBlob.
- **NLP Chat Assistant:** Ask supported questions about the text and access available analysis features through a simple chat interface.

## 🛠️ Technologies Used

- Python
- Streamlit
- NLTK
- WordNet
- TextBlob
- PyMuPDF

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Open the Project Folder

```bash
cd SmartText-AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

## 📂 Project Structure

```text
SmartText-AI/
├── app.py
├── nlp_utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🎯 Project Objective

The objective of SmartText AI is to demonstrate fundamental NLP techniques through an interactive application that helps users explore, process, and understand textual data.

## 📌 Limitations

- Word Sense Disambiguation uses a basic dictionary-overlap approach.
- Text summarization uses an extractive, frequency-based method.
- Sentiment analysis uses a lexicon-based approach and may not correctly interpret every context.
- The chat assistant supports predefined question patterns and is not a generative AI chatbot.

## 👩‍💻 Author

**Mamta Tripathi**  
MCA AI Student

## 📄 License

This project is intended for academic and educational purposes.
