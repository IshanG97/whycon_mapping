#Ishan Godawatta, The University of Manchester, 2020, ID:9651584

#This file is used to process the data sent into the grid map array and calculate, save and load the data from WhyCon, the ultrasound sensors, and the MD/GPR sensor.
from pathlib import Path
import numpy as np

PATH_CELL = 3
OBSTACLE_CELL = 4
MINE_CELL = 5

# THIS FUNCTION RETURNS THE SIZE OF THE REQUIRED GRID #
def grid_size():
    return 200,6

# THIS FUNCTION CAN BE MODIFIED TO ALERT THE OPERATOR IF AN OBSTACLE IS HIT OR THE ROBOT REACHES THE END OF THE LANE #
def stop_buggy():
    return

# THIS FUNCTION IS USED TO UPDATE THE LANE NUMBER WHEN MOVING TO A NEW LANE #
def update_lane_number(lanenum):
    f = open("lane_num.txt", "w")
    f.write(str(lanenum))
    f.close()
    return

# THIS FUNCTION IS USED TO UPDATE THE MARKER BEING USED FOR LOCALISATION #
def update_marker_number(markernum):
    f = open("marker_num.txt", "w")
    f.write(str(markernum))
    f.close()
    return

# THIS FUNCTION LOADS THE LANE NUMBER FROM THE TEXT FILE #
def load_lane_number():
    f = open("lane_num.txt", "r")
    first_line = f.readline()
    f.close()
    return int(first_line)

# THIS FUNCTION LOADS THE MARKER NUMBER FROM THE TEXT FILE #
def load_marker_number():
    f = open("marker_num.txt", "r")
    first_line = f.readline()
    f.close()
    return int(first_line)

# THIS FUNCTION LOADS THE MARKER LOCATION IN METRES #
def load_marker_locations():
    filename = "marker_locations.txt"

    if Path(filename).is_file():
        f = open(filename, "r")
        #read first marker location
        first_line = f.readline()
        val = first_line.split()
        y_1 = float(val[0])
        x_1 = float(val[1])

        #read second marker location
        for last_line in f:
            val = last_line.split()
            y_2 = float(val[0])
            x_2 = float(val[1])

        f.close()
    return y_1,x_1,y_2,x_2

# THIS FUNCTION CALCULATES INPUT DATA FROM THE METAL DETECTOR (MD) TO DETERMINE WHETHER A MINE HAS BEEN DETECTED #
def load_sensor_data(data):
    rows,cols = grid_size()
    lanenum = load_lane_number()
    filename = "mine_locations_{}.txt".format(lanenum)
    #EDIT FROM HERE
    # THE FOLLOWING IS A MOCK REPRESENTATION OF MD INPUT #
    data[32,3] = MINE_CELL
    data[32,4] = MINE_CELL
    data[32,2] = MINE_CELL
    #TO HERE
    return data

# THIS FUNCTION CONSIDERS WHETHER AN OBSTACLE HAS BEEN DETECTED #
def load_ultrasound_data(data):
    rows,cols = grid_size()
    lanenum = load_lane_number()
    filename = "obstacle_locations_{}.txt".format(lanenum)
    #EDIT FROM HERE
    #the following is a mock representation of ultrasound input
    data[18,3] = OBSTACLE_CELL
    #TO HERE
    return data

# THIS FUNCTION LOADS THE POSE HISTORY INTO THE MAP ARRAY #
def pose_history(data):
    lanenum = load_lane_number();
    filename = "pose_history_{}.txt".format(lanenum)

    f = open(filename, "r");
    for line in f:
        val = line.split()
        data[int(val[0]),int(val[1])] = PATH_CELL
    f.close()

    return data

