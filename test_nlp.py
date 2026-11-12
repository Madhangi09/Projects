
from nlp_engine import get_similarity, get_feedback

pairs = [
    ("ocean", "sea"),
    ("happy", "joyful"),
    ("cat", "table"),
    ("car", "vehicle")
]

for word1, word2 in pairs:

    score = get_similarity(word1, word2)

    print(f"\n{word1} - {word2}")
    print(f"Similarity: {score:.2f}")
    print(get_feedback(score))
