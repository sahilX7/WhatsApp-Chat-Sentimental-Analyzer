import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def preprocess(data):
    pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{2}:\d{2}\s-\s")
    dates = pattern.findall(data)
    userMessage = pattern.split(data)
    userMessage=userMessage[1:]
    df=pd.DataFrame({
        'dateTime':dates,
        'userMessage':userMessage
    })
    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%m/%d/%y, %H:%M - ')
    df['day']=df['dateTime'].dt.day
    df['month']=df['dateTime'].dt.month_name()
    df['year']=df['dateTime'].dt.year
    df['hour']=df['dateTime'].dt.hour
    df['minute']=df['dateTime'].dt.minute
    df['monthNum']=df['dateTime'].dt.month
    df['dayName']=df['dateTime'].dt.strftime('%A')

    users = []
    messages = []
    for message in df['userMessage']:
        pattern = re.compile(r'([\w\W]+?):\s')
        entry = pattern.split(message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['userMessage'], inplace=True)
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'You deleted this message\n']
    df = df[df['user'] != 'group_notification']

    period = []
    for hour in df[['dayName', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period']=period

    #Sentimental Analysis
    sia = SentimentIntensityAnalyzer()
    pos = []
    neu = []
    neg = []
    compound = []
    for message in df['message']:
        score = sia.polarity_scores(message)
        pos.append(score['pos'])
        neu.append(score['neu'])
        neg.append(score['neg'])
        compound.append(score['compound'])

    df['pos'] = pos
    df['neu'] = neu
    df['neg'] = neg
    df['compound'] = compound

    tag = []
    for score in df['compound']:
        if score == 0.0000:
            tag.append('Neutral')
        elif score > 0.0000:
            tag.append('Positive')
        else:
            tag.append('Negative')

    df['tag'] = tag
    return df