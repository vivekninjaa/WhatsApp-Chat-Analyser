import re
import pandas as pd

def preprocess(data):
    # Define the regex pattern for date and time in both 12-hour and 24-hour formats
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*(?:[apAP][mM])?\s*-\s*'

    messages = re.split(pattern, data)[1:]  # Split messages based on the regex pattern
    dates = re.findall(pattern, data)  # Find all matching date and time entries

    # Check if the number of messages and dates match
    if len(messages) != len(dates):
        raise ValueError("Messages and dates lengths do not match. Please check the input data.")

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Function to convert the date using multiple formats
    def convert_date(date_str):
        try:
            # Try 24-hour format first
            return pd.to_datetime(date_str, format='%d/%m/%y, %H:%M - ', dayfirst=True)
        except ValueError:
            try:
                # Then try 12-hour format
                return pd.to_datetime(date_str, format='%d/%m/%Y, %I:%M %p - ', dayfirst=True)
            except ValueError:
                # If both fail, return NaT
                return pd.NaT

    df['message_date'] = df['message_date'].apply(convert_date)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    # Loop through each message in the DataFrame
    for message in df['user_message']:
        # Use a raw string for the regex pattern
        entry = re.split(r'([\w\W]+?):\s', message)

        if entry[1:]:  # Check if there are captured groups (user name)
            users.append(entry[1])  # Append the username
            messages.append(" ".join(entry[2:]))  # Append the message text
        else:
            users.append('group_notification')  # Default for notifications
            messages.append(entry[0])  # Append the message

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional columns for time-based analysis
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year.astype(str).str.zfill(4)  # Ensure the year is 4 digits
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00' + '-' + str(hour + 1)))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period



    return df
