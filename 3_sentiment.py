# ============================================================
# FILE 3: SENTIMENT ANALYSIS
# ============================================================
# Yeh file har comment ka sentiment nikaalti hai:
# - Positive
# - Negative
# - Neutral
# Aur channel-wise summary bhi banati hai
# ============================================================

import pandas as pd
from textblob import TextBlob

print("\n" + "="*70)
print("🧠 STEP 3: SENTIMENT ANALYSIS")
print("="*70)

# Load clean data
df = pd.read_csv('clean_comments.csv')
print(f"\n📂 Comments to analyze: {len(df)}")

# ============================================================
# Sentiment Function
# ============================================================
def get_sentiment(text):
    try:
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.05:
            return 'Positive'
        elif polarity < -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    except:
        return 'Neutral'

print("\n🔍 Analyzing sentiment (yeh thoda waqt lega)...")
df['sentiment'] = df['clean_comment'].apply(get_sentiment)

# Save results
df.to_csv('sentiment_results.csv', index=False, encoding='utf-8')

# ============================================================
# SUMMARY 1: Overall Sentiment
# ============================================================
print("\n" + "="*70)
print("📊 OVERALL SENTIMENT SUMMARY")
print("="*70)

overall = df['sentiment'].value_counts()
total = len(df)

for sentiment in ['Positive', 'Negative', 'Neutral']:
    count = overall.get(sentiment, 0)
    percent = (count / total) * 100
    print(f"   {sentiment:10s}: {count:5d}  ({percent:.2f}%)")

print(f"\n   TOTAL: {total} comments")

# ============================================================
# SUMMARY 2: Channel-wise Sentiment
# ============================================================
print("\n" + "="*70)
print("📊 CHANNEL-WISE SENTIMENT")
print("="*70)

channel_sentiment = df.groupby(['channel_name', 'sentiment']).size().unstack(fill_value=0)
print(channel_sentiment)

# Save channel summary
channel_sentiment.to_csv('channel_sentiment_summary.csv')
print("\n✅ Saved: channel_sentiment_summary.csv")

# ============================================================
# SUMMARY 3: Video-wise Sentiment
# ============================================================
print("\n" + "="*70)
print("📊 VIDEO-WISE SENTIMENT (Top 10)")
print("="*70)

video_sentiment = df.groupby(['video_title', 'sentiment']).size().unstack(fill_value=0)
print(video_sentiment.head(10))

# Save video summary
video_sentiment.to_csv('video_sentiment_summary.csv')
print("\n✅ Saved: video_sentiment_summary.csv")

# ============================================================
# TOP POSITIVE / NEGATIVE COMMENTS
# ============================================================
print("\n" + "="*70)
print("😊 TOP 5 MOST POSITIVE COMMENTS")
print("="*70)

df['polarity'] = df['clean_comment'].apply(
    lambda x: TextBlob(str(x)).sentiment.polarity
)

top_positive = df.nlargest(5, 'polarity')
for i, row in top_positive.iterrows():
    print(f"\n   [{row['channel_name']}]")
    print(f"   {row['comment'][:120]}...")
    print(f"   Polarity: {row['polarity']:.3f}")

print("\n" + "="*70)
print("😠 TOP 5 MOST NEGATIVE COMMENTS")
print("="*70)

top_negative = df.nsmallest(5, 'polarity')
for i, row in top_negative.iterrows():
    print(f"\n   [{row['channel_name']}]")
    print(f"   {row['comment'][:120]}...")
    print(f"   Polarity: {row['polarity']:.3f}")

print("\n" + "="*70)
print("🎉 SENTIMENT ANALYSIS COMPLETED!")
print("="*70)