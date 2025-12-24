from Camera.myCamera import Camera
from HostContrller.device import device
from ImgProcesser.ImgProcesser import Img
from RobotServer.RobotServer import RobotServer

HOST_device = '192.168.60.69'
PORT_device = '502'
HOST_robot = '192.168.60.68'
PORT_robot = '8080'

# 
device = device(HOST_device, PORT_device)
# robot = RobotServer(HOST_robot, PORT_robot)

