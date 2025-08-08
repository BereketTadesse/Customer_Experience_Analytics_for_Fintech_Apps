# ─────────────────────────────────────────────
# 📦 Step 0: Import Required Libraries
# ─────────────────────────────────────────────
import pandas as pd
import re
from tqdm import tqdm
from langdetect import detect, DetectorFactory
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import spacy

# Enable consistent language detection
DetectorFactory.seed = 0
tqdm.pandas()

# ─────────────────────────────────────────────
# 📥 Step 1: Load Raw Reviews
# ─────────────────────────────────────────────
df = pd.read_csv("mobile_bank_reviews.csv")

# ─────────────────────────────────────────────
# 🧹 Step 2: Basic Cleaning (drop nulls, normalize dates)
# ─────────────────────────────────────────────
df.dropna(subset=["ReviewText", "Rating"], inplace=True)
df["ReviewDate"] = pd.to_datetime(df["ReviewDate"], errors="coerce").dt.strftime('%Y-%m-%d')
df = df[df["ReviewText"].str.strip() != ""]

# ─────────────────────────────────────────────
# 🚫 Step 3: Language & Gibberish Filtering
# ─────────────────────────────────────────────
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def is_gibberish(text):
    if re.search(r"(.)\1{4,}", text):  # repeated chars
        return True
    if len(re.findall(r"[a-zA-Z]", text)) < 3:
        return True
    return False

print("🌐 Detecting languages and filtering gibberish...")
df["lang"] = df["ReviewText"].progress_apply(detect_language)
df = df[df["lang"] == "en"]

df = df[~df["ReviewText"].apply(is_gibberish)]
df.drop(columns=["lang"], inplace=True)

df.to_csv("cleaned.csv", index=False, encoding="utf-8-sig")
print("✅ Saved results to 'cleaned.csv'")