import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import scipy as sc
from babel.numbers import format_currency

sns.set(style='dark')

# Menyiapkan Daily_User_Df
def create_daily_user_df(df):
    daily_user_df = pengguna_bulanan_day = df.resample(rule='D', on='dteday').agg({
    'yr': 'unique',
    'cnt': 'sum'
    })
    daily_user_df = daily_user_df.reset_index()
    daily_user_df.rename(columns={
        "yr": "tahun",
        "cnt": "total_pengguna"
    }, inplace=True)
    
    return daily_user_df
    
# Menyiapkan Season_Df
def create_season_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=False).reset_index()
    return season_df

# Menyiapkan Weather_Df:
def create_weather_df(df):
    weather_df = df.groupby(by=["weathersit","yr"]).agg({
    "cnt": "sum"
    }).sort_values(by="cnt",ascending=False).reset_index()
    return weather_df

# Menyiapkan Tipe_Df
def create_tipe_df(df):
    tipe_df = df.groupby(by="yr").agg({
    "casual": "sum",
    "registered": "sum"
    }).sort_values(by=["casual", "registered"], ascending=False).reset_index()
    return tipe_df

# Menyiapkan Hari_Df
def create_hari_df(df):
    hari_df = df.groupby(by="weekday").agg({
    "cnt": "sum"
    }).sort_values(by="cnt", ascending=False).reset_index()
    return hari_df

# Menyiapkan Jam_Df
def create_jam_df(df):
    jam_df = df.groupby(by="hr").agg({
    "cnt": "sum"
    }).sort_values(by="cnt", ascending=False).reset_index()
    return jam_df

#Load Data CSV
day_clean = pd.read_csv("day_clean.csv")
hour_clean = pd.read_csv("hour_clean.csv")

# mengurutkan DataFrame berdasarkan tanggan (dteday) serta memastikan kolom tersebut bertipe datetime
datetime_columns = ["dteday"]
day_clean.sort_values(by="dteday", inplace=True)
day_clean.reset_index(inplace=True)

datetime_columns = ["dteday"]
hour_clean.sort_values(by="dteday", inplace=True)
hour_clean.reset_index(inplace=True)

for column in datetime_columns:
    day_clean[column] = pd.to_datetime(day_clean[column])
    hour_clean[column] = pd.to_datetime(hour_clean[column])

# Membuat Komponen Filter
min_date = day_clean["dteday"].min()
max_date = day_clean["dteday"].max()

with st.sidebar:
    # Menambahkan logo website
    st.image("https://media.tenor.com/Qc90hq71WI4AAAAM/cycling-bicycle.gif")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

     # Memilih jenis data
    selected_data = st.radio("Pilih Jenis Data", ["Day (Harian)", "Hour (Per-Jam)"])


# Untuk day_clean
main_df_day = day_clean[(day_clean["dteday"] >= str(start_date)) & 
                        (day_clean["dteday"] <= str(end_date))]

# Untuk hour_clean
main_df_hour = hour_clean[(hour_clean["dteday"] >= str(start_date)) & 
                          (hour_clean["dteday"] <= str(end_date))]

# Me-Load Fungsi Yang Telah Dibuat
daily_user_df = create_daily_user_df(main_df_day)
season_df = create_season_df(main_df_day)
weather_df = create_weather_df(main_df_day)
tipe_df = create_tipe_df(main_df_day)
hari_df = create_hari_df(main_df_day)

# Lakukan hal yang sama untuk hour_clean
daily_user_df_hour = create_daily_user_df(main_df_hour)
season_df_hour = create_season_df(main_df_hour)
weather_df_hour = create_weather_df(main_df_hour)
tipe_df_hour = create_tipe_df(main_df_hour)
jam_df_hour = create_jam_df(main_df_hour)

# Menampilkan DataFrame berdasarkan pilihan pengguna
if selected_data == "Day (Harian)":
    selected_df = main_df_day
else:
    selected_df = main_df_hour

st.header('Proyek Analisis Bike Sharing')

# Membuat Grafik Musim (Season)
st.subheader('Demografi Musim')

col1, col2 = st.columns(2)

with col1:
    jumlah_musim = selected_df.season.nunique()
    st.metric("Jumlah Musim", value=jumlah_musim)
 
with col2:
    jumlah_pengguna = selected_df.cnt.sum()
    st.metric("Total Jumlah Pengguna", value=jumlah_pengguna)

fig, ax = plt.subplots(figsize=(30, 20))
season_order = selected_df.groupby('season')['cnt'].sum().sort_values(ascending=False).index
sns.barplot(data=selected_df, x='season', y='cnt', hue='yr',order=season_order, errorbar=None)
for p in plt.gca().patches:
    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='baseline', fontsize=30, color='black', xytext=(5, 10),
                 textcoords='offset points')