# THIS FUNCTION CALCULATES THE MARKER NUMBER AND COORDINATES FROM THE WHYCON LOG TEXT FILES #
def load_pose():
    lanenum = load_lane_number()
    y_marker_1,x_marker_1,y_marker_2,x_marker_2 = load_marker_locations()
    markernum = load_marker_number()
    filename = "whycon_log_{}.txt".format(lanenum)

    if Path(filename).is_file():
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-2]
            second_line = lines[-3]
            f.close()

            ll = last_line.split()
            sl = second_line.split()
            y_ll = float(ll[8])
            x_ll = float(ll[9])
            y_sl = float(sl[8])
            x_sl = float(sl[9])

            if markernum == 1:
                if ll[1] == sl[1]:
                    if y_sl < 0.5:
                        update_marker_number(2) #switch to marker 2 if 1st marker is getting close
                    y_pose = y_marker_1 - y_sl
                    x_pose = x_marker_1 - x_sl
                else:
                    if y_ll < 0.5:
                        update_marker_number(2)
                    y_pose = y_marker_1 - y_ll
                    x_pose = x_marker_1 - x_ll
            else:
                if ll[1] == sl[1]:
                    if y_ll < 0.5:
                        stop_buggy() #stop the buggy if second marker is too close
                    y_pose = y_marker_2 - y_ll
                    x_pose = x_marker_2 - x_ll
                else:
                    if y_sl < 0.5:
                        stop_buggy()
                    y_pose = y_marker_2 - y_sl
                    x_pose = x_marker_2 - x_sl

    return y_pose,x_pose

# THIS FUNCTION CALCULATES THE POSE COORDINATES TO BE PLOTTED ON THE MAP BASED ON THE CALCULATED POSE #
def calculate_pose_coordinates():
    rows,cols = grid_size()
    y_pose,x_pose = load_pose()

    y_coord = round(y_pose*rows/10)
    x_coord = round(x_pose*cols/0.3)

    if y_coord < 0:
        y_coord = 0
    if y_coord > rows-1:
        y_coord = rows-1
    if x_coord < 0:
        x_coord = 0
    if x_coord > cols-1:
        x_coord = cols-1

    print(y_coord,x_coord)
    return y_coord,x_coord

# THIS FUNCTION CALCULATES THE MARKER COORDINATES TO BE PLOTTED ON THE MAP BASED ON THE CALCULATED MARKER LOCATIONS #
def calculate_marker_coordinates():
    rows,cols = grid_size()
    y_1,x_1,y_2,x_2 = load_marker_locations()

    y_1 = round(y_1*rows/10)
    x_1 = round(x_1*cols/0.3)
    y_2 = round(y_2*rows/10)
    x_2 = round(x_2*cols/0.3)

    if y_1 < 0:
        y_1 = 0
    if y_1 > rows-1:
        y_1 = rows-1
    if x_1 < 0:
        x_1 = 0
    if x_1 > cols-1:
        x_1 = cols-1

    if y_2 < 0:
        y_2 = 0
    if y_2 > rows-1:
        y_2 = rows-1
    if x_2 < 0:
        x_2 = 0
    if x_2 > cols-1:
        x_2 = cols-1

    return y_1,x_1,y_2,x_2

# THIS FUNCTION SAVES THE CURRENT POSE INTO THE POSE HISTORY TEXT FILE #
def save_pose(y_coord,x_coord):
    lanenum = load_lane_number()
    filename = "pose_history_{}.txt".format(lanenum)

    if not Path(filename).is_file(): #if file doesn't exist, create it
        f = open(filename,"w+")
        f.write(str(y_coord) + ' ' + str(x_coord) +'\n')
        f.close()

    f = open(filename, "r");
    for last_line in f:
        val = last_line.split()
        y_last = int(val[0])
        x_last = int(val[1])
    f.close()

    if(y_coord!=y_last or x_coord!=x_last):
        f = open(filename, "a+")
        f.write(str(y_coord) + ' ' + str(x_coord) +'\n')
        f.close()

if __name__ == "__main__":
    calculate_pose_coordinates()
