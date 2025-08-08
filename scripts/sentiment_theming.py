 
# ─────────────────────────────────────────────
# 📦 Step 0: Import Required Libraries
# ─────────────────────────────────────────────
import pandas as pd
from tqdm import tqdm
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import spacy

# ─────────────────────────────────────────────
# 📥 Step 1: Load Preprocessed Data
# ─────────────────────────────────────────────
df = pd.read_csv("cleaned_reviews.csv")

# ─────────────────────────────────────────────
# 🧠 Step 2: Sentiment Analysis with DistilBERT
# ─────────────────────────────────────────────
print("🔍 Running sentiment analysis...")
tqdm.pandas()
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Apply model on reviews (truncate at 512 characters to avoid overflow)
df["sentiment_result"] = df["review"].progress_apply(lambda x: sentiment_model(x[:512])[0])
df["sentiment_label"] = df["sentiment_result"].apply(lambda x: x["label"])
df["sentiment_score"] = df["sentiment_result"].apply(lambda x: round(x["score"], 3))

# Optional: Convert "LABEL_1"/"LABEL_2" into Positive/Negative if needed
df["sentiment_label"] = df["sentiment_label"].str.capitalize()

# ─────────────────────────────────────────────
# 💬 Step 3: Keyword Extraction per Bank (TF-IDF)
# ─────────────────────────────────────────────
print("🧠 Extracting keywords with TF-IDF...")
keywords_by_bank = defaultdict(list)

for bank in df["bank"].unique():
    bank_reviews = df[df["bank"] == bank]["review"]
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2), stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(bank_reviews)
    keywords = vectorizer.get_feature_names_out()
    keywords_by_bank[bank] = keywords[:15]

print("Top keywords per bank:")
for bank, words in keywords_by_bank.items():
    print(f"{bank}: {', '.join(words)}")

# ─────────────────────────────────────────────
# 🏷 Step 4: Rule-Based Thematic Clustering
# ─────────────────────────────────────────────
print("🔖 Grouping keywords into high-level themes...")

# Manually defined themes based on recurring review issues
theme_rules = {
    "Account Access Issues": ["login", "sign in", "password", "authentication"],
    "Transaction Performance": ["slow", "transfer", "payment", "crash", "delay", "failed"],
    "User Interface & Experience": ["interface", "design", "easy", "navigation", "dark mode"],
    "Customer Support": ["support", "help", "customer", "response", "contact"],
    "Feature Requests": ["fingerprint", "notification", "biometric", "alert", "balance"]
}

def identify_themes(text):
    matches = []
    text_lower = text.lower()
    for theme, keywords in theme_rules.items():
        if any(kw in text_lower for kw in keywords):
            matches.append(theme)
    return ", ".join(matches) if matches else "Other"

df["themes"] = df["review"].progress_apply(identify_themes)

# ─────────────────────────────────────────────
# 💾 Step 5: Save Final Output
# ─────────────────────────────────────────────
df_final = df[["review", "rating", "date", "bank", "source", "sentiment_label", "sentiment_score", "themes"]]
df_final.to_csv("task2_sentiment_themes.csv", index=False, encoding="utf-8-sig")
print("✅ Sentiment and theme analysis saved to 'task2_sentiment_themes.csv'")
