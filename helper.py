# -*- coding: utf-8 -*-

from urlextract import URLExtract  # To extract the url . retuens a list consisting the urls from string
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract() #Object of urlextract
sentiments = SentimentIntensityAnalyzer()

# Get info about the user
def fetch_stats(selected_user,df):
    #No. of messages
    if selected_user != "Overall":
        df = df[df['user']==selected_user] #Dataframe containing data only about the particular user
    num_messages = df.shape[0]
    
    words=[]
    # No. of words 
    for message in df['message']:
        words.extend(message.split())

    total_media_msgs=df[df['message']=='<Media omitted>\n'].shape[0] #Get the MEdia shared
    
    links=[]
    # No. of links shared
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return num_messages,len(words),total_media_msgs,len(links)
    
# Most active users in group
def fetch_most_busy(df):
    x = df['user'].value_counts().head()
    # New dataframe consisting of percentage of their contribution in group
    df = round((df['user'].value_counts()/df['user'].shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    f = open('stop_hinglish.txt','r')
    hinglish_stop_words = f.read()
    
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    temp = df[df['user']!="group_notification"]
    temp=temp[temp['message']!='<Media omitted>\n']
    temp=temp[temp['message']!="This message was deleted\n"]
    
    def remove_stop_words(message):
        new_sent=[]
        for word in message.lower().split():
            if word not in hinglish_stop_words:
                new_sent.append(word)
        return " ".join(new_sent)
    
    temp['message']=temp['message'].apply(remove_stop_words)
                
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].astype(str).str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    hinglish_stop_words = f.read()
    
    #Removing group notifications , media and msgs deleted msgs 
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    temp = df[df['user']!="group_notification"]
    temp=temp[temp['message']!='<Media omitted>\n']
    temp=temp[temp['message']!="This message was deleted\n"]
    
    words = []
 
    #Remove hinglish stop words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in hinglish_stop_words:
                words.append(word)
    # Counter is used to get the no. of occurance 
    most_common_words = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words

def get_emoji(selected_user,df):
    emojis=[] 
    #emojis_info=[]
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
        
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        #emojis_info.extend([emoji.UNICODE_EMOJI['en'][c] for c in message if c in emoji.UNICODE_EMOJI['en']])
    #(c,emoji.UNICODE_EMOJI['en'][c])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.rename(columns={0:'Emoji',1:'Count'},inplace=True)
    # emoji_df.set_index("Emoji")
    return emoji_df

#Get the Monthly activity graph
def monthly_timeline(selected_user,df):
    time =[]
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" +str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

#Get the daily activity graph
def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

#Get busiest days  detail
def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()

#Get busisest monthly detail
def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    return df['month'].value_counts()

#Weekly activity map
def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    activity_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_heatmap

#Sentiment of chat
def check_sentiment(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    temp = df[df['user']!="group_notification"]
    temp=temp[temp['message']!='<Media omitted>\n']
    temp=temp[temp['message']!="This message was deleted\n"]

    temp["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in temp["message"]]
    temp["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in temp["message"]]
    temp["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in temp["message"]]

    Pos = sum(temp['Positive'])
    Neg = sum(temp['Negative'])
    Neu = sum(temp['Neutral'])

    if Pos >= Neg and Pos >= Neu:
        result = "Positive"
    elif Neg > Pos and Neg > Neu:
        result = "Negative"
    else:
        result = "Neutral"
    
    return result


        
    
    
    