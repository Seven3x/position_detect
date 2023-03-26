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

    # This line of code packs the x, y, and z values of a 3D coordinate into a byte string using struct.pack.
    # The format string '<bhhh' specifies that the values should be packed as little-endian short integers.
    # The first value in the byte string is a hex value of 0x11, which is used to indicate the start of a new message.
    # The next three values are the x, y, and z values of the coordinate, multiplied by 1000 and converted to integers.
    data = struct.pack('<bhhh', 0x11, int(coord[0]*1000), int(coord[1]*1000), int(coord[2]*1000))


    
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
    send_3d_coordinate(ser, crood, debug= True)
    