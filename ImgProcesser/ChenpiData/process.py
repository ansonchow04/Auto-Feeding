from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    # 加载 1.bmp，并将其平铺拼接成 4x4 的大图后显示
    img_path = Path(__file__).with_name("1.bmp")
    img = plt.imread(str(img_path))

    # img 可能是 (H,W) 灰度或 (H,W,C) 彩色；分别处理 tile 的 reps
    reps = (4, 4) if img.ndim == 2 else (4, 4, 1)
    tiled = np.tile(img, reps)

    fig, ax = plt.subplots()
    if tiled.ndim == 2:
        ax.imshow(tiled, cmap="gray")
    else:
        ax.imshow(tiled)
    ax.axis("off")
    fig.tight_layout(pad=0)

    # 注意：很多后端在 plt.show() 之后会关闭/清空当前图像，导致 savefig 变成“全白”。
    fig.savefig("tiled_image.png", dpi=600, bbox_inches="tight", pad_inches=0)
    plt.show()


if __name__ == "__main__":
    main()