import pyrealsense2 as rs
import numpy as np
import cv2

def init_d455(id = None, width = 640, height = 480, fps = 15):
    '''
    init d455 depth camera. 
    low fps may cause error
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
    
    # # Set the config parameters for the specified device
    # config.enable_device(device.get_info(rs.camera_info.serial_number))
    
    # Enable depth stream, format z16 (16-bit unsigned integer)
    config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
    config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)
    
    # Start the pipeline and return a profile object
    profile = pipeline.start(config)

    # # get depth scale
    # depth_scale = profile.device.first_depth_sensor().get_depth_scale()
    
    # Print some device information and profile information
    # print("Initialized device:", device.get_info(rs.camera_info.name))
    # print("Started depth stream:", profile.get_stream(rs.stream.depth))

    # 创建对齐对象与color流对齐
    align_to = rs.stream.color      
    align = rs.align(align_to)      

    return pipeline, profile, align

def get_frame(pipeline, align):
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
    # x and y are the pixel coordinates
    
    # Get depth value at pixel coordinate (x, y)
    dis = aligned_depth_frame.get_distance(x, y)
    
    # Convert pixel coordinate to 3D coordinate in camera space
    cam_coord = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [x, y], dis)
    
    # Return a 3D coordinate object that contains X, Y and Z values
    return cam_coord, dis


if __name__ == "__main__":
    pipeline, profile, align = init_d455()
    while True:
        depth_frame, color_frame, depth_intrinsics, color_intrinsics = get_frame(pipeline, align)
        
        if depth_frame is None or depth_frame is None:
            continue
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        cam_coord, dis = get_3d_coordinate(depth_frame, 320, 240, depth_intrinsics)
        
        
        cv2.circle(color_image, (320,240), 8, [255,0,255], thickness=-1)
        cv2.putText(color_image,"Dis:"+str(dis)+" m", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
        cv2.putText(color_image,"X:"+str(cam_coord[0])+" m", (80,80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(color_image,"Y:"+str(cam_coord[1])+" m", (80,120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(color_image,"Z:"+str(cam_coord[2])+" m", (80,160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])

        cv2.imshow('color', color_image)
        # quit when press q
        if cv2.waitKey (1) & 0xFF == ord ('q'): 
            break
                
    