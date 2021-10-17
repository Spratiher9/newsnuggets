# import asyncio
import streamlit as st
from constants import *
from utils import get_client

st.title('News Nuggets 📰')
st.sidebar.title("News App preferences! 📝")

country_choice = st.sidebar.selectbox("Country 🎌:", options=countries,
                                      index=5,
                                      help='Choose the country whose news you want to see👇')
search_choice = st.sidebar.radio('Search News by : ', options=['Top Headlines', 'Search Term'])

if search_choice == 'Top Headlines':
    Client = get_client()

    category = st.sidebar.selectbox('Topics:',
                                    options=topics, index=0)

    st.sidebar.write("## Enter search specs 🔎")
    time_span = st.sidebar.text_input("Time Span: ⏲ ", '7d',
                                      help="""
        - h = hours (eg: 12h)
        - d = days (eg: 7d)
        - m = months (eg: 6m)
        - y = years (eg: 1y)
    """)
    article_num = st.sidebar.number_input("Number of Articles 🔢 ", 1, 100, 10)
    lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                index=0,
                                help='Language of news to be fetched')

    Client.period = time_span
    Client.country = country_choice
    Client.max_results = article_num
    Client.language = lang

    if category == "GENERAL":
        st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
        # General call of gnews client
        news_ls = Client.get_top_news()

    else:
        st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
        # Topic call of gnews client
        news_ls = Client.get_news_by_topic(category.upper())

elif search_choice == 'Search Term':
    Client = get_client()

    search_term = st.sidebar.text_input('Enter Search Term:', value= 'Interesting Search term here')

    st.sidebar.write("## Enter search specs 🔎")
    time_span = st.sidebar.text_input("Time Span: ⏲ ", '7d',
                                      help="""
        - h = hours (eg: 12h)
        - d = days (eg: 7d)
        - m = months (eg: 6m)
        - y = years (eg: 1y)
    """)
    article_num = st.sidebar.number_input("Number of Articles 🔢 ", 5, 100, 10)
    lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                index=0,
                                help='Language of news to be fetched')

    Client.period = time_span
    Client.country = country_choice
    Client.max_results = article_num
    Client.language = lang

    st.write(f'**You are seeing articles about** _{search_term.upper()}_ **!!**')
    news_ls = Client.get_news(search_term)


# def get_tasks():
#     tasks = []
#     for i in range(len(news_ls)):
#         tasks.append(asyncio.create_task(Client.get_full_article(news_ls[i]['url'])))
#     # print("Tasks:")
#     # print(tasks)
#     return tasks
#
#
# articles = list()
#
#
# async def get_article_conc():
#     tasks = get_tasks()
#     responses = await asyncio.gather(*tasks)
#     for response in responses:
#         articles.append(await response)
#
#
# asyncio.run(get_article_conc())
#
# for i in range(len(articles)):
#     st.title(i.title)
#     st.image(i.top_image)
#     st.write(f"###### Published at: {news_ls[i]['published date']}")
#     st.write(f"###### Source: {news_ls[i]['publisher']['title']}")
#     st.write(i.text)
#     st.write(f"Read more [here]({news_ls[i]['url']})")


for i in range(len(news_ls)):
    try:
        article = Client.get_full_article(news_ls[i]['url'])
        st.title(article.title)
        st.image(article.top_image)
        st.write(f"###### Published at: {news_ls[i]['published date']}")
        st.write(f"###### Source: {news_ls[i]['publisher']['title']}")
        with st.expander("Read Full News 📖 "):
            st.write(article.text)
        st.write(f"[Original article here]({news_ls[i]['url']})")
    except Exception as err:
        print(err)
