import pandas as pd
import plotly.graph_objects as go


# Define the file path
file_path = './pdsi_all_data.csv'

# Specify data types for each column to avoid mixed-type warnings
dtype_spec = {
    'Year': 'int64',
    'Month': 'int64',
    'Latitude': 'float64',
    'Longitude': 'float64',
    'PDSI': 'float64'
}

# Load the data with specified dtypes
df = pd.read_csv(file_path, dtype=dtype_spec, low_memory=False)

# Confirm data types were correctly applied
print(df.dtypes)
print(df.head())



# Define the latitude and longitude range for the map center
min_lat = 24.5625
max_lat = 49.22916793823242
min_lon = -124.6875
max_lon = -67.35416412353516

# Prepare frames for each Year-Month combination
frames = []
unique_dates = df[['Year', 'Month']].drop_duplicates().sort_values(['Year', 'Month'])


# Map PDSI values to a valid color scale
def get_color(PDSI_value):
    # Clamp values to ensure RGB components stay within 0–255
    red = int(255 * (1 - min(max((PDSI_value + 4) / 8, 0), 1)))
    blue = int(255 * min(max((PDSI_value + 4) / 8, 0), 1))
    return f'rgb({red}, 0, {blue})'


for _, row in unique_dates.iterrows():
    year, month = row['Year'], row['Month']
    monthly_data = df[(df['Year'] == year) & (df['Month'] == month)]

    # Add the frame for each year-month
    frames.append(go.Frame(
        data=[
            go.Scattermapbox(
                lat=monthly_data['Latitude'],
                lon=monthly_data['Longitude'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=[get_color(PDSI) for PDSI in monthly_data['PDSI']],
                    cmin=-4, cmax=4,
                    colorscale="RdBu",  # Red to Blue color scale
                    colorbar=dict(title="PDSI", tickvals=[-4, 0, 4], ticks="outside")
                ),
                text=[f"PDSI: {PDSI:.2f}" for PDSI in monthly_data['PDSI']]
            )
        ],
        name=f"{year}-{month:02d}"
    ))

# Create the figure
fig = go.Figure(
    data=[
        go.Scattermapbox(
            lat=[30.49],
            lon=[-100.4194],
            mode='markers',
            marker=dict(size=12, color='orange')
        )
    ],
    layout=go.Layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=(min_lat + max_lat) / 2, lon=(min_lon + max_lon) / 2),
            zoom=4,
            pitch=0
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]
            )]
        )]
    ),
    frames=frames
)

# Show the figure
fig.show()
