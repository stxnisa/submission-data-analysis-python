import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_hour = pd.read_csv('/content/hour.csv')
df_daily = pd.read_csv('/content/day.csv')

df_hour.head()

df_hour.info()

df_hour.describe()

df_daily.head()

df_daily.info()

df_daily.describe()

df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

df_hour.isnull().sum()

df_daily['dteday'] = pd.to_datetime(df_daily['dteday'])

df_daily.isnull().sum()

hourly_agg = df_hour.groupby('dteday').agg({
    'season': 'first',
    'yr': 'first',
    'mnth': 'first',
    'holiday': 'first',
    'weekday': 'first',
    'workingday': 'first',
    'weathersit': 'mean',  # Mean weather situation over the day
    'temp': 'mean',  # Average temperature
    'atemp': 'mean',  # Average feeling temperature
    'hum': 'mean',  # Average humidity
    'windspeed': 'mean',  # Average wind speed
    'casual': 'sum',  # Total casual users
    'registered': 'sum',  # Total registered users
    'cnt': 'sum'  # Total bike rentals
}).reset_index()

df = pd.merge(df_daily, hourly_agg, on='dteday', suffixes=('_daily', '_hourly'))

df.head()

df.describe()

df.corr()

st.title("Bike Sharing Data Analysis")

st.subheader("Question 1: Total Rentals Over Time (Daily)")

st.write("Visualizing the total number of bike rentals over time on a daily basis.")
fig, ax = plt.subplots()
sns.lineplot(data=df, x='dteday', y='cnt_daily', ax=ax)
ax.set_title('Total Rentals Over Time (Daily)')
st.pyplot(fig)

st.subheader("Question 2: Impact of Weather Conditions on Rentals")

st.write("Visualizing rentals by season.")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='season_daily', y='cnt_daily', ax=ax)
ax.set_title('Rentals by Season (Daily)')
st.pyplot(fig)

st.write("Visualizing rentals by weather situation.")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='weathersit_daily', y='cnt_daily', ax=ax)
ax.set_title('Rentals by Weather Situation (Daily)')
st.pyplot(fig)

st.write("Visualizing rentals vs temperature.")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='temp_daily', y='cnt_daily', ax=ax)
ax.set_title('Rentals vs Temperature (Daily)')
st.pyplot(fig)

st.write("Visualizing rentals vs humidity.")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='hum_daily', y='cnt_daily', ax=ax)
ax.set_title('Rentals vs Humidity (Daily)')
st.pyplot(fig)

st.header("Rentals vs Wind Speed (Daily)")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='windspeed_daily', y='cnt_daily', ax=ax)
ax.set_title('Rentals vs Wind Speed (Daily)')
st.pyplot(fig)
