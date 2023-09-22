from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # fetch Number of messages
    num_messages = df.shape[0]

    # fetch Number of Words
    words = []
    for i in df['Message']:
        words.extend(i.split())

    # fetch number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    extract = URLExtract()
    links = []
    for i in df['Message']:
        links.extend(extract.find_urls(i))


    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'User': 'Percent'})
    return x, df


def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words :
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    Emojis = []
    for message in df['Message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                Emojis.extend(c)

    emoji_df = pd.DataFrame(Counter(Emojis).most_common(len(Counter(Emojis))),columns=["Emoji", "Count"])

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month', 'month_name']).count()['Message'].reset_index()
    timeline['time'] = timeline['month_name'] + ' - ' + timeline['Year'].astype(str)

    return timeline

def Daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    Daily_timeline = df.groupby(['only_Date']).count()['Message'].reset_index()

    return Daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap











































