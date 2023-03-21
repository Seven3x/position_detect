import pyrealsense2 as rs
import numpy as np
import cv2

def init_d455(id = None, width = 640, height = 480, fps = 30):
    '''
    init d455 depth camera. 
    '''
    
    # Create a context object, which manages all connected realsense devices
    context = rs.context()
    
    # Get the device list
    devices = context.query_devices()
    
    # If no device is connected, exit the program
    if len(devices) == 0:
        print("No device found")
        exit(0)
    
    # Select the device 
    device = devices[0]
    
    # Create a pipeline object, which configures and starts the data streams
    pipeline = rs.pipeline(context)
    
    # Create a config object, which specifies the streams and formats you want to open
    config = rs.config()
    
    # Set the config parameters for the specified device
    config.enable_device(device.get_info(rs.camera_info.serial_number))
    
    # Enable depth stream, format z16 (16-bit unsigned integer)
    config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
    
    # Start the pipeline and return a profile object
    profile = pipeline.start(config)

    # get intrinsics of the depth camera
    depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
    # get intrinsics of the color camera
    color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
    # get depth scale
    depth_scale = pipeline.profile.device.first_depth_sensor().get_depth_scale()
    
    # Print some device information and profile information
    # print("Initialized device:", device.get_info(rs.camera_info.name))
    # print("Started depth stream:", profile.get_stream(rs.stream.depth))

    return pipeline, depth_intrinsics, color_intrinsics, depth_scale

def get_frame(pipeline):
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    
    # Get depth frame and color frame
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    
    # Validate that both frames are valid
    if not depth_frame or not color_frame:
        return None, None
    
    # Convert images to numpy arrays
    # depth_image = np.asanyarray(depth_frame.get_data())
    # color_image = np.asanyarray(color_frame.get_data())
    
    # Return a frame object that contains both images
    return depth_frame, color_frame


def get_3d_coordinate(depth_frame, x, y, depth_scale):
    # x and y are the pixel coordinates

    # Get depth intrinsics
    depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
    
    
    # Get depth value at pixel coordinate (x, y)
    z = depth_frame.get_distance(x, y) * depth_scale
    
    # Convert pixel coordinate to 3D coordinate in camera space
    X, Y, Z = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [x, y], z)
    
    # Return a 3D coordinate object that contains X, Y and Z values
    return rs.coordinate((X, Y, Z)) 