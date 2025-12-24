from device import device
from device import ACTION
import time

# 目标设备地址（请根据实际设备修改）
HOST = "192.168.60.69"
PORT = "502"

with device(HOST, PORT) as d:
    d.platform.set_gather(vertical_time=1, horizontal_time=1, total_time=4)
    d.platform.set_special_action(action=ACTION.CENTER_HORIZONTAL, voltage=22, frequency=90, time_sec=5)
    d.platform.set_special_action(action=ACTION.CENTER_VERTICAL, voltage=22, frequency=60, time_sec=5)
    d.platform.set_directional_action(direction=ACTION.UP, voltage=20, frequency=50, time_sec=5)
    d.platform.stop()