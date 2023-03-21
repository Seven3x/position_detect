import cv2
import numpy as np

# Define a function that takes an image as an argument and returns a list of ping pong balls' pixel coordinates and sizes
def detect_ping_pong_balls(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper boundaries of the orange color in HSV
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])
    
    # Create a mask for the orange color
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # Find the contours of the ping pong balls in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create an empty list to store the ping pong balls' pixel coordinates and sizes
    balls = []
    
    # Loop over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Filter out small or large areas that are not likely to be ping pong balls
        if area > 1000 and area < 10000:
            # Find the minimum enclosing circle of the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            # Round the values to integers
            x = int(x)
            y = int(y)
            radius = int(radius)
            
            # Append a tuple of (x, y) coordinate and radius size to the balls list
            balls.append((x, y, radius))
    
    # Return the balls list
    return balls