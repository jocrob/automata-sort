import argparse
from PIL import Image 

p = argparse.ArgumentParser(description="sort pixels through an automata")
p.add_argument("image", help="input image file")
p.add_argument("automata", help = "input an automata to sort with")
p.add_argument("iteration", help = "input the number of times the automata should run on the image", type = int)
args = p.parse_args()

# global variables that represent the coordinates of a zero pixel when one can't be found quickly
zeroRow = 0
zeroCol = 0
zeroFound = 0
oneFound = 0

def main():
	print("Opening image...")
	img = Image.open(args.image)
	aut = args.automata
	autIter = args.iteration

	print("Converting to RGBA...")
	img = img.convert('RGBA')

	new = Image.new('RGBA', img.size)
	print("Running automata...")
	#2D array of pixel data
	for z in range(autIter):
		data = img.load()
		pixels = []
		for y in range(img.size[1]):
			pixels.append([])
			for x in range(img.size[0]):
				pixels[y].append(data[x, y])

		pixelValues = []
		pixelValues = getVals(pixels)

		if(zeroFound == 0 or oneFound == 0):
			print("The intensity setting is either too high or low for the automata to have an effect on the image")
			return

		sortedPixels = []
		if(aut == "rule90"):
			sortedPixels = rule90(pixels, pixelValues);
		elif(aut == "rule184"):
			sortedPixels = rule184(pixels, pixelValues);
		elif(aut == "life"):
			sortedPixels = life(pixels, pixelValues)

		for y in range(img.size[1]):
			#print(len(sortedPixels[y]))
			for x in range(img.size[0]):
				new.putpixel((x, y), sortedPixels[y][x])

		img = new

	print("Saving image...")
	new.save('output.png')

# 0 and 1 values are deterined by rgb intensity. 	higher intensity = 1	lower intensity = 0
def getVals(pixels):
	global zeroRow
	global zeroCol
	global zeroFound
	global oneFound
	values = []
	rgbLim = 300
	for row in range(len(pixels)):
		values.append([])
		col = 0
		for pixel in pixels[row]:
			if((pixel[0] + pixel[1] + pixel[2]) < rgbLim):
				values[row].append(1)
				oneFound = 1
			else:
				values[row].append(0)
				zeroRow = row
				zeroCol = col
				zeroFound = 1
			col += 1

	return values


# For all automata...
# When pixel value changes, the pixel is replaced by another pixel matching that value
# if no pixel matching that value can be found (in the row for 1D automata), the pixel remains unchanged 

# rule90 automata 
def rule90(pixels, values):
	sorted = []
	locZeroRow = len(pixels)							#used to hold a zero value pixel that is closer than the global zero value pixel
	locZeroCol = len(pixels[0])
	for row in range(len(pixels)):
		sorted.append([])
		for x in range(len(pixels[row])):
			prevp = 0
			nextp = 0

			if(values[row][x] == 0):
				locZeroRow = row
				locZeroCol = x

			if(x == 0):						
				prevp = len(values[row]) - 1			#wraps around to end cell if cell is at left edge
				nextp = x + 1
			elif(x == len(pixels[row]) - 1):
				prevp = x - 1
				nextp = 0					#wraps around to beginning cell if cell is at right edge
			else:
				prevp = x - 1
				nextp = x + 1

			oldVal = values[row][x]
			newVal = values[row][prevp] ^ values[row][nextp]		#performs rule90 function for new cell value
		
			if(oldVal == newVal):								#cases: 000, 101, 110, 011
				sorted[row].append(pixels[row][x])
			elif(newVal == 0):
				if(values[row][prevp] == 0):						#case: 010 
					if(x % 2 == 0):
						sorted[row].append(pixels[row][prevp])
					else:
						sorted[row].append(pixels[row][nextp])
				else:									#case: 111
						if(locZeroRow < len(pixels)):									#first searches for a nearby 0 pixel to insert 
							sorted[row].append(pixels[locZeroRow][locZeroCol])
						else:															#if none are found
							sorted[row].append(pixels[zeroRow][zeroCol])			#inserts a generic zero valued pixel from the image
			elif(newVal == 1):
				if(values[row][prevp] == 1):						#case 100
					sorted[row].append(pixels[row][prevp])
				else:									#case 001
					sorted[row].append(pixels[row][nextp])

	return sorted;

# rule184 automata "traffic rule"
def rule184(pixels, values):
	sorted = []
	for row in range(len(pixels)):
		sorted.append([])
		for x in range(len(pixels[row])):
			prevp = 0
			nextp = 0
			if(x == 0):						
				prevp = len(values[row]) - 1			#wraps around to end cell if cell is at left edge
				nextp = x + 1
			elif(x == len(pixels[row]) - 1):
				prevp = x - 1
				nextp = 0					#wraps around to beginning cell if cell is at right edge
			else:
				prevp = x - 1
				nextp = x + 1

			currVal = values[row][x]
			prevVal = values[row][prevp]
			nextVal = values[row][nextp]

			if(currVal == 1 & nextVal == 0):				#cases 110 010 (current 1 pixel fills space of next 0 pixel, leaving a 0 space)
				sorted[row].append(pixels[row][nextp])
			elif(prevVal == 1 & currVal == 0):				#cases 101 100 (previous 1 pixel fills space of current 0 pixel)
				sorted[row].append(pixels[row][prevp])
			else:								#cases 000 001 011 111 no 1 pixel can fill the space of a 0 pixel so the pixels stay the same
				sorted[row].append(pixels[row][x])

	return sorted

# Conway's Game of Life
def life(pixels, values):
	sorted = []
	locZeroRow = len(pixels)					#len(pixels) used as a null value to show a zero hasn't been found
	locZeroCol = len(pixels[0])
	for row in range(len(pixels)):
		sorted.append([])
		for col in range(len(pixels[row])):
			neighbors = 0
			for y in range(row-1, row+2):
				for x in range(col-1, col+2):
					if(y < 0 or y >= len(pixels)):		#checks if on edge
						break
					if(x < 0 or x >= len(pixels[0])):
						continue
					if(x == col and y == row):
						continue
					if(values[y][x] == 1):
						neighbors += 1

			one = searchNeighborhood(values, row, col, 1)
			zero = searchNeighborhood(values, row, col, 0)
			
			if(neighbors < 2 or neighbors > 3 and values[row][col] == 1):			#case dying
				if(zero):
					sorted[row].append(pixels[zero[0]][zero[1]])
				elif(locZeroRow < len(pixels)):										
					sorted[row].append(pixels[locZeroRow][locZeroCol])
				else:				
					sorted[row].append(pixels[zeroRow][zeroCol])
			elif((neighbors == 2 or neighbors == 3) and values[row][col] == 1):		#case living
				sorted[row].append(pixels[row][col])
			elif(neighbors == 3):								#case born	
				sorted[row].append(pixels[one[0]][one[1]]) 
			else:										#case dead
				sorted[row].append(pixels[row][col])

	return sorted

# returns the coordinates of a certain value pixel (1 or 0) in a given neighborhood (9 pixels)
def searchNeighborhood(values, row, col, val):
	for y in range(row-1, row+2):
		for x in range(col-1, col+2):
			if(y < 0 or y >= len(values)):
				break
			if(x < 0 or x >= len(values[0])):
				continue
			if(values[y][x] == val):
				#print(y)
				#print(x)
				coordinates = [y, x]
				return coordinates
	coordinates = []
	return coordinates

if __name__ == "__main__":
	main()
