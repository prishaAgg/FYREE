import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv('Data.csv')

df3 = df[df.Group2 == "Onsite"].reset_index()
df4 = df3['Center'].value_counts().sort_index().reset_index()
df4.columns = ['Center', 'Count']


df5 = df[df.Group2 == "Tele"]
df6 = df5['Center'].value_counts().sort_index().reset_index()
df6.columns = ['Center', 'Count']

# Merge df4 and df6 on 'Center'
result_df = pd.merge(df4, df6, on='Center', how='left')
result_df = result_df.rename(columns={'Count_x': 'Onsite Count', 'Count_y': 'Tele Count'})
print(result_df)

providers = result_df['Center']
onsite_counts = result_df['Onsite Count']
tele_counts = result_df['Tele Count']

# Set the width of the bars
bar_width = 0.35

# Create index for the providers
ind = np.arange(len(providers))

# Create the double bar graph
fig, ax = plt.subplots()
onsite_bar = ax.bar(ind, onsite_counts, bar_width, label='Onsite')
tele_bar = ax.bar(ind + bar_width, tele_counts, bar_width, label='Tele')

# Set labels and title
ax.set_xlabel('Center')
ax.set_ylabel('Count')
ax.set_title('Onsite and Tele Counts by Center')
ax.set_xticks(ind + bar_width / 2)
ax.set_xticklabels(providers, rotation=45, ha='right')

# Add legend
ax.legend()

# Show the plot
plt.show()


# X contains features and y contains target counts
X1 = df3[['LeadDays', 'ProviderType']]  # Example features
X2 = df5[['LeadDays', 'ProviderType']]  # Example features
y_onsite = df4['Count']  # Target variable for Onsite counts
y_tele = df6['Count']  # Target variable for Tele counts

# Split the data into training and testing sets
X_train_onsite, X_test_onsite, y_train_onsite, y_test_onsite = train_test_split(X1, y_onsite, test_size=0.2, random_state=42)
X_train_tele, X_test_tele, y_train_tele, y_test_tele = train_test_split(X2, y_tele, test_size=0.2, random_state=42)

# Initialize and train the linear regression model for Onsite counts
model_onsite = LinearRegression()
model_onsite.fit(X_train_onsite, y_train_onsite)

# Make predictions for Onsite counts
predictions_onsite = model_onsite.predict(X_test_onsite)

# Evaluate the model for Onsite counts
mse_onsite = mean_squared_error(y_test_onsite, predictions_onsite)
print("Mean Squared Error for Onsite counts:", mse_onsite)

# Repeat the process for Tele counts
model_tele = LinearRegression()
model_tele.fit(X_train_tele, y_train_tele)
predictions_tele = model_tele.predict(X_test_tele)
mse_tele = mean_squared_error(y_test_tele, predictions_tele)
print("Mean Squared Error for Tele counts:", mse_tele)
