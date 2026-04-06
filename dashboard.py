import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# mengimport data
hour_df = pd.read_csv(r"C:\Users\slyth\Downloads\bike sharing project\bike_sharing_cleaned.csv")

# membuat judul
st.title('Bike Sharing Dashboard Analysis')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = hour_df.cnt.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    total_casual = hour_df.casual.sum()
    st.metric("Total Casual Customers", value=total_casual)

with col3:
    total_registered = hour_df.registered.sum()
    st.metric("Total Registered Customers", value=total_registered)

min_date = hour_df['dteday'].min()
max_date = hour_df['dteday'].max()

with st.sidebar:
    start_date, end_date =  st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )

tab1, tab2, tab3 = st.tabs(["Tren", "Pelanggan", "Penyewaan"])

# visualisasi tren penyewaan sepeda dari waktu ke waktu
with tab1:
    st.header("Grafik tren penyewaan sepeda dari waktu ke waktu")

    hour_df['dteday'] = pd.to_datetime(hour_df['dteday']) 

    total_rental = hour_df.groupby(by=hour_df['dteday'].dt.to_period("M")).agg({ 
        "casual": "sum", 
        "registered": "sum", 
        "cnt": "sum" }).reset_index() 
    total_rental['dteday'] = total_rental['dteday'].dt.to_timestamp()
    
    fig1, ax1 = plt.subplots(figsize=(12, 6)) 
    sns.lineplot(data=total_rental, x='dteday', y='cnt', marker='o', ax=ax1) 
    ax1.set_title('Tren Jumlah Penyewaan Sepeda dari Waktu ke Waktu (2011-2012)') 
    ax1.set_xlabel('Tanggal') 
    ax1.set_ylabel('Total Penyewaan') 
    ax1.grid(True) 
    
    st.pyplot(fig1)

# visualisasi perbandingan jumlah pelanggan casual vs registered
with tab2:
    st.header("Data banyaknya pelanggan casual vs registered")

    labels_pl = ['Casual', 'Registered']
    counts_pl = [hour_df['casual'].sum(), hour_df['registered'].sum()]
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=labels_pl, y=counts_pl, hue=labels_pl, palette='viridis', legend=False, ax=ax2)
    ax2.set_title('Perbandingan Jumlah Pelanggan Casual vs Registered')
    ax2.set_xlabel('Tipe Pelanggan')
    ax2.set_ylabel('Total Penyewaan')
    st.pyplot(fig2)

# visualisasi jumlah penyewaan sepeda berdasarkan hari kerja vs akhir pekan
with tab3:
    st.header("Jumlah penyewaan sepeda saat hari kerja vs akhir pekan")

    labels_day = ['Hari Kerja', 'Akhir Pekan']
    counts_day = [hour_df[hour_df['is_workingday'] == 1]['cnt'].sum(), hour_df[hour_df['is_workingday'] == 0]['cnt'].sum()]
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=labels_day, y=counts_day, hue=labels_day, palette='viridis', legend=False, ax=ax3)
    ax3.set_title('Perilaku Pelanggan Penyewaan Sepeda berdasarkan Hari Kerja vs Akhir Pekan')
    ax3.set_xlabel('Tipe Hari')
    ax3.set_ylabel('Total Penyewaan')
    st.pyplot(fig3) 

# visualisasi jumlah penyewaan sepeda berdasarkan musim
with tab3:
    st.header("Jumlah penyewaan sepeda berdasarkan musim")

    labels_ss = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    counts_ss = [hour_df[hour_df['season'] == 1]['cnt'].sum(),
          hour_df[hour_df['season'] == 2]['cnt'].sum(),
          hour_df[hour_df['season'] == 3]['cnt'].sum(),
          hour_df[hour_df['season'] == 4]['cnt'].sum()]
    
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=labels_ss, y=counts_ss, hue=labels_ss, palette='viridis', legend=False, ax=ax4)
    ax4.set_title('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Musim')
    ax4.set_xlabel('Musim')
    ax4.set_ylabel('Total Penyewaan')
    st.pyplot(fig4)

# visualisasi analisis lanjutan
with tab2:
    st.header("Data banyaknya pelanggan berdasarkan kondisi cuaca")
    
    labels_cc = ['Cuaca Cerah', 'Cuaca Berawan', 'Cuaca Hujan', 'Cuaca Badai']
    counts_cc = [hour_df[hour_df['weathersit'] == 1]['cnt'].sum(),
                 hour_df[hour_df['weathersit'] == 2]['cnt'].sum(),
                 hour_df[hour_df['weathersit'] == 3]['cnt'].sum(),
                 hour_df[hour_df['weathersit'] == 4]['cnt'].sum()]
        
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=labels_cc, y=counts_cc, hue=labels_cc, palette='coolwarm', legend=False, ax=ax5)
    ax5.set_title('Perbandingan total jumlah penyewaan sepeda berdasarkan kondisi cuaca', fontsize=18)
    ax5.set_xlabel(None)
    ax5.set_ylabel('Jumlah Penyewaan', fontsize=14)
    ax5.tick_params(axis='both', labelsize=12)

    plt.tight_layout()
    st.pyplot(fig5)

    st.header('Data banyaknya pelanggan berdasarkan kondisi suhu')

    labels_sh = ['Very Cold', 'Cold', 'Mild', 'Warm', 'Hot']
    counts_sh = [hour_df[hour_df['temp_category'] == 'Very Cold']['cnt'].sum(),
                    hour_df[hour_df['temp_category'] == 'Cold']['cnt'].sum(),
                    hour_df[hour_df['temp_category'] == 'Mild']['cnt'].sum(),
                    hour_df[hour_df['temp_category'] == 'Warm']['cnt'].sum(),
                    hour_df[hour_df['temp_category'] == 'Hot']['cnt'].sum()]
    
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=labels_sh, y=counts_sh, hue=labels_sh, palette='viridis', legend=False, ax=ax6)
    ax6.set_title('Perbandingan total jumlah penyewaan sepeda berdasarkan suhu', fontsize=18)
    ax6.set_xlabel(None)
    ax6.set_ylabel('Jumlah Penyewaan', fontsize=14)
    ax6.tick_params(axis='both', labelsize=12)

    plt.tight_layout()
    st.pyplot(fig6)