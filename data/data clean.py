import pandas as pd
import re

file_path = 'hotels.csv'
hotels_data = pd.read_csv(file_path, encoding='ISO-8859-1')


def process_hotel_names(name):
    return re.sub(r'^\d+\.\s+', '', name)


def process_number_of_reviews(reviews):
    if pd.isna(reviews) or reviews == '':
        return "NA"
    numbers = re.findall(r'(\d+)', reviews)
    numbers = [int(num.replace(',', '')) for num in numbers]
    return sum(numbers)


def process_ratings(ratings):
    if pd.isna(ratings) or ratings == '':
        return "NA"
    rating_numbers = re.findall(r'(\d+(\.\d+)?)', ratings)
    if not rating_numbers:
        return "NA"

    first_rating = float(rating_numbers[0][0])

    return f"{first_rating}"


def extract_city(location):
    parts = location.split(',')
    if len(parts) > 1:
        return parts[1].strip()
    else:
        return "NA"


hotels_data['Hotel Names'] = hotels_data['Hotel Names'].apply(process_hotel_names)

hotels_data['city'] = hotels_data['location'].apply(extract_city)

grouped_data = hotels_data.groupby('Hotel Names').agg({
    'Ratings': lambda x: process_ratings(','.join(x.dropna().astype(str))),
    'Number of Reviews': lambda x: process_number_of_reviews(','.join(x.dropna().astype(str))),
    'amenities': 'first',
    'links': 'first',
    'location': 'first',
    'Description': 'first',
    'city': 'first'
}).reset_index()

print(grouped_data.head())

grouped_data.to_csv('processed_hotels_data.csv', index=False)
