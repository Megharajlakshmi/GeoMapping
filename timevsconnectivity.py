import pandas as pd
import folium
from folium.plugins import HeatMap

# File path for input data
file_path = 'data/timevsconnectivityfinal.txt'  # Replace with the actual file path

# Load data
data = pd.read_csv(file_path, sep=",")  # Adjust delimiter if necessary

# Parse 'time' as datetime and handle missing or erroneous values
data['time'] = pd.to_datetime(data['time'], errors='coerce').dt.time

# Clean and convert the 'connectivity' column
# Remove '%' and convert to float
data['connectivity'] = data['connectivity'].str.rstrip('%').astype(float)

# Drop rows with missing latitude, longitude, connectivity, or time
data_cleaned = data.dropna(subset=['longitude', 'latitude', 'connectivity', 'time'])

# Ensure numeric types for latitude and longitude
data_cleaned = data_cleaned.astype({
    'longitude': 'float',
    'latitude': 'float'
})

# Convert 'time' to seconds since midnight for consistent rounding
data_cleaned['time_in_seconds'] = (
    data_cleaned['time'].apply(lambda t: t.hour * 3600 + t.minute * 60 + t.second)
)

# Round time to the nearest 9 seconds
data_cleaned['time_in_seconds'] = (data_cleaned['time_in_seconds'] // 9 * 9)

# Generate rounded 'time' in standard time format
data_cleaned['time'] = data_cleaned['time_in_seconds'].apply(
    lambda t: (pd.Timestamp('1970-01-01') + pd.Timedelta(seconds=t)).time()
)

# Prepare data for heatmap: filter for valid rows only
heatmap_data = data_cleaned[['latitude', 'longitude', 'connectivity']].dropna().values.tolist()

# Verify all values in heatmap_data are numeric and within valid ranges
heatmap_data = [
    [lat, lon, weight]
    for lat, lon, weight in heatmap_data
    if isinstance(lat, (int, float)) and isinstance(lon, (int, float)) and isinstance(weight, (int, float))
]

# Create a Folium map centered on the mean location
map_center = [
    data_cleaned['latitude'].mean(),
    data_cleaned['longitude'].mean()
]
m = folium.Map(location=map_center, zoom_start=13)

# Add the heatmap layer
HeatMap(heatmap_data, radius=8, blur=15, max_zoom=1).add_to(m)

# Save the map as an HTML file
output_path = "timevsconnectivity.html"
m.save(output_path)
print(f"Interactive heatmap saved to {output_path}")