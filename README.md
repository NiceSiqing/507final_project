My project involves the management and visualization of hotel data, primarily in the form of tables and graphical structures. Below is a detailed description of the data structures:

Hotel Data Table:

My project primarily uses a data table containing hotel information, which stores various attributes for each hotel, including hotel name, rating, number of reviews, price, amenities, address, and more. This table is a typical two-dimensional table stored in CSV format in a file.

The fields in the data table include:

- Hotel Names: Hotel name
- Price: Hotel price
- Ratings: Hotel rating
- Number of Reviews: Number of reviews
- Price: Price
- Amenities: Amenities
- Address: Address
- City: City
- Latitude: Latitude
- Longitude: Longitude
- Description: Description

This data table provides structured storage of detailed information for each hotel.

Hotel Network Graph:

A graphical structure is used to represent the relationships between cities and hotels. This network graph employs a graph data structure and uses a network graph representation.

Nodes: Each node represents either a city or a hotel. City nodes have the type "city" and come with an attribute for the number of reviews. Hotel nodes have the type "hotel" and come with an attribute for the number of reviews.

Edges: Edges represent the relationships between cities and the hotels they contain. There are edges between city nodes and the hotel nodes they contain.

The network graph is used to display the relationships between cities and hotels on the "Network Graph Visualization" page, and it dynamically generates the graph based on user filtering criteria.

Graphical Visualization:

The project uses the Plotly library to generate various graphical visualizations, including scatter plots, bar charts, tables, and more. These visualization tools are used to present different aspects of hotel data, such as the number of hotels in cities, rating distributions, hotel details, the relationship between hotel ratings and the number of reviews, and more. Graphical visualizations are embedded in web pages and combined with the data table and network graph, providing interactive data analysis tools.

Overall, my project uses multiple data structures, including data tables, graphical network graphs, and graphical visualizations, to effectively manage and display hotel data, allowing users to gain insights into various hotel attributes and relationships. This combination of data structures offers rich functionality for data storage, analysis, and visualization.