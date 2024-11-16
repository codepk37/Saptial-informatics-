import pandas as pd

# Load the CSV data
file_path = './pdsi_all_data.csv'
dtype_spec = {
    'Year': 'int64',
    'Month': 'int64',
    'Latitude': 'float64',
    'Longitude': 'float64',
    'PDSI': 'float64'
}
df = pd.read_csv(file_path, dtype=dtype_spec)


# Group by Year, Latitude, and Longitude, calculate the mean PDSI
yearly_avg_df = df.groupby(['Year', 'Latitude', 'Longitude'], as_index=False)['PDSI'].mean()

# Multiply the average PDSI by 5
yearly_avg_df['PDSI'] = yearly_avg_df['PDSI'] * 1

# Save or display the resulting dataframe
yearly_avg_df.to_csv('./yearly_avg_pdsi.csv', index=False)

