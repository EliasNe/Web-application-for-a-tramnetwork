

### COPIED FROM LAB1 ######

import sys
import json
import re
import math

# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'
TRAM_FILE = './tramnetwork.json'

def build_tram_stops(jsonobject):
    with open(jsonobject, 'r', encoding="UTF-8") as f: 
        dict = json.load(f)

    # Make empty dictonary to update and store new lat and lon values
    tram_stop_dict = {}

    # Iterate through the whole dictonary for keys and values
    for key, value in dict.items():
        # Extract the values for lat and long from "position" in the dictonary
        lat,lon = map(float,value['position'])

        # Create dictonary containing lat and lon
        lat_and_lon = {
            'lat': lat,
            'lon': lon
        }

        # Associate each key with the dictionary containing latitude and longitude values
        tram_stop_dict[key] = lat_and_lon

    # Return the dictionary with latitude and longitude values             
    return tram_stop_dict


def build_tramplines(lines):
    # Initialize dictionaries to store tram lines and transition times
    line_dict = {}
    time_dict = {}

    # Initialize variables for current and previous stops
    current_station = [""]
    previous_station = [""]

    # Flag to check if a station should be skipped
    skip_station = 0

    # Open the tram lines file
    with open(lines, 'r', encoding="UTF-8") as tram_lines_file:
        line_number = "0" 


        # Iterate through each line in the tram lines file
        for line in tram_lines_file:
            # If the line starts with a digit, treat it as a line number
            if line[0].isdigit():
                line_number = line[0:-2] 
                line_dict[line_number] = []   
            # If the line does not start with a digit, add it to the line dictionary    
            elif not line[0].isdigit():
                result = line.rsplit(" ", 1)
                result2 = result[0].strip()
                line_dict[line_number].append(result2)

        # Seek to the beginning of the file to process transition times
        tram_lines_file.seek(0)

        # Iterate through each line again to process transition times
        for line in tram_lines_file:   
            # If the line is not a digit and not empty       
            if not line[0].isdigit() and line != '\n':
                # Split the string into two parts e.g ["valand", "10:00"] and remove leading/trailing spaces
                current_station = line.rsplit(" ", 1)
                current_station[0] = current_station[0].strip()

                # If the previous station is not empty, continue processing
                if  previous_station[0] != "": 
                    if previous_station[0] not in time_dict:
                        # Add the previous station as a key to the time dictionary
                        previous_station[0] = previous_station[0].strip()
                        time_dict[previous_station[0]] = {}
                    
                    # Loop to remove non-digit characters from the line
                    tmp = ""
                    for char in line:
                        if char.isdigit():
                            tmp += char
                    
                    # Check if the current station exists in the time dictionary
                    if current_station[0] in time_dict:
                        # Check if the previous station should be skipped
                        for value in time_dict[current_station[0]]:
                            if previous_station[0] == value:
                                skip_station = 1
                    
                    # If the station should not be skipped, calculate the time difference
                    if skip_station != 1:
                        previous_time = previous_station[1].split(":")
                        current_time = current_station[1].split(":")
                    
                        previous_time_minutes = int(previous_time[0]) * 60 + int(previous_time[1])
                        current_time_minutes = int(current_time[0]) * 60 + int(current_time[1])
                       
                        difference_time = abs(current_time_minutes - previous_time_minutes) 
                       
                        time_dict[previous_station[0]][current_station[0]] =  difference_time
                
                # Assign the current station to the previous station
                previous_station = current_station 
            else: 
                # Special case if the line is empty
                previous_station=[""]
            
            # Reset the skip_station flag
            skip_station = 0

    # Remove empty strings from the lists in line_dict
    for key, value_list in line_dict.items():
        line_dict[key] = [value for value in value_list if value != '']
    
    return line_dict,time_dict

    
def build_tram_network(stop_file, line_file):
    # Call each function to extract stops, lines and times
    stops = build_tram_stops(stop_file)
    lines = build_tramplines(line_file)

    # Assign stops, lines, and times to the build_tram_network_dict
    build_tram_network_dict = {"stops": stops, "lines": lines[0], "times": lines[1]}

    # Write to a file and create the file tramnetwork.json
    with open('tramnetwork.json', 'w', encoding = "UTF-8") as json_file:
        json.dump(build_tram_network_dict, json_file, indent=4)

    return build_tram_network_dict
    
        
# Extract all the lines with the given stop
def lines_via_stop(linedict, stop):
    lines_via_stops_list = [] 

    for key, values in linedict.items():
        if stop in values:
                lines_via_stops_list.append(key)
   
    return lines_via_stops_list
    
    
# Extract the lines between two stops.
def lines_between_stops(linedict, stop1, stop2):
    stops_list = [] 

    for key,values in linedict.items():
        if stop1 in values and stop2 in values:
            stops_list.append(key)
    
    return stops_list


