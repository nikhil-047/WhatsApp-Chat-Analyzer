# -*- coding: utf-8 -*-
import re
import pandas as pd

#This function will take the data and convert to dataframe    
def preprocess(data):
        # We need to seprate the above content into three parts
        # 1 -> Date and time
        # 2 -> Sender NAme
        # 3 -> the message
        # For doing this we use regular expression

        # pattern for 24 hrs format "1/31/21, 18:54 - " 
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        # pattern for 12 hrs format "18/07/19, 8:13 pm - " 
        pattern2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-zA-Z]{1,2}\s-\s'
    
        #messages = re.split(pattern, data)[1:]
        #dates = re.findall(pattern, data)

        # Separate the date and message from string data
        messages=re.split(pattern,data)[1:]
        if len(messages)==0:
            messages=re.split(pattern2,data)[1:]
            dates=re.findall(pattern2,data)
        else:
            dates=re.findall(pattern,data)
            
        #  Create a dataframe and store messages and dates in columns   
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # Convert string date to datetime.datetime convert will come handy further
        try:
            df['message_date'] = pd.to_datetime(dates,format='%m/%d/%y, %H:%M - ')
        except:
            df['message_date'] = pd.to_datetime(dates,format='%d/%m/%y, %I:%M %p - ')
        
        
        #df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    
        df.rename(columns={'message_date': 'date'}, inplace=True)

        # Will separte the messages and users from string and will create a new column called group notification to store notifications

        users = []
        messages = []
        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:  # user name
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                users.append('group_notification')
                messages.append(entry[0])
    
        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)
        
        # Since we have converted the data column to datetime we can use the following functions
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        
        periods=[]
        for hour in df['hour']:
            if hour== 23:
                periods.append(str(hour)+"-"+str('00'))
            elif hour == 0:
                periods.append(str('00')+"-"+str(hour+1))
            else:
                periods.append(str(hour)+"-"+str(hour+1))
        df['period']=periods        
        
        return df
        
        
        
        