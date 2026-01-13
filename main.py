from Camera.myCamera import Camera
from HostContrller.device import device
from ImgProcesser.ImgProcesser import Img
from RobotServer.RobotServer import RobotServer

import time
import matplotlib.pyplot as plt
import random

HOST_device = '192.168.60.69'
PORT_device = '502'
HOST_robot = '192.168.60.1'
PORT_robot = '8080'

if True:
    ctrlboard = device(host=HOST_device, port=PORT_device)
    ctrlboard.hopper_relay.open()
    time.sleep(2)
    ctrlboard.hopper_relay.close()
    

if False:
    ctrlboard = device(host=HOST_device, port=PORT_device)
    robot = RobotServer(host=HOST_robot, port=PORT_robot)
    robot.start()
    camera = Camera()

    # img = Img(data=camera.capture())
    # robot.coords_append(img.centroid(min_area=50000, draw=True))

    while True:
        if len(robot.coords) < 3:
            for i in range(10):
                robot.coords_append([random.randint(0, 100), random.randint(0, 100), -100]) # const 100
                # here, method should not be append, because after zhensan, coords before is not valid anymore
                # the correct way is: clear -> append
        
        # robot.coords_print()
        # print(robot.coords_pop())
        robot.run_once()
        time.sleep(0.1)
