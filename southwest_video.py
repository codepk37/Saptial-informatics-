import pandas as pd
import plotly.express as px

# Load the yearly average PDSI data
file_path = './yearly_avg_pdsi.csv'
dtype_spec = {
    'Year': 'int64',
    'Latitude': 'float64',
    'Longitude': 'float64',
    'PDSI': 'float64'
}
df = pd.read_csv(file_path, dtype=dtype_spec)

# Filter data for the Southwest U.S. region
southwest_filter = (
    ((df['Latitude'] >= 32.5) & (df['Latitude'] <= 37.0) & (df['Longitude'] >= -120.0) & (df['Longitude'] <= -113.0)) |  # California
    ((df['Latitude'] >= 32.5) & (df['Latitude'] <= 36.5) & (df['Longitude'] >= -114.0) & (df['Longitude'] <= -109.5)) |  # Arizona
    ((df['Latitude'] >= 35.5) & (df['Latitude'] <= 39.5) & (df['Longitude'] >= -116.5) & (df['Longitude'] <= -113.0))    # Nevada
)
southwest_df = df[southwest_filter]

# Define bins and assign colors using the new color scheme
bins = [-float('inf'), -2, 0, 2, float('inf')]
labels = ['< -2', '-2 to 0', '0 to 2', '> 2']
colors = ['#8B0000', '#FF0000', '#90EE90', '#006400']  # Color codes for dark red, red, light green, and dark green

# Assign color labels based on PDSI
southwest_df['PDSI_Label'] = pd.cut(
    southwest_df['PDSI'],
    bins=bins,
    labels=labels
)

# Create the Plotly figure
fig = px.scatter_geo(
    southwest_df,
    lat='Latitude',
    lon='Longitude',
    color='PDSI_Label',
    color_discrete_map=dict(zip(labels, colors)),  # Map the labels to their respective colors
    size=abs(southwest_df['PDSI']),  # Use PDSI magnitude for marker size
    animation_frame='Year',  # Animate by year
    title='PDSI Trends in Southwest U.S. (4 Bins)',
    projection='natural earth',
    labels={'PDSI_Label': 'PDSI Category', 'PDSI': 'PDSI Magnitude'}
)

# Customize the layout
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor='lightgray',
        showcountries=True,
        countrycolor='gray',
        projection_scale=5.5,  # Zoom in
        center={'lat': 36.5, 'lon': -113.5}  # Focus on Southwest U.S.
    ),
    title_x=0.5,
    coloraxis_showscale=True
)

# Save the animation as an HTML file
fig.write_html('./southwest_pdsi_animation_colored_with_labels.html')

# Show the plot
fig.show()
