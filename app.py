import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# タイトルと説明
st.set_page_config(page_title="月次売上ダッシュボード", layout="wide")
st.title("📊 月次売上ダッシュボード")
st.markdown("売上、利益、利益率などをカテゴリ別・月別で可視化しています。")

# データ読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("sample_sales_data.csv", parse_dates=["date"])
    df["date"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# サイドバーでフィルター
categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect("カテゴリ選択", categories, default=categories)
filtered_df = df[df["category"].isin(selected_categories)]

# 折れ線グラフ：カテゴリごとの売上推移
st.subheader("📈 カテゴリごとの売上推移")
fig1 = px.line(
    filtered_df,
    x="date",
    y="sales",
    color='category',
    template='plotly_white'
)
st.plotly_chart(fig1, use_container_width=True)

# 棒グラフ：月ごとのカテゴリ別売上
st.subheader("📊 月ごとのカテゴリ別売上（棒グラフ）")
fig2 = px.bar(
    filtered_df,
    x='date',
    y='sales',
    color='category',
    template='plotly_white'
)
st.plotly_chart(fig2, use_container_width=True)

# 円グラフ：6ヶ月のカテゴリ別売上割合
st.subheader("🥧 売上割合（カテゴリ別）")
fig3 = px.pie(
    filtered_df,
    values='sales',
    names='category',
    title='Sales by Category',
    template='plotly_white'
)
st.plotly_chart(fig3, use_container_width=True)

# 散布図：売上と利益の関係
st.subheader("🧮 売上 vs 利益（カテゴリ別）")
fig4 = px.scatter(
    filtered_df,
    x="profit",
    y="sales",
    color="category",
    size="volume",
    template='plotly_white'
)
st.plotly_chart(fig4, use_container_width=True)

# 箱ひげ図：売上のばらつき
st.subheader("📦 売上のばらつき（カテゴリ別）")
fig5 = px.box(
    filtered_df,
    x="category",
    y="sales",
    template="plotly_white",
    points="all",
    hover_data=["profit", "volume", "date"]
)
st.plotly_chart(fig5, use_container_width=True)

# サブプロット：売上と利益
st.subheader("📚 カテゴリごとの売上と利益")
fig6 = make_subplots(rows=1, cols=2, subplot_titles=("売上", "利益"))
for cat in filtered_df['category'].unique():
    cat_data = filtered_df[filtered_df['category'] == cat]
    fig6.add_trace(go.Bar(x=cat_data['date'], y=cat_data['sales'], name=cat), row=1, col=1)
    fig6.add_trace(go.Bar(x=cat_data['date'], y=cat_data['profit'], name=cat, showlegend=False), row=1, col=2)
fig6.update_layout(title_text="Sales and Profit by Category", template="plotly_white")
st.plotly_chart(fig6, use_container_width=True)

# アニメーションバー：カテゴリ別月次売上
st.subheader("🎬 カテゴリ別月次売上の推移（アニメーション）")
fig7 = px.bar(
    filtered_df,
    x='category',
    y='sales',
    color='category',
    animation_frame='date',
    template='plotly_white'
)
st.plotly_chart(fig7, use_container_width=True)

# 売上と利益率の2軸グラフ
st.subheader("📉 売上と利益率")
monthly = filtered_df.groupby("date").agg({
    "sales": "sum",
    "profit": "sum"
}).reset_index()
monthly["profit_margin"] = (monthly["profit"] / monthly["sales"]) * 100
fig8 = go.Figure()
fig8.add_trace(go.Bar(x=monthly["date"], y=monthly["sales"], name="売上", yaxis="y1", marker_color="#636EFA"))
fig8.add_trace(go.Scatter(x=monthly["date"], y=monthly["profit_margin"], name="利益率（%）", yaxis="y2",
                          mode="lines+markers", line=dict(color="#EF553B", width=3)))
fig8.update_layout(
    title="月別 売上と利益率",
    xaxis=dict(title="月"),
    yaxis=dict(title="売上（円）", titlefont=dict(color="#636EFA"), tickfont=dict(color="#636EFA")),
    yaxis2=dict(title="利益率（%）", titlefont=dict(color="#EF553B"), tickfont=dict(color="#EF553B"),
                overlaying="y", side="right"),
    legend=dict(x=0.01, y=0.99),
    template="plotly_white"
)
st.plotly_chart(fig8, use_container_width=True)

# ヒートマップ：カテゴリ×月の売上
st.subheader("🌡️ カテゴリ×月の売上ヒートマップ")
pivot_df = filtered_df.pivot_table(index="category", columns="date", values="sales", aggfunc="sum")
fig9 = px.imshow(pivot_df, text_auto=True, color_continuous_scale='Blues')
fig9.update_layout(title="Heatmap of Sales by Category and Date")
st.plotly_chart(fig9, use_container_width=True)
