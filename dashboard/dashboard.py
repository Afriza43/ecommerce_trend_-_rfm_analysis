import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


def create_trend_order(df):
    trend_order = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "count",
        "payment_value": "sum"
    })
    trend_order = trend_order.reset_index()
    trend_order.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return trend_order


all_df = pd.read_csv("semua_data.csv")


datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()


st.header('Brazilian E-Commerce Dashboard')
st.subheader('Monthly Orders')

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(min_date)) & (
    all_df["order_purchase_timestamp"] <= str(max_date))]

trend_order = create_trend_order(main_df)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    trend_order["order_purchase_timestamp"],
    trend_order["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Order Count", fontsize=15)
ax.set_title("Order Trend", fontsize=30)


st.pyplot(fig)

st.subheader("Customer Segmentation")

col1, col2, col3 = st.columns(3)

with col1:
    recently = all_df.order_purchase_timestamp.dt.date.max().strftime("%d-%m-%Y")
    st.metric("Recently Order", value=recently)

with col2:
    st.metric("Most Frequency", value=all_df.Frequency.max())

with col3:
    currency = format_currency(all_df.Monetary.max(), 'R$', locale='pt_BR')
    st.metric("Most Spend", value=currency)

fig, ax = plt.subplots(figsize=(16, 8))
sns.countplot(x="Segment", data=all_df,
              order=all_df['Segment'].value_counts().index, hue="Segment")

for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2., height + 5,
            f'{height}',
            ha="center", fontsize=20)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=90)
ax.set_xlabel("Customer Segment", fontsize=15)
ax.set_ylabel("Jumlah Customer", fontsize=15)
ax.set_title("Customer Distribution", fontsize=30)

st.pyplot(fig)
