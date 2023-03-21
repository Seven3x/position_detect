import pingpang
import rspoint
import stm32


if __name__ == "__main__":
    pipeline, depth_intrinsics, color_intrinsics, depth_scale = rspoint.init_d455()
    color_frame, depth_frame = rspoint.get_frame(pipeline= pipeline)
    
    # detect pingpang
    balls = pingpang.detect_ping_pong_balls(color_frame)
    
    # only use the first one
    x = int(balls[0][0])
    y = int(balls[0][1])
    r = int(balls[0][2])
    
    # transfer to x,y,z
    coordinate = rspoint.get_3d_coordinate(depth_frame, x, y, depth_scale)
    
    stm32.send_3d_coordinate(coord= coordinate)
    
    
    
    