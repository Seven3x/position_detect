# position_detect

## Introduction
This project aims to detect the real-time position of a ping pong ball and send the coordinates to a microcontroller. The system uses a Realsense camera to capture the ball's position and a computer vision algorithm to track its position. The coordinates are then sent to the microcontroller via a serial port.

## Installation
To use this project, you will need to install the following dependencies:
- Python 3.6 or higher
- OpenCV
- PySerial
- Pyrealsense2
- Numpy

You can install OpenCV and PySerial using pip:
```
pip install opencv-python
pip install numpy
pip install pyserial
pip install pyrealsense2
```

## Usage
To run the program, simply execute the following command:
```
python main.py
```

The program will start capturing video from your default camera and detecting the position of the ping pong ball. The coordinates will be sent to the microcontroller via the serial port.

### Serial Communication
The coordinates of the ping pong ball are sent to the microcontroller via a serial port. 
You can configure the serial port used by modifying the `serial_port` parameter in the `main.py` file.
During communication, 7 bytes are sent at a time: the first byte is the frame header `0x11`, and every two bytes after that represent the coordinates of an axis. The order of the coordinates is x, y, and z. The data type is integer and the unit is millimeters. If you need to change the data type being sent, you can modify the `stm32.py` file.

## Configuration
You can configure the program by modifying the global paraments in `main.py` file. Here are some of the parameters you can change:
- `debug`: Set to True to enable debug mode.
- `houghparam1`: The first threshold for the circle detection algorithm.
- `houghparam2`: The second threshold for the circle detection algorithm.
- `lower_limit`: The lower limit for the color range used to detect the ball.
- `upper_limit`: The upper limit for the color range used to detect the ball.
- `serial_port`: The serial port used to communicate with the microcontroller.

## Credits
This project was created by MagiL0 . If you have any questions or suggestions, please feel free to contact me at fengmagil@gmail.com.