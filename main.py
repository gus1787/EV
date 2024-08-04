import time
start_time = time.time()

import os
import numpy as np
import pandas as pd
import sqlalchemy
import sqlite3
import datetime



# Get the directory where the current script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_directory)

# Verify the current working directory
print("Current working directory:", os.getcwd())

# Create a new directory based on the current timestamp
timestamp = datetime.datetime.now().strftime("%m_%d_%Y")
output_dir = f'Data_{timestamp}'
os.makedirs(output_dir, exist_ok=True)

# List all CSV files in the current directory
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
print(csv_files)


for file in csv_files:
    # Read the CSV file
    df = pd.read_csv(file)
    # Perform operations on the DataFrame
    print(f"Contents of {file}:")
    print(df)

    value_counts = df['region'].value_counts()
print(value_counts)

columns = df.columns
print("Column names:", columns)

for column in df.columns:
    print(f"Column: {column}")                          
    print(df[column].unique())
    print()
    
print(df.head())

# Order the DataFrame by 'year' (desc) and 'powertrain' (asc)
df = df.sort_values(by=[ 'powertrain','year'], ascending=[False, True])

# Get unique values in the 'Condition' column
Country_parameter = df[['parameter', 'region']].drop_duplicates()

# # Create a file for each unique value
# for _,row in parameter:
#     filtered_df = df[df['parameter'] == parameter]
#     filename = f"data_{parameter}.csv"
#     filtered_df.to_csv(filename, index=False)
#     print(f"File created: {filename}")

# Create a file for each unique combination and print the filenames
for _, row in Country_parameter.iterrows():
    parameter, region = row['parameter'], row['region']
    filtered_df = df[(df['parameter'] == parameter) & (df['region'] == region)]
    filename = f"data_{parameter}_{region}.csv"
    filepath = os.path.join(output_dir, filename)
    filtered_df.to_csv(filepath, index=False)
    print(f"File created: {filename}")

inc = 0

print(f"\nFiles in the directory {output_dir}:")
for file in os.listdir(output_dir):
    print(file)
    inc += 1

dfs = []

# Read each CSV file and append it to the list
for file in os.listdir(output_dir):
    if file.endswith('.csv'):
        filepath = os.path.join(output_dir, file)
        df1 = pd.read_csv(filepath)
        dfs.append(df1)

# Concatenate all DataFrames
combined_df = pd.concat(dfs, ignore_index=True)

# Optionally, save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_data.csv', index=False)

print(combined_df)

#checking for same data
concat_df = pd.concat([combined_df,df ])


# Using len() function
row_count_len = len(df)
print(f"Row count using len(): {row_count_len}")

print(df)
# Using len() function
row_count_len_combined_df = len(combined_df)
print(f"Row count using len(): {row_count_len_combined_df}")

# Using len() function
row_count_len_combined_concat_df = len(concat_df)
print(f"Row count using len(): {row_count_len_combined_concat_df}")

# Using shape attribute
row_count = df.shape[0]
print(f"Row count using shape: {row_count}")

no_dupes = concat_df.drop_duplicates()
print(no_dupes)

# Using len() function
no_dupes_count= len(no_dupes)
print(f"Row count using len(): {no_dupes_count}")

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")