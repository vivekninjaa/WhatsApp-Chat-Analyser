import streamlit as st
import Preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar title
st.sidebar.title("Whatsapp Chat Analyser")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Process uploaded file
if uploaded_file is not None:
    # Read the file as bytes and decode it to string
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the data using the Preprocessor
    df = Preprocessor.preprocess(data)

    # Display the processed DataFrame
    st.dataframe(df)

    # Fetch unique users from the dataframe
    user_list = df['user'].unique().tolist()

    # Check if 'group_notification' is in the list, then remove it
    if "group_notification" in user_list:
        user_list.remove("group_notification")

    # Sort the user list alphabetically and add "Overall" at the top
    user_list.sort()
    user_list.insert(0, "Overall")

    # Sidebar selectbox for user selection
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # When the "Show Analysis" button is clicked
    if st.sidebar.button("Show Analysis"):
        # Fetch statistics (messages, words, media messages, links)
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        # Display stats using columns
        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.subheader("Total Messages")
            st.subheader(num_messages)

        with col2:
            st.subheader("Total Words")
            st.subheader(words)

        with col3:
            st.subheader("Total Media Messages")
            st.subheader(num_media_messages)

        with col4:
            st.subheader("Total Links")
            st.subheader(num_links)
        st.title("Timeline")

        col1,col2 = st.columns(2)

        with col1:

        # monthly timeline
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color = 'pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:

            #daily timeline
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'],color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Heat map
        st.title("Weekly activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots(figsize = (20,6))
        ax = sns.heatmap(user_heatmap)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)






        # Analysis for overall chat: busiest users
        if selected_user == "Overall":
            st.title("Most Active Users")
            x, new_df = helper.most_busy_users(df)

            # Plot the busiest users using bar chart
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='brown')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Word cloud generation and display
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)  # Fixed typo 'crete_wordcloud' to 'create_wordcloud'
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Display most common words using a bar chart
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.title("Emoji Analysis")
            st.dataframe(emoji_df)

        with col2:
            # Display emoji distribution using a pie chart
            st.title("Pie Chart")
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Description'].head(), autopct="%0.2f%%")
            st.pyplot(fig)
