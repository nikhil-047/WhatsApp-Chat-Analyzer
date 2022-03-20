# -*- coding: utf-8 -*-
import re
import pandas as pd
    
def preprocess(data):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        pattern2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-zA-Z]{1,2}\s-\s'
    
        #messages = re.split(pattern, data)[1:]
        #dates = re.findall(pattern, data)
        messages=re.split(pattern,data)[1:]
        if len(messages)==0:
            messages=re.split(pattern2,data)[1:]
            dates=re.findall(pattern2,data)
        else:
            dates=re.findall(pattern,data)
            
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        # convert message_date type
        
        try:
            df['message_date'] = pd.to_datetime(dates,format='%m/%d/%y, %H:%M - ')
        except:
            df['message_date'] = pd.to_datetime(dates,format='%d/%m/%y, %I:%M %p - ')
        
        
        #df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    
        df.rename(columns={'message_date': 'date'}, inplace=True)
    
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
                periods.append(str(hour)+"-"+str('0,0'))
            elif hour == 0:
                periods.append(str('00')+"-"+str(hour+1))
            else:
                periods.append(str(hour)+"-"+str(hour+1))
        df['period']=periods        
        
        return df
        
        
        
        