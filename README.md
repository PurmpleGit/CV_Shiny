# What is this?
This is the point-in-time source code for the video [ Using Computer Vision to Catch Shiny Pokemon in Pokemon Ruby ](https://www.youtube.com/watch?v=VRqTQQnRZxk).

This requires a capture card / webcam to run.

# How to Use

## Arduino

Code is located at 

> arduino/controller.ino

Upload using the default Arduino IDE.

## Python State Machine
Installation:
```
pip install -r ./requirements.txt
```
Running:
```
python opencv/main.py
```
The Python will not run unless it connect to a COM Port for Windows. If this is the reason you get a startup failure, adjust the COM port used in controller.py line 21.