# Calculate the time between two stops on a specific line.
def time_between_stops(linedict, timedict, line, stop1, stop2):
    line_stops = linedict[line]
    start_index, end_index = sorted([line_stops.index(stop1), line_stops.index(stop2)])

    sliced_line = line_stops[start_index: end_index + 1]

    total_time = 0

    for current_stop in sliced_line:
        stop_index = sliced_line.index(current_stop)
        
        if stop_index == len(sliced_line) - 1:
            break

        next_stop_from_list = sliced_line[stop_index + 1]
        
        next_stops_dict = timedict.get(current_stop)
        reverse_stops_dict = timedict.get(next_stop_from_list)

        if next_stop_from_list in next_stops_dict:
            time_to = next_stops_dict[next_stop_from_list]
            total_time += time_to
          
        elif current_stop in reverse_stops_dict:
            reverse_time_to = reverse_stops_dict[current_stop]
            total_time += reverse_time_to

    return total_time


# Calculate the distance between two stops.
def distance_between_stops(stopdict, stop1, stop2):

        stop1_coordinates = []
        stop2_coordinates = []
        
        for key, value in stopdict.items():
                if key == stop1:
                    stop1_coordinates = value['lat'], value['lon']
                if key == stop2:
                    stop2_coordinates = value['lat'], value['lon']
        
        distance = round(calculate_Distance(*stop1_coordinates, *stop2_coordinates), 3)
        return distance


# Calculate the Haversine distance between two sets of coordinates.                 
def calculate_Distance(lat1,lon1,lat2,lon2):

    r = 6371.009

    # Make the lat,lon from degress to radiues
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the difference
    dlatitude = lat2_rad -lat1_rad 
    dlongitude = lon2_rad -lon1_rad

    # The formula for haversine
    a = math.sin(dlatitude / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlongitude / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = r*c 

    return distance


# function which handle the answer and give back the result to the dialogue
def answer_query(tramdict, query):

    split_user_input = query.split(" ",1)
    first_word = split_user_input[0]

    stopdict, linedict, timedict = (
        tramdict['stops'],
        tramdict['lines'],
        tramdict['times']
    )
    
    if first_word == "via":
        lines_via_stop_result = lines_via_stop(linedict,split_user_input[1])
        if lines_via_stop_result == [] :
            return("unknown arguments")
        else:
            return lines_via_stop_result 
    
    elif first_word == "between":
        list_between = slice_stop_between(split_user_input[1]) 
        lines_list = lines_between_stops(linedict, list_between[0], list_between[1])
        if lines_list == [] :
            return ("unknown arguments")
        else:
            list_between = slice_stop_between(split_user_input[1]) 
            return lines_list
    
    elif first_word == "distance":
        list_distance = slice_stop_distance(split_user_input[1])
        if list_distance[0] not in stopdict or list_distance[1] not in stopdict:
            return ("unknown arguments")
        else : 
            return distance_between_stops(stopdict,list_distance[0],list_distance[1])
    
    elif first_word == "time":
        tokenized = slice_stop_time(split_user_input[1])
        line = tokenized[0]
        stop1 = tokenized[1]
        stop2 = tokenized[2]

        if line not in linedict :
            return("unknown arguments")
        elif stop1 not in linedict[line] or stop2 not in linedict[line] :
            return("unknown arguments")
        else :
            return time_between_stops(linedict, timedict, line, stop1 , stop2)
    
    else: 
        return("Sorry try again")
        

# Helper functions to the answer query
def slice_stop_between(stop_string):
    stop_names = stop_string.split(" and ")

    return [stop.strip() for stop in stop_names]


def slice_stop_distance(stop_string):
    stop_string = re.sub(r'\d+|from|, ', '', stop_string).strip()  
    stop_names = stop_string.split(" to ")

    return [stop.strip() for stop in stop_names]
    

def slice_stop_time(stop_string):
    stop_names_line = stop_string.split(' from ')
    stop_names_line2 = stop_names_line[1].split( " to ")
    stop_names_line3 = stop_names_line[0].split(" ")
    extract_line = stop_names_line3[1]
    stop_names_line2.insert(0, extract_line)

    return stop_names_line2
    
    
# The dialogue function
def dialogue(tramfile=TRAM_FILE):

    with open(tramfile,'r',encoding="UTF-8") as trampstops: 
            dictonary = json.load(trampstops)
            
            while True:
                userinput = input("> ")
                if userinput== "quit":
                    break
                else:
                    print(answer_query(dictonary,userinput))
    return 
  

if __name__ == '__main__':

    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()
   
                
                        
                        
                    
                        
                                
                                

                        
                
                

              
