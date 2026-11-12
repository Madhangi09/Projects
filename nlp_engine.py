
from sentence_transformers import SentenceTransformer, util
from functools import lru_cache
from nltk.corpus import wordnet
import nltk

# Download WordNet if required
try:
    wordnet.synsets("game")
except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")


# Load NLP model once
@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# Text preprocessing
def preprocess_text(text):
    return text.lower().strip()


# Semantic similarity
def get_similarity(word1, word2):

    word1 = preprocess_text(word1)
    word2 = preprocess_text(word2)

    if word1 == word2:
        return 1.0

    model = load_model()

    embeddings = model.encode(
        [word1, word2],
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    return util.cos_sim(
        embeddings[0],
        embeddings[1]
    ).item()


# NLP feedback
def get_feedback(score):

    if score >= 0.55:
        return "🔥 Hot! Very close!"

    elif score >= 0.30:
        return "🌤️ Warm! Keep trying!"

    else:
        return "❄️ Cold! Try another word!"


# Smart hint generation
def get_smart_hint(target_word, fallback_hint=""):

    synsets = wordnet.synsets(
        target_word,
        pos=wordnet.NOUN
    )

    if synsets:

        meaning = synsets[0].definition()
        examples = synsets[0].examples()

        hint = f"🧠 Meaning: {meaning}"

        if examples:
            hint += f"\n\n📖 Example: {examples[0]}"

        return hint

    return fallback_hint or "Think about the meaning of the hidden word!"
