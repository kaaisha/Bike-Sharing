#import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("default")

#load data
all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
#sidebar
with st.sidebar:
    st.title('Bike Sharing Population')
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    year_list = list(all_df.dteday.unique())[::-1]
    selected_year = st.selectbox('Pilih tahun', year_list)
    selected_year_df = all_df[all_df == selected_year]
    selected_year_sorted_df = all_df.sort_values(by="dteday", ascending=False)
main_df = all_df[(all_df["dteday"] >= str(start_date)) &
(all_df["dteday"] <= str(end_date))]


#chart 1
st.markdown("<h1 style='text-align: center;'>Bike Sharing Dashboard</h1>", unsafe_allow_html=True)
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Musim')
fig = plt.figure(figsize=(10, 6))
p = sns.barplot(x='season_x', y='cnt_x', data=all_df, palette='Spectral', estimator=sum)
plt.title('Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
total = all_df['cnt_x'].sum()
for patch in p.patches:
    percentage = patch.get_height() / total * 100
    p.annotate(f'{percentage:.2f}%', 
               (patch.get_x() + patch.get_width() / 2., patch.get_height()), 
               ha='center', va='center', xytext=(0, 5), textcoords='offset points')
st.pyplot(fig)

#chart 2
st.subheader('Hubungan antara cuaca dan jumlah penyewaan sepeda')
fig = plt.figure(figsize=(10, 6))
p = sns.barplot(x='weathersit_x', y='cnt_x', data=all_df, palette='coolwarm', estimator=sum)
plt.title('Peyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
total = all_df['cnt_x'].sum()
for patch in p.patches:
    percentage = patch.get_height() / total * 100
    p.annotate(f'{percentage:.2f}%',
               (patch.get_x() + patch.get_width() / 2., patch.get_height()),
               ha='center', va='center', xytext=(0, 5), textcoords='offset points')
st.pyplot(fig)

#chart 3
st.subheader('Hubungan antara musim dn kondisi cuaca terhadap jumlah penyewa sepeda')
cat_plot = sns.catplot(x='season_x', y='cnt_x', hue='weathersit_x', data=all_df, kind='bar', palette='Set2', estimator=sum, height=6, aspect=2)
fig = sns.catplot(x='season_x', y='cnt_x', hue='weathersit_x', data=all_df, kind='bar', 
                       palette='Set2', estimator=sum, height=6, aspect=2)
plt.title('Penyewaan Sepeda Berdasarkan Kombinasi Musim dan Kondisi Cuaca')
plt.xlabel('Musim')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
ax = cat_plot.ax
total = all_df['cnt_x'].sum()
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:
            percentage = height / total
            ax.annotate(f'{percentage:.2%}',
                        (bar.get_x() + bar.get_width() / 2., height),
                        ha='center', va='center',
                        xytext=(0, 6), textcoords='offset points', fontsize=8)
st.pyplot(cat_plot.fig)

#chart 4
st.subheader('Jumlah penyewa sepeda dari tahun ke tahun')
monthly_usage = all_df.groupby(['yr_x', 'mnth_x'])['cnt_x'].sum().reset_index()
monthly_usage['mnth_x'] = monthly_usage['mnth_x'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
fig = plt.figure(figsize=(12, 6))
sns.lineplot(x='mnth_x', y='cnt_x', hue='yr_x', data=monthly_usage, marker='o', palette='Set1')
plt.title('Penyewaan Sepeda dari Tahun ke Tahun')
plt.xlabel('Bulan')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(rotation=45)
plt.legend(title='Tahun', labels=['2011', '2012'])
plt.tight_layout()
st.pyplot(fig)

