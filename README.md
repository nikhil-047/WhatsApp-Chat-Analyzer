# WhatsApp-Chat-Analyzer

The project is aimed to analyze the WhatsApp chats, extract insights and create different charts.I have used Streamlit to create a UI dashboard where the user can upload the WhatsApp chats file and a detailed analysis of the chats will be displayed to the user. Most common words, emojis used, most active users, activity map of users for month and week, sentiment analysis of the chats, and more analysis.This website is deployed in Heroku.

# Extracting the WhatsApp chats

You can use the export chat feature to export a copy of the chat history from an individual or group chat.
1. Open the individual or group chat.
2. Tap More options > More > Export chat.
3. Choose to export without media.

The chat will be exported as a .txt document.

# Data Cleaning 

- To extract the meaningful info from the chatsa we need to clean and transform the data.
- Will use Regular expression to extract all the features from the chat.Will extract useful features such as time, date, message content, message sender, etc.
- Will then create a datafranme from the result.
- And perform various actions on the data.
- Will use Streamlit to create an interactive web app which will help us to display all our findings in form of charts and graphs.

# How to run the app
1. Download the folder
3. Run the python file "app.py" in cmd by using the following commapnd "streamlit run app.py"

# Dependencies
- Python
- Jupyter notebook
- Numpy and Pandas
- Matplotlib
- Sklearn
- Streamlit
- Emoji
- Plotly
- WordCloud

The project is deployed on Heroku : https://wca-np.herokuapp.com
