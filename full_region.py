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

# Define bins and assign colors using the new color scheme
bins = [-float('inf'), -2, 0, 2, float('inf')]
labels = ['< -2', '-2 to 0', '0 to 2', '> 2']
colors = ['#8B0000', '#FF0000', '#90EE90', '#006400']  # Color codes for dark red, red, light green, and dark green

# Assign color labels based on PDSI
df['PDSI_Label'] = pd.cut(
    df['PDSI'],
    bins=bins,
    labels=labels
)

# Create the Plotly figure
fig = px.scatter_geo(
    df,
    lat='Latitude',
    lon='Longitude',
    color='PDSI_Label',
    color_discrete_map=dict(zip(labels, colors)),  # Map the labels to their respective colors
    # size=abs(df['PDSI']),  # Use PDSI magnitude for marker size
    animation_frame='Year',  # Animate by year
    title='PDSI Trends Worldwide (4 Bins)',
    projection='natural earth',  # Use a natural earth projection
    labels={'PDSI_Label': 'PDSI Category', 'PDSI': 'PDSI Magnitude'},
    size_max=90 
)

# Customize the layout
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor='lightgray',
        showcountries=True,
        countrycolor='gray',
        projection_scale=1,  # Default zoom for a world map
    ),
    title_x=0.5,
    coloraxis_showscale=True
)

# Save the animation as an HTML file
fig.write_html('./world_pdsi_animation_colored_with_labels.html')

# Show the plot
fig.show()
