# SmartText AI
### NLP-Based Text Analysis System

SmartText AI is an interactive text analysis application developed using Python and Streamlit. It brings together fundamental Natural Language Processing (NLP) techniques in a single interface to help users explore language patterns, examine word relationships, summarize text, and analyze sentiment.

## Key Features

- **N-gram Analysis:** Examines unigram, bigram, and trigram frequency patterns.
- **Semantic Analysis:** Retrieves word definitions, synonyms, and antonyms using WordNet.
- **Word Sense Analysis:** Demonstrates a basic dictionary-overlap approach to exploring word meaning in context.
- **Text Summarization:** Generates extractive summaries by selecting sentences from the original text.
- **Sentiment Analysis:** Classifies text polarity as positive, negative, or neutral using TextBlob.
- **Document Processing:** Supports text extraction from PDF and TXT files.
- **NLP Chat Assistant:** Provides rule-based responses to supported text-analysis queries.

## Technology Stack

Python · Streamlit · NLTK · WordNet · TextBlob · PyMuPDF

## Project Structure

```text
SmartText-AI/
├── app.py
├── nlp_utils.py
├── requirements.txt
├── README.md
└── screenshots/
```

## Getting Started

### Prerequisites
- Python installed on your system
- Internet access for installing dependencies and downloading required NLTK resources when needed

### Installation

```bash
git clone YOUR_REPOSITORY_URL
cd SmartText-AI
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the application:

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal.

## Applications

- Exploring word and phrase frequency patterns
- Learning lexical semantics and word relationships
- Creating shorter versions of lengthy text
- Examining basic sentiment polarity
- Extracting and analyzing text from documents

## Limitations

This project is an educational NLP application. Its summarizer is extractive, sentiment analysis is lexicon-based, word-sense analysis uses a simple overlap method, and the chat assistant is rule-based rather than a generative AI chatbot. Results may require verification against the original text.

## Project Goal

The goal of SmartText AI is to demonstrate how multiple core NLP techniques can be combined into one accessible, interactive Python application.

Feedback and suggestions are welcome.
