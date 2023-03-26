import serial
import struct
import pyrealsense2 as rs

def ser_init(com = 'COM3', baudrate = 115200, timeout = 0):
    # Create a serial object with the port name and baud rate
    ser = serial.Serial(com, 9600, timeout= 0)
    return ser

# Define a function that takes a 3D coordinate as an argument and sends it to the serial port
def send_3d_coordinate(ser , coord, debug = False):
    # Convert the coordinate values to bytes using struct.pack
    # Use '<fff' as the format string for little-endian float values
    data = struct.pack('<hhh', int(coord[0]*1000), int(coord[1]*1000), int(coord[2]*1000))
    
    if debug:
        print(data)
    
    # Write the data to the serial port
    ser.write(data)
    

    
if __name__ == "__main__":
    ser = ser_init(com='COM7')
    
    crood = [0,1,2]
    
    send_3d_coordinate(ser, crood)
    