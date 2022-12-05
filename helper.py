import pandas as pd
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

def createDictionary(x):
    dict = {'January':0,'February':0,'March':0,'April':0,'May':0,'June':0,'July':0,'August':0,'September':0,'October':0,'November':0,'December':0}
    if 'January' in x.index:
        dict['January'] = x['January']
    if 'February' in x.index:
        dict['February'] = x['February']
    if 'March' in x.index:
        dict['March'] = x['March']
    if 'April' in x.index:
        dict['April'] = x['April']
    if 'May' in x.index:
        dict['May'] = x['May']
    if 'June' in x.index:
        dict['June'] = x['June']
    if 'July' in x.index:
        dict['July'] = x['July']
    if 'August' in x.index:
        dict['August'] = x['August']
    if 'September' in x.index:
        dict['September'] = x['September']
    if 'October' in x.index:
        dict['October'] = x['October']
    if 'November' in x.index:
        dict['November'] = x['November']
    if 'December' in x.index:
        dict['December'] = x['December']
    return dict;

#Getting Monthly Activity
def getMonthlyActivity(selected_user,df,identifier):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    monthlyBundle = df[df['tag'] == sentiment]
    x = monthlyBundle['month'].value_counts()
    dict = createDictionary(x)
    return dict

#Getting Daily Activity
def getDailyActivity(selected_user,df,identifier):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    dailyBundle = df[df['tag'] == sentiment]
    x = dailyBundle['dayName'].value_counts()
    return x

#Getting Weekly Activity
def getWeeklyHeatmap(selected_user,df,identifier):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    df=df[df['tag']==sentiment]
    if df.shape[0]==0: #Handling error if df is empty
        df.loc[len(df.index)] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'',np.nan,'Null',0-0,np.nan,np.nan,np.nan,np.nan,np.nan,]

    df = df.pivot_table(index='dayName', columns='period', values='message', aggfunc='count').fillna(0)
    return df

#Getting Contribution from users
def getContribution(selected_user,df,identifier):
    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    UserMap = df[df['tag'] == sentiment]
    x = UserMap['user'].value_counts()
    users=[]
    percent=[]
    total=UserMap.shape[0]
    for user in x.index:
        users.append(user)

    for cnt in x.values:
        percent.append(round((cnt/total)*100,3))

    UserDf = pd.DataFrame({
        'User': users,
        'Percentage': percent
    })

    if selected_user!='Overall':
        UserDf=UserDf[UserDf['User']==selected_user]

    if UserDf.shape[0]==0:
        UserDf.loc[len(UserDf.index)] = [selected_user,0.00]

    return UserDf;

#Getting WordCloud
def getWordCloud(selected_user,df,identifier):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]

    f=open('stop_hinglish.txt','r',encoding="utf-8")
    stop_words=f.read()
    words = []
    for message in df['message']:
        for word in message.split():
            if word not in stop_words:
                words.append(word)

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    sia = SentimentIntensityAnalyzer()
    tag = []
    for word in words:
        score = sia.polarity_scores(word)['compound']
        if score == 0.0000:
            tag.append('Neutral')
        elif score > 0.0000:
            tag.append('Positive')
        else:
            tag.append('Negative')

    wordDf = pd.DataFrame({
        'word': words,
        'tag': tag
    })

    wordDf = wordDf[wordDf['tag'] == sentiment]
    if wordDf.shape[0]==0:
        wordDf.loc[len(wordDf.index)] = ['NULL', sentiment]
    wc = WordCloud(collocations=False,width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(wordDf['word'].str.cat(sep=" "))
    return df_wc

#Getting frequency of words
def getWordFrequency(selected_user,df,identifier):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    words = []
    for message in df['message']:
        for word in message.lower().split():
            words.append(word)

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    sia = SentimentIntensityAnalyzer()
    tag = []
    for word in words:
        score = sia.polarity_scores(word)['compound']
        if score == 0.0000:
            tag.append('Neutral')
        elif score > 0.0000:
            tag.append('Positive')
        else:
            tag.append('Negative')

    wordDf = pd.DataFrame({
        'word': words,
        'tag': tag
    })

    wordDf = wordDf[wordDf['tag'] == sentiment]
    bundle=wordDf['word'].value_counts()
    bundle=bundle.nlargest(10)
    return bundle

#Getting Monthly Timeline
def monthlyTimeline(selected_user,df,identifier):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    df=df[df['tag']==sentiment]
    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

#Getting Daily Timeline
def dailyTimeline(selected_user,df,identifier):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    sentiment='To be Computed'
    if identifier == 0:
        sentiment='Positive'
    elif identifier == 1:
        sentiment='Neutral'
    else:
        sentiment='Negative'

    df=df[df['tag']==sentiment]
    daily_timeline = df.groupby('dateTime').count()['message'].reset_index()
    return daily_timeline
