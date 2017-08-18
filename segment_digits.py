import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 0.02

image_name = "bold_text.png"
img = cv2.imread(image_name, 0)
img = cv2.bitwise_not(img)

# Initializing vertical histogram
col_histo_width = img.shape[1]
col_histo_height = 200
col_histogram = np.zeros((col_histo_height, col_histo_width), np.uint8)

# Initializing horizontal histogram
row_histo_height = img.shape[0]
row_histo_width = 400
row_histogram = np.zeros((row_histo_height, row_histo_width), np.uint8)

# Calculating horizontal histogram
for row in range(row_histo_height):
	running_sum = sum(img[row, :]) // 255
	row_histogram[row, :running_sum] = 255

# calculating bounding indexes for rows using the histogram 
all_digit_rects = []
line_rects = []
starting_idx = False
for j in range(row_histo_height):
	thresholded_idx = int(THRESHOLD*row_histo_width)
	if row_histogram[j,thresholded_idx] == 255 and not starting_idx:
		starting_idx = j
	elif row_histogram[j,thresholded_idx] != 255 and starting_idx != False:
		last_idx = j
		if abs(starting_idx - last_idx) > 20:
			line_rects.append((starting_idx, last_idx))
		starting_idx = False

if len(line_rects) == 0:
	line_rects.append((0, row_histo_height))


for idx, line_rect in enumerate(line_rects):
	line = img[line_rect[0]:line_rect[1], :]

	# calculating vertical histogram for current row
	for column in range(col_histo_width):
		running_sum = sum(line[:, column]) // 255
		col_histogram[:running_sum, column] = 255

	# calculating bounding boxes for each digit
	digit_rects = []
	starting_idx = False
	for j in range(col_histo_width):
		thresholded_idx = int(THRESHOLD*col_histo_height)
		if col_histogram[thresholded_idx,j] == 255 and not starting_idx:
			starting_idx = j
		elif col_histogram[thresholded_idx,j] != 255 and starting_idx != False:
			last_idx = j
			if abs(starting_idx - last_idx) > 20:
				digit_rects.append((starting_idx, last_idx))
			starting_idx = False
	for digit in digit_rects:
		all_digit_rects.append((line_rect[0],line_rect[1], digit[0], digit[1]))

# To make it pretty
col_histogram = cv2.bitwise_not(col_histogram)
row_histogram = cv2.bitwise_not(row_histogram)

# plotting digits
fig = plt.figure()
mat_size = math.ceil(math.sqrt(len(all_digit_rects)))
for idx, digit in enumerate(all_digit_rects):
	a = fig.add_subplot(mat_size,mat_size,idx+1)
	img_plot = plt.imshow(img[all_digit_rects[idx][0]:all_digit_rects[idx][1], all_digit_rects[idx][2]:all_digit_rects[idx][3]])
plt.show()


cv2.imshow("original", img)
cv2.imshow("col_histogram", col_histogram)
cv2.imshow("row_histogram", row_histogram)
cv2.waitKey(0)
cv2.destroyAllWindows()