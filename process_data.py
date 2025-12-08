import pandas as pd
import os

# Path to the data directory
data_path = './data'

# Get a list of all CSV files in the data directory
all_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith('.csv')]

# Read and concatenate all files
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
 
# Display info of the combined dataframe
print("Combined DataFrame Info:")
df.info()
 
print("\nA few rows of the combined data:")
print(df.head())


print("\nProcessing data...")

# Filter for "Pink Morsel"
df = df[df['product'] == 'Pink Morsel']

# Calculate the 'sales' column
df['sales'] = df['quantity'] * df['price']

# Select the final columns
final_df = df[['sales', 'date', 'region']]
 
print("Processed DataFrame head:")
print(final_df.head())

print("\nProcessed DataFrame Info:")
final_df.info()


# Save the processed data to a new CSV file
output_file_name = 'processed_sales_data.csv'
final_df.to_csv(output_file_name, index=False)

print(f"\nProcessed data saved to {output_file_name}")
 
# Optional: Display the first few rows of the saved file to verify
print(f"\nVerifying the first few rows of {output_file_name}:")
verified_df = pd.read_csv(output_file_name)
print(verified_df.head())
