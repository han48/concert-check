import cv2
import numpy as np

from concert_helpers import bright_max

input = 'source/sample.jpg'
threshold, max_count = bright_max(input)
print("MAX: ", threshold, max_count)