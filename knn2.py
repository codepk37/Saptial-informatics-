import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load your data
file_path = './pdsi_all_data.csv'
dtype_spec = {
    'Year': 'int64',
    'Month': 'int64',
    'Latitude': 'float64',
    'Longitude': 'float64',
    'PDSI': 'float64'
}
df = pd.read_csv(file_path, dtype=dtype_spec, low_memory=False)

# Aggregate PDSI by Year and Month (creating a temporal feature vector)
temporal_data = df.groupby(['Latitude', 'Longitude', 'Year', 'Month'])['PDSI'].mean().reset_index()

# Standardize the data (important for K-means)
scaler = StandardScaler()
temporal_data_scaled = scaler.fit_transform(temporal_data[['Latitude', 'Longitude', 'PDSI']])

# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
temporal_data['Cluster_KMeans'] = kmeans.fit_predict(temporal_data_scaled)

# Create hover text with Year, Month, and PDSI information
hovertext = temporal_data['Year'].astype(str) + '-' + temporal_data['Month'].astype(str) + '<br>PDSI: ' + temporal_data['PDSI'].round(2).astype(str)

# Create a Plotly scattergeo plot
fig = go.Figure(go.Scattergeo(
    lon=temporal_data['Longitude'],  # Longitude
    lat=temporal_data['Latitude'],   # Latitude
    mode='markers',       # Scatter points
    marker=dict(
        color=temporal_data['Cluster_KMeans'],  # Color by cluster
        colorscale='Viridis',  # Color scale for clusters
        size=6,
        opacity=0.7,
        colorbar=dict(title='Cluster ID')  # Color bar showing cluster labels
    ),
    hovertext=hovertext,  # Add hover text
    hoverinfo='text'      # Display hover text
))

# Set layout options for better map visualization
fig.update_layout(
    geo=dict(
        projection_type='mercator',  # Map projection
        showland=True,               # Show land
        landcolor='white',           # Land color
        coastlinecolor='black',      # Coastline color
        countrycolor='black',        # Country borders color
        projection_scale=5           # Adjust zoom level
    ),
    title='Cluster Visualization of PDSI Over Time',
)

# Save the plot as an image (use kaleido)
fig.write_image("temporal_clustered_map.png")  # Save as PNG

# Optionally, show the plot (if you want to see it on-screen as well)
# fig.show()
