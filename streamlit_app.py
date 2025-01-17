import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm

# # 日本語フォントのパスを指定
# font_path = '/Users/tabuchitomohisa/Desktop/ryokou/Noto_Sans_JP/NotoSansJP-VariableFont_wght.ttf'
# font_prop = fm.FontProperties(fname=font_path, weight='bold')

from utils import check_season

# ---- サイドバー ---- #
# year = st.sidebar.selectbox('売上を計算する年を選択', ['2018', '2019', '2020', '2021', '2022', '2023'])
year_min, year_max = st.sidebar.slider('売上を計算する範囲を選択', 2018, 2023, (2018, 2023))
# y_min, y_max = st.sidebar.slider('yの範囲', 0, 100000000, (0, 10000000))

st.sidebar.title("パラメータの設定")
# st.sidebar.subheader("獲得顧客について")
# rate1 = st.sidebar.number_input('全体の内、対象とする顧客の割合 (%)', min_value=0, max_value=100, value=20, step=1)
# rate2 = st.sidebar.number_input('全体の内、対象とする顧客の割合 (%)', min_value=0, max_value=100, value=25, step=1)
# rate1 = rate1 / 100
# rate2 = rate2 / 100
# final_rate = rate1 * rate2

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
st.title("年間収益シミュレーション")
st.write("宿泊施設の年間収益シミュレーション")

num_people_per_family = num_adult + num_child
cols = ['宿泊人数', '平均単価', '宿泊組数（1組' + str(num_people_per_family) + '人）', '売上', '売上（オンライン）', '売上（店舗）']
vals = [[num_people, total_sales_[-1] // num_people, num_people / num_people_per_family, total_sales_[-1], total_sales_[-1] * rate3, total_sales_[-1] * rate4]]
df = pd.DataFrame(vals, columns=cols)
# df_1 = df['宿泊人数', '宿泊組数（1組' + str(num_people_per_family) + '人）', '一人当たりの平均単価'].copy()
# df_2 = df['売上', '売上（オンライン）', '売上（店舗）'].copy()
# st.write(df_1)
# st.write(df_2)
st.write(df)

df2 = pd.read_csv('data.csv')
# st.write(df)

# TMP = '2019'
# df2['合計人数'] = df2.sum(axis=1)
# total_num = df2.loc[df2['年'] == 2019, '合計人数'].values[0]

# countries = df2.columns

df3 = pd.read_csv('data2.csv')
# st.write(df3)

st.sidebar.subheader("一か月あたりの固定費")
# a1 = st.sidebar.number_input('人件費', min_value=0, max_value=100000000, value=17500000, step=500000)
a1_1 = st.sidebar.number_input('人件費（一人当たり）', min_value=0, max_value=10000000, value=300000, step=500000)
a1_2 = st.sidebar.number_input('人数', min_value=0, max_value=1000000, value=20, step=1)
a1 = a1_1 * a1_2 * (len(days) // 30)
a2 = st.sidebar.number_input('保険料', min_value=0, max_value=10000000, value=600000, step=100000)
a2 = a2 * (len(days) // 30)
a3 = st.sidebar.number_input('メンテナンス費用', min_value=0, max_value=10000000, value=800000, step=100000)
a3 = a3 * (len(days) // 30)
a4 = st.sidebar.number_input('マーケティング費用', min_value=0, max_value=10000000, value=500000, step=100000)
a4 = a4 * (len(days) // 30)
a5 = st.sidebar.number_input('セキュリティ費用', min_value=0, max_value=10000000, value=1200000, step=100000)
a5 = a5 * (len(days) // 30)
a6 = st.sidebar.number_input('広告宣伝費', min_value=0, max_value=10000000, value=2400000, step=100000)
a6 = a6 * (len(days) // 30)

st.sidebar.subheader("一か月あたりの変動費")
b1 = st.sidebar.number_input('清掃費', min_value=0, max_value=1000000, value=300000, step=50000)
b1 = b1 * (len(days) // 30)
b2 = st.sidebar.number_input('光熱費', min_value=0, max_value=1000000, value=200000, step=50000)
b2 = b2 * (len(days) // 30)
b3 = st.sidebar.number_input('消耗品費', min_value=0, max_value=1000000, value=100000, step=10000)
b3 = b3 * (len(days) // 30)
b4 = st.sidebar.number_input('諸経費', min_value=0, max_value=10000000, value=500000, step=100000)
b4 = b4 * (len(days) // 30)
b5 = st.sidebar.number_input('交通費', min_value=0, max_value=10000000, value=300000, step=50000)
b5 = b5 * (len(days) // 30)

a_cols = ['人件費', '保険料', 'メンテナンス費用', 'マーケティング費用', 'セキュリティ費用', '広告宣伝費']
a_vals = [[a1, a2, a3, a4, a5, a6]]
df_a = pd.DataFrame(a_vals, columns=a_cols)

df_a_1 = df_a[['人件費', '保険料', 'メンテナンス費用']].copy()
df_a_2 = df_a[['マーケティング費用', 'セキュリティ費用', '広告宣伝費']].copy()
st.write(f"固定費（{str(len(days) // 30)}か月分）")
st.write(f"一人当たりの人件費: {a1_1} 円、人数: {a1_2} 人")
st.write(df_a_1)
st.write(df_a_2)

b_cols = ['清掃費', '光熱費', '消耗品費', '諸経費', '交通費']
b_vals = [[b1, b2, b3, b4, b5]]
df_b = pd.DataFrame(b_vals, columns=b_cols)
st.write(f"変動費（{str(len(days) // 30)}か月分）")
st.write(f"{str(len(days) // 30)}か月分")
st.write(df_b)

# 総売上
x = ['売上高', '販管費', '営業利益（売上高 - 販管費）']
hankanhi = (sum(a_vals[0]) + sum(b_vals[0])) * (year_max - year_min + 1)
y = [[total_sales_[-1], hankanhi, total_sales_[-1] - hankanhi]]
df_c = pd.DataFrame(y, columns=x)
st.write("営業利益")
st.write(df_c)


fig, ax = plt.subplots()
ax.plot(days, total_sales_, linestyle='-')
ax.set_title('Annual sales fluctuation')
ax.set_xlabel('Days')
ax.set_ylabel('Sales')
ax.set_xlim(0, len(days))
ax.set_ylim(0, 100000000)
ax.grid(True)
st.pyplot(fig)
