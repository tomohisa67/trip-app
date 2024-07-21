import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントのパスを指定
font_path = '/Users/tabuchitomohisa/Desktop/ryokou/Noto_Sans_JP/NotoSansJP-VariableFont_wght.ttf'
font_prop = fm.FontProperties(fname=font_path, weight='bold')

from utils import check_season

# ---- サイドバー ---- #
# year = st.sidebar.selectbox('売上を計算する年を選択', ['2018', '2019', '2020', '2021', '2022', '2023'])
year_min, year_max = st.sidebar.slider('売上を計算する範囲を選択', 2018, 2023, (2018, 2023))
# y_min, y_max = st.sidebar.slider('yの範囲', 0, 100000000, (0, 10000000))

st.sidebar.title("パラメータの設定")
st.sidebar.subheader("獲得顧客について")
rate1 = st.sidebar.number_input('全体の内、対象とする顧客の割合 (%)', min_value=0, max_value=100, value=20, step=1)
rate2 = st.sidebar.number_input('全体の内、対象とする顧客の割合 (%)', min_value=0, max_value=100, value=25, step=1)
rate1 = rate1 / 100
rate2 = rate2 / 100
final_rate = rate1 * rate2

rate3 = st.sidebar.number_input('オンライン (%)', min_value=0, max_value=100, value=60, step=1)
rate4 = st.sidebar.number_input('店舗 (%)', min_value=0, max_value=100, value=40, step=1)
rate3 = rate3 / 100
rate4 = rate4 / 100

st.sidebar.subheader("宿泊客について")
num_adult = st.sidebar.number_input('大人の人数', min_value=0, max_value=100, value=2, step=1)
num_child = st.sidebar.number_input('子どもの人数', min_value=0, max_value=100, value=2, step=1)

st.sidebar.subheader("価格について")
price_adult_on = st.sidebar.number_input('客単価（大人、オンシーズン）', min_value=10000, max_value=100000, value=30000, step=1000)
price_child_on = st.sidebar.number_input('客単価（子ども、オンシーズン）', min_value=10000, max_value=100000, value=15000, step=1000)

price_adult_off = st.sidebar.number_input('客単価（大人、オフシーズン）', min_value=10000, max_value=100000, value=20000, step=1000)
price_child_off = st.sidebar.number_input('客単価（子ども、オフシーズン）', min_value=10000, max_value=100000, value=10000, step=1000)

BBQ_set = st.sidebar.number_input('BBQセットのレンタル料金', min_value=10000, max_value=100000, value=20000, step=1000)
BBQ_ingredients_adult = st.sidebar.number_input('BBQの食材費（大人）', min_value=1000, max_value=100000, value=10000, step=1000)
BBQ_ingredients_child = st.sidebar.number_input('BBQの食材費（子ども）', min_value=1000, max_value=100000, value=5000, step=1000)
BBQ_ingredients_prob = st.sidebar.number_input('BBQの食材費を申し込む割合 (%)', min_value=0, max_value=100, value=95, step=1)
BBQ_ingredients_prob = BBQ_ingredients_prob / 100

occupacy_rate_on = st.sidebar.number_input('オンシーズンの稼働率 (%)', min_value=0, max_value=100, value=60, step=1)
occupacy_rate_off = st.sidebar.number_input('オフシーズンの稼働率 (%)', min_value=0, max_value=100, value=40, step=1)
occupacy_rate_on = occupacy_rate_on / 100
occupacy_rate_off = occupacy_rate_off / 100

total_sales = []
days = [i+1 for i in range(365 * (year_max - year_min + 1))]
num_people = 0
for d in days:
    season = 'on' if check_season(d) else 'off'
    if season == 'on':
        if np.random.rand() < occupacy_rate_on:
            sales = price_adult_on * num_adult + price_child_on * num_child
            num_people += num_adult + num_child
        else:
            total_sales.append(0)
            continue
    else:
        if np.random.rand() < occupacy_rate_off:
            sales = price_adult_off * num_adult + price_child_off * num_child
            num_people += num_adult + num_child
        else:
            total_sales.append(0)
            continue

    sales += BBQ_set
    if np.random.rand() < BBQ_ingredients_prob:
        sales += BBQ_ingredients_adult * num_adult + BBQ_ingredients_child * num_child

    total_sales.append(sales)

# 累積和
total_sales_ = np.cumsum(total_sales)

# ---- メインページ ---- #
# タイトルと説明の追加
st.title("年間売上変動の可視化")
st.write("このアプリは宿泊施設の年間売上変動を可視化します。")

cols = ['宿泊した人数', '一人当たりの平均単価', '売上', '売上（オンライン）', '売上（店舗）']
vals = [[num_people, total_sales_[-1] // num_people, total_sales_[-1], total_sales_[-1] * rate3, total_sales_[-1] * rate4]]
df = pd.DataFrame(vals, columns=cols)
st.write(df)

fig, ax = plt.subplots()
ax.plot(days, total_sales_, linestyle='-')
ax.set_title('Annual sales fluctuation')
ax.set_xlabel('Days')
ax.set_ylabel('Sales')
ax.set_xlim(0, len(days))
ax.set_ylim(0, 100000000)
ax.grid(True)
st.pyplot(fig)
