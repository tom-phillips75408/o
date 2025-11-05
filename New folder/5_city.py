# Lab Assignment - 5
# Problem Statement: Write a program for performing industrial data analysis using relevant tools and techniques.

# Step 1 : Import Required Libraries
import os
import warnings
warnings.filterwarnings('ignore')
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Step 2 : Load data and brief inspection
df = pd.read_csv('/content/City_Types.csv')

print(df.head())
print(df.shape)
print(df.info())
print(df.describe(include=[np.number]).T)

# Step 3 : Handle missing values
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
possible_date_cols = [c for c in cat_cols if 'date' in c.lower() or 'time' in c.lower()]

for c in possible_date_cols:
    df[c] = pd.to_datetime(df[c], errors='coerce')

for c in num_cols:
    df[c].fillna(df[c].median(), inplace=True)

for c in cat_cols:
    df[c].fillna(df[c].mode()[0], inplace=True)

# Step 4 : Remove duplicate records
df.drop_duplicates(inplace=True)

# Step 5 : Standardize inconsistent categorical data
def clean_string(s):
    if pd.isna(s):
        return s
    return ' '.join(str(s).strip().split()).lower()

for c in cat_cols:
    df[c] = df[c].apply(clean_string)

# Convert remaining date-like columns
for c in cat_cols:
    if any(x in c.lower() for x in ['date', 'time']):
        df[c] = pd.to_datetime(df[c], errors='coerce')

# Step 6 : Identify and handle outliers (IQR) and visualize
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

n = len(num_cols)
cols = 3
rows = math.ceil(n / cols)
plt.figure(figsize=(5*cols, 4*rows))

for i, c in enumerate(num_cols, 1):
    Q1, Q3 = df[c].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    df[c] = np.where(df[c] < lower, lower, df[c])
    df[c] = np.where(df[c] > upper, upper, df[c])

    plt.subplot(rows, cols, i)
    sns.boxplot(x=df[c])
    plt.title(f'Boxplot for {c}', fontsize=10)

plt.tight_layout()
plt.show()

# Step 7 : Correlation heatmap
corr = df.corr(numeric_only=True)
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Step 8 : Feature impact on air quality
possible_targets = [c for c in df.columns if any(k in c.lower() for k in ['air', 'aqi', 'pollut', 'pm'])]
target = possible_targets[0] if possible_targets else None

if target:
    numeric_df = df.select_dtypes(include=[np.number])
    corrs = numeric_df.corr()[target].drop(target).sort_values(key=lambda s: s.abs(), ascending=False)
    print(corrs.head())

    X = numeric_df.drop(columns=[target])
    y = numeric_df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(random_state=42)
    rf.fit(X_train, y_train)

    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    importances.head(10).plot(kind='bar')
    plt.title('Feature Importance for Air Quality')
    plt.show()

# Step 9 : City with highest air pollution
city_col = [c for c in df.columns if 'city' in c.lower()]
if city_col and target:
    city_pollution = df.groupby(city_col[0])[target].mean().sort_values(ascending=False)
    print(city_pollution.head())
    city_pollution.head(10).plot(kind='bar')
    plt.title('Top Cities by Air Pollution')
    plt.ylabel(target)
    plt.show()

# Step 10 : Type effect on city pollution
type_col = [c for c in df.columns if 'type' in c.lower()]
if type_col and target:
    type_effect = df.groupby(type_col[0])[target].mean().sort_values(ascending=False)
    print(type_effect)
    type_effect.plot(kind='bar')
    plt.title('Air Quality by City Type')
    plt.ylabel(target)
    plt.show()

# Step 11 : Calculate average air quality metrics for each city type
average_pollution_by_type = df.groupby('Type')[['CO', 'NO2', 'SO2', 'O3', 'PM2.5', 'PM10']].mean()
display(average_pollution_by_type)

# Step 12 : Create a bar plot showing average air quality metrics for each city type
average_pollution_by_type.plot(kind='bar', figsize=(12, 7))
plt.title('Average Air Quality Metrics by City Type')
plt.ylabel('Average Concentration')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()
