from PIL import Image
import numpy as np


def get_changed_touche(color: tuple, bg_color: tuple, img):
    """Will return an image with same bg_color and change everything else to color"""

    load = img.load()

    pic = []
    for j in range(img.height):
        l = []
        for i in range(img.width):
            px = load[i, j]
            l.append(
                px if px == bg_color else color)
        pic.append(l)

    im = Image.fromarray(np.array(pic, dtype=np.uint8))
    return im
