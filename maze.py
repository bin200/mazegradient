from PIL import Image
from matplotlib import pyplot as plt

import numpy as np

import configparser

# Import config
configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)
gradient_range = int(configParser.get('your-config', 'gradient_range'))
start_y = int(configParser.get('your-config', 'start_y'))
start_x = int(configParser.get('your-config', 'start_x'))
mode = configParser.get('your-config', 'mode')

# Open image
img = Image.open('maze.png').convert('L')

# Image converts to binary matrix
binary_matrix = np.array(img)
binary_matrix = ~binary_matrix # invert B&W
binary_matrix [binary_matrix > 0] = 1

#  Create output matrix
matrix_height = len(binary_matrix)
matrix_width = len(binary_matrix[0])
output_matrix = np.zeros([matrix_height, matrix_width], dtype=int)
output_matrix = ~output_matrix

start_tile = (start_y, start_x)
increment_move = (-1, -1)

# Set the moves to a high number based on the image size to ensure that the walls (at 0) are a much lower number than the first step of the path
current_moves = (matrix_height * matrix_width) / gradient_range

tiles_todo = [start_tile, increment_move]
check_for_end = False

# Breadth-first traversal of the maze, main loop
for tile in tiles_todo:

	# Only increment the moves once all tiles of a certain depth have been checked. All tiles of a depth level are added to tiles_todo between increment_move items.
	if (tile[0] == -1 and tile[1] == -1):
		if (check_for_end):
			break # If two increment_move tiles in a row, there are no more tiles left and the traversal is over
		current_moves += 1
		tiles_todo.append(increment_move)
		check_for_end = True
		continue
	else:
		check_for_end = False
	
	right_tile = (tile[0], tile[1] + 1)
	left_tile = (tile[0], tile[1] - 1)
	down_tile = (tile[0] + 1, tile[1])
	up_tile = (tile[0] - 1, tile[1])
	possible_moves = [up_tile, down_tile, right_tile, left_tile]
	
	for move in possible_moves:
		y = move[0]
		x = move[1]
		if (y <= (matrix_height - 1) and y >= 0 and x <= (matrix_width - 1) and x >= 0):
			if (binary_matrix[y][x] == 0): # If not a wall
				if ((y, x) not in tiles_todo):
					tiles_todo.append((y, x))
					output_matrix[y][x] = current_moves

# Set the start point to the maximum moves colour for visibility
output_matrix[start_y][start_x] = current_moves

binary_matrix = ~binary_matrix # invert B&W again for colour consistency

if (mode == "binary"):
	plt.imshow(binary_matrix, interpolation='nearest')
if (mode == "gradient"):
	plt.imshow(output_matrix, interpolation='nearest')
plt.show()