ax.set_title("Grafik Penggunaan Per-Musim (Season)", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=50)
ax.tick_params(axis='x', labelsize=50)
ax.legend(fontsize=30)
st.pyplot(fig)

# Membuat Grafik Cuaca (Weathersit)
st.subheader('Demografi Cuaca')

col1, col2 = st.columns(2)

with col1:
    jumlah_musim = selected_df.weathersit.nunique()
    st.metric("Jumlah Cuaca", value=jumlah_musim)
 
with col2:
    jumlah_pengguna = selected_df.cnt.sum()
    st.metric("Total Jumlah Pengguna", value=jumlah_pengguna)

fig, ax = plt.subplots(figsize=(30, 20))
weathersit_order = selected_df.groupby('weathersit')['cnt'].sum().sort_values(ascending=False).index
sns.barplot(data=selected_df, x='weathersit', y='cnt', hue='yr',order=weathersit_order, errorbar=None)
for p in plt.gca().patches:
    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='baseline', fontsize=30, color='black', xytext=(0, 5),
                 textcoords='offset points')
ax.set_title("Grafik Penggunaan Berdasarkan Cuaca (Weathersit)", loc="center", fontsize=40)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=50)
ax.tick_params(axis='x', labelsize=50)
ax.legend(fontsize=30)
st.pyplot(fig)


# Membuat Grafik Tipe (Registered & Casual)
if selected_data == "Day (Harian)":
    selected_df = main_df_day
    st.subheader('Demografi Tipe Pengguna')

    tipe_df.set_index('yr', inplace=True)
    tipe_df = tipe_df.reset_index().melt(id_vars=['yr'], var_name='Type', value_name='Total')
    tipe_df = tipe_df.sort_values(by='Total', ascending=False)

    fig, ax = plt.subplots(figsize=(30, 20))
    sns.barplot(data=tipe_df, x='yr', y='Total', hue='Type', palette='pastel')
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=30, color='black', xytext=(0, 5),
                     textcoords='offset points')
    ax.set_title("Grafik Penggunaan Berdasarkan Tipe", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=50)
    ax.legend(fontsize=30)
    st.pyplot(fig)
else:
    selected_df = main_df_hour
    st.subheader('Demografi Tipe Pengguna')

    tipe_df_hour.set_index('yr', inplace=True)
    tipe_df_hour = tipe_df_hour.reset_index().melt(id_vars=['yr'], var_name='Type', value_name='Total')
    tipe_df_hour = tipe_df_hour.sort_values(by='Total', ascending=False)

    fig, ax = plt.subplots(figsize=(30, 20))
    sns.barplot(data=tipe_df_hour, x='yr', y='Total', hue='Type', palette='pastel')
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=30, color='black', xytext=(0, 5),
                     textcoords='offset points')
    ax.set_title("Grafik Penggunaan Berdasarkan Tipe", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=50)
    ax.legend(fontsize=30)
    st.pyplot(fig)

# Membuat Grafik Hari (Untuk Data day_df) dan Jam (Untuk Data hour_df)
if selected_data == "Day (Harian)":
    selected_df = main_df_day
    st.subheader('Demografi Jumlah Pengguna Berdasarkan Hari')

    fig, ax = plt.subplots(figsize=(30, 20))
    weekday_order = hari_df.groupby('weekday')['cnt'].sum().sort_values(ascending=False).index
    sns.barplot(data=hari_df, x='weekday', y='cnt',order=weekday_order, palette='pastel', errorbar=None)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=30, color='black', xytext=(0, 5),
                     textcoords='offset points')
    ax.set_title("Grafik Penggunaan Berdasarkan Hari", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=50)
    ax.legend(fontsize=30)
    st.pyplot(fig)


else:
    selected_df = main_df_hour
    st.subheader('Demografi Jumlah Pengguna Berdasarkan Jam')

    fig, ax = plt.subplots(figsize=(30, 20))
    hour_order = jam_df_hour.groupby('hr')['cnt'].sum().index
    sns.barplot(data=jam_df_hour, x='hr', y='cnt',order=hour_order, palette='pastel', errorbar=None)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=30, color='black', xytext=(0, 5),
                     textcoords='offset points')
    ax.set_title("Grafik Penggunaan Berdasarkan Jam", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=50)
    ax.legend(fontsize=30)
    st.pyplot(fig)


# Membuat Grafik Line Chart Berdasarkan Tanggal
st.subheader('Daily Users')
 
col1, col2 = st.columns(2)
 
with col1:
    jumlah_hari = selected_df.dteday.nunique()
    st.metric("Jumlah Hari", value=jumlah_hari)
 
with col2:
    jumlah_pengguna = selected_df.cnt.sum()
    st.metric("Total Jumlah Pengguna", value=jumlah_pengguna)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    selected_df["dteday"],
    selected_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.markdown('<style>div.Widget.caption span{align:center !important;}</style>', unsafe_allow_html=True)
st.caption(':blue[Copyright (c) Arif Budiman 2023]')
