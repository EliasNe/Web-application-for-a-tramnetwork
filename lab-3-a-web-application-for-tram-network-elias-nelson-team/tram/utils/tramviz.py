from .trams import readTramNetwork
from .color_tram_svg import color_svg_network
from django.conf import settings

def show_shortest(dep, dest):
    # Create a TramNetwork graph object
    network = readTramNetwork()
    
    # Find the shortest path based on time
    total_time, quickest = network.shortest_path(dep, dest, cost=lambda u, v: network.get_weight(u, v))
    
    # Find the shortest path based on distance
    shortest_dict = network.dijkstra(dep, cost =lambda u, v: network.geo_distance(u, v))
    distance = network.geo_distance(dep, dest)
    shortest = shortest_dict[dest]

    # Generate strings that show path information
    timepath = f'Quickest: {", ".join(quickest)}, {total_time} minutes'
    geopath = f'Shortest: {", ".join(shortest)}, {distance} km'

    # Define colors for the visulalization
    def colors(v):
        if v in quickest and v in shortest:
            return 'cyan'
        elif v in shortest:
            return 'green'
        elif v in quickest:
            return 'orange'
        else:
            return 'white'     

    # Update the SVG image with the shortest path colors
    color_svg_network(colormap=colors)

    # Return the path information to be displayed on the web page
    return timepath, geopath

