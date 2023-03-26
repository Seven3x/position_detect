import pyrealsense2 as rs
import numpy as np
import cv2

def init_d455(id = None, width = 640, height = 480, fps = 15):
    '''
    This function initializes the d455 depth camera. 
    Low fps may cause error.

    Input:
        id: device id, default is None
        width: width of the image, default is 640
        height: height of the image, default is 480
        fps: frame rate, default is 15

    Output:
        pipeline: pipeline object
        profile: profile object
        align: align object
    '''
        
    # Create a context object, which manages all connected realsense devices
    context = rs.context()
    
    # Get the device list
    devices = context.query_devices()
    
    # If no device is connected, exit the program
    if len(devices) == 0:
        print("No device found")
        exit(0)

    
    # Create a pipeline object, which configures and starts the data streams
    pipeline = rs.pipeline()
    
    # Create a config object, which specifies the streams and formats you want to open
    config = rs.config()
    
    # Enable depth stream, format z16 (16-bit unsigned integer)
    config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
    config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
    
    # Start the pipeline and return a profile object
    profile = pipeline.start(config)

    
    # Align the depth and color frames
    align_to = rs.stream.color      
    align = rs.align(align_to)      


    return pipeline, profile, align




def get_frame(pipeline, align):
    '''
    This function gets the depth and color frames from the d455 camera and returns them as a frame object.
    
    Input:
        pipeline: pipeline object
        align: align object
    
    Output:
        aligned_depth_frame: depth frame object
        aligned_color_frame: color frame object
        depth_intrinsics: depth camera intrinsics object
        color_intrinsics: color camera intrinsics object
    '''
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    
    # Get depth frame and color frame
    aligned_depth_frame = aligned_frames.get_depth_frame() 
    aligned_color_frame = aligned_frames.first(rs.stream.color)  

    
    # get intrinsics of the depth camera
    depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    # get intrinsics of the color camera
    color_intrinsics = aligned_color_frame.profile.as_video_stream_profile().intrinsics
    
    
    # Validate that both frames are valid
    if not depth_intrinsics or not color_intrinsics:
        return None, None, None, None
    
    
    # Return a frame object that contains both images
    return aligned_depth_frame, aligned_color_frame, depth_intrinsics, color_intrinsics



def get_3d_coordinate(aligned_depth_frame, x, y, depth_intrinsics):
    '''
    This function takes in an aligned depth frame, pixel coordinates x and y, and depth intrinsics and returns the 3D coordinate of the pixel in camera space and the distance to the pixel.

    Input:
        aligned_depth_frame: aligned depth frame object
        x: x pixel coordinate
        y: y pixel coordinate
        depth_intrinsics: depth camera intrinsics object

    Output:
        cam_coord: 3D coordinate object that contains X, Y and Z values
        dis: distance to the pixel
    '''
    # x and y are the pixel coordinates
    
    # Get depth value at pixel coordinate (x, y)
    dis = aligned_depth_frame.get_distance(x, y)
    
    # Convert pixel coordinate to 3D coordinate in camera space
    cam_coord = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [x, y], dis)
    
    # Return a 3D coordinate object that contains X, Y and Z values
    return cam_coord, dis



if __name__ == "__main__":
    # initialize the d455 camera
    pipeline, profile, align = init_d455()
    while True:
        # get the depth and color frames
        depth_frame, color_frame, depth_intrinsics, color_intrinsics = get_frame(pipeline, align)
        
        # if either frame is invalid, skip this iteration
        if depth_frame is None or depth_frame is None:
            continue
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # get the 3D coordinate of the center of the image
        cam_coord, dis = get_3d_coordinate(depth_frame, 320, 240, depth_intrinsics)
        
        # draw a circle at the center of the image
        cv2.circle(color_image, (320,240), 8, [255,0,255], thickness=-1)
        
        # display the distance, X, Y, and Z coordinates of the center of the image
        cv2.putText(color_image,"Dis:"+str(dis)+" m", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
        cv2.putText(color_image,"X:"+str(cam_coord[0])+" m", (80,80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(color_image,"Y:"+str(cam_coord[1])+" m", (80,120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(color_image,"Z:"+str(cam_coord[2])+" m", (80,160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])

        # display the color image
        cv2.imshow('color', color_image)
        
        # quit when press q
        if cv2.waitKey (1) & 0xFF == ord ('q'): 
            break

                
    