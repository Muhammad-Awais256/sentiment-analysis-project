# ============================================================
# SENTIMENT ANALYSIS GUI - Dashboard
# ============================================================
# Yeh file ek GUI banati hai jisme buttons hain:
# - Data Load karo
# - Sentiment Show karo (Positive/Negative/Neutral)
# - Graphs dekho
# - Channel-wise dekho
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

# ============================================================
# MAIN WINDOW SETUP
# ============================================================
root = tk.Tk()
root.title("📊 Sentiment Analysis Dashboard")
root.geometry("1400x800")
root.configure(bg="#2c3e50")

# Global variables
df_sentiment = None
df_clean = None

# ============================================================
# HEADER
# ============================================================
header = tk.Frame(root, bg="#1abc9c", height=80)
header.pack(fill=tk.X)

title_label = tk.Label(
    header,
    text="📊 YOUTUBE COMMENTS SENTIMENT ANALYSIS DASHBOARD",
    font=("Arial", 20, "bold"),
    bg="#1abc9c",
    fg="white"
)
title_label.pack(pady=20)

# ============================================================
# LEFT SIDEBAR - Buttons
# ============================================================
sidebar = tk.Frame(root, bg="#34495e", width=280)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)

menu_title = tk.Label(
    sidebar,
    text="🎛️ MENU",
    font=("Arial", 16, "bold"),
    bg="#34495e",
    fg="white"
)
menu_title.pack(pady=20)

# ============================================================
# MAIN CONTENT AREA
# ============================================================
content = tk.Frame(root, bg="#ecf0f1")
content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ============================================================
# FUNCTIONS
# ============================================================

def clear_content():
    """Content area saaf karein"""
    for widget in content.winfo_children():
        widget.destroy()


def load_data():
    """CSV files load karein"""
    global df_sentiment, df_clean
    try:
        if os.path.exists('sentiment_results.csv'):
            df_sentiment = pd.read_csv('sentiment_results.csv')
        if os.path.exists('clean_comments.csv'):
            df_clean = pd.read_csv('clean_comments.csv')
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Data load nahi hua:\n{e}")
        return False


def show_summary():
    """Overall summary dikhayein"""
    clear_content()
    load_data()

    if df_sentiment is None:
        messagebox.showwarning("Warning", "Pehle '3_sentiment.py' chalayein!\nsentiment_results.csv nahi mili.")
        return

    # Title
    tk.Label(content, text="📊 OVERALL SENTIMENT SUMMARY",
             font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    # Stats Frame
    stats_frame = tk.Frame(content, bg="#ecf0f1")
    stats_frame.pack(pady=20)

    counts = df_sentiment['sentiment'].value_counts()
    total = len(df_sentiment)

    colors = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}

    for sentiment in ['Positive', 'Negative', 'Neutral']:
        count = counts.get(sentiment, 0)
        percent = (count / total) * 100

        card = tk.Frame(stats_frame, bg=colors[sentiment], width=280, height=180)
        card.pack(side=tk.LEFT, padx=15)
        card.pack_propagate(False)

        tk.Label(card, text=sentiment.upper(), font=("Arial", 14, "bold"),
                 bg=colors[sentiment], fg="white").pack(pady=15)

        tk.Label(card, text=str(count), font=("Arial", 36, "bold"),
                 bg=colors[sentiment], fg="white").pack()

        tk.Label(card, text=f"({percent:.1f}%)", font=("Arial", 14),
                 bg=colors[sentiment], fg="white").pack(pady=10)

    # Total
    tk.Label(content, text=f"TOTAL COMMENTS: {total}",
             font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    # Top Comments
    tk.Label(content, text="🔥 TOP 3 POSITIVE COMMENTS",
             font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#27ae60").pack(pady=10)

    top_pos = df_sentiment.nlargest(3, 'comment') if 'comment' in df_sentiment.columns else df_sentiment.head(3)

    for i, row in top_pos.iterrows():
        text = str(row['comment'])[:100]
        tk.Label(content, text=f"• {text}...", font=("Arial", 10),
                 bg="#ecf0f1", fg="#2c3e50", wraplength=900, justify=tk.LEFT).pack(anchor=tk.W, padx=40, pady=3)


def show_channel_summary():
    """Channel-wise summary dikhayein"""
    clear_content()
    load_data()

    if df_sentiment is None:
        messagebox.showwarning("Warning", "Pehle '3_sentiment.py' chalayein!")
        return

    tk.Label(content, text="📺 CHANNEL-WISE SENTIMENT",
             font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    # Treeview
    frame = tk.Frame(content, bg="#ecf0f1")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    tree = ttk.Treeview(frame, columns=("Channel", "Positive", "Negative", "Neutral", "Total"),
                        show='headings', height=15)

    tree.heading("Channel", text="Channel Name")
    tree.heading("Positive", text="😊 Positive")
    tree.heading("Negative", text="😠 Negative")
    tree.heading("Neutral", text="😐 Neutral")
    tree.heading("Total", text="📊 Total")

    tree.column("Channel", width=250)
    tree.column("Positive", width=120)
    tree.column("Negative", width=120)
    tree.column("Neutral", width=120)
    tree.column("Total", width=100)

    channel_summary = df_sentiment.groupby(['channel_name', 'sentiment']).size().unstack(fill_value=0)
    channel_summary['Total'] = channel_summary.sum(axis=1)
    channel_summary = channel_summary.sort_values('Total', ascending=False)

    for channel, row in channel_summary.iterrows():
        tree.insert('', tk.END, values=(
            channel,
            row.get('Positive', 0),
            row.get('Negative', 0),
            row.get('Neutral', 0),
            row['Total']
        ))

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def show_chart(filename, title):
    """Chart image dikhayein"""
    clear_content()

    tk.Label(content, text=title, font=("Arial", 18, "bold"),
             bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    if not os.path.exists(filename):
        messagebox.showwarning("Warning", f"Pehle '4_eda.py' chalayein!\n{filename} nahi mili.")
        return

    try:
        img = Image.open(filename)
        img = img.resize((900, 550), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(content, image=photo, bg="#ecf0f1")
        label.image = photo
        label.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Image load nahi hui:\n{e}")


def show_live_chart():
    """Live chart banayein matplotlib se"""
    clear_content()
    load_data()

    if df_sentiment is None:
        messagebox.showwarning("Warning", "Pehle '3_sentiment.py' chalayein!")
        return

    tk.Label(content, text="📊 LIVE SENTIMENT CHART",
             font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart
    counts = df_sentiment['sentiment'].value_counts()
    colors_map = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
    bars = ax1.bar(counts.index, counts.values,
                   color=[colors_map.get(x, 'blue') for x in counts.index])
    ax1.set_title('Overall Sentiment', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Comments')
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}', ha='center', va='bottom')

    # Pie chart
    ax2.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
            colors=[colors_map.get(x, 'blue') for x in counts.index])
    ax2.set_title('Sentiment Percentage', fontsize=14, fontweight='bold')

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=content)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


def show_wordcloud():
    """Wordcloud dikhayein"""
    show_chart('4_wordcloud.png', '☁️ WORD CLOUD')


def show_stats_text():
    """Text stats dikhayein"""
    clear_content()
    load_data()

    if df_sentiment is None:
        messagebox.showwarning("Warning", "Pehle '3_sentiment.py' chalayein!")
        return

    tk.Label(content, text="📈 DETAILED STATISTICS",
             font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    text_frame = tk.Frame(content, bg="#ecf0f1")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    text_widget = tk.Text(text_frame, font=("Consolas", 12), bg="white", fg="#2c3e50", wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Stats
    counts = df_sentiment['sentiment'].value_counts()
    total = len(df_sentiment)

    stats = f"""
╔══════════════════════════════════════════════════════════╗
║           SENTIMENT ANALYSIS STATISTICS                  ║
╚══════════════════════════════════════════════════════════╝

📊 TOTAL COMMENTS ANALYZED: {total}

😊 POSITIVE COMMENTS  : {counts.get('Positive', 0)}  ({counts.get('Positive', 0)/total*100:.2f}%)
😠 NEGATIVE COMMENTS  : {counts.get('Negative', 0)}  ({counts.get('Negative', 0)/total*100:.2f}%)
😐 NEUTRAL COMMENTS   : {counts.get('Neutral', 0)}  ({counts.get('Neutral', 0)/total*100:.2f}%)

📺 TOTAL CHANNELS: {df_sentiment['channel_name'].nunique()}
🎬 TOTAL VIDEOS: {df_sentiment['video_title'].nunique()}

═══════════════════════════════════════════════════════════
                  TOP 5 CHANNELS
═══════════════════════════════════════════════════════════
"""
    top_channels = df_sentiment['channel_name'].value_counts().head(5)
    for i, (channel, count) in enumerate(top_channels.items(), 1):
        stats += f"\n{i}. {channel}: {count} comments"

    stats += "\n\n═══════════════════════════════════════════════════════════\n"
    stats += "                  INSIGHTS\n"
    stats += "═══════════════════════════════════════════════════════════\n\n"

    pos_pct = counts.get('Positive', 0)/total*100
    if pos_pct > 50:
        stats += "✅ OVERALL SENTIMENT: POSITIVE\n"
        stats += "   Logon ka raye positive hai. Product launch ke liye acha waqt hai!\n"
    elif pos_pct > 30:
        stats += "⚠️ OVERALL SENTIMENT: MIXED\n"
        stats += "   Kuch log khush hain, kuch naraz. Feedback zaroor dekh lein.\n"
    else:
        stats += "❌ OVERALL SENTIMENT: NEGATIVE\n"
        stats += "   Logon ki raye negative hai. Product improve karein.\n"

    text_widget.insert(tk.END, stats)
    text_widget.config(state=tk.DISABLED)


def exit_app():
    """App band karein"""
    if messagebox.askyesno("Exit", "Kya aap dashboard band karna chahte hain?"):
        root.destroy()


# ============================================================
# BUTTONS
# ============================================================

btn_style = {
    'font': ("Arial", 12, "bold"),
    'bg': "#3498db",
    'fg': "white",
    'activebackground': "#2980b9",
    'activeforeground': "white",
    'relief': tk.FLAT,
    'width': 22,
    'height': 2,
    'cursor': "hand2"
}

# Button 1: Summary
btn1 = tk.Button(sidebar, text="📊 Overall Summary", command=show_summary, **btn_style)
btn1.pack(pady=8, padx=20)

# Button 2: Channel Summary
btn2 = tk.Button(sidebar, text="📺 Channel-wise", command=show_channel_summary, **btn_style)
btn2.pack(pady=8, padx=20)

# Button 3: Live Chart
btn3 = tk.Button(sidebar, text="📈 Live Charts", command=show_live_chart, **btn_style)
btn3.pack(pady=8, padx=20)

# Button 4: Bar Chart
btn4 = tk.Button(sidebar, text="📉 Overall Chart", 
                 command=lambda: show_chart('1_overall_sentiment.png', '📉 OVERALL SENTIMENT'),
                 **btn_style)
btn4.pack(pady=8, padx=20)

# Button 5: Pie Chart
btn5 = tk.Button(sidebar, text="🥧 Pie Chart",
                 command=lambda: show_chart('2_sentiment_pie.png', '🥧 SENTIMENT PIE'),
                 **btn_style)
btn5.pack(pady=8, padx=20)

# Button 6: Channel Chart
btn6 = tk.Button(sidebar, text="📊 Channel Chart",
                 command=lambda: show_chart('3_channel_sentiment.png', '📊 CHANNEL-WISE SENTIMENT'),
                 **btn_style)
btn6.pack(pady=8, padx=20)

# Button 7: Word Cloud
btn7 = tk.Button(sidebar, text="☁️ Word Cloud", command=show_wordcloud, **btn_style)
btn7.pack(pady=8, padx=20)

# Button 8: Top Channels
btn8 = tk.Button(sidebar, text="🏆 Top Channels",
                 command=lambda: show_chart('5_top_channels.png', '🏆 TOP 10 CHANNELS'),
                 **btn_style)
btn8.pack(pady=8, padx=20)

# Button 9: Detailed Stats
btn9 = tk.Button(sidebar, text="📈 Detailed Stats", command=show_stats_text, **btn_style)
btn9.pack(pady=8, padx=20)

# Button 10: Exit
exit_btn_style = btn_style.copy()
exit_btn_style['bg'] = "#e74c3c"
exit_btn_style['activebackground'] = "#c0392b"

btn10 = tk.Button(sidebar, text="❌ Exit", command=exit_app, **exit_btn_style)
btn10.pack(pady=20, padx=20)

# ============================================================
# WELCOME SCREEN
# ============================================================
welcome_frame = tk.Frame(content, bg="#ecf0f1")
welcome_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(welcome_frame, text="👋 WELCOME!",
         font=("Arial", 32, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=80)

tk.Label(welcome_frame,
         text="Sentiment Analysis Dashboard\n\nLeft side ke buttons se results dekhein!",
         font=("Arial", 16), bg="#ecf0f1", fg="#7f8c8d").pack(pady=20)

tk.Label(welcome_frame,
         text="👈 Click any button on the left menu",
         font=("Arial", 14, "italic"), bg="#ecf0f1", fg="#3498db").pack(pady=30)

# ============================================================
# RUN
# ============================================================
root.mainloop()