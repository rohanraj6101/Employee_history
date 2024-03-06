import pandas as pd

# Read the input CSV file
input_file = 'input.csv'
df = pd.read_csv(input_file)

# Sort the DataFrame by Employee Code and Date of Joining
df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
df.sort_values(by=['Employee Code', 'Date of Joining'], inplace=True)

# Define a function to calculate effective and end dates
def calculate_dates(group):
    group['End Date'] = group['Date of Joining'].shift(-1) - pd.Timedelta(days=1)
    group.loc[group['End Date'].isnull(), 'End Date'] = pd.to_datetime('2100-01-01')
    group['Effective Date'] = group['End Date'].shift(1) + pd.Timedelta(days=1)
    return group

# Apply the function to the DataFrame
df = df.groupby('Employee Code').apply(calculate_dates)

# Forward fill missing values
cols_to_fill = ['Compensation', 'Compensation 1', 'Compensation 2',
                'Review 1', 'Review 2', 'Engagement 1', 'Engagement 2']
df[cols_to_fill] = df[cols_to_fill].ffill()

# Select relevant columns for the output
output_df = df[['Manager Employee Code', 'Compensation', 'Compensation 1', 'Compensation 2',
                'Review 1', 'Review 2', 'Engagement 1', 'Engagement 2',
                'Effective Date', 'End Date']]

# Rename columns
output_df.columns = ['Manager Employee Code', 'Last Compensation', 'Compensation',
                     'Last Pay Raise Date', 'Variable Pay', 'Tenure in Org',
                     'Performance Rating', 'Engagement Score', 'Effective Date', 'End Date']

# Write the transformed data to a new CSV file
output_file = 'output.csv'
output_df.to_csv(output_file, index=False)