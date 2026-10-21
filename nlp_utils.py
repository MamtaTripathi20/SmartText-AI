import re
from collections import Counter
from itertools import islice

import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from textblob import TextBlob


def _ensure_nltk_resources():
    """Try to make required tokenization/WordNet resources available."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]
    for resource_path, package in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass


def tokenize_words(text):
    """Return lowercase word tokens, ignoring punctuation-only tokens."""
    _ensure_nltk_resources()
    try:
        tokens = word_tokenize(text.lower())
    except LookupError:
        tokens = re.findall(r"\b[\w'-]+\b", text.lower())
    return [token for token in tokens if re.search(r"[a-z0-9]", token)]


def _top_ngrams(tokens, n, limit=12):
    grams = [tuple(tokens[i:i+n]) for i in range(max(0, len(tokens) - n + 1))]
    counter = Counter(grams)
    return [
        {"N-gram": " ".join(gram), "Count": count}
        for gram, count in counter.most_common(limit)
    ]


def get_ngram_counts(text):
    tokens = tokenize_words(text)
    return {
        "unigrams": _top_ngrams(tokens, 1),
        "bigrams": _top_ngrams(tokens, 2),
        "trigrams": _top_ngrams(tokens, 3),
    }


def get_word_relations(word):
    """Fetch a small set of definitions, synonyms and antonyms from WordNet."""
    _ensure_nltk_resources()
    definitions = []
    synonyms = set()
    antonyms = set()

    try:
        synsets = wn.synsets(word.replace(" ", "_"))
    except LookupError:
        synsets = []

    for synset in synsets[:8]:
        if synset.definition():
            definitions.append(f"{synset.name()}: {synset.definition()}")
        for lemma in synset.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                synonyms.add(name)
            for antonym in lemma.antonyms():
                antonyms.add(antonym.name().replace("_", " "))

    return {
        "definitions": list(dict.fromkeys(definitions)),
        "synonyms": sorted(synonyms),
        "antonyms": sorted(antonyms),
    }


def get_basic_wsd_hint(context, target_word):
    """
    Basic dictionary-overlap WSD demonstration:
    ranks WordNet senses by overlap between definition words and context words.
    This is a small baseline, not a robust general WSD system.
    """
    _ensure_nltk_resources()
    try:
        senses = wn.synsets(target_word.replace(" ", "_"))
    except LookupError:
        senses = []

    if not senses:
        return "No candidate WordNet senses found. Try another common English word."

    stop_words = {
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
        "to", "of", "in", "on", "for", "with", "it", "this", "that", "as",
        "by", "at", "be", "from", "has", "have", "had", "into"
    }
    context_tokens = set(tokenize_words(context)) - stop_words - {target_word.lower()}

    scored = []
    for sense in senses:
        definition_tokens = set(re.findall(r"\b[a-z]+\b", sense.definition().lower())) - stop_words
        overlap = len(context_tokens & definition_tokens)
        scored.append((overlap, sense))

    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_sense = scored[0]
    if best_score == 0:
        return (
            "The simple dictionary-overlap method found no clear context match. "
            f"One candidate sense is: {best_sense.definition()}"
        )
    return (
        f"Best-overlap candidate: {best_sense.name()} — {best_sense.definition()} "
        f"(overlap score: {best_score})."
    )


def _sentences(text):
    # Simple sentence splitter; adequate for this educational starter app.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def summarize_text(text, sentence_limit=3):
    """
    Extractive baseline: scores sentences using normalized word frequency,
    then returns selected sentences in their original order.
    This is not LexRank; the UI labels it as a baseline.
    """
    sentences = _sentences(text)
    if not sentences:
        return ""

    if len(sentences) <= sentence_limit:
        return " ".join(sentences)

    stop_words = {
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
        "to", "of", "in", "on", "for", "with", "it", "this", "that", "as",
        "by", "at", "be", "from", "has", "have", "had", "into", "their",
        "they", "them", "he", "she", "we", "you", "i"
    }
    all_tokens = tokenize_words(text)
    frequencies = Counter(token for token in all_tokens if token not in stop_words)
    if not frequencies:
        return " ".join(sentences[:sentence_limit])

    max_freq = max(frequencies.values())
    normalized = {word: count / max_freq for word, count in frequencies.items()}

    scored = []
    for index, sentence in enumerate(sentences):
        tokens = [t for t in tokenize_words(sentence) if t not in stop_words]
        score = sum(normalized.get(token, 0) for token in tokens) / max(1, len(tokens))
        scored.append((score, index, sentence))

    chosen = sorted(scored, key=lambda item: item[0], reverse=True)[:sentence_limit]
    chosen_in_order = sorted(chosen, key=lambda item: item[1])
    return " ".join(item[2] for item in chosen_in_order)


def analyze_sentiment(text):
    """Return a simple TextBlob polarity label and an explanatory message."""
    polarity = float(TextBlob(text).sentiment.polarity)
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "polarity": polarity,
        "explanation": (
            "Polarity ranges roughly from -1 (negative) to +1 (positive). "
            "This is a lexicon-based baseline; it is not a guaranteed interpretation."
        ),
    }
