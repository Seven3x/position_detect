import pingpang
import rspoint
import stm32
import numpy as np
import cv2

if __name__ == "__main__":
    # init d455, get info from the camera
    pipeline, profile, align = rspoint.init_d455()
    
    # init transmation between stm32
    # stm32.ser_init('COM3', 115200)
    
    # start to loop
    while True:
        depth_frame, color_frame, depth_intrinsics, color_intrinsics = rspoint.get_frame(pipeline, align)
        
        if depth_frame is None or depth_frame is None:
            continue
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # detect pingpang
        balls = pingpang.detect_ping_pong_balls(color_image)

        # make sure        
        if len(balls) != 0:
            # only use the first pingpang
            (x,y,r) = balls[0]
            color_image = cv2.rectangle(color_image, (x-r,y-r), (x+r,y+r), (0,255,0), 2)
            
            if 0:
                xa, ya, za = (0,0,0)
                dy, dx = int(y-r/2) - int(y+r/2), int(x-r/2) - int(x+r/2)
                for i in range(int(x-r/2),dx):
                    for j in range(int(y-r/2), dy):  
                        cam_coord, dis = rspoint.get_3d_coordinate(depth_frame, i, j, depth_intrinsics)
                        xa = int(cam_coord[0]*100)
                        ya = int(cam_coord[1]*100)
                        za = int(cam_coord[2]*100)
                
                x0 = xa / dx
                y0 = ya / dy
                z0 = ya / dy
            else:
                cam_coord, dis = rspoint.get_3d_coordinate(depth_frame, x, y, depth_intrinsics)
                x0 = int(cam_coord[0]*100)
                y0 = int(cam_coord[1]*100)
                z0 = int(cam_coord[2]*100)

            # transfer to x,y,z
            cv2.putText(color_image,"X:"+str(x0)+" cm", (80,80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
            cv2.putText(color_image,"Y:"+str(y0)+" cm", (80,120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
            cv2.putText(color_image,"Z:"+str(z0)+" cm", (80,160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
            
            print(x0,y0,z0)
            
            # transfer data
            # stm32.send_3d_coordinate(coord= coordinate)
        cv2.imshow('color', color_image)
        # quit when press q
        if cv2.waitKey (1) & 0xFF == ord ('q'): 
            break
    
    
    