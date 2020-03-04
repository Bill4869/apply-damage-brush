import cv2 
import random
import numpy as np
# import imutils
import knn

from os import path
from gen_map import generate_map
from PIL import Image
from options import BaseOptions
from poissonblending import poisson
  
def getGrid_data(map, gridSize, location):
	density = 0.0
	tensity = 0.0
	last_point = location
	for y in range(location[0], location[0] + gridSize):
		for x in range(location[1], location[1] + gridSize):
			if map[y, x] != 255:
				tensity += map[y, x]
				density += 1
				last_point = (y, x)

	height = last_point[0] - location[0] + 1
	width = last_point[1] - location[1] + 1
	if density: 
		tensity /= 255 * density
		density /= gridSize * gridSize
	grid_data = [height, width, density, tensity]
	return grid_data

def update_source_mask(source, mask, brushes, brush_masks, neighbors, location, pasting_method):
	# angle = random.randint(0, 360)

	neighbor = random.choice(neighbors)

	brush = brushes[neighbor[-1]]
	# brush = imutils.rotate(brushes[ran], angle) to randomly rotate brush
	brush_mask = brush_masks[neighbor[-1]]

	pasting_method.paste(brush, (location[1], location[0]), brush)
	source.paste(brush, (location[1], location[0]), brush)
	mask.paste(brush_mask, (location[1], location[0]), brush_mask)

def main():
	opt = BaseOptions().parse()
	BaseOptions().mkdir(opt.output)

	# load target
	target = Image.open(opt.target)
	width, height = target.size
	pasting_method = target.copy()

	# generate map from target
	if (opt.map) and path.exists(opt.map): 
		prob_map = np.array(Image.open(opt.map))
	else: prob_map = generate_map(opt.target, opt.sigma, opt.threshold)

	gridSize = int(opt.gridScale * width / 100)
	print("grid size : " + str(gridSize))
	
	# source and mask for poisson image blending
	source = Image.new('RGB', (width, height), color = 'black')
	mask = Image.new('RGB', (width, height), color = 'black')

	# brush images, brush masks, and brush data([width, height, density, intensity]) list 
	brushes, brush_masks, brushes_data = knn.load_brushes(opt.brushesRoot)

	# loop probability map by tile
	y = 0
	while height - y >= gridSize: # while at least one tile left toward the bottom
		x = 0
		while width - x >= gridSize: # while at least one tile left toward the right
			location = (y, x)
			ran = random.random()
			grid_data = getGrid_data(prob_map, gridSize, location)
			# use tile's density and intensity to decide whether to apply brush
			if grid_data[-2] > 0.1 and grid_data[-1] * 0.1 > ran:
				neighbors = knn.get_neighbors(brushes_data, grid_data, 10) # get 10 nearest neighbors
				update_source_mask(source, mask, brushes, brush_masks, neighbors, location, pasting_method)
			x += gridSize
		y += gridSize

	pasting_method.save(path.join(opt.output, 'pasting_method.png')) 
	# source.save(path.join(opt.output, 'source.png'))
	# mask.save(path.join(opt.output, 'mask.png'))
	# target.save(path.join(opt.output, 'target.png'))
	Image.fromarray(prob_map).save(path.join(opt.output, 'map.png'))
	
	if (opt.usePoisson):
		poisson_method = poisson(mask, source, target)
		poisson_method.save(path.join(opt.output, 'poisson_method.png'))
		

if __name__ == '__main__':
	main()

