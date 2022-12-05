import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import wordcloud
import seaborn as sns

st.sidebar.title('WhatsApp Chat Sentimental Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a File")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #Fetching unique users
    userList=df['user'].unique().tolist()
    userList.sort()
    userList.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt. ",userList)

    if st.sidebar.button('Show Analysis'):
        st.markdown("<h1 style='text-align: center; color: black;'>Showing Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'></h1>", unsafe_allow_html=True)


        #Monthly Activity
        posBundle=helper.getMonthlyActivity(selected_user,df,0)
        neuBundle=helper.getMonthlyActivity(selected_user,df,1)
        negBundle=helper.getMonthlyActivity(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>Monthly Activity</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.bar(posBundle.keys(),posBundle.values(),color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.bar(neuBundle.keys(),neuBundle.values(),color='gray')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.bar(negBundle.keys(),negBundle.values(),color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)


        #Daily Activity
        posBundle=helper.getDailyActivity(selected_user,df,0)
        neuBundle=helper.getDailyActivity(selected_user,df,1)
        negBundle=helper.getDailyActivity(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>Daily Activity</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.pie(posBundle.values, labels=posBundle.index, autopct='%1.1f',radius=0.8)
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.pie(neuBundle.values, labels=neuBundle.index, autopct='%1.1f',radius=0.8)
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.pie(negBundle.values, labels=negBundle.index, autopct='%1.1f',radius=0.8)
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)


        #Weekly Heatmap
        posHeatmap=helper.getWeeklyHeatmap(selected_user,df,0)
        neuHeatmap=helper.getWeeklyHeatmap(selected_user,df,1)
        negHeatmap=helper.getWeeklyHeatmap(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>Weekly Heatmap</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax=sns.heatmap(posHeatmap)
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax=sns.heatmap(neuHeatmap)
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax=sns.heatmap(negHeatmap)
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)


        # Monthly Timeline
        posTimeline = helper.monthlyTimeline(selected_user, df, 0)
        neuTimeline = helper.monthlyTimeline(selected_user, df, 1)
        negTimeline = helper.monthlyTimeline(selected_user, df, 2)
        st.markdown("<h3 style='text-align: left; color: black;'>Monthly Timeline</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(posTimeline['time'], posTimeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(neuTimeline['time'], neuTimeline['message'], color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(negTimeline['time'], negTimeline['message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)

        # Daily Timeline
        posTimeline = helper.dailyTimeline(selected_user, df, 0)
        neuTimeline = helper.dailyTimeline(selected_user, df, 1)
        negTimeline = helper.dailyTimeline(selected_user, df, 2)
        st.markdown("<h3 style='text-align: left; color: black;'>Daily Timeline</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(posTimeline['dateTime'], posTimeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(neuTimeline['dateTime'], neuTimeline['message'], color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.plot(negTimeline['dateTime'], negTimeline['message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)


        #Contribution
        posUserDf=helper.getContribution(selected_user,df,0)
        neuUserDf=helper.getContribution(selected_user,df,1)
        negUserDf=helper.getContribution(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>User Contribution</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: left; color: green;'>Positive</h5>", unsafe_allow_html=True)
            st.dataframe(posUserDf)

        with col2:
            st.markdown("<h5 style='text-align: left; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            st.dataframe(neuUserDf)


        with col3:
            st.markdown("<h5 style='text-align: left; color: red;'>Negative</h5>", unsafe_allow_html=True)
            st.dataframe(negUserDf)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)

        #Word Frequency
        posBundle=helper.getWordFrequency(selected_user,df,0)
        neuBundle=helper.getWordFrequency(selected_user,df,1)
        negBundle=helper.getWordFrequency(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>Word Frequency</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.barh(posBundle.index,posBundle.values,color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.barh(neuBundle.index,neuBundle.values,color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig,ax=plt.subplots()
            ax.barh(negBundle.index,negBundle.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("<h1 style='text-align: left; color: grey;'></h1>", unsafe_allow_html=True)


        #WordCloud
        posWc=helper.getWordCloud(selected_user,df,0)
        neuWc=helper.getWordCloud(selected_user,df,1)
        negWc=helper.getWordCloud(selected_user,df,2)
        st.markdown("<h3 style='text-align: left; color: black;'>WordCloud</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: grey;'></h3>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown("<h5 style='text-align: center; color: green;'>Positive</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.imshow(posWc)
            st.pyplot(fig)

        with col2:
            st.markdown("<h5 style='text-align: center; color: grey;'>Neutral</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.imshow(neuWc)
            st.pyplot(fig)

        with col3:
            st.markdown("<h5 style='text-align: center; color: red;'>Negative</h5>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.imshow(negWc)
            st.pyplot(fig)

