import streamlit as st
import pandas as pd
import plotly.express as px

# タイトル
st.title("📊 月次売上ダッシュボード")

# データ読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", parse_dates=["日付"])
    df["月"] = df["日付"].dt.to_period("M").astype(str)
    return df

df = load_data()

# サイドバーでフィルタ
selected_month = st.sidebar.selectbox("月を選択", sorted(df["月"].unique(), reverse=True))
df_filtered = df[df["月"] == selected_month]

# 売上推移グラフ（月別合計）
monthly_sales = df.groupby("月")["売上"].sum().reset_index()
fig_line = px.line(monthly_sales, x="月", y="売上", title="📈 月別売上推移")

# カテゴリ別売上（円グラフ）
category_sales = df_filtered.groupby("カテゴリ")["売上"].sum().reset_index()
fig_pie = px.pie(category_sales, values="売上", names="カテゴリ", title=f"{selected_month} のカテゴリ別売上")

# 表示
st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)

# データテーブル表示
with st.expander("🔍 生データを表示"):
    st.dataframe(df_filtered)
