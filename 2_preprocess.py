# ============================================================
# FILE 2: DATA PREPROCESSING (CLEANING)
# ============================================================
# Yeh file raw comments ko saaf karti hai:
# - Lowercase karti hai
# - Links, emojis, mentions hataati hai
# - Stopwords (the, is, at) hataati hai
# ============================================================

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Load raw data
print("\n" + "="*70)
print("🧹 STEP 2: DATA PREPROCESSING")
print("="*70)

df = pd.read_csv('raw_comments.csv')
print(f"\n📂 Original comments loaded: {len(df)}")

# Stopwords load karein
stop_words = set(stopwords.words('english'))
print(f"📚 Total stopwords: {len(stop_words)}")

# ============================================================
# Cleaning Function
# ============================================================
def clean_text(text):
    text = str(text).lower()                        # Lowercase
    text = re.sub(r'http\S+', '', text)             # Links hatao
    text = re.sub(r'www\.\S+', '', text)            # www hatao
    text = re.sub(r'@\w+', '', text)                # Mentions hatao
    text = re.sub(r'#\w+', '', text)                # Hashtags hatao
    text = re.sub(r'[^a-zA-Z\s]', '', text)         # Sirf letters
    text = re.sub(r'\s+', ' ', text).strip()        # Extra spaces
    return text

print("\n🧼 Cleaning comments...")
df['clean_comment'] = df['comment'].apply(clean_text)

# Khali comments hatao
before = len(df)
df = df[df['clean_comment'].str.len() > 3]
print(f"   Removed {before - len(df)} empty/short comments")

# Stopwords hatao
df['clean_comment'] = df['clean_comment'].apply(
    lambda x: ' '.join([w for w in x.split() if w not in stop_words])
)

# Khali rows dobara hatao
before = len(df)
df = df[df['clean_comment'].str.len() > 0]
print(f"   Removed {before - len(df)} more empty comments")

# Save
df.to_csv('clean_comments.csv', index=False, encoding='utf-8')

print("\n" + "="*70)
print(f"✅ CLEANED COMMENTS: {len(df)}")
print("="*70)
print("\n📊 FIRST 5 CLEANED COMMENTS:")
print("-"*70)
for i, row in df.head(5).iterrows():
    print(f"\n{i+1}. [{row['channel_name']}]")
    print(f"   Original: {row['comment'][:80]}...")
    print(f"   Cleaned:  {row['clean_comment'][:80]}...")