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

# Standardize the data (important for K-means)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(df[['Latitude', 'Longitude', 'PDSI']])

# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster_KMeans'] = kmeans.fit_predict(data_scaled)

# Create hover text with Year, Month, and PDSI information
hovertext = df['Year'].astype(str) + '-' + df['Month'].astype(str) + '<br>PDSI: ' + df['PDSI'].round(2).astype(str)

# Create a Plotly scattergeo plot
fig = go.Figure(go.Scattergeo(
    lon=df['Longitude'],  # Longitude
    lat=df['Latitude'],   # Latitude
    mode='markers',       # Scatter points
    marker=dict(
        color=df['Cluster_KMeans'],  # Color by cluster
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
    title='Cluster Visualization on World Map',
)

# Save the plot as an image (use kaleido)
fig.write_image("clustered_map.png")  # Save as PNG

# Optionally, show the plot (if you want to see it on-screen as well)
# fig.show()
