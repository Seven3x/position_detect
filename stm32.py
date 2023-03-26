import serial
import struct
import pyrealsense2 as rs

def ser_init(com = 'COM3', baudrate = 115200, timeout = 0):
    """
    Initializes a serial object with the specified port name, baud rate, and timeout.

    Args:
        com (str): The name of the serial port to use. Default is 'COM3'.
        baudrate (int): The baud rate to use. Default is 115200.
        timeout (float): The timeout value in seconds. Default is 0.

    Returns:
        serial.Serial: A serial object with the specified settings.
    """
    # Create a serial object with the port name and baud rate
    ser = serial.Serial(com, 9600, timeout= 0)
    return ser


def send_3d_coordinate(ser , coord, debug = False):
    """
    Sends a 3D coordinate to the specified serial port.

    Args:
        ser (serial.Serial): The serial port to send the coordinate to.
        coord (list): A list containing the x, y, and z values of the coordinate.
        debug (bool): Whether or not to print the data being sent. Default is False.
    """
    # Convert the coordinate values to bytes using struct.pack
    # Use '<fff' as the format string for little-endian float values
    data = struct.pack('<hhh', int(coord[0]*1000), int(coord[1]*1000), int(coord[2]*1000))
    
    if debug:
        print(data)
    
    # Write the data to the serial port
    ser.write(data)

    

    
if __name__ == "__main__":
    # create and init
    ser = ser_init(com='COM7')
    
    # test set
    crood = [0,1,2]
    
    # send message
    send_3d_coordinate(ser, crood)
    