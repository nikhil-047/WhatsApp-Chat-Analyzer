# -*- coding: utf-8 -*-
import streamlit as st
import preprocessor ,helper
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.express as px
import plotly.graph_objects as go

def myFunc(e):
    k=True
    if e[0]=="+" :
   		k=False
    return k


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # convert byte to string
    data = bytes_data.decode("utf-8")
    #st.text(data)
    # Calling the preprocess function 
    df = preprocessor.preprocess(data)
    
    # display dataframe
    #st.dataframe(df)
    
    #Get all the unique users fro dropdown
    user_list = df['user'].unique().tolist()

    #Removing group notifications from the user list
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    # Sort the user list 
    user_list.sort(reverse=True,key=myFunc)
    #sorted(user_list, key=lambda x: (x.isnumeric(),int(x) if x.isnumeric() else x))
     
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    #If button is clicked then..
    if st.sidebar.button("Show Analysis"): 
        if selected_user=="Overall":
            st.write("Analysis on the group chats")
        else:
            st.write("Analysis on ",selected_user,"'s chats") 

        num_messages,words,total_media_msgs,total_links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)  #Creating columns 
        # Stats of users total msgs, words,links shared,media shared
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(total_media_msgs)
        with col4:
            st.header("Total Links Shared")
            st.title(total_links)

        senti = helper.check_sentiment(selected_user,df)
        # st.write(senti)
        st.title("Sentiment of Chat")
        st.select_slider(
        'The Sentiment Anlaysis of this chat seems : ',value=senti,
        options=['Positive', 'Neutral', 'Negative']) 


        # Most active users in group
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df = helper.fetch_most_busy(df)
            fig,ax=plt.subplots()
            col1,col2 = st.columns(2) #Creating columns
            
            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation='vertical',color="green")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                
        st.header("Wordcloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    
        most_common_words = helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()
        ax.barh(most_common_words[0],most_common_words[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        #st.dataframe(most_common_words)
        
        #Analysis of Emoji
        emoji_df = helper.get_emoji(selected_user, df)
        st.title("Emoji Analysis")
        if len(emoji_df)==0:
            st.info("No Emojis used")
        else:
            col1,col2 = st.columns([1,5]) #st.columns(2) 
            
            with col1:
                st.dataframe(emoji_df.set_index("Emoji"))
            with col2:
                fig = go.Figure(
                go.Pie(
                labels = emoji_df["Emoji"].head(),
                values = emoji_df["Count"].head(),
                hoverinfo = "label",
                textinfo = "value+percent"
                ))
                st.plotly_chart(fig)
                
                #fig,ax=plt.subplots()
                #ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                #ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                #st.pyplot(fig)
                
                #fig = px.treemap(emoji_df, path= [0],
                 #   values = emoji_df[1].tolist(),
                #)
                
                
                #st.pyplot(fig)
                
                
    
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
            
        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df) 
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
           
        st.title("Weekly Activity Map")    
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)