import streamlit as st
import pandas as pd
import plotly.express as px

# タイトル
st.title("📊 月次売上ダッシュボード")

# データ読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("sample_sales_data.csv", parse_dates=["date"])
    df["date"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

#折れ線グラフで、カテゴリごとの売上推移を表示
fig = px.line(
    df,
    x="date",
    y="sales",
    color='category',
    template='plotly_white'
    )
fig.show()

#棒グラフで、月ごとのカテゴリ別売上比較
fig = px.bar(
    df,
    x='date',
    y='sales',
    color='category',
    hover_data=['sales'],
    labels={'sales': 'Sales'},
    template='plotly_white'
)
fig.show()

#円グラフで、6ヶ月間のカテゴリ別売上の割合を表示
fig = px.pie(
    df,
    values='sales',
    names='category',
    title='Sales by Category',
    template='plotly_white'
    )
fig.show()

#散布図で、売上と利益の関係をカテゴリ別に表示
fig = px.scatter(
    df,
    x="profit",
    y="sales",
    color="category",
    size="volume",
    template='plotly_white'
    )
fig.show()

#箱ひげ図で、カテゴリごとの売上のばらつきを確認
fig = px.box(
    df,
    x="category",
    y="sales",
    template="plotly_white",
    points="all",
    hover_data=["profit", "volume", "date"])
fig.show()


#カテゴリごとの売上と利益を並べて表示

from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=2, subplot_titles=("Sales", "Profit"))

for cat in df['category'].unique():
    cat_data = df[df['category'] == cat]
    fig.add_trace(go.Bar(x=cat_data['date'], y=cat_data['sales'], name=cat), row=1, col=1)
    fig.add_trace(go.Bar(x=cat_data['date'], y=cat_data['profit'], name=cat, showlegend=False), row=1, col=2)

fig.update_layout(title_text="Category-wise Sales and Profit", template="plotly_white")
fig.show()

#月ごとの推移などを動きで見せる
fig = px.bar(
    df,
    x='category',
    y='sales',
    color='category',
    animation_frame='date',
    template='plotly_white'
)
fig.show()

#売上を棒グラフ、利益率を折れ線で表示

monthly = df.groupby("date").agg({
    "sales": "sum",
    "profit": "sum"
}).reset_index()

monthly["profit_margin"] = (monthly["profit"] / monthly["sales"]) * 100

fig = go.Figure()

# 売上（棒グラフ）
fig.add_trace(go.Bar(
    x=monthly["date"],
    y=monthly["sales"],
    name="売上",
    yaxis="y1",
    marker_color="#636EFA"
))

# 利益率（折れ線）
fig.add_trace(go.Scatter(
    x=monthly["date"],
    y=monthly["profit_margin"],
    name="利益率（%）",
    yaxis="y2",
    mode="lines+markers",
    line=dict(color="#EF553B", width=3),
    marker=dict(size=6)
  ))

# レイアウト調整
fig.update_layout(
    title="月別 売上と利益率",
    xaxis=dict(title="日付"),
    yaxis=dict(
        title="売上（円）",
        titlefont=dict(color="#636EFA"),
        tickfont=dict(color="#636EFA")
    ),
    yaxis2=dict(
        title="利益率（%）",
        titlefont=dict(color="#EF553B"),
        tickfont=dict(color="#EF553B"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    template="plotly_white"
)

fig.show()

#カテゴリ×月の売上を色で表現

pivot_df = df.pivot_table(index="category", columns="date", values="sales", aggfunc="sum")
fig = px.imshow(pivot_df, text_auto=True, color_continuous_scale='Blues')
fig.update_layout(title="Heatmap of Sales by Category and Date")
fig.show()
