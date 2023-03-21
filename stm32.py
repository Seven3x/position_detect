import serial
import struct

def ser_init(com = 'COM3', baudrate = 115200, timeout = 0):
    # Create a serial object with the port name and baud rate
    ser = serial.Serial('COM3', 9600, timeout= 0)

# Define a function that takes a 3D coordinate as an argument and sends it to the serial port
def send_3d_coordinate(coord):
    # Convert the coordinate values to bytes using struct.pack
    # Use '<fff' as the format string for little-endian float values
    data = struct.pack('<fff', coord.X, coord.Y, coord.Z)
    
    # Write the data to the serial port
    ser.write(data)