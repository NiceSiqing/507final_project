import requests
import pandas as pd

def get_geocode(api_key, address):
    """ Get latitude and longitude for a given address using the MapQuest Geocoding API. """
    base_url = "http://www.mapquestapi.com/geocoding/v1/address"
    params = {
        "key": api_key,
        "location": address
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()
        locations = results.get("results", [])[0].get("locations", [])
        if locations:
            best_match = locations[0]
            lat_lng = best_match.get("latLng", {})
            return lat_lng.get("lat"), lat_lng.get("lng")
    return None, None

# MapQuest API key
api_key = 'VmE4MoZPZZfSHKJAMmYIc53NctDapCQY'

# Load data
file_path = 'processed_hotels_data.csv'
hotels_data = pd.read_csv(file_path)

# Create new columns to store latitude and longitude data
hotels_data['latitude'] = None
hotels_data['longitude'] = None

# Assuming your dataset has a 'Hotel Names' column containing hotel names
for index, row in hotels_data.iterrows():
    lat, lng = get_geocode(api_key, row['Hotel Names'])
    hotels_data.at[index, 'latitude'] = lat
    hotels_data.at[index, 'longitude'] = lng

# Check the retrieved latitude and longitude data
print(hotels_data.head())

# Save the DataFrame with geocode data to a new CSV file
output_file_path = 'hotels_with_geocode.csv'
hotels_data.to_csv(output_file_path, index=False)

print(f"Saved the DataFrame with geocode data to {output_file_path} file.")
