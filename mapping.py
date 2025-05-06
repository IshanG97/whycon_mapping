#Ishan Godawatta, The University of Manchester, 2020, ID:9651584

#This file is used to create the grid map array to be used for the SVG map creation.
import matplotlib.pyplot as plt #used to create the prototype map
from matplotlib import colors
import numpy as np #used for complex data array calculations
import pose #this is the pose file added as a module

EMPTY_CELL = 0
START_CELL = 1
GOAL_CELL = 2
PATH_CELL = 3
OBSTACLE_CELL = 4
MINE_CELL = 5
ROUNDEL_CELL = 6
GREY_CELL = 7
BUGGY_CELL = 8

### THE BELOW FUNCTION IS DEPRECATED AND ONLY USED FOR TESTING ###
### THIS PROCESSES THE DATA ARRAY FROM THE GENERATE_MAP_ARRAY FUNCTION TO CREATE A PNG MAP ###
def create_png_map(data):
    # LOAD GRID SIZE #
    rows,cols = pose.grid_size()
    # LOAD LANE NUMBER FROM TEXT FILE #
    lanenum = pose.load_lane_number();

    # CREATE DISCRETE COLOURMAP #
    cmap = colors.ListedColormap(['white', 'yellow', 'green', 'cyan', 'black', 'red', 'purple', 'grey', 'blue'])
    bounds = [EMPTY_CELL, START_CELL, GOAL_CELL, PATH_CELL, OBSTACLE_CELL, MINE_CELL, ROUNDEL_CELL, GREY_CELL, BUGGY_CELL, BUGGY_CELL+1]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)

    # DRAW GRIDLINES #
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.5)
    ax.set_xticks(np.arange(0.5, cols, 1)); #cols
    ax.set_yticks(np.arange(0.5, rows, 1)); #rows
    plt.tick_params(axis='both', labelsize=5, length = 1)
    plt.savefig("lane_" + str (lanenum) + ".png", dpi=250)
    ax.invert_yaxis()
    plt.show()

### THIS PROCESSES THE DATA ARRAY FROM THE GENERATE_MAP_ARRAY FUNCTION TO CREATE AN SVG MAP ###
def create_svg_map(data):
    x = ''
    offset = [20,20]
    multip = 10
    widthmultip = 1

    data = np.flip(data, 0)
    y = np.nonzero(data.astype(int))


    length = len(y[0])
    print("length y: ", len(y[0]), len(y[1]))
    x += '<svg height="2200" width="500" xmlns="http://www.w3.org/2000/svg">\n'

    for i in range(length):
        val = int(data[y[0][i]][y[1][i]])
        col = ''
        cols = ['white', 'yellow', 'green', 'cyan', 'black', 'red', 'purple', 'grey', 'blue']
        col = cols[int(abs(val))]

        x1 = str(y[1][i]*multip + (offset[0]-int(multip/2)))
        y1 = str(y[0][i]*multip + (offset[1]-int(multip/2)))

        if val == 7:
            x += '<rect x="'+ x1 +'" y="'+ y1 +'" width="'+str(multip*widthmultip)+'" height="'+str(multip*widthmultip)+'" fill-opacity="1" fill="'+ col +'" />\n'

    for i in range(length):
        val = int(data[y[0][i]][y[1][i]])
        col = ''
        cols = ['white', 'yellow', 'green', 'cyan', 'black', 'red', 'purple', 'grey', 'blue']
        col = cols[int(abs(val))]

        x1 = str(y[1][i]*multip + (offset[0]-int(multip/2)))
        y1 = str(y[0][i]*multip + (offset[1]-int(multip/2)))

        if val != 7:
            x += '<rect x="'+ x1 +'" y="'+ y1 +'" width="'+str(multip*widthmultip)+'" height="'+str(multip*widthmultip)+'" fill-opacity="1" fill="'+ col +'" />\n'

    x += '</svg>\n'
    lanenum = pose.load_lane_number()
    file = open('lane_{}.svg'.format(lanenum), 'w')
    file.write(x)
    file.close()
    return x

### THIS FUNCTION GENERATES THE OCCUPANCY GRID MAP ARRAY ###
def generate_map_array():
    rows,cols = pose.grid_size() #gives resolution of 0.25 meters per cell with extra column to show roundel
    data = np.zeros(rows * cols).reshape(rows, cols)

    # PLOT SAFE AREA #
    for x in range(0,rows):
        data[x,0] = GREY_CELL

    # PLOT START AND GOAL CELLS #
    if data[0, cols//2] != MINE_CELL or data[0, cols//2] != OBSTACLE_CELL:
        data[0, cols//2] = START_CELL

    if data[rows-1, cols // 2] != MINE_CELL or data[rows-1, cols // 2] != OBSTACLE_CELL:
        data[rows-1, cols // 2] = GOAL_CELL

    # LOAD MARKER LOCATIONS #
    y_1, x_1, y_2, x_2 = pose.calculate_marker_coordinates()
    data[y_1,x_1] = ROUNDEL_CELL
    data[y_2,x_2] = ROUNDEL_CELL

    # LOAD POSE FROM WHYCON #
    y_coord, x_coord = pose.calculate_pose_coordinates()

    # SAVE POSE #
    if data[y_coord,x_coord] != MINE_CELL or data[y_coord,x_coord] != OBSTACLE_CELL:
        pose.save_pose(y_coord, x_coord)

    # LOAD POSE HISTORY #
    data = pose.pose_history(data)

    # FILL OUT ROBOT POSE BASED ON 0.4x0.6m DIMENSIONS #
    if data[y_coord,x_coord] != MINE_CELL or data[y_coord,x_coord]!= OBSTACLE_CELL:
        data[y_coord,x_coord] = BUGGY_CELL

    if y_coord-1 < rows-1 and y_coord-1 > 0 and (data[y_coord-1, x_coord] != MINE_CELL or data[y_coord,x_coord] != OBSTACLE_CELL):
        data[y_coord-1,x_coord] = BUGGY_CELL

    if y_coord-2 < rows-1 and y_coord-2 > 0 and (data[y_coord-2, x_coord] != MINE_CELL or data[y_coord,x_coord] != OBSTACLE_CELL):
        data[y_coord-2,x_coord] = BUGGY_CELL

    # LOAD DATA MD/GPR SENSOR DATA TO PLOT MINE LOCATIONS #
    data = pose.load_sensor_data(data)

    # LOAD ULTRASOUND DATA TO PLOT OBSTACLES #
    data = pose.load_ultrasound_data(data)

    return data

if __name__ == "__main__":
    x = generate_map_array()
    #create_png_map(x) #deprecated map method
    create_svg_map(x)
