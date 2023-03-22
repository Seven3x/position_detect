import cv2
import numpy as np
import rspoint

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


if __name__ == '__main__':
    pipeline, profile, align = rspoint.init_d455()
    
    while True:
        depth_frame, color_frame, depth_intrinsics, color_intrinsics = rspoint.get_frame(pipeline, align)
        
        if depth_frame is None or depth_frame is None:
            continue
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        
        balls = detect_ping_pong_balls(color_image)
        
        print(len(balls))
        
        if len(balls) != 0:
            (x,y,r) = balls[0]
            color_image = cv2.rectangle(color_image, (x-r,y-r), (x+r,y+r), (0,255,0), 2)
            
        cv2.imshow('color', color_image)
        # quit when press q
        if cv2.waitKey (1) & 0xFF == ord ('q'): 
            break