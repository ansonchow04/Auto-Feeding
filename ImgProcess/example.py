from ImgProcess import Img
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

coords = list()

for i in tqdm(range(1, 114)):
# if True:
    # i = 50
    img_path = f'datasetALL/{i}.bmp'
    img = Img(path=img_path)
    plt.figure()

    plt.subplot(1, 2, 1)
    img.show(title="Original")

    plt.subplot(1, 2, 2)
    img.gray().\
        blur(method="median", ksize=5).\
        otsu(inverse=True).\
        open(ksize=3, shape="ellipse").\
        remove_small_objects(min_area=50000)
    coords.append(img.centroid(min_area=50000, draw=True))
    img.show(title="Processed")
    
    plt.tight_layout()
    plt.savefig(f'processed_image/processed_{i}{coords[-1]}.jpg', dpi=600)
    # plt.show()
    plt.close()

# print(coords)