# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# import requests
# import json
# import time
#
# from paramiko import file
#
# # to expand the content in the web page
# st.set_page_config(layout='wide')
#
# # inserting logo
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
#
# st.title('Crypto Price App')
# st.markdown(""" This Page is under construction. We are working smart and hard, so will show you soon.
# """)
#
# expander_bar = st.expander("About")
# expander_bar.markdown("""
# * **Python Libraries: **base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, time
# """)
#
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
#
# col1.header('User Input Options')
# cur_price_unit = col1._selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
#
# @st.cache_data
# def load_data():
#     cmc = requests.get("https://coinmarketcap.com/")
#     soup = BeautifulSoup(cmc.content, 'html.parser')
#
#     data = soup.find('script', id='__NEXT_DATA__', type='application/json')
#     coins = {}
#     coin_data = json.loads(data.contents[0])
#     props = coin_data.get('props', {})
#     initialI18nStore = props.get('initialI18nStore', {})
#     sheet_Cryptocurrencies = initialI18nStore.get('sheet_Cryptocurrencies', {})
#     listingParams = sheet_Cryptocurrencies.get('listingParams', {})
#     data = listingParams.get('data', [])
#
#     coin_name = []
#     coin_symbol = []
#     market_cap = []
#     per_chg_1h = []
#     per_chg_24h = []
#     per_chg_7d = []
#     price = []
#     volume_24hr = []
#
#     for i in data:
#         coin_name.append(i['slug'])
#         coin_symbol.append(i['symbol'])
#         price.append(i['quote'][cur_price_unit]['price'])
#         per_chg_1h.append(i['quote'][cur_price_unit]['percentChange1h'])
#         per_chg_24h.append(i['quote'][cur_price_unit]['percentChange24h'])
#         per_chg_7d.append(i['quote'][cur_price_unit]['percentChange7d'])
#         market_cap.append(i['quote'][cur_price_unit]['marketCap'])
#         volume_24hr.append(i['quote'][cur_price_unit]['volume24h'])
#
#     df = pd.DataFrame(
#         columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d',
#                  'price', 'volume24h'])
#     df['coin_name'] = coin_name
#     df['coin_symbol'] = coin_symbol
#     df['marketCap'] = market_cap
#     df['percentChange1h'] = per_chg_1h
#     df['percentChange24h'] = per_chg_24h
#     df['percentChange7d'] = per_chg_7d
#     df['price'] = price
#     df['volume24h'] = volume_24hr
#     return df
#
#
# df = load_data()
#
# sorted_coin = sorted(df['coin_symbol'])
# selected_coin = col1.multiselect('Crytocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]
#
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
#
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "percentChange7d", "24h": "percentChange24h", "1h": "percentChange1h"}
# selected_percent_tf = percent_dict[per_timeframe]
#
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
#
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write('Date Dimension: ' + str(df_selected_coin.shape[0]) + 'rows and' + str(df_selected_coin.shape[1])
#            + 'columns.')
#
# col2.dataframe(df_coins)
#
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
#
# col2.header("Total of % Price change ")
# df_change = pd.concat([df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h,
#                        df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_per_chg_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_per_chg_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_per_chg_7d'] = df_change['percentChange7d'] > 0
#
# col2.dataframe(df_change)
# col2.header('Table of % Price Change')
# df_change = pd.concat(
#     [df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# #
# # # Conditional creation of Bar plot (time frame)
# # col3.header('Bar plot of % Price Change')
# #
# # if per_timeframe == '7d':
# #     if sort_values == 'Yes':
# #         df_change = df_change.sort_values(by=['percentChange7d'])
# #     col3.write('*7 days period*')
# #     plt.figure(figsize=(5, 25))
# #     plt.subplots_adjust(top=1, bottom=0)
# #     df_change['percentChange7d'].plot(kind='barh',
# #                                       color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
# #     col3.pyplot(plt)
# # elif per_timeframe == '24h':
# #     if sort_values == 'Yes':
# #         df_change = df_change.sort_values(by=['percentChange24h'])
# #     col3.write('*24 hour period*')
# #     plt.figure(figsize=(5, 25))
# #     plt.subplots_adjust(top=1, bottom=0)
# #     df_change['percentChange24h'].plot(kind='barh',
# #                                        color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
# #     col3.pyplot(plt)
# # else:
# #     if sort_values == 'Yes':
# #         df_change = df_change.sort_values(by=['percentChange1h'])
# #     col3.write('*1 hour period*')
# #     plt.figure(figsize=(5, 25))
# #     plt.subplots_adjust(top=1, bottom=0)
# #     df_change['percentChange1h'].plot(kind='barh',
# #                                       color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
# #     col3.pyplot(plt)
#
#
#
#
#
#
#
#
#
#
#
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange7d'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange7d'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange24h'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange24h'].plot(kind='barh',
#                                            color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange1h'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange1h'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#
#
#
#
#
# Final as on 051024
#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# import requests
# import json
# st.set_page_config(layout='wide')
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
# st.title('Crypto Price App')
# st.markdown(""" This Page is under construction. We are working smart and hard, so will show you soon.""")
# expander_bar = st.expander("About")
# expander_bar.markdown("""
# * **Python Libraries: **base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, time""")
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
# col1.header('User Input Options')
# cur_price_unit = col1._selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
# @st.cache_data
# def load_data():
#     cmc = requests.get("https://coinmarketcap.com/")
#     soup = BeautifulSoup(cmc.content, 'html.parser')
#     data = soup.find('script', id='__NEXT_DATA__', type='application/json')
#     coins = {}
#     coin_data = json.loads(data.contents[0])
#     props = coin_data.get('props', {})
#     initialI18nStore = props.get('initialI18nStore', {})
#     sheet_Cryptocurrencies = initialI18nStore.get('sheet_Cryptocurrencies', {})
#     listingParams = sheet_Cryptocurrencies.get('listingParams', {})
#     data = listingParams.get('data', [])
#     coin_name = []
#     coin_symbol = []
#     market_cap = []
#     per_chg_1h = []
#     per_chg_24h = []
#     per_chg_7d = []
#     price = []
#     volume_24hr = []
#     for i in data:
#         coin_name.append(i['slug'])
#         coin_symbol.append(i['symbol'])
#         price.append(i['quote'][cur_price_unit]['price'])
#         per_chg_1h.append(i['quote'][cur_price_unit]['percentChange1h'])
#         per_chg_24h.append(i['quote'][cur_price_unit]['percentChange24h'])
#         per_chg_7d.append(i['quote'][cur_price_unit]['percentChange7d'])
#         market_cap.append(i['quote'][cur_price_unit]['marketCap'])
#         volume_24hr.append(i['quote'][cur_price_unit]['volume24h'])
#     df = pd.DataFrame(
#         columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d',
#                  'price', 'volume24h'])
#     df['coin_name'] = coin_name
#     df['coin_symbol'] = coin_symbol
#     df['marketCap'] = market_cap
#     df['percentChange1h'] = per_chg_1h
#     df['percentChange24h'] = per_chg_24h
#     df['percentChange7d'] = per_chg_7d
#     df['price'] = price
#     df['volume24h'] = volume_24hr
#     return df
# df = load_data()
# sorted_coin = sorted(df['coin_symbol'])
# selected_coin = col1.multiselect('Crytocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "percentChange7d", "24h": "percentChange24h", "1h": "percentChange1h"}
# selected_percent_tf = percent_dict[per_timeframe]
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write('Date Dimension: ' + str(df_selected_coin.shape[0]) + 'rows and' + str(df_selected_coin.shape[1])+ 'columns.')
# col2.dataframe(df_coins)
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
# col2.header("Total of % Price change ")
# df_change = pd.concat([df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h,
#                        df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_per_chg_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_per_chg_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_per_chg_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# col2.header('Table of % Price Change')
# df_change = pd.concat(
#     [df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# col3.header('Bar plot of % Price Change')
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange7d'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange7d'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange24h'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange24h'].plot(kind='barh',
#                                            color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange1h'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange1h'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#
#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# import requests
# import json
#
# st.set_page_config(layout='wide')
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
# st.title('Crypto Price App')
# st.markdown(""" This Page is under construction. We are working smart and hard, so will show you soon.""")
# expander_bar = st.expander("About")
# expander_bar.markdown("""
# * **Python Libraries: **base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, time""")
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
# col1.header('User Input Options')
# cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
#
# @st.cache_data
# def load_data():
#     cmc = requests.get("https://coinmarketcap.com/")
#     soup = BeautifulSoup(cmc.content, 'html.parser')
#     data = soup.find('script', id='__NEXT_DATA__', type='application/json')
#     coins = {}
#     coin_data = json.loads(data.contents[0])
#
#     # Debug: Print the structure of coin_data
#     print(json.dumps(coin_data, indent=2))
#
#     quotes_latest_data = coin_data.get('quotesLatestData', [])
#
#     # Debug: Print the structure of quotes_latest_data
#     print(json.dumps(quotes_latest_data, indent=2))
#
#     coin_name = []
#     coin_symbol = []
#     market_cap = []
#     per_chg_1h = []
#     per_chg_24h = []
#     per_chg_7d = []
#     price = []
#     volume_24hr = []
#
#     for coin in quotes_latest_data:
#         if 'id' in coin and 'symbol' in coin and 'p' in coin:
#             coin_name.append(coin['id'])
#             coin_symbol.append(coin['symbol'])
#             price.append(coin['p'])
#             per_chg_1h.append(coin.get('p1h', 0))
#             per_chg_24h.append(coin.get('p24h', 0))
#             per_chg_7d.append(coin.get('p7d', 0))
#             market_cap.append(coin.get('marketCap', 0))
#             volume_24hr.append(coin.get('volume24h', 0))
#
#     df = pd.DataFrame(
#         columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d',
#                  'price', 'volume24h'])
#     df['coin_name'] = coin_name
#     df['coin_symbol'] = coin_symbol
#     df['marketCap'] = market_cap
#     df['percentChange1h'] = per_chg_1h
#     df['percentChange24h'] = per_chg_24h
#     df['percentChange7d'] = per_chg_7d
#     df['price'] = price
#     df['volume24h'] = volume_24hr
#
#     # Debug: Print the DataFrame
#     print(df.head())
#
#     return df
#
#
# df = load_data()
# sorted_coin = sorted(df['coin_symbol'])
# selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "percentChange7d", "24h": "percentChange24h", "1h": "percentChange1h"}
# selected_percent_tf = percent_dict[per_timeframe]
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write(
#     'Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
# col2.dataframe(df_coins)
#
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
# col2.header("Total of % Price change ")
# df_change = pd.concat(
#     [df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange7d'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange7d'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange24h'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange24h'].plot(kind='barh',
#                                            color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange1h'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 0.5))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange1h'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#
#
#
#
#
#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# import requests
# import json
#
# st.set_page_config(layout='wide')
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
# st.title('Crypto Price App')
# st.markdown(""" This Page is under construction. We are working smart and hard, so will show you soon.""")
# expander_bar = st.expander("About")
# expander_bar.markdown("""
# * **Python Libraries: **base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, time""")
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
# col1.header('User Input Options')
# cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
#
# @st.cache_data
# def load_data():
#     cmc = requests.get("https://coinmarketcap.com/")
#     soup = BeautifulSoup(cmc.content, 'html.parser')
#     data = soup.find('script', id='__NEXT_DATA__', type='application/json')
#     coins = {}
#     coin_data = json.loads(data.contents[0])
#
#     # Debug: Print the structure of coin_data
#     print(json.dumps(coin_data, indent=2))
#
#     # Access the correct part of the JSON structure
#     quotes_latest_data = coin_data.get('props', {}).get('quotesLatestData', [])
#
#     # Debug: Print the structure of quotes_latest_data
#     print(json.dumps(quotes_latest_data, indent=2))
#
#     coin_name = []
#     coin_symbol = []
#     market_cap = []
#     per_chg_1h = []
#     per_chg_24h = []
#     per_chg_7d = []
#     price = []
#     volume_24hr = []
#
#     for coin in quotes_latest_data:
#         if 'id' in coin and 'symbol' in coin and 'p' in coin:
#             coin_name.append(coin['id'])
#             coin_symbol.append(coin['symbol'])
#             price.append(coin['p'])
#             per_chg_1h.append(coin.get('p1h', 0))
#             per_chg_24h.append(coin.get('p24h', 0))
#             per_chg_7d.append(coin.get('p7d', 0))
#             market_cap.append(coin.get('marketCap', 0))
#             volume_24hr.append(coin.get('volume24h', 0))
#
#     df = pd.DataFrame(
#         columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d',
#                  'price', 'volume24h'])
#     df['coin_name'] = coin_name
#     df['coin_symbol'] = coin_symbol
#     df['marketCap'] = market_cap
#     df['percentChange1h'] = per_chg_1h
#     df['percentChange24h'] = per_chg_24h
#     df['percentChange7d'] = per_chg_7d
#     df['price'] = price
#     df['volume24h'] = volume_24hr
#
#     # Debug: Print the DataFrame
#     print(df.head())
#
#     return df
#
#
# df = load_data()
# sorted_coin = sorted(df['coin_symbol'])
# selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "percentChange7d", "24h": "percentChange24h", "1h": "percentChange1h"}
# selected_percent_tf = percent_dict[per_timeframe]
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write(
#     'Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
# col2.dataframe(df_coins)
#
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
# col2.header("Total of % Price change ")
# df_change = pd.concat(
#     [df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange7d'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange7d'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange24h'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange24h'].plot(kind='barh',
#                                            color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange1h'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange1h'].plot(kind='barh',
#                                           color=(df_change.positive_percent_change_1h.map({True: 'g', False: 'r'})))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#


#
#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# import requests
# import json
#
# st.set_page_config(layout='wide')
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
# st.title('Crypto Price App')
# st.markdown(""" This Page is under construction. We are working smart and hard, so will show you soon.""")
# expander_bar = st.expander("About")
# expander_bar.markdown("""
# * **Python Libraries: **base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, time""")
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
# col1.header('User Input Options')
# cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
#
# @st.cache_data
# def load_data():
#     cmc = requests.get("https://coinmarketcap.com/")
#     soup = BeautifulSoup(cmc.content, 'html.parser')
#     data = soup.find('script', id='__NEXT_DATA__', type='application/json')
#     coins = {}
#     coin_data = json.loads(data.contents[0])
#
#     # Debug: Print the structure of coin_data
#     print(json.dumps(coin_data, indent=2))
#
#     # Access the correct part of the JSON structure
#     quotes_latest_data = coin_data.get('props', {}).get('quotesLatestData', [])
#
#     # Debug: Print the structure of quotes_latest_data
#     print(json.dumps(quotes_latest_data, indent=2))
#
#     coin_name = []
#     coin_symbol = []
#     market_cap = []
#     per_chg_1h = []
#     per_chg_24h = []
#     per_chg_7d = []
#     price = []
#     volume_24hr = []
#
#     for coin in quotes_latest_data:
#         if 'id' in coin and 'symbol' in coin and 'p' in coin:
#             coin_name.append(coin['id'])
#             coin_symbol.append(coin['symbol'])
#             price.append(coin['p'])
#             per_chg_1h.append(coin.get('p1h', 0))
#             per_chg_24h.append(coin.get('p24h', 0))
#             per_chg_7d.append(coin.get('p7d', 0))
#             market_cap.append(coin.get('marketCap', 0))
#             volume_24hr.append(coin.get('volume24h', 0))
#
#     df = pd.DataFrame(
#         columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d',
#                  'price', 'volume24h'])
#     df['coin_name'] = coin_name
#     df['coin_symbol'] = coin_symbol
#     df['marketCap'] = market_cap
#     df['percentChange1h'] = per_chg_1h
#     df['percentChange24h'] = per_chg_24h
#     df['percentChange7d'] = per_chg_7d
#     df['price'] = price
#     df['volume24h'] = volume_24hr
#
#     # Debug: Print the DataFrame
#     print(df.head())
#
#     return df
#
#
# df = load_data()
# sorted_coin = sorted(df['coin_symbol'])
# selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "percentChange7d", "24h": "percentChange24h", "1h": "percentChange1h"}
# selected_percent_tf = percent_dict[per_timeframe]
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write(
#     'Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
# col2.dataframe(df_coins)
#
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
# col2.header("Total of % Price change ")
# df_change = pd.concat(
#     [df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
# df_change = df_change.set_index('coin_symbol')
# df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
# df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
# df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
# col2.dataframe(df_change)
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange7d'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange7d'].plot(kind='barh',
#                                           color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange24h'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange24h'].plot(kind='barh',
#                                            color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['percentChange1h'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['percentChange1h'].plot(kind='barh',
#                                           color=(df_change.positive_percent_change_1h.map({True: 'g', False: 'r'})))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#


# project progress as on 131024
#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
#
# st.set_page_config(layout='wide')
#
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
#
# st.title('Crypto Price App')
# st.markdown("""
#     This Page is under construction. We are working smart and hard, so will show you soon.
# """)
#
# expander_bar = st.expander("About")
# expander_bar.markdown("""
#     * **Python Libraries: ** base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, selenium, time
# """)
#
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
#
# col1.header('User Input Options')
# cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
# @st.cache_data
# def fetch_crypto_data(url):
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome()
#     driver.get(url)
#     try:
#         select_all = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-7d96a92a-0 iuFFJS sc-c8d6e27d-0 cycNPx']"))
#         )
#         select_all.click()
#         driver.execute_script("window.scrollTo(0, 8100);")  # Adjust scroll amount as needed
#         show_100_option = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-4c05d6ef-0 sc-4cedfb43-0 dlQYLv hKzaCa']"))
#         )
#         show_100_option.click()
#         time.sleep(3)  # Adjust sleep time if necessary
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         crypto_table = soup.find('table', {'class': 'cmc-table'})
#         rows = crypto_table.find_all('tr')
#         data = {
#             'Name': [], 'Price': [], '1h %': [], '24h %': [], '7d %': [], 'Market Cap': [], 'Volume (24h)': [], 'Symbol': []
#         }
#         for row in rows[1:]:
#             cells = row.find_all('td')
#             if len(cells) > 9:
#                 data['Name'].append(cells[2].text)
#                 data['Price'].append(cells[3].text.strip())
#                 data['1h %'].append(cells[4].text.strip())
#                 data['24h %'].append(cells[5].text.strip())
#                 data['7d %'].append(cells[6].text.strip())
#                 data['Market Cap'].append(cells[7].text.strip())
#                 data['Volume (24h)'].append(cells[8].text.strip())
#                 data['Symbol'].append(cells[8].text.split(" ")[-1])
#         df = pd.DataFrame(data)
#         print("Initial DataFrame created with {} records".format(len(df)))
#         scroll_step = 2000  # Adjust scroll amount as needed
#         current_scroll = 8100  # Starting scroll position
#         while True:
#             current_scroll += scroll_step
#             driver.execute_script(f"window.scrollTo(0, {current_scroll});")
#             time.sleep(2)
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             crypto_table = soup.find('table', {'class': 'cmc-table'})
#             rows = crypto_table.find_all('tr')
#             if len(rows) == len(df) + 1:
#                 break
#             for row in rows[len(df) + 1:]:
#                 cells = row.find_all('td')
#                 if len(cells) > 9:
#                     data['Name'].append(cells[2].text)
#                     data['Price'].append(cells[3].text.strip())
#                     data['1h %'].append(cells[4].text.strip())
#                     data['24h %'].append(cells[5].text.strip())
#                     data['7d %'].append(cells[6].text.strip())
#                     data['Market Cap'].append(cells[7].text.strip())
#                     data['Volume (24h)'].append(cells[8].text.strip())
#                     data['Symbol'].append(cells[8].text.split(" ")[-1])
#             df = pd.DataFrame(data)
#             print(f"DataFrame updated with {len(df)} records")
#         print("All records fetched.")
#         return df
#     finally:
#         driver.quit()
#
# url = "https://coinmarketcap.com/"
# df = fetch_crypto_data(url)
#
# sorted_coin = sorted(df['Symbol'])
# selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['Symbol'].isin(selected_coin)]
#
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
#
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "7d %", "24h": "24h %", "1h": "1h %"}
# selected_percent_tf = percent_dict[per_timeframe]
#
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
#
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
# col2.dataframe(df_coins)
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
#
# col2.header("Total of % Price change ")
#
# df_change = pd.concat([df_coins.Symbol, df_coins['1h %'], df_coins['24h %'], df_coins['7d %']], axis=1)
# df_change = df_change.set_index('Symbol')
# df_change['positive_percent_change_1h'] = df_change['1h %'].str.rstrip('%').astype(float) > 0
# df_change['positive_percent_change_24h'] = df_change['24h %'].str.rstrip('%').astype(float) > 0
# df_change['positive_percent_change_7d'] = df_change['7d %'].str.rstrip('%').astype(float) > 0
#
# col2.dataframe(df_change)
#
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['7d %'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['7d %'].str.rstrip('%').astype(float).plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['24h %'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['24h %'].str.rstrip('%').astype(float).plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['1h %'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['1h %'].str.rstrip('%').astype(float).plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
#
#
#
#
#
#
#
#
#
#
#
#

#
# import streamlit as st
# from PIL import Image
# import pandas as pd
# import base64
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
#
# st.set_page_config(layout='wide')
#
# image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
# st.image(image, width=500)
#
# st.title('Crypto Price App')
# st.markdown("""
#     This Page is under construction. We are working smart and hard, so will show you soon.
# """)
#
# expander_bar = st.expander("About")
# expander_bar.markdown("""
#     * **Python Libraries: ** base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, selenium, time
# """)
#
# col1 = st.sidebar
# col2, col3 = st.columns((2, 1))
#
# col1.header('User Input Options')
# cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))
#
#
# @st.cache_data
# def fetch_crypto_data(url):
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome()
#     driver.get(url)
#     try:
#         select_all = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-7d96a92a-0 iuFFJS sc-c8d6e27d-0 cycNPx']"))
#         )
#         select_all.click()
#         driver.execute_script("window.scrollTo(0, 8100);")  # Adjust scroll amount as needed
#         show_100_option = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-4c05d6ef-0 sc-4cedfb43-0 dlQYLv hKzaCa']"))
#         )
#         show_100_option.click()
#         time.sleep(3)  # Adjust sleep time if necessary
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         crypto_table = soup.find('table', {'class': 'cmc-table'})
#         rows = crypto_table.find_all('tr')
#         data = {
#             'Name': [], 'Symbol': [], 'Price': [], '1h %': [], '24h %': [], '7d %': [], 'Market Cap': [],
#             'Volume (24h)': []
#         }
#         for row in rows[1:]:
#             cells = row.find_all('td')
#             if len(cells) > 9:
#                 name = cells[2].text
#                 symbol = cells[8].text.split(" ")[-1]
#                 if symbol in name:
#                     name = name.replace(symbol, '', 1).strip()
#                 data['Name'].append(name)
#                 data['Symbol'].append(symbol)
#                 data['Price'].append(cells[3].text.strip().replace('$', ' '))
#                 data['1h %'].append(cells[4].text.strip())
#                 data['24h %'].append(cells[5].text.strip())
#                 data['7d %'].append(cells[6].text.strip())
#                 market_cap_value = cells[7].text.strip().split('$')[-1].replace(',', '')
#                 data['Market Cap'].append(market_cap_value)
#                 data['Volume (24h)'].append(cells[8].text.strip().replace('$', '').split(' ')[0])
#
#         df = pd.DataFrame(data)
#         # print("Initial DataFrame created with {} records".format(len(df)))
#         scroll_step = 2000  # Adjust scroll amount as needed
#         current_scroll = 8100  # Starting scroll position
#         while True:
#             current_scroll += scroll_step
#             driver.execute_script(f"window.scrollTo(0, {current_scroll});")
#             time.sleep(2)
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             crypto_table = soup.find('table', {'class': 'cmc-table'})
#             rows = crypto_table.find_all('tr')
#             if len(rows) == len(df) + 1:
#                 break
#             for row in rows[len(df) + 1:]:
#                 cells = row.find_all('td')
#                 if len(cells) > 9:
#                     name = cells[2].text
#                     symbol = cells[8].text.split(" ")[-1]
#                     if symbol in name:
#                         name = name.replace(symbol, '', 1).strip()
#                     data['Name'].append(name)
#                     data['Symbol'].append(symbol)
#                     data['Price'].append(cells[3].text.strip().replace('$', ''))
#                     data['1h %'].append(cells[4].text.strip())
#                     data['24h %'].append(cells[5].text.strip())
#                     data['7d %'].append(cells[6].text.strip())
#                     market_cap_value = cells[7].text.strip().split('$')[-1].replace(',', '')
#                     data['Market Cap'].append(market_cap_value)
#                     data['Volume (24h)'].append(cells[8].text.strip().replace('$', '').split(' ')[0])
#
#             df = pd.DataFrame(data, columns=['Name', 'Symbol', 'Price', '1h %', '24h %', '7d %', 'Market Cap',
#                                              'Volume (24h)'], index=None)
#             # print(f"DataFrame updated with {len(df)} records")
#         # print("All records fetched.")
#         return df
#     finally:
#         driver.quit()
#
#
# url = "https://coinmarketcap.com/"
# df = fetch_crypto_data(url)
#
# sorted_coin = sorted(df['Symbol'].unique())
# selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# df_selected_coin = df[df['Symbol'].isin(selected_coin)]
#
# num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
# df_coins = df_selected_coin[:num_coin]
#
# per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
# percent_dict = {"7d": "7d %", "24h": "24h %", "1h": "1h %"}
# selected_percent_tf = percent_dict[per_timeframe]
#
# sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])
#
# col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write(
#     'Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
# col2.dataframe(df_coins)
#
#
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
#     return href
#
#
# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)
#
# col2.header("Total of % Price change ")
#
# df_change = pd.concat([df_coins.Symbol, df_coins['1h %'], df_coins['24h %'], df_coins['7d %']], axis=1)
# df_change = df_change.set_index('Symbol')
# df_change['positive_percent_change_1h'] = df_change['1h %'].str.rstrip('%').astype(float) > 0
# df_change['positive_percent_change_24h'] = df_change['24h %'].str.rstrip('%').astype(float) > 0
# df_change['positive_percent_change_7d'] = df_change['7d %'].str.rstrip('%').astype(float) > 0
#
# col2.dataframe(df_change)
#
# col3.header('Bar plot of % Price Change')
#
# if per_timeframe == '7d':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['7d %'])
#     col3.write('*7 days period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['7d %'].str.rstrip('%').astype(float).plot(kind='barh',
#                                                              color=df_change.positive_percent_change_7d.map(
#                                                                  {True: 'green', False: 'red'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# elif per_timeframe == '24h':
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['24h %'])
#     col3.write('*24 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['24h %'].str.rstrip('%').astype(float).plot(kind='barh',
#                                                               color=df_change.positive_percent_change_24h.map(
#                                                                   {True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")
# else:
#     if sort_values == 'Yes':
#         df_change = df_change.sort_values(by=['1h %'])
#     col3.write('*1 hour period*')
#     if not df_change.empty:
#         plt.figure(figsize=(10, len(df_change) * 1))
#         plt.subplots_adjust(top=1, bottom=0)
#         df_change['1h %'].str.rstrip('%').astype(float).plot(kind='barh',
#                                                              color=df_change.positive_percent_change_1h.map(
#                                                                  {True: 'g', False: 'r'}))
#         col3.pyplot(plt)
#     else:
#         col3.write("No data available for the selected timeframe.")






















import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

st.set_page_config(layout='wide')

image = Image.open(r"D:\2025\Portfolio Projects\CryptoCurrency Webpage\Resources\Main LOGO.jpg")
st.image(image, width=500)

st.title('Crypto Price App')
st.markdown("""
    This Page is under construction. We are working smart and hard, so will show you soon.
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
    * **Python Libraries: ** base64, pandas, matplotlib, streamlit, BeautifulSoup, requests, json, selenium, time
""")

col1 = st.sidebar
col2, col3 = st.columns((2, 1))

col1.header('User Input Options')
cur_price_unit = col1.selectbox("Select currency for Price", ('USD', 'BTC', 'ETH'))


@st.cache_data
def fetch_crypto_data(url):
    cache_file = 'crypto_data.csv'
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        select_all = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-7d96a92a-0 iuFFJS sc-c8d6e27d-0 cycNPx']"))
        )
        select_all.click()
        driver.execute_script("window.scrollTo(0, 8100);")  # Adjust scroll amount as needed
        show_100_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-4c05d6ef-0 sc-4cedfb43-0 dlQYLv hKzaCa']"))
        )
        show_100_option.click()
        time.sleep(3)  # Adjust sleep time if necessary
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        crypto_table = soup.find('table', {'class': 'cmc-table'})
        rows = crypto_table.find_all('tr')
        data = {
            'Name': [], 'Symbol': [], 'Price': [], '1h %': [], '24h %': [], '7d %': [], 'Market Cap': [],
            'Volume (24h)': []
        }
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) > 9:
                name = cells[2].text
                symbol = cells[8].text.split(" ")[-1]
                if symbol in name:
                    name = name.replace(symbol, '', 1).strip()
                data['Name'].append(name)
                data['Symbol'].append(symbol)
                data['Price'].append(cells[3].text.strip().replace('$', ' '))
                data['1h %'].append(cells[4].text.strip())
                data['24h %'].append(cells[5].text.strip())
                data['7d %'].append(cells[6].text.strip())
                market_cap_value = cells[7].text.strip().split('$')[-1].replace(',', '')
                data['Market Cap'].append(market_cap_value)
                data['Volume (24h)'].append(cells[8].text.strip().replace('$', '').split(' ')[0])

        df = pd.DataFrame(data)
        # print("Initial DataFrame created with {} records".format(len(df)))
        scroll_step = 2000  # Adjust scroll amount as needed
        current_scroll = 8100  # Starting scroll position
        while True:
            current_scroll += scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_scroll});")
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            crypto_table = soup.find('table', {'class': 'cmc-table'})
            rows = crypto_table.find_all('tr')
            if len(rows) == len(df) + 1:
                break
            for row in rows[len(df) + 1:]:
                cells = row.find_all('td')
                if len(cells) > 9:
                    name = cells[2].text
                    symbol = cells[8].text.split(" ")[-1]
                    if symbol in name:
                        name = name.replace(symbol, '', 1).strip()
                    data['Name'].append(name)
                    data['Symbol'].append(symbol)
                    data['Price'].append(cells[3].text.strip().replace('$', ''))
                    data['1h %'].append(cells[4].text.strip())
                    data['24h %'].append(cells[5].text.strip())
                    data['7d %'].append(cells[6].text.strip())
                    market_cap_value = cells[7].text.strip().split('$')[-1].replace(',', '')
                    data['Market Cap'].append(market_cap_value)
                    data['Volume (24h)'].append(cells[8].text.strip().replace('$', '').split(' ')[0])

            df = pd.DataFrame(data, columns=['Name', 'Symbol', 'Price', '1h %', '24h %', '7d %', 'Market Cap',
                                             'Volume (24h)'], index=None)
            # print(f"DataFrame updated with {len(df)} records")
        # print("All records fetched.")
        df.to_csv(cache_file, index=False)
        return df
    finally:
        driver.quit()


