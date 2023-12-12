import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

# Load data from JSON file
file_path = 'data/processed_hotels_data.json'
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# Create DataFrame
hotels_data = pd.DataFrame(data)

# Set rating and review count thresholds
rating_threshold = 4.0
review_count_threshold = 1000

# Filter data based on thresholds
filtered_data = hotels_data[(hotels_data['Ratings'] >= rating_threshold) & (hotels_data['Number of Reviews'] >= review_count_threshold)]

# Create a directed graph
G = nx.DiGraph()

# Add USA as the root node
G.add_node('USA', type='country')

# Get unique cities
cities = set(filtered_data['city'])

# Add city nodes and edges
for city in cities:
    G.add_node(city, type='city')
    G.add_edge('USA', city)
    hotels_in_city = filtered_data[filtered_data['city'] == city]
    for _, hotel in hotels_in_city.iterrows():
        hotel_name = hotel['Hotel Names']
        G.add_node(hotel_name, type='hotel')
        G.add_edge(city, hotel_name)

        # Set label for hotel nodes
        G.nodes[hotel_name]['label'] = '\n'.join([hotel_name[i:i+15] for i in range(0, len(hotel_name), 15)])

# Plot the graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G)
labels = {node: G.nodes[node].get('label', node) for node in G.nodes()}  # Use multi-line labels
nx.draw(G, pos, labels=labels, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, font_color='black', font_weight='bold')
plt.title('Tree Structure of Hotels by City with USA as Root (Filtered Data)')
plt.show()
