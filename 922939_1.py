import os
import csv
from pyproj import Proj, transform
import datetime 


def read_csv_file(csv_file_name):
    """
    This function reads a csv file and returns a 
    nested list containing the data where each 
    row in the list is a row in the csv file.
    
    The csv file contains the following columns:
    trajectory_id, node_id, timestamp, latitude, longitude, speed_limit
    
    The latitude and longitude are in EPSG 4326 coordinate system.
     
    Keyword arguments:
    csv_file_name -- string text containing name of the csv file
    
    Return:
    A nested list consisting of the data in the csv file and variables containing 
    indexes for each of the columns that are expected in the csv file
    """
    execution_halted_str = 'Execution halted in the function read_csv_file!!!'
    path = os.path.join(os.getcwd(),csv_file_name)
    if os.path.exists(path) == True:
        with open(path, 'r') as inFile:
            data = list(csv.reader(inFile))
        columns = data[0]
        if len(columns) == 6:
            try:
                trajectory_index = data[0].index('trajectory_id')
                node_id_index = data[0].index('node_id')
                timestamp_index = data[0].index('timestamp')
                latitude_index = data[0].index('latitude')
                longitude_index = data[0].index('longitude')
                speed_index = data[0].index('speed_limit')
                
                return data, trajectory_index, node_id_index, timestamp_index, latitude_index, longitude_index, speed_index
            except ValueError as value_error:
                value_error = str(value_error)
                
                if value_error == "'trajectory_id' is not in list":
                    raise Exception('{} The csv file provided does not contain the column trajectory_id.'.format(execution_halted_str))
                elif value_error == "'node_id' is not in list":
                    raise Exception('{} The csv file provided does not contain the column node_id.'.format(execution_halted_str))
                elif value_error == "'timestamp' is not in list":
                    raise Exception('{} The csv file provided does not contain the column timestamp.'.format(execution_halted_str))
                elif value_error == "'latitude' is not in list":
                    raise Exception('{} The csv file provided does not contain the column latitude.'.format(execution_halted_str))
                elif value_error == "'longitude' is not in list":
                    raise Exception('{} The csv file provided does not contain the column longitude.'.format(execution_halted_str))
                elif value_error == "'speed_limit' is not in list":
                    raise Exception('{} The csv file provided does not contain the column speed.'.format(execution_halted_str))
                else:
                    raise Exception('{} The csv file provided does not contain the required columns.'.format(execution_halted_str))
                
        else:
            raise Exception('{} The file does not contain the correct number of columns as per the requirement of this project.'.format(execution_halted_str))
        
    else:
        raise FileNotFoundException("{} The file "+csv_file_name+" was not found in the current directory.".format(execution_halted_str))
        
