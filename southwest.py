import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = './pdsi_all_data.csv'
dtype_spec = {
    'Year': 'int64',
    'Latitude': 'float64',
    'Longitude': 'float64',
    'PDSI': 'float64'
}
df = pd.read_csv(file_path, dtype=dtype_spec)

# Filter data for Southwest U.S. region
southwest_filter = (
    ((df['Latitude'] >= 32.5) & (df['Latitude'] <= 37.0) & (df['Longitude'] >= -120.0) & (df['Longitude'] <= -113.0)) |  # California
    ((df['Latitude'] >= 32.5) & (df['Latitude'] <= 36.5) & (df['Longitude'] >= -114.0) & (df['Longitude'] <= -109.5)) |  # Arizona
    ((df['Latitude'] >= 35.5) & (df['Latitude'] <= 39.5) & (df['Longitude'] >= -116.5) & (df['Longitude'] <= -113.0))    # Nevada
)
southwest_df = df[southwest_filter]

# Group by Year and calculate mean PDSI
timeseries_df = southwest_df.groupby('Year', as_index=False)['PDSI'].mean()

# Plot the timeseries
plt.figure(figsize=(10, 6))
plt.plot(timeseries_df['Year'], timeseries_df['PDSI'], marker='o', linestyle='-', color='b', label='Mean PDSI')
plt.axhline(0, color='r', linestyle='--', label='Neutral PDSI')
plt.title('Timeseries of Mean PDSI for Southwest U.S. Region')
plt.xlabel('Year')
plt.ylabel('Mean PDSI')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save or display the plot
plt.savefig('./southwest_pdsi_timeseries.png')  # Save the plot as an image
plt.show()  # Display the plot
