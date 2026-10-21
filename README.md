# SmartText AI

A Python-based educational NLP application demonstrating selected concepts from Modules III, IV and V.

## Features
- N-gram counts: unigram, bigram and trigram
- Sample-based N-gram analysis
- WordNet definitions, synonyms and antonyms
- Basic dictionary-overlap WSD demonstration
- Extractive sentence-summary baseline
- TextBlob sentiment polarity and label

## Requirements
- Python 3.10+
- Internet access for initial installation and NLTK resource downloads (when not already present)

## Setup on Windows (VS Code terminal)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can run:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Important academic note
The included summarizer is a frequency-scored extractive baseline, not full LexRank. The WSD component is a simple dictionary-overlap demonstration, not a robust general-purpose WSD model. These should be described accurately in the report and presentation. Full LexRank and optimization-based summarization can be implemented as future extensions.
