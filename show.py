from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    messages_num = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return messages_num, len(words), media_messages, len(links)

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] 

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] 

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def activity_map_week(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] 

    return df['day_name'].value_counts()

def activity_map_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] 

    return df['month'].value_counts()

def most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns = {'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
     
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    remove = df[df['user'] != 'group_notification']
    remove = remove[remove['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)
    wc = WordCloud(width = 500,height = 500,min_font_size = 10,background_color = 'white')
    remove['message'] = remove['message'].apply(remove_stop_words)
    df_wc = wc.generate(remove['message'].str.cat(sep = " "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
     
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    remove = df[df['user'] != 'group_notification']
    remove = remove[remove['message'] != '<Media omitted>\n']

    words = []

    for message in remove['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_show(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    def extract_emojis(text):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U0001F004-\U0001F0CF"  # Miscellaneous Symbols and Pictographs
                               u"\U0001F170-\U0001F251"  # Enclosed Characters
                               "]+", flags=re.UNICODE)
        return ''.join(emoji_pattern.findall(text))

    emojis = []
    for message in df['message']:
        extracted_emojis = extract_emojis(message)
        emojis.extend(extracted_emojis)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)

    return activity_heatmap