import streamlit as st
import pymupdf
import re

from nlp_utils import (
    get_ngram_counts,
    get_word_relations,
    get_basic_wsd_hint,
    summarize_text,
    analyze_sentiment,
)

st.set_page_config(
    page_title="SmartText AI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 SmartText AI")
st.subheader("NLP-Based Text Analysis System")
st.write(
    "Analyze text using N-grams, WordNet, "
    "summarization, and sentiment analysis."
)

DEFAULT_TEXT = (
    "Artificial intelligence is transforming education. "
    "AI tools help students learn difficult topics. "
    "Responsible use of AI is important. "
    "Natural Language Processing helps computers understand language."
)

if "user_text" not in st.session_state:
    st.session_state.user_text = DEFAULT_TEXT

with st.sidebar:
    st.header("Analysis Settings")
    summary_sentences = st.slider(
        "Summary length (sentences)", 1, 10, 3
    )

st.markdown("## 📄 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"],
)

if uploaded_file is not None:
    signature = (uploaded_file.name, uploaded_file.size)

    if st.session_state.get("file_signature") != signature:
        try:
            if uploaded_file.name.lower().endswith(".pdf"):
                with pymupdf.open(
                    stream=uploaded_file.getvalue(),
                    filetype="pdf",
                ) as pdf:
                    extracted_text = "\n".join(
                        page.get_text() for page in pdf
                    )
            else:
                extracted_text = uploaded_file.getvalue().decode(
                    "utf-8-sig", errors="replace"
                )

            if extracted_text.strip():
                st.session_state.user_text = extracted_text
                st.session_state.file_signature = signature
                st.success("Document uploaded successfully!")
            else:
                st.warning(
                    "No readable text found. Scanned PDFs need OCR."
                )
        except Exception as error:
            st.error(f"Document error: {error}")

user_text = st.text_area(
    "Enter text or edit uploaded document text:",
    height=220,
    key="user_text",
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 N-grams",
    "📚 Semantic Analysis",
    "📝 Summary",
    "💬 Sentiment",
    "💬 NLP Chat Assistant",
])

with tab1:
    st.markdown("### N-gram Analysis")
    if user_text.strip():
        counts = get_ngram_counts(user_text)

        c1, c2, c3 = st.columns(3)
        c1.metric("Unigrams", len(counts["unigrams"]))
        c2.metric("Bigrams", len(counts["bigrams"]))
        c3.metric("Trigrams", len(counts["trigrams"]))

        st.write("Most frequent unigrams")
        st.dataframe(counts["unigrams"], use_container_width=True)

        st.write("Most frequent bigrams")
        st.dataframe(counts["bigrams"], use_container_width=True)

        st.write("Most frequent trigrams")
        st.dataframe(counts["trigrams"], use_container_width=True)

with tab2:
    st.markdown("### Semantic Analysis")
    word = st.text_input(
        "Enter an English word:",
        value="language",
        key="semantic_word",
    ).strip()

    if word:
        relations = get_word_relations(word)

        st.write("Definitions")
        for definition in relations.get("definitions", [])[:4]:
            st.write(f"• {definition}")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Synonyms")
            st.write(
                ", ".join(relations.get("synonyms", [])[:20])
                or "No synonyms found."
            )
        with col2:
            st.write("Antonyms")
            st.write(
                ", ".join(relations.get("antonyms", [])[:20])
                or "No antonyms found."
            )

        st.write("Context-based sense hint")
        st.write(get_basic_wsd_hint(user_text, word))

with tab3:
    st.markdown("### Text Summarization")

    if user_text.strip():
        summary = summarize_text(
            user_text,
            sentence_limit=summary_sentences,
        )
        st.write(summary or "No summary available.")

        original_words = len(user_text.split())
        summary_words = len(summary.split()) if summary else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Original words", original_words)
        c2.metric("Summary words", summary_words)

        reduction = (
            round((1 - summary_words / original_words) * 100)
            if original_words else 0
        )
        c3.metric("Reduction", f"{max(0, reduction)}%")

with tab4:
    st.markdown("### Sentiment Analysis")

    if user_text.strip():
        result = analyze_sentiment(user_text)

        c1, c2 = st.columns(2)
        c1.metric("Predicted sentiment", result["label"])
        c2.metric("Polarity score", f'{result["polarity"]:.3f}')

        st.write(result["explanation"])


with tab5:
    st.markdown("### 💬 NLP Chat Assistant")
    st.write(
        "Ask questions about your uploaded document "
        "or use the available NLP analysis features."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask about your text, e.g. summarize this document..."
    )

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt,
        })

        question = prompt.lower().strip()
        answer = ""
        text = st.session_state.user_text

        if not text.strip():
            answer = "Please enter text or upload a document first."

        elif any(word in question for word in [
            "summarize", "summary", "short summary",
            "सारांश", "summary do"
        ]):
            answer = summarize_text(
                text,
                sentence_limit=summary_sentences,
            )

        elif "sentiment" in question or "feeling" in question:
            result = analyze_sentiment(text)
            answer = (
                f"Sentiment: {result['label']}\n\n"
                f"Polarity score: {result['polarity']:.3f}\n\n"
                f"{result['explanation']}"
            )

        elif "synonym" in question or "antonym" in question:
            words = re.findall(r"[a-zA-Z]+", question)
            ignored = {
                "give", "me", "the", "for", "of", "and",
                "what", "are", "is", "find", "show"
            }
            candidates = [w for w in words if w.lower() not in ignored]
            target = candidates[-1] if candidates else ""

            if target:
                relations = get_word_relations(target)
                if "antonym" in question:
                    items = relations.get("antonyms", [])
                    label = "Antonyms"
                else:
                    items = relations.get("synonyms", [])
                    label = "Synonyms"

                answer = (
                    f"{label} of **{target}**: "
                    + (", ".join(items[:15]) or "No results found.")
                )
            else:
                answer = "Please include an English word in your question."

        elif "define" in question or "meaning" in question or "definition" in question:
            words = re.findall(r"[a-zA-Z]+", question)
            ignored = {
                "define", "meaning", "definition", "of", "what",
                "is", "the", "word", "please", "tell", "me"
            }
            candidates = [w for w in words if w.lower() not in ignored]
            target = candidates[-1] if candidates else ""

            if target:
                relations = get_word_relations(target)
                definitions = relations.get("definitions", [])
                answer = "\n\n".join(definitions[:3]) or "No definition found."
            else:
                answer = "Please enter a word whose meaning you want."

        elif "search" in question or "find" in question or "where" in question:
            words = re.findall(r"[a-zA-Z]+", question)
            ignored = {
                "search", "find", "where", "in", "this", "text",
                "document", "for", "the", "please", "me", "about"
            }
            terms = [w.lower() for w in words if w.lower() not in ignored]
            matches = []

            for sentence in re.split(r"(?<=[.!?])\s+", text):
                if any(term in sentence.lower() for term in terms):
                    matches.append(sentence.strip())

            answer = (
                "\n\n".join(matches[:5])
                if matches else "No matching sentences found in the text."
            )

        else:
            answer = (
                "I can help with this document. Try asking:\n\n"
                "- Summarize this document\n"
                "- What is the sentiment?\n"
                "- Give synonyms for language\n"
                "- Define language\n"
                "- Search for education"
            )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
        })
        st.rerun()

st.divider()
st.caption(
    "SmartText AI | Python | Streamlit | NLTK | WordNet | TextBlob"
)
