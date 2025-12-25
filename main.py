from Camera.myCamera import Camera
from HostContrller.device import device
from ImgProcesser.ImgProcesser import Img
from RobotServer.RobotServer import RobotServer

import time
import matplotlib.pyplot as plt

HOST_device = '192.168.60.69'
PORT_device = '502'
HOST_robot = '192.168.60.1'
PORT_robot = '8080'

ctrlboard = device(host=HOST_device, port=PORT_device)
robot = RobotServer(host=HOST_robot, port=PORT_robot)
robot.start()
camera = Camera()

img = Img(data=camera.capture())
robot.coords_append(img.centroid(min_area=50000, draw=True))

while True:
    if len(robot.coords) < 3:
        
    robot.run_once()
    time.sleep(0.1)
