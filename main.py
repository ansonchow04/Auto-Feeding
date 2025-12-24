from Camera.myCamera import Camera
from HostContrller.device import device
from ImgProcesser.ImgProcesser import Img
from RobotServer.RobotServer import RobotServer

import time

HOST_device = '192.168.60.69'
PORT_device = '502'
HOST_robot = '192.168.60.1'
PORT_robot = '8080'

# device = device(host=HOST_device, port=PORT_device)
# robot = RobotServer(host=HOST_robot, port=PORT_robot)
# robot.start()
camera = Camera()
camera.save(filename='test.bmp')

# while True:
#     robot.run_once()
#     time.sleep(1)

