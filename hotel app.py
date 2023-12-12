import networkx as nx
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import json
import plotly.figure_factory as ff
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go

app = Flask(__name__)

# Load hotel data from a CSV file
file_path = 'data/hotels_with_geocode.csv'
hotels_data = pd.read_csv(file_path)

# Define the root route
@app.route('/')
def index():
    # Get unique city names from the data
    cities = hotels_data['city'].unique()
    return render_template('index.html', cities=cities)

# Define route for comparing selected hotels
@app.route('/compare_hotels', methods=['POST'])
def compare_hotels():
    # Get selected hotels from the form
    selected_hotels = request.form.getlist('hotel')
    # Filter data to include only selected hotels
    comparison_data = hotels_data[hotels_data['Hotel Names'].isin(selected_hotels)]
    return render_template('compare_hotels.html', hotels=comparison_data)

# Define route for displaying hotels in a specific city
@app.route('/city_hotels')
def city_hotels():
    # Get city, rating filter, and amenities filter from the request
    city = request.args.get('city', '')
    rating_filter = request.args.get('rating', type=float)
    amenities_filter = request.args.get('amenities', default='')

    # Filter data based on the selected city
    filtered_data = hotels_data[hotels_data['city'] == city]

    # Apply rating filter if provided
    if rating_filter:
        filtered_data = filtered_data[filtered_data['Ratings'] >= rating_filter]

    # Apply amenities filter (if 'Amenities' column exists)
    if amenities_filter and 'Amenities' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['Amenities'].str.contains(amenities_filter, case=False, na=False)]

    # Create a map visualization using Plotly
    fig = px.scatter_mapbox(filtered_data, lat='latitude', lon='longitude',
                            hover_name='Hotel Names',
                            zoom=10, height=1200, width=1400,
                            title=f'Hotels in {city}')
    fig.update_layout(mapbox_style='open-street-map')
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    # Pass the hotel data to the template
    hotels_list = filtered_data.to_dict('records')

    return render_template('city_hotels.html', graph_json=graph_json, city=city, hotels=hotels_list)

# Define route for various visualizations based on chart_type
@app.route('/visualization/<string:chart_type>')
def visualization(chart_type):
    if chart_type == 'city_hotel_count':
        # Number of hotels in each city
        city_hotel_count = hotels_data['city'].value_counts().reset_index()
        city_hotel_count.columns = ['City', 'Number of Hotels']
        fig = px.bar(city_hotel_count, x='City', y='Number of Hotels',
                     title='Number of Hotels in Each City')
    elif chart_type == 'rating_distribution':
        # Distribution of hotel ratings
        fig = px.histogram(hotels_data, x='Ratings', title='Distribution of Hotel Ratings')
    elif chart_type == 'hotel_details':
        # Display details and user reviews of hotels
        columns = ['Hotel Names', 'Ratings', 'Number of Reviews', 'Description']
        fig = ff.create_table(hotels_data[columns].head(10))
    elif chart_type == 'hotel_comparison':
        # Compare ratings and number of reviews of different hotels
        fig = px.bar(hotels_data, x='Hotel Names', y=['Ratings', 'Number of Reviews'],
                     title='Comparison of Ratings and Number of Reviews of Hotels')
    elif chart_type == 'rating_reviews':
        # Scatter plot of hotel ratings vs. number of reviews
        fig = px.scatter(hotels_data, x='Number of Reviews', y='Ratings',
                         title='Hotel Ratings vs. Number of Reviews')
    else:
        return "Invalid chart type", 400

    # Convert the plot to JSON for rendering in the template
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('visualization.html', graph_json=graph_json, title=fig.layout.title.text)

# Create a network graph of cities and hotels
def create_city_hotel_graph(data):
    G = nx.Graph()
    for city in data['city'].unique():
        G.add_node(city, type='city', reviews=0)  # City nodes with reviews count initialized to 0
        hotels_in_city = data[data['city'] == city]
        for _, hotel in hotels_in_city.iterrows():
            hotel_name = hotel['Hotel Names']
            reviews = hotel['Number of Reviews']
            G.add_node(hotel_name, type='hotel', reviews=reviews)
            G.add_edge(city, hotel_name)
    return G

# Visualize the network graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    edge_x, edge_y, node_x, node_y, node_color = [], [], [], [], []

    # Create data for edges and nodes
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        reviews = G.nodes[node]['reviews']
        node_color.append(reviews)  # Use reviews count for color mapping

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='#888'), hoverinfo='none')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text', text=list(G.nodes()),
                            marker=dict(showscale=True, colorscale='YlOrRd', size=10, color=node_color, colorbar=dict(thickness=15)))

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=20, l=5, r=5, t=40)))
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return graph_json

# Define route for the network graph visualization
@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        city = request.form.get('city', '')
        min_rating = request.form.get('min_rating', type=float)
        max_price = request.form.get('max_price', type=float)

        # Filter data based on selected criteria
        filtered_data = hotels_data
        if city:
            filtered_data = filtered_data[filtered_data['city'] == city]
        if min_rating:
            filtered_data = filtered_data[filtered_data['Ratings'] >= min_rating]
        if max_price:
            filtered_data = filtered_data[filtered_data['Price'] <= max_price]

        # Generate the graph
        G = create_city_hotel_graph(filtered_data)
        graph_json = visualize_graph(G)
        return render_template('graph.html', graph_json=graph_json, cities=hotels_data['city'].unique())

    else:
        # Display the graph with all data by default
        G = create_city_hotel_graph(hotels_data)
        graph_json = visualize_graph(G)
        return render_template('graph.html', graph_json=graph_json, cities=hotels_data['city'].unique())

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
