from myCamera import Camera
import matplotlib.pyplot as plt

# 使用 with 语句自动管理资源
with Camera() as cam:
    # show image
    frame = cam.save(filename="captured_image.bmp")