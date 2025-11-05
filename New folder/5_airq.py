# Practical 5 – Data Visualization using matplotlib

# Import Required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
try:
    df = pd.read_csv('/content/AirQuality.csv', sep=';', decimal=',')
except FileNotFoundError:
    print("Make sure the 'AirQuality.csv' file is in the same directory as your script.")
    exit()

# Preprocessing the data
# Drop empty columns that might be at the end of the file
df = df.dropna(axis=1, how='all')

# Clean up rows that are completely empty before processing
df.dropna(how='all', inplace=True)

# Ensure the column is treated as a string before replacing
df['Time'] = df['Time'].astype(str).str.replace('.', ':', regex=False)

# Combine 'Date' and 'Time' into a single datetime column with the correct format
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')

# Set the new 'DateTime' column as the index
df.set_index('DateTime', inplace=True)

# Drop the original 'Date' and 'Time' columns
df.drop(['Date', 'Time'], axis=1, inplace=True)

# Replace the placeholder -200 with NaN (Not a Number) to represent missing values
df.replace(to_replace=-200, value=np.nan, inplace=True)

# Exploring the dataset
print("Dataset Information:")
df.info()

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nDescriptive Statistics:")
print(df.describe())

# Create a line plot for CO(GT) concentration over time
plt.figure(figsize=(15, 7))
plt.plot(df.index, df['CO(GT)'], label='CO(GT)', color='blue')
plt.title('CO Concentration Trend Over Time')
plt.xlabel('Date')
plt.ylabel('CO Concentration (mg/m^3)')
plt.legend()
plt.grid(True)
plt.show()

# Create subplots for individual pollutants
fig, axes = plt.subplots(4, 1, figsize=(15, 20), sharex=True)

# Plot for CO(GT)
axes[0].plot(df.index, df['CO(GT)'], label='CO(GT)', color='blue')
axes[0].set_title('CO (GT) Concentration')
axes[0].set_ylabel('mg/m^3')
axes[0].legend()
axes[0].grid(True)

# Plot for C6H6(GT)
axes[1].plot(df.index, df['C6H6(GT)'], label='C6H6(GT)', color='green')
axes[1].set_title('Benzene (C6H6) Concentration')
axes[1].set_ylabel('µg/m^3')
axes[1].legend()
axes[1].grid(True)

# Plot for NOx(GT)
axes[2].plot(df.index, df['NOx(GT)'], label='NOx(GT)', color='red')
axes[2].set_title('NOx (GT) Concentration')
axes[2].set_ylabel('ppb')
axes[2].legend()
axes[2].grid(True)

# Plot for NO2(GT)
axes[3].plot(df.index, df['NO2(GT)'], label='NO2(GT)', color='purple')
axes[3].set_title('NO2 (GT) Concentration')
axes[3].set_xlabel('Date')
axes[3].set_ylabel('µg/m^3')
axes[3].legend()
axes[3].grid(True)

plt.tight_layout()
plt.show()

# Create a bar plot
daily_co = df['CO(GT)'].resample('D').mean()
plt.figure(figsize=(15, 7))
daily_co.head(30).plot(kind='bar', color='skyblue')
plt.title('Average Daily CO Concentration (First 30 Days)')
plt.xlabel('Date')
plt.ylabel('Average CO (mg/m^3)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# Create the box plot
pollutants = df[['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']]
plt.figure(figsize=(12, 8))
pollutants.boxplot()
plt.title('Distribution of Pollutant Concentrations')
plt.ylabel('Concentration')
plt.xticks(rotation=45)
plt.show()

# Create a scatter plot (duplicated section, corrected below)
plt.figure(figsize=(12, 8))
plt.scatter(df['CO(GT)'], df['C6H6(GT)'], color='orange', alpha=0.6)
plt.title('Scatter Plot: CO(GT) vs C6H6(GT)')
plt.xlabel('CO(GT)')
plt.ylabel('C6H6(GT)')
plt.grid(True)
plt.show()
