import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

final_all_df = pd.read_csv("all_data.csv") 

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Latihan Analisis Data E-Commerce dengan Python</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>made by fajri haryanto | muhamadfajri2804@gmail.com | mijimo</p>", unsafe_allow_html=True)

# 1. Kategori Produk Terpopuler dan Tidak Populer
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("Kategori produk apa yang paling populer dan tidak populer di antara pelanggan berdasarkan jumlah produk terjual?")

col1, col2 = st.columns(2)

# Grafik 1: Top 10 Kategori Produk Terlaku
with col1:
    st.markdown("### Top 10 Kategori Produk Terlaku")
    product_sales = final_all_df.groupby('product_category_name')['order_item_id'].count().sort_values(ascending=False).head(10)
    colors = ['darkblue'] + ['skyblue'] * (len(product_sales) - 1)
    fig, ax = plt.subplots(figsize=(8, 6))
    product_sales.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('Top 10 Kategori Produk Terlaku')
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Jumlah Penjualan')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Grafik 2: 10 Kategori Produk Kurang Laku
with col2:
    st.markdown("### 10 Kategori Produk Kurang Laku")
    product_sales = final_all_df.groupby('product_category_name')['order_item_id'].count().sort_values(ascending=False).tail(10)
    colors = ['skyblue'] * (len(product_sales) - 1) + ['darkblue']
    fig, ax = plt.subplots(figsize=(8, 6))
    product_sales.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('10 Kategori Produk Kurang Laku')
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Jumlah Penjualan')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 2. Kategori Produk dengan Pendapatan Tertinggi
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("Kategori produk mana yang memberikan kontribusi pendapatan terbesar bagi perusahaan?")

product_revenue = final_all_df.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10)
colors = ['green'] + ['lightgreen'] * (len(product_revenue) - 1)
fig, ax = plt.subplots(figsize=(12, 6))
product_revenue.plot(kind='bar', color=colors, ax=ax)
ax.set_title('Top 10 Kategori Produk dengan Pendapatan Tertinggi')
ax.set_xlabel('Kategori Produk')
ax.set_ylabel('Pendapatan Total')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# 3. Distribusi Metode Pembayaran
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("Metode pembayaran mana yang paling sering digunakan oleh pelanggan berdasarkan total transaksi?")

col1, col2 = st.columns(2)

# Grafik 3: Pie Chart Distribusi Metode Pembayaran
with col1:
    payment_distribution = final_all_df['payment_type'].value_counts()
    colors = ['lightgreen', 'pink', 'lightblue', 'purple']
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(payment_distribution, autopct='%1.1f%%', startangle=90, colors=colors, pctdistance=1.20)
    ax.legend(wedges, payment_distribution.index, title="Metode Pembayaran", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=5)
    plt.setp(autotexts, size=9, weight="bold")
    ax.set_title('Distribusi Metode Pembayaran', fontsize=15)
    st.pyplot(fig)

# Informasi pendapatan per metode pembayaran
with col2:
    st.markdown("### Pendapatan Total Berdasarkan Metode Pembayaran")
    payment_revenue = final_all_df.groupby('payment_type')['price'].sum()
    for payment_type, revenue in payment_revenue.items():
        st.write(f"- **{payment_type}**: Total Transaksi $ {revenue:,.2f}")

# 4. Tren Penjualan Bulanan
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("Bagaimana total penjualan produk dari waktu ke waktu?")

final_all_df['order_purchase_timestamp'] = pd.to_datetime(final_all_df['order_purchase_timestamp'])
sales_trend = final_all_df.set_index('order_purchase_timestamp').resample('ME')['price'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
sales_trend.plot(color='orange', marker='o', ax=ax)
ax.set_title('Tren Total Penjualan Bulanan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penjualan')
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# 5. Segmentasi Pelanggan
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.subheader("Segmentasi Pelanggan Berdasarkan Nilai Total Transaksi Pembayaran")

customer_total_payment = final_all_df.groupby('customer_id')['payment_value'].sum()

def categorize_spending(payment_value):
    if payment_value > 200:
        return 'High Spend'
    elif payment_value >= 100:
        return 'Medium Spend'
    else:
        return 'Low Spend'

customer_payment_grouped = customer_total_payment.apply(categorize_spending)
final_all_df['payment_group'] = final_all_df['customer_id'].map(customer_payment_grouped)
group_distribution = final_all_df['payment_group'].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
group_distribution.plot(kind='barh', color=['lightcoral', 'gold', 'lightskyblue'], ax=ax)
ax.set_title('Distribusi Pengelompokan Pelanggan Berdasarkan Nilai Total Transaksi Pembayaran')
ax.set_xlabel('Jumlah Pelanggan')
ax.set_ylabel('Nilai Transaksi Yang Dibayar')
st.pyplot(fig)
