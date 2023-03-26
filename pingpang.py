import cv2
import numpy as np
import rspoint

# Define a function that takes an image as an argument and returns a list of ping pong balls' pixel coordinates and sizes
def detect_color(image, lower_limit = np.array([5, 100, 100]), upper_limit = np.array([15, 255, 255]), debug = False):
    """
    Detects ping pong balls in an image and returns their pixel coordinates and sizes.
    
    Args:
        image: A numpy array representing the image to be processed.
        lower_limit: A numpy array representing the lower limit of the orange color range in HSV color space.
        upper_limit: A numpy array representing the upper limit of the orange color range in HSV color space.
        debug: A boolean value indicating whether to show debug information.
        
    Returns:
        A list of tuples representing the (x, y) coordinates and radius size of the detected ping pong balls.
    """
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the orange color
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    
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



# Define a function that takes an image as an argument and returns a list of ping pong balls' pixel coordinates and sizes
def detect_circle(image, lower_limit = np.array([5, 100, 100]), upper_limit = np.array([15, 255, 255]), debug = False):
    """
    Detects ping pong balls in an image and returns their pixel coordinates and sizes.
    
    Args:
        image: A numpy array representing the image to be processed.
        lower_limit: A numpy array representing the lower limit of the orange color range in HSV color space.
        upper_limit: A numpy array representing the upper limit of the orange color range in HSV color space.
        debug: A boolean value indicating whether to show debug information.
        
    Returns:
        A list of tuples representing the (x, y) coordinates and radius size of the detected ping pong balls.
    """
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    b,g,r = cv2.split(image)
    
    
    # kernel for dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    
    # Create a mask for the orange color
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    mask = cv2.dilate(mask, kernel, 10)
    
    # import color data
    r = mask*r
    
    # Hough detect
    circles = cv2.HoughCircles(r, cv2.HOUGH_GRADIENT, 1, 50,
                         param1=100, param2=45, minRadius=0, maxRadius=10000)
    
    # regular output
    if circles is None:
        circles = []
    else:
        circles = circles[0]
        if(debug):
            print(circles)
    
    # show_image
    if(debug):
        cv2.imshow('mask', r)   
        
    return circles


    
    

if __name__ == '__main__':
    # initialize the pipeline, profile, and align
    pipeline, profile, align = rspoint.init_d455()
    
    while True:
        # get the depth frame, color frame, depth intrinsics, and color intrinsics
        depth_frame, color_frame, depth_intrinsics, color_intrinsics = rspoint.get_frame(pipeline, align)
        
        # if either the depth frame or color frame is None, continue to the next iteration
        if depth_frame is None or depth_frame is None:
            continue
        
        # Convert the color frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())
        
        # detect the ping pong balls in the color image
        balls = detect_circle(color_image)
        
        # if there are any ping pong balls detected, draw a rectangle around the first one
        if len(balls) != 0:
            (x,y,r) = balls[0]
            color_image = cv2.rectangle(color_image, (int(x-r),int(y-r)), (int(x+r),int(y+r)), (0,255,0), 2)
            
        # split the color image into its RGB channels
        b,g,r = cv2.split(color_image)
        
        # show the color image and the red channel
        cv2.imshow('color', color_image)
        cv2.imshow('r', r)
        
        # quit the program when the 'q' key is pressed
        if cv2.waitKey (1) & 0xFF == ord ('q'): 
            break
