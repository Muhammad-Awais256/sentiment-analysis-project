# ============================================================
# FILE 4: EDA - GRAPHS & VISUALIZATIONS
# ============================================================
# Yeh file 5 graphs banati hai:
# 1. Overall sentiment bar chart
# 2. Pie chart
# 3. Channel-wise sentiment
# 4. Word cloud
# 5. Top channels
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

print("\n" + "="*70)
print("📊 STEP 4: EDA & VISUALIZATIONS")
print("="*70)

df = pd.read_csv('sentiment_results.csv')
print(f"\n📂 Loaded {len(df)} comments for visualization")

colors = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
sentiment_counts = df['sentiment'].value_counts()

# ============================================================
# 1. Overall Sentiment Bar Chart
# ============================================================
print("\n🎨 Creating Chart 1: Overall Sentiment...")

plt.figure(figsize=(8, 5))
bars = plt.bar(sentiment_counts.index, sentiment_counts.values,
               color=[colors.get(x, 'blue') for x in sentiment_counts.index])
plt.title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Sentiment', fontsize=12)
plt.ylabel('Number of Comments', fontsize=12)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig('1_overall_sentiment.png', dpi=150)
plt.close()
print("   ✅ Saved: 1_overall_sentiment.png")

# ============================================================
# 2. Pie Chart
# ============================================================
print("\n🎨 Creating Chart 2: Sentiment Pie...")

plt.figure(figsize=(7, 7))
plt.pie(sentiment_counts.values, labels=sentiment_counts.index,
        autopct='%1.1f%%', startangle=90,
        colors=[colors.get(x, 'blue') for x in sentiment_counts.index],
        textprops={'fontsize': 12})
plt.title('Sentiment Percentage', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('2_sentiment_pie.png', dpi=150)
plt.close()
print("   ✅ Saved: 2_sentiment_pie.png")

# ============================================================
# 3. Channel-wise Sentiment
# ============================================================
print("\n🎨 Creating Chart 3: Channel-wise Sentiment...")

channel_sent = df.groupby(['channel_name', 'sentiment']).size().unstack(fill_value=0)
channel_sent = channel_sent.sort_values(by=channel_sent.columns[0], ascending=True)

plt.figure(figsize=(10, 8))
channel_sent.plot(kind='barh', stacked=True, ax=plt.gca(),
                  color=[colors.get(x, 'blue') for x in channel_sent.columns])
plt.title('Channel-wise Sentiment Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Number of Comments', fontsize=12)
plt.ylabel('Channel Name', fontsize=12)
plt.legend(title='Sentiment')
plt.tight_layout()
plt.savefig('3_channel_sentiment.png', dpi=150)
plt.close()
print("   ✅ Saved: 3_channel_sentiment.png")

# ============================================================
# 4. Word Cloud
# ============================================================
print("\n🎨 Creating Chart 4: Word Cloud...")

text = ' '.join(df['clean_comment'].dropna().astype(str))
if len(text) > 100:
    wc = WordCloud(width=1200, height=600, background_color='white',
                   max_words=100, colormap='viridis').generate(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Most Common Words in Comments', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('4_wordcloud.png', dpi=150)
    plt.close()
    print("   ✅ Saved: 4_wordcloud.png")

# ============================================================
# 5. Top 10 Channels
# ============================================================
print("\n🎨 Creating Chart 5: Top Channels...")

plt.figure(figsize=(10, 6))
top_channels = df['channel_name'].value_counts().head(10)
top_channels.plot(kind='bar', color='steelblue')
plt.title('Top 10 Channels by Number of Comments', fontsize=14, fontweight='bold')
plt.xlabel('Channel Name', fontsize=12)
plt.ylabel('Number of Comments', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('5_top_channels.png', dpi=150)
plt.close()
print("   ✅ Saved: 5_top_channels.png")

print("\n" + "="*70)
print("🎉 ALL VISUALIZATIONS COMPLETED!")
print("="*70)
print("\n📁 OUTPUT FILES:")
print("   📊 1_overall_sentiment.png")
print("   📊 2_sentiment_pie.png")
print("   📊 3_channel_sentiment.png")
print("   📊 4_wordcloud.png")
print("   📊 5_top_channels.png")
print("="*70)