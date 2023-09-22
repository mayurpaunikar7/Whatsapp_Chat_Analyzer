import pandas as pd
import re


def preprocess(data):
    pattern = '\d{1,2}\D\d{1,2}\D\d{2},\s+\d{1,2}:\d{2}\s+[APap][Mm]\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'Date': dates})

    # convert message_date to date time format
    df['Date'] = pd.to_datetime(df['Date'].str.replace('\u202F', ' '), format='%m/%d/%y, %I:%M %p - ')

    # seperate users and messages
    users = []
    messages = []

    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    # Extract year from Date column
    df['Year'] = df['Date'].dt.year

    # Extract month number from Date column
    df['Month'] = df['Date'].dt.month

    # Extract month name from Date column
    df['month_name'] = df['Date'].dt.month_name()

    # Extract Day name from Date column
    df['Day'] = df['Date'].dt.day

    # Extract Hour from Date column
    df['Hour'] = df['Date'].dt.hour

    # Extract Minute from Date column
    df['Minute'] = df['Date'].dt.minute

    # Extract only Date from Date column
    df['only_Date'] = df['Date'].dt.date

    # Extract Day Name from Date column
    df['day_name'] = df['Date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df



