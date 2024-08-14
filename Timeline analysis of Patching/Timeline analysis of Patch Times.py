# %% [markdown]
# This file is part of Google Zero Day In the Wild Security Vulnerabilities Analysis Project. 
# This script aims to analyze the time taken from the discovery of a vulnerability to its patching across different vendors. Identify which vendors are quicker or slower in addressing security issues.


# Required Imports

# %%
import pandas as pd
import  matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# %% [markdown]
# Data Preaparation and Data Cleaning

# %%
df = pd.read_csv('/Users/samir/Documents/GitHub/Google-Zero-Day-in-the-Wild-/0day _In the Wild_ - All.csv')
df.head()

# %% [markdown]
# Checking Null Values and droping rows where 'Date Discovered'values are missing.

# %%
missing_values = df.isnull().sum()
missing_values


# %%
df_cleaned = df.dropna(subset=['Date Discovered'])
df_cleaned.isnull().sum()
df_cleaned['Date Discovered'] = pd.to_datetime(df_cleaned['Date Discovered'], errors='coerce')
df_cleaned['Date Patched'] = pd.to_datetime(df_cleaned['Date Patched'], errors='coerce')
df_cleaned['Date Discovered']

# %% [markdown]
# Creating a new Column: Time to Patch(Days); and calculating it.

# %%
df_cleaned['Time to Patch (Days)'] = (df_cleaned['Date Patched'] - df_cleaned['Date Discovered']).dt.days

# Filtering out entries where the 'Time to Patch' is negative or null
final_data = df_cleaned[(df_cleaned['Time to Patch (Days)'] >= 0) & (df_cleaned['Time to Patch (Days)'].notnull())]

# Displaying the updated dataframe
final_data[['Vendor', 'Product', 'Time to Patch (Days)']].head()

# %% [markdown]
# Calculating Average Patch Time per Vendor

# %%
# Calculating the average patch time per vendor
average_patch_time_per_vendor = final_data.groupby('Vendor')['Time to Patch (Days)'].mean().sort_values()
plt.figure(figsize=(12, 8))
plt.barh(average_patch_time_per_vendor.index, average_patch_time_per_vendor.values, color='skyblue')
plt.title('Average Patch Time by Vendor')
plt.xlabel('Average Time to Patch (Days)')
plt.ylabel('Vendor')
plt.show()

# %% [markdown]
# Distribution of patch times for each Vendor.

# %%
# Calculating the distribution of patch times for each vendor
patch_time_distribution_per_vendor = final_data.groupby('Vendor')['Time to Patch (Days)'].describe()
plt.figure(figsize=(12, 8))

sns.stripplot(x='Vendor', y='Time to Patch (Days)', data=final_data, jitter=True, dodge=True, marker='o', alpha=0.6)
plt.title('Distribution of Patch Times per Vendor')
plt.xlabel('Vendor')
plt.ylabel('Time to Patch (Days)')
plt.yscale('log')
plt.xticks(rotation=45, ha='right')
plt.show()

# %% [markdown]
# Checking if certain vulnerabilities take longer than expected patch times.

# %%
# Vulnerabilities and their Patch times in days
patch_time_by_type = final_data.groupby('Type')['Time to Patch (Days)'].mean().sort_values()
plt.figure(figsize=(12, 8))
plt.barh(patch_time_by_type.index, patch_time_by_type.values, color='lightcoral')
plt.title('Average Patch Time by Vulnerability Type')
plt.xlabel('Average Time to Patch (Days)')
plt.ylabel('Vulnerability Type')
plt.show()



