import pingpang
import rspoint
import stm32


if __name__ == "__main__":
    # init d455, get info from the camera
    pipeline, depth_intrinsics, color_intrinsics, depth_scale = rspoint.init_d455()
    
    # init transmation between stm32
    stm32.ser_init('COM3', 115200)
    
    # start to loop
    while True:
        # get frame
        color_frame, depth_frame = rspoint.get_frame(pipeline= pipeline)
        
        # detect pingpang
        balls = pingpang.detect_ping_pong_balls(color_frame)
        
        # only use the first pingpang
        x = int(balls[0][0])
        y = int(balls[0][1])
        r = int(balls[0][2])
        
        # transfer to x,y,z
        coordinate = rspoint.get_3d_coordinate(depth_frame, x, y, depth_scale)
        
        # transfer data
        stm32.send_3d_coordinate(coord= coordinate)
        
    
    
    