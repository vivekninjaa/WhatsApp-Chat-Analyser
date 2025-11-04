from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


# Initialize the URL extractor
extractor = URLExtract()


# Fetch basic statistics: total messages, words, media messages, and links
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch number of media messages
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # Fetch number of links
    links = []
    for message in df['message']:
        urls = extractor.find_urls(message)  # Extract URLs from the message
        links.extend(urls)

    return num_messages, len(words), num_media_messages, len(links)


# Fetch most active users and their percentage of activity
def most_busy_users(df):
    # Fetch top 5 users based on message count
    x = df['user'].value_counts().head()

    # Calculate percentage of messages sent by each user
    user_percent = round(100 * (df['user'].value_counts() / df.shape[0]), 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return x, user_percent


# Generate a word cloud based on the chat data
def create_wordcloud(selected_user, df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Load stopwords for filtering
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    with open('stopwords-hi.txt', 'r') as f2:
        hindi_stopwords = f2.read()

    # Helper function to remove stopwords from a message
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words and word not in hindi_stopwords:
                y.append(word)
        return " ".join(y)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Apply stopword removal
    temp['message'] = temp['message'].apply(remove_stopwords)

    # Generate word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


# Fetch the 20 most common words from the chat data
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Load stopwords for filtering
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    with open('stopwords-hi.txt', 'r') as f2:
        hindi_stopwords = f2.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in hindi_stopwords:
                words.append(word)

    # Create DataFrame of the 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


# Helper function to analyze emoji usage in chat data
emoji_dict = {
    '🎂': 'Birthday Cake',
    '🙏': 'Thank You',
    '❤️': 'Love',
    '🎉': 'Celebration',
    '🎊': 'Confetti',
    '🏻': 'Skin Tone 1',
    '🥰': 'Smiling Face with Hearts',
    '🥳': 'Party Face',
    '🎁': 'Gift',
    '🌹': 'Rose',
    '🩷': 'Light Pink Heart',
    '🍰': 'Cake Slice',
    '🍬': 'Candy',
    '🍭': 'Lollipop',
    '☕': 'Hot Beverage',
    '🙂': 'Slightly Smiling Face',
    '🙊': 'Speak No Evil',
    '🚩': 'Triangular Flag',
    '💐': 'Bouquet',
    '✌': 'Victory Hand',
    '❣': 'Heart Exclamation',
    '😘': 'Face Blowing a Kiss',
    '🍫': 'Chocolate Bar',
    '🤔': 'Thinking Face',
    '💓': 'Beating Heart',
    '💕': 'Two Hearts',
    '✅': 'Check Mark',
    '🥧': 'Pie',
    '🍎': 'Red Apple',
    '👌': 'OK Hand',
    '😢': 'Crying Face',
    '🤗': 'Hugging Face',
    '😍': 'Smiling Face with Heart-Eyes',
    '💗': 'Growing Heart',
    '⛳': 'Flag in Hole',
    '😳': 'Flushed Face',
    '👆': 'Backhand Index Pointing Up',
    '🥮': 'Moon Cake',
    '🧁': 'Cupcake',
    '👏': 'Clapping Hands',
    '🌀': 'Cyclone',
    '🪷': 'Lotus',
    '🎈': 'Balloon',
    '💖': 'Sparkling Heart',
    '🍩': 'Doughnut',
    '✍': 'Writing Hand',
    '💃': 'Dancing Woman',
    '🏽': 'Skin Tone 4',
    '😯': 'Hushed Face',
    '🤭': 'Face with Hand Over Mouth',
    '😂': 'Face with Tears of Joy',
    '‼': 'Double Exclamation Mark',
    '🥎': 'Softball',
    '✨': 'Sparkles',
    '👞': 'Man’s Shoe',
    '🧿': 'Nazar Amulet',
    '😞': 'Disappointed Face',
    '😱': 'Face Screaming in Fear',
    '🤫': 'Shushing Face',
    '🎇': 'Sparkler',
    '😊': 'Smiling Face with Smiling Eyes',
    '☠': 'Skull',
    '®': 'Registered Trademark',
    '✊': 'Raised Fist',
    '🙄': 'Face with Rolling Eyes',
    '🤦': 'Face Palm',
    '♀': 'Female Sign',
    '🤝': 'Handshake',
    '💪': 'Flexed Biceps',
    '😟': 'Worried Face',
    '🥴': 'Woozy Face',
    '😏': 'Smirking Face',
    '😑': 'Expressionless Face',
    '😉': 'Winking Face',
    '😇': 'Smiling Face with Halo',
    '👸': 'Princess',
    '🫡': 'Saluting Face',
    '👇': 'Backhand Index Pointing Down',
    '❗': 'Exclamation Mark',
    '👍': 'Thumbs Up'
}
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji_dict])  # Use emoji_dict for compatibility

    # Count the occurrences of each emoji
    emoji_counts = Counter(emojis).most_common()

    # Prepare result dictionary
    result = {
        'Emoji': [],
        'Count': [],
        'Description': []
    }

    # Populate result dictionary with emoji data
    for emoji_char, count in emoji_counts:
        result['Emoji'].append(emoji_char)
        result['Count'].append(count)
        result['Description'].append(emoji_dict.get(emoji_char, "Unknown"))  # Fallback to 'Unknown'

    # Convert result to DataFrame
    emoji_df = pd.DataFrame(result)

    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_heatmap




