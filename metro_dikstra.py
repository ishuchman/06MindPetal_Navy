import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

# ------------------------------
# Part 1: Process Ridership Data
# ------------------------------
# Read the ridership CSV.
df = pd.read_csv("ridership.csv")

# Display first few rows of the raw data
print("Raw Ridership Data:")
print(df.head())

# Calculate total ridership per row as the sum of Entries and exits.
df['Total'] = df['Entries'] + df['exits']

# Pivot the data so that each station has columns for each time period (Evening, LateNights)
df_pivot = df.pivot_table(index='Station', columns='Time', values='Total', aggfunc='sum').reset_index()
df_pivot = df_pivot.fillna(0)
print("\nAggregated Ridership Data:")
print(df_pivot.head())

# Define nightlife stations.
nightlife_stations = {"Dupont", "Gallery", "NavyYard", "Foggy"}

# Project ridership:
# For each station, the projected ridership equals Evening + LateNights.
# For nightlife stations, add an extra two hours’ worth of LateNights (i.e. LateNights * 2).
def project_ridership(row):
    evening = row.get("Evening", 0)
    late_nights = row.get("LateNights", 0)
    base = evening + late_nights
    extra = late_nights * 2 if row['Station'] in nightlife_stations else 0
    return base + extra

df_pivot['Projected'] = df_pivot.apply(project_ridership, axis=1)

print("\nProjected Ridership by Station:")
print(df_pivot[['Station', 'Projected']])

# Create a Plotly bar chart for the projected ridership.
fig = px.bar(df_pivot, x='Station', y='Projected',
             title='Projected Ridership with Extended Service Until 3 AM',
             labels={'Projected': 'Projected Total Ridership', 'Station': 'Station'})
fig.write_html("projected_ridership.html")
print("\nPlotly bar chart saved as 'projected_ridership.html'.")

# ------------------------------
# Part 2: Build and Analyze the Transit Network
# ------------------------------
# Load the metro network CSV.
df_network = pd.read_csv("metro_network.csv")
print("\nMetro Network Data:")
print(df_network.head())

# Create the graph from the network CSV.
# Assumed columns in metro_network.csv: 'Source', 'Target', 'Weight'
G = nx.Graph()
for _, row in df_network.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

# Compute optimal routes using Dijkstra’s algorithm.
# Route 1: From a nightlife hub (Dupont) to a residential station (Rosslyn)
try:
    route1 = nx.dijkstra_path(G, source='Dupont', target='Rosslyn', weight='weight')
except nx.NetworkXNoPath:
    route1 = []
    print("No path found from Dupont to Rosslyn.")

# Route 2: From another nightlife area (NavyYard) to a residential hub (Tenleytown)
try:
    route2 = nx.dijkstra_path(G, source='NavyYard', target='Tenleytown', weight='weight')
except nx.NetworkXNoPath:
    route2 = []
    print("No path found from NavyYard to Tenleytown.")

print("\nOptimal Route 1 (Dupont -> Rosslyn):", route1)
print("Optimal Route 2 (NavyYard -> Tenleytown):", route2)

# Plot the transit network using a spring layout and highlight the optimal routes.
pos = nx.spring_layout(G, seed=42)  # for reproducibility

plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edges(G, pos, edge_color='gray', width=1)

# Helper function: convert a path list into edge list tuples.
def path_to_edge_list(path):
    return [(path[i], path[i+1]) for i in range(len(path)-1)]

if route1:
    edges_route1 = path_to_edge_list(route1)
    nx.draw_networkx_edges(G, pos, edgelist=edges_route1, edge_color='red', width=3, label='Route 1')

if route2:
    edges_route2 = path_to_edge_list(route2)
    nx.draw_networkx_edges(G, pos, edgelist=edges_route2, edge_color='green', width=3, label='Route 2')

plt.title("Metro Network with Optimal Routes")
plt.axis('off')
plt.legend(['Route 1', 'Route 2'])
plt.savefig("metro_network_routes.png")
plt.show()
print("\nNetwork graph saved as 'metro_network_routes.png'.")
