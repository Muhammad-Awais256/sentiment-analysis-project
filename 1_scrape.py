# ============================================================
# FILE 1: SCRAPE COMMENTS FROM YOUTUBE
# ============================================================
# Yeh file YouTube se videos search karti hai aur unke comments
# nikal kar CSV file mein save karti hai (channel name ke saath)
# ============================================================

from googleapiclient.discovery import build
import pandas as pd

# ============================================================
# 🔑 YAHAN APNI NAYI API KEY DAALEIN
# ============================================================
# Purani key delete kar dein aur yeh nayi key paste karein
# Yeh key "AIzaSyC..." se shuru hoti hai

API_KEY = "Write Your API KEY"

# ============================================================
# YouTube API Connect Karein
# ============================================================
youtube = build('youtube', 'v3', developerKey=API_KEY)

# ============================================================
# 🔍 Aapka Topic (Yahan Apni Marzi Se Change Karein)
# ============================================================
# Options:
#   "smart watch review"      -> Smart watches
#   "handbag review"          -> Handbags
#   "school bag review"       -> School bags
#   "casio watch review"      -> Casio watches
#   "apple watch review"      -> Apple watches

search_query = "smart watch review"

print("\n" + "="*70)
print(f"🎯 SEARCH TOPIC: {search_query}")
print("="*70)

# ============================================================
# STEP 1: YouTube Par Videos Search Karein
# ============================================================
print("\n🔍 Searching videos on YouTube...\n")

search_response = youtube.search().list(
    q=search_query,
    part='id,snippet',
    maxResults=25,           # 25 videos
    type='video',
    order='relevance'        # Best match videos
).execute()

# Videos ki detail nikaalein (channel name ke saath)
video_info = []
for item in search_response['items']:
    video_info.append({
        'video_id': item['id']['videoId'],
        'video_title': item['snippet']['title'],
        'channel_name': item['snippet']['channelTitle'],
        'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    })

# ============================================================
# STEP 2: Selected Videos Ki List Print Karein
# ============================================================
print(f"\n📺 TOTAL {len(video_info)} VIDEOS SELECTED:\n")
print("-" * 70)

for i, v in enumerate(video_info, 1):
    print(f"{i}. {v['video_title'][:65]}")
    print(f"   📢 Channel: {v['channel_name']}")
    print(f"   🔗 URL: {v['video_url']}")
    print()

print("-" * 70)

# ============================================================
# STEP 3: Comments Nikalne Ka Function
# ============================================================
def get_comments(video_id, video_title, channel_name, video_url, max_comments=500):
    """
    Yeh function ek video se comments nikalta hai.
    Har comment ke saath channel name aur video title bhi save karta hai.
    """
    comments = []
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            textFormat='plainText'
        ).execute()

        while response and len(comments) < max_comments:
            for item in response['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append({
                    'comment': comment_text,
                    'video_title': video_title,
                    'channel_name': channel_name,
                    'video_id': video_id,
                    'video_url': video_url
                })
                if len(comments) >= max_comments:
                    break

            # Agla page (agar aur comments hain)
            if 'nextPageToken' in response and len(comments) < max_comments:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response['nextPageToken'],
                    textFormat='plainText'
                ).execute()
            else:
                break
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    return comments

# ============================================================
# STEP 4: Saare Videos Se Comments Collect Karein
# ============================================================
print("\n" + "="*70)
print("📥 SCRAPING COMMENTS (YEH THODA WAQT LEGA)...")
print("="*70 + "\n")

all_comments = []

for i, v in enumerate(video_info, 1):
    if len(all_comments) >= 3200:        # 3000+ ka buffer
        break
    print(f"[{i}/{len(video_info)}] Scraping: {v['video_title'][:50]}...")
    print(f"      Channel: {v['channel_name']}")
    comments = get_comments(
        v['video_id'],
        v['video_title'],
        v['channel_name'],
        v['video_url'],
        max_comments=500
    )
    all_comments.extend(comments)
    print(f"      ✅ Total so far: {len(all_comments)}\n")

# ============================================================
# STEP 5: Data Save Karein (CSV File)
# ============================================================
df = pd.DataFrame(all_comments)
df.to_csv('raw_comments.csv', index=False, encoding='utf-8')

# ============================================================
# STEP 6: Summary Print Karein
# ============================================================
print("\n" + "="*70)
print(f"✅ TOTAL {len(df)} COMMENTS SAVED TO 'raw_comments.csv'")
print("="*70)

print("\n📊 COMMENTS PER CHANNEL:")
print("-" * 70)
print(df['channel_name'].value_counts())

print("\n📊 COMMENTS PER VIDEO (Top 10):")
print("-" * 70)
print(df['video_title'].value_counts().head(10))

print("\n📊 FIRST 5 COMMENTS (Preview):")
print("-" * 70)
for i, row in df.head(5).iterrows():
    print(f"\n{i+1}. [{row['channel_name']}]")
    print(f"   {row['comment'][:100]}...")

print("\n" + "="*70)
print("🎉 SCRAPING COMPLETED SUCCESSFULLY!")
print("="*70)