url = "https://coinmarketcap.com/"
df = fetch_crypto_data(url)

sorted_coin = sorted(df['Symbol'].unique())
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
df_selected_coin = df[df['Symbol'].isin(selected_coin)]

num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

per_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
percent_dict = {"7d": "7d %", "24h": "24h %", "1h": "1h %"}
selected_percent_tf = percent_dict[per_timeframe]

sort_values = col1.selectbox("Sort Values?", ["Yes", "No"])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write(
    'Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
col2.dataframe(df_coins)


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href


col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

col2.header("Total of % Price change ")

df_change = pd.concat([df_coins.Symbol, df_coins['1h %'], df_coins['24h %'], df_coins['7d %']], axis=1)
df_change = df_change.set_index('Symbol')
df_change['positive_percent_change_1h'] = df_change['1h %'].str.rstrip('%').astype(float) > 0
df_change['positive_percent_change_24h'] = df_change['24h %'].str.rstrip('%').astype(float) > 0
df_change['positive_percent_change_7d'] = df_change['7d %'].str.rstrip('%').astype(float) > 0

col2.dataframe(df_change)

col3.header('Bar plot of % Price Change')

if per_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['7d %'])
    col3.write('*7 days period*')
    if not df_change.empty:
        plt.figure(figsize=(10, len(df_change) * 1))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['7d %'].str.rstrip('%').astype(float).plot(kind='barh',
                                                             color=df_change.positive_percent_change_7d.map(
                                                                 {True: 'green', False: 'red'}))
        col3.pyplot(plt)
    else:
        col3.write("No data available for the selected timeframe.")
elif per_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['24h %'])
    col3.write('*24 hour period*')
    if not df_change.empty:
        plt.figure(figsize=(10, len(df_change) * 1))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['24h %'].str.rstrip('%').astype(float).plot(kind='barh',
                                                              color=df_change.positive_percent_change_24h.map(
                                                                  {True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        col3.write("No data available for the selected timeframe.")
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['1h %'])
    col3.write('*1 hour period*')
    if not df_change.empty:
        plt.figure(figsize=(10, len(df_change) * 1))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['1h %'].str.rstrip('%').astype(float).plot(kind='barh',
                                                             color=df_change.positive_percent_change_1h.map(
                                                                 {True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        col3.write("No data available for the selected timeframe.")
