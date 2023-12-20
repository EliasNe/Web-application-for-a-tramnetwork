import json
import os
from .graphs import WeightedGraph
from .tramdata import distance_between_stops, lines_via_stop
from django.conf import settings


class TramNetwork(WeightedGraph):
    def __init__(self, lines, stops, times, start=None): 
        super().__init__(start)
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times


    # Return a list of all tram lines
    def all_lines(self):
        return list(self._linedict.keys())
    

    # Return a set of all tram stops
    def all_stops(self): 
        stops_list = []
        
        for lines in self._linedict.keys():
            for stop in self._linedict[lines]:
                stops_list.append(stop)
            
        return set(stops_list)
    

    # Return the minimum and maximum latitude and longitude of all tram stops
    def extreme_positions(self):
        lat_list = [pos['lat'] for pos in self._stopdict.values()]
        lon_list = [pos['lon'] for pos in self._stopdict.values()]
        return min(lon_list), min(lat_list), max(lon_list), max(lat_list)


    # Calculate the geographical distance between two tram stops
    def geo_distance(self, stop1, stop2):
        return distance_between_stops(self._stopdict, stop1, stop2)
    

    # Return a list of tram stops for a given tram line
    def line_stops(self, line):
        return self._linedict[line]
    

    # Return a list of tram lines passing through a given tram stop
    def stop_lines(self, stop):
        return lines_via_stop(self._linedict, stop)
    

    # Return the geographical position of a tram stop
    def stop_position(self, stop):
        return self._stopdict[stop]


    # Return the transition time (weight) between two tram stops
    def transition_time(self, stop1, stop2):
        return self.get_weight(stop1, stop2)


# Return a tramnetwork object with time between stops as weight
def readTramNetwork(file='tramnetwork.json'):
    # Change directory and get the tramnetwork file, then change back to base dir.
    base_dir = os.getcwd()
    file_path_utils = os.path.join(os.getcwd(), 'tram', 'utils')  # Use forward slashes here
    os.chdir(file_path_utils)
    with open(file, 'r', encoding="UTF-8") as trampstops: 
        tramdict = json.load(trampstops)
    os.chdir(base_dir)
    
    edge_list = createEdges(tramdict['times'])
    tram_network = TramNetwork(tramdict['lines'], tramdict['stops'], tramdict['times'], edge_list)
    addWeights(tram_network, tramdict['times'])

    return tram_network


# Create a list of tuples containing all edges.
def createEdges(timedict):
    edge_list = []
    for key, values in timedict.items():
        for value in values:
            edge_list.append((key, value))

    return edge_list


# Add weights to a tramnetwork
def addWeights(tram_network, timedict):
    for a, b in tram_network.edges():
        next_stops_a = timedict[a].keys()
        
        for stop in next_stops_a:
            if stop == b:
                weight = timedict[a][stop]
                tram_network.set_weight(a, b, weight)
                
        if b in timedict.keys():
            next_stops_b = timedict[b].keys() 
        
            for stop in next_stops_b: 
                if stop == a:
                    weight = timedict[b][stop]
                    tram_network.set_weight(b, a, weight)



#### Bonus tasks(not done) #############

# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance


