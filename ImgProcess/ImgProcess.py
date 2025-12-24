import cv2
import numpy as np
import matplotlib.pyplot as plt

class Img:
    def __init__(self, path=None, data=None):
        if path is not None:
            img = cv2.imread(path)
            assert img is not None, "Image not found at the specified path."
            self.data = img
        else:
            self.data = data
    
    def copy(self):
        """Return a copy of the image object."""
        return Img(data=self.data.copy())

    def gray(self):
        """Convert image to grayscale."""
        if len(self.data.shape) == 3:
            img_ = self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return self

    def invert(self):
        """Invert the image (Black <-> White)."""
        self.data = cv2.bitwise_not(self.data)
        return self

    def blur(self, method="gaussian", ksize=5):
        """Apply blurring to the image."""
        if method == "gaussian":
            self.data = cv2.GaussianBlur(self.data, (ksize, ksize), 0)
        elif method == "median":
            self.data = cv2.medianBlur(self.data, ksize)
        return self

    def show(self, cmap="gray", title=None):
        """Display the image."""
        plt.imshow(self.data, cmap=cmap)
        if title:
            plt.title(title)
        plt.axis("off")
        # plt.show()
        return self
    
    def threshold(self, thresh=128):
        """Apply global thresholding to the image."""
        _, self.data = cv2.threshold(
            self.data, thresh, 255, cv2.THRESH_BINARY
        )
        return self

    def otsu(self, inverse=False):
        """Apply Otsu's thresholding. 
           inverse=True produces White Object on Black Background (recommended for morphology).
        """
        flag = cv2.THRESH_BINARY_INV if inverse else cv2.THRESH_BINARY
        _, self.data = cv2.threshold(
            self.data, 0, 255,
            flag + cv2.THRESH_OTSU
        )
        return self

    def adaptive(self, block=11, C=2, inverse=True):
        """
        Apply adaptive thresholding.
        inverse=True: 适合【白底黑物】的图，处理后物体变白，背景变黑。
        block: 邻域大小，必须是奇数 (如 11, 21, 31, 55...)。
        C: 阈值减去的常数，用来控制敏感度。
        """
        method = cv2.THRESH_BINARY_INV if inverse else cv2.THRESH_BINARY
        self.data = cv2.adaptiveThreshold(
            self.data, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, # 或者 cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            method,
            block, C
        )
        return self
    
    def close(self, ksize=3, shape="rect"):
        """Apply morphological closing to the image."""
        if len(self.data.shape) != 2:
            raise ValueError("Morphological operations require a binary image.")
        if shape == "rect":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
        elif shape == "ellipse":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        else:
            raise ValueError("Unsupported shape type.")
        self.data = cv2.morphologyEx(self.data, cv2.MORPH_CLOSE, kernel)
        return self

    def open(self, ksize=3, shape="rect"):
        """Apply morphological opening to the image."""
        if len(self.data.shape) != 2:
            raise ValueError("Morphological operations require a binary image.")
        if shape == "rect":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
        elif shape == "ellipse":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        else:
            raise ValueError("Unsupported shape type.")
        self.data = cv2.morphologyEx(self.data, cv2.MORPH_OPEN, kernel)
        return self

    def remove_small_objects(self, min_area=200):
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            self.data, connectivity=8
        )
        new_img = self.data.copy()
        for i in range(1, num_labels):  # 0是背景
            area = stats[i, cv2.CC_STAT_AREA]
            if area < min_area:
                new_img[labels == i] = 0
        self.data = new_img
        return self
    
    def centroid(self, min_area=300, draw=True):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            self.data, connectivity=8
        )
        max_area = 0
        target_idx = -1
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area < min_area:
                continue
            if area > max_area:
                max_area = area
                target_idx = i
        if target_idx == -1:
            return None
        cx, cy = centroids[target_idx]
        cx, cy = int(cx), int(cy)
        if draw:
            vis = cv2.cvtColor(self.data, cv2.COLOR_GRAY2BGR)
            cv2.drawMarker(
                vis,
                (cx, cy),
                (255, 0, 0),
                markerType=cv2.MARKER_TILTED_CROSS,
                markerSize=12,
                thickness=2
            )
            self.data = vis
        return (cx, cy)

if __name__ == "__main__":
    img = Img(path='datasetALL/1.bmp')

    plt.figure(figsize=(12, 8))

    # Original Image
    plt.subplot(2, 2, 1)
    img.show(title="Original")

    # Grayscale Conversion & Median Blurring
    plt.subplot(2, 2, 2)
    img.gray()\
       .blur(method="median", ksize=5)\
       .show(title="Gray + Median Blur")

    # Otsu's Thresholding
    plt.subplot(2, 2, 3)
    img.otsu(inverse=True)\
       .show(title="Otsu Thresholding")
    
    # Centroid Detection
    plt.subplot(2, 2, 4)
    coord = img.centroid(min_area=50000, draw=True)
    img.show(title="Centroid Detection")
    print(f"Centroid Coordinates: {coord}")

    #save processed image
    cv2.imwrite('processed_image.bmp', img.data)

    plt.tight_layout()
    plt.show()