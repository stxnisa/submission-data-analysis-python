import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Data Gathering
# Assuming 'hour.csv' and 'day.csv' are in the current working directory
hourly_data = pd.read_csv('hour.csv')
daily_data = pd.read_csv('day.csv')

# Step 2: Data Assessing and Cleaning
# Check for any missing values or data quality issues
print("Hourly Data Info:")
print(hourly_data.info())
print("\nDaily Data Info:")
print(daily_data.info())

# Step 3: Data Cleaning and Preparation
# Convert date columns to datetime format
hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

# Step 4: Data Wrangling - Merging Datasets
# Aggregate hourly data to daily level
hourly_aggregated = hourly_data.groupby('dteday').agg({
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

# Merge the daily dataset with the aggregated hourly data
merged_data = pd.merge(daily_data, hourly_aggregated, on='dteday', suffixes=('_daily', '_hourly'))

# Step 5: Data Analysis - Exploratory Analysis
# Plotting relationships between variables
fig, axs = plt.subplots(3, 2, figsize=(15, 15))

sns.lineplot(data=merged_data, x='dteday', y='cnt_daily', ax=axs[0, 0])
axs[0, 0].set_title('Total Rentals Over Time (Daily)')

sns.boxplot(data=merged_data, x='season_daily', y='cnt_daily', ax=axs[0, 1])
axs[0, 1].set_title('Rentals by Season (Daily)')

sns.boxplot(data=merged_data, x='weathersit_daily', y='cnt_daily', ax=axs[1, 0])
axs[1, 0].set_title('Rentals by Weather Situation (Daily)')

sns.scatterplot(data=merged_data, x='temp_daily', y='cnt_daily', ax=axs[1, 1])
axs[1, 1].set_title('Rentals vs Temperature (Daily)')

sns.scatterplot(data=merged_data, x='hum_daily', y='cnt_daily', ax=axs[2, 0])
axs[2, 0].set_title('Rentals vs Humidity (Daily)')

sns.scatterplot(data=merged_data, x='windspeed_daily', y='cnt_daily', ax=axs[2, 1])
axs[2, 1].set_title('Rentals vs Wind Speed (Daily)')

plt.tight_layout()
plt.show()

# Step 6: Additional Analysis - Event Analysis Example
# Example: Hurricane Sandy Analysis
event_date = pd.to_datetime('2012-10-30')

# Extract the data for the event and the surrounding days
event_data = merged_data[merged_data['dteday'].isin([event_date - pd.Timedelta(days=1), event_date, event_date + pd.Timedelta(days=1)])]

# Compare the rental counts on the event day with the days before and after
print(event_data[['dteday', 'cnt_daily']])

# Plot the comparison
sns.barplot(data=event_data, x='dteday', y='cnt_daily')
plt.title('Bike Rentals Around Hurricane Sandy')
plt.xlabel('Date')
plt.ylabel('Total Rentals')
plt.show()
