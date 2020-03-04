import glob
import cv2
import os
import numpy as np
from math import sqrt
from PIL import Image, ImageFilter


# Calculate the Euclidean distance between two vectors
def euclidean_distance(a, b):
	distance = 0.0
	for (va, vb) in zip(a,b):
		distance += (va - vb)**2
	return sqrt(distance)

# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors):
	distances = list()
	for train_row in train:

        # consider only particular parameters
		h,w,d,i=test_row
		a = [i]
		h,w,d,i,_=train_row 
		b = [i]
		# dist = np.linalg.norm(b - a)
		dist = euclidean_distance(a, b)

        # consider everything [height, width, density, intensity]
		# dist = euclidean_distance(test_row, train_row)

		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1])
	neighbors = list()
	for i in range(num_neighbors):
		neighbors.append(distances[i][0])
	return neighbors

def load_brushes(brush_dir):
    path = os.path.join(brush_dir, '*g')
    files = glob.glob(path)

    brushes = []
    brush_masks = []
    brushes_data = []

    for i, fileName in enumerate(files):
        # [height, width, density, tensity, index]
        brush = Image.open(fileName)
        brushes.append(brush)

        ni = np.array(brush)
        alpha = ni[:,:,3]>0
        mask = Image.fromarray((alpha*255).astype(np.uint8))
        brush_masks.append(mask)
        
        width, height = brush.size
        size = width * height
        density = 0.0
        tensity = 0.0
        
        gray = brush.convert('LA')
        px = gray.load()
        for y in range(height):
            for x in range(width):
                if px[x, y][0] < 255 and px[x, y][0] > 0:
                    density += 1
                    tensity += px[x, y][0]
        tensity /= 255 * density
        density /= size
        brush_data = [height, width, density, tensity, i]
        brushes_data.append(brush_data)

    return brushes, brush_masks, brushes_data