def write_csv_file(csv_file_name, data):
    path = os.path.join(os.getcwd(),csv_file_name)
    with open(csv_file_name, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(data)



def reference_frame_transformation(data, output_file_transformed, trajectory_index, node_id_index, timestamp_index, latitude_index, longitude_index, speed_index):
    """
    This function converts the langitude and longitude values from
    EPSG 4326 to EPSG 7855 and then write back to the csv file.
     
    Keyword arguments:
    data -- nested list containing trajectory data
    output_file_transformed -- string text containing the name of the file where the transformed projected data will be saved at
    indexes for the columns that are expected to be in the cvs file
    Return:
    A nested list with the modified projected data
    """
    execution_halted_str = 'Execution halted in the function reference_frame_transformation!!!'

    # Input: 'epsg:4326'
    # Output: 'epsg:7855'
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:7855')
    projected_data = [['trajectory_id', 'node_id', 'timestamp', 'latitude', 'longitude', 'speed_limit']]
    for i,data_obj in enumerate(data):
        
        if i>0:
            latitude = 0.0
            longitude = 0.0
            try:
                latitude = float(data_obj[latitude_index])
            except ValueError as valueError:
                raise Exception("{} Latitude provided at index {} is not a float number.".format(execution_halted_str, i))
            
            try:
                longitude = float(data_obj[longitude_index])
            except ValueError as valueError:
                raise Exception("{} Longitude provided at index {} is not a float number.".format(execution_halted_str, i))

            if -180 <= float(longitude) <=180:
                if -90 <= float(latitude) <=90:
                    x, y = transform(inProj,outProj,longitude,latitude)
                    #data_obj[3] = y
                    #data_obj[4] = x
                    projected_data.append([data_obj[trajectory_index],data_obj[node_id_index],data_obj[timestamp_index],y,x,data_obj[speed_index]])
                else:
                    raise Exception("{} The latitude at index {} should be between -90 and 90 degrees.".format(execution_halted_str, i))
            else:
                raise Exception("{} The longitude at index {} should be between -180 and 180 degrees.".format(execution_halted_str, i))
            
    write_csv_file(output_file_transformed, projected_data)
    return projected_data



def compute_distance(origin, destination):
    """
    This function computes the euclidean distance between two 
    points.
    
    Since the csv file contains the order (latitude, longitude) this
    assignment will also assume this order instead of the (longitude, latitude)
    for ease of use and to reduce confusion, so the x coordinate has been taken
    as the latitude, and y coordinate has been taken as the y coordinate.
    
    Keyword arguments:
    origin -- tuple containing (latitude, longitude)
    destination -- tuple containing (latitude, longitude)
    
    """
    x_diff = (origin[0]-destination[0])**2
    y_diff = (origin[1]-destination[1])**2
    distance = x_diff + y_diff
    distance = distance**0.5
    return distance
    


def compute_time_difference(origin_time, destination_time):
    """
    This function computes the differnce in time
    between the origin and destination times that
    have been provided.
    
    Keyword arguments:
    origin_time -- String of the format hours:minutes:seconds
    destination_time -- String of the format hours:minutes:seconds    
    """
    execution_halted_str = 'Execution halted in the function compute_time_difference!!!'
    
    try:
        origin_time = datetime.datetime.strptime(origin_time, '%H:%M:%S')
    except ValueError as error:
        raise Exception("{} origin_{}".format(execution_halted_str, error))
    try:
        destination_time = datetime.datetime.strptime(destination_time, '%H:%M:%S')
    except ValueError as error:
        raise Exception("{} destination_{}".format(execution_halted_str, error))
        
    time_difference = destination_time - origin_time
    if time_difference.total_seconds() >=0:
        return abs(time_difference.total_seconds())
    else:
        raise Exception("{} The time difference must be greater than and equals to zero.".format(execution_halted_str))
    


def compute_speed(distance, time):
    """
    This function computes the speed by
    using the speed, distance and time formula.
    
    Keyword arguments:
    distance -- numeric value of the distance
    time -- numeric value of the time in seconds
    
    Return:
    speed 
    """
    execution_halted_str = 'Execution halted in the function compute_speed!!!'

    if time > 0:
        speed = distance / time
    else:
        raise Exception("{} divide by zero error encoutered.".format(execution_halted_str))
    return speed



try:
    input_file = 'trajectory_data.csv'
    data, trajectory_index, node_id_index, timestamp_index, latitude_index, longitude_index, speed_index = read_csv_file(input_file)
    projected_data = reference_frame_transformation(data, input_file, trajectory_index, node_id_index, timestamp_index, latitude_index, longitude_index, speed_index)
    trajectories = []# This contains the index of each trajectory
    distances_trajectory = []# This contains the distances of each trajectory
    max_distance_per_trajectory = []# This contains the maximum distance of a segment in each trajectory
    number_of_segments_per_trajectory = []# This contains the number of segments in each trajectory
    times_per_trajectory = []# This contains the total time of each trajectory
    sample_rate_per_trajectory = []
    min_speed_per_trajectory = []
    max_speed_per_trajectory = []
    trajectory_starting_index = [] # This contains the index at which the trajectory starts at
    limit = len(projected_data)# Number of rows in the projected data

    # In order to iterate over the projected data I am taking two points at a time.
    # I am looking at the data point at index i and i+1 to calculate. I am then 
    # cascading down two rows at a time till I reach the end of the list.
    
    for i in range(1,limit):
        if (i+1) < limit:
            # Over here I am initializing the lists with the initial 
            # values so that later on I can populate these lists with 
            # appropriate data. Suppose that there are 8 trajectories in 
            # data, then each list will have a length of 8 where each 
            # index will correspond to a single trajectory at that index 
            # in the data.

            if projected_data[i][0] not in trajectories:
                # I am appending the trajectories list with the 
                # index of the trajectory.

                trajectories.append(projected_data[i][0])
                distances_trajectory.append(0)
                number_of_segments_per_trajectory.append(0)
                max_distance_per_trajectory.append([0,0])
                times_per_trajectory.append(0)
                min_speed_per_trajectory.append([10000000,0]) # For the minimum speed i have to initialize the speed value with some arbitrary value
                max_speed_per_trajectory.append([0,0])
                trajectory_starting_index.append(i)
                
               
            # Over here I am getting the index of the trajectory. This will
            # be used to index these lists. The index function returns the 
            # index of the element in the list which i can then use.

            if projected_data[i][0]==projected_data[i+1][0]:
                index = trajectories.index(projected_data[i][0])
                # Compute the distance between data point at i and i+1 index. This is the distance between data point i and i+1.
                distance = compute_distance((projected_data[i][3],projected_data[i][4]),(projected_data[i+1][3],projected_data[i+1][4]))
                distances_trajectory[index] = distances_trajectory[index] + distance
                time_diff = compute_time_difference(projected_data[i][2], projected_data[i+1][2])
                times_per_trajectory[index] = times_per_trajectory[index] + time_diff

                # Calculate the minimun and maximum speed for each segment for each trajectory
                speed = compute_speed(distance,time_diff)

                if max_speed_per_trajectory[index][0] < speed:
                    max_speed_per_trajectory[index][0] = speed
                    max_speed_per_trajectory[index][1] = (i+1) - trajectory_starting_index[index] # Find a way to calculate the index of the segment

                if min_speed_per_trajectory[index][0] >= speed:
                    min_speed_per_trajectory[index][0] = speed
                    min_speed_per_trajectory[index][1] = (i+1) - trajectory_starting_index[index] # Find a way to calculate the index of the segment

                # This is calculating the maximum distance and then saving 
                # it in the segment_sizes list at the corresponding index 
                # of the trajectory.

                if max_distance_per_trajectory[index][0] < distance:
                    max_distance_per_trajectory[index][0] = distance
                    max_distance_per_trajectory[index][1] = (i+1) - trajectory_starting_index[index]
                number_of_segments_per_trajectory[index] = number_of_segments_per_trajectory[index] + 1
                # Due to the indexing, i have to add 1 to the size of the last segment in the list

                if (i+1) == limit-1:
                    number_of_segments_per_trajectory[index] = number_of_segments_per_trajectory[index] + 1

    index_longest_trajectory = number_of_segments_per_trajectory.index(max(number_of_segments_per_trajectory))
    for i,d in enumerate(number_of_segments_per_trajectory):
        sample_rate_per_trajectory.append(times_per_trajectory[i]/number_of_segments_per_trajectory[i])
    for i,data in enumerate(trajectories):
        trajectory_id = i+1
        print("Trace {}'s length is {:.2f}m.".format(trajectory_id, distances_trajectory[i]))
        print("The length of its longest segment is {:.2f}m and the index is {}.".format(max_distance_per_trajectory[i][0],max_distance_per_trajectory[i][1]))
        print("The average sampling rate for the trace is {:.2f}s.".format(sample_rate_per_trajectory[i]))
        print("For the segment index {}, the minimal travel speed is reached.".format(min_speed_per_trajectory[i][1]))
        print("For the segment index {}, the maximum travel speed is reached.".format(max_speed_per_trajectory[i][1]))
        print("----")

    print("The total length of all traces is {:.2f}m.".format(sum(distances_trajectory)))
    index_trace = distances_trajectory.index(max(distances_trajectory))
    average_speed = compute_speed(distances_trajectory[index_trace],times_per_trajectory[index_trace])

    print("The index of the longest trace is {}, and the average speed along the trace is {:.2f}m/s.".format(index_trace,average_speed))

except Exception as error:
    # Either some or all of the required columns are not found in the csv file.
    # Execution of the application can not continue.
    print(error)
    #print('The required columns could not be found in the provided csv file. Application execution cannot continue.')




