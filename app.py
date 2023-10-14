import streamlit as st
import preprocessing, show
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    #st.text(data)
    df = preprocessing.preprocess(data)

    user_lst = df['user'].unique().tolist()
    user_lst.remove('notification')
    user_lst.sort()
    user_lst.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis', user_lst)

    if st.sidebar.button('WhatsApp Analysis'):
        
        messages_num, words, media_messages, links = show.fetch_stats(selected_user, df) 
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(messages_num)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(media_messages)
        with col4:
            st.header('Links Shared')
            st.title(links)

        # monthly timeline
        st.title('Monthly Timeline')
        timeline = show.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'orange')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = show.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most active day')
            busy_day = show.activity_map_week(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'brown')
            plt.xticks(rotation = 45)
            st.pyplot(fig)

        with col2:
            st.header('Most active Month')
            busy_month = show.activity_map_month(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'yellow')
            plt.xticks(rotation = 45)
            st.pyplot(fig)

        # weekly activity map
        st.title('Weekly Activity Map')
        user_heatmap = show.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # the active user
        if selected_user == 'Overall':
            st.title('Most Active User')
            x, new_df = show.most_active_user(df)
            fig, ax  = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color = 'green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("wordcloud")
        df_wc = show.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = show.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color = 'red')
        plt.xticks(rotation = 'vertical')
        st.title('Most common words')
        st.pyplot(fig)
        
        # emoji analysis
        emoji_df = show.emoji_show(selected_user, df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct="%0.2f", shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=90)
            st.pyplot(fig)

