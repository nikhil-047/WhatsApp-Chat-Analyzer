# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 01:16:44 2022

@author: pooja
"""
import streamlit as st
import preprocessor ,helper
import matplotlib.pyplot as plt
import seaborn as sns

def myFunc(e):
  k=True
  if e[0]=="+" :
   		k=False
  	#return k
  return k


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)
    
    st.dataframe(df)
    
    #Get all the unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort(reverse=True,key=myFunc)
    #sorted(user_list, key=lambda x: (x.isnumeric(),int(x) if x.isnumeric() else x))
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,total_media_msgs,total_links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        
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
        
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df = helper.fetch_most_busy(df)
            fig,ax=plt.subplots()
            col1,col2 = st.columns(2)
            
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
        
        emoji_df = helper.get_emoji(selected_user, df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2) 
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
    
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
        
        st.title("Activity MAp")
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