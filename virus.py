import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import time

class ImageHandler:
    def __init__(self, f):
        """
        :param f: Filepath or name for image
        """
        # Filename
        self.filename = f

        self.img = tiff.imread(self.filename)
        self.img_size = self.img.size  # Size of image
        self.img_shape = self.img.shape # Image shape
        self.height, self.width = self.img_shape
        self.img_datatype = self.img.dtype

    def get_properties(self):
        print("-" * 32 + "\nFile: {0}\nSize: {1}\nData type: {2}\nShape: {3}\nDimensions: w {4} x h {5}\n".format(
            self.filename,
            self.img_size,
            self.img_datatype,
            self.img_shape,
            self.width,
            self.height)
              + "-" * 32)

    def data(self):
        return self.img

    def find_pixel(self, x, y):
        if self.width >= x and self.height >= y:
            return self.img[y][x]

    def square_image(self, corner_1, corner_2, convert_to_np=True):

        final_array = []
        pixels = []

        c1_x = corner_1[0]
        c1_y = corner_1[1]

        c2_x = corner_2[0]
        c2_y = corner_2[1]

        max_h = max(c2_y, c1_y)
        max_w = max(c2_x, c1_x)

        i_x = min(c2_x, c1_x)
        i_y = min(c2_y, c1_y)

        while i_x <= max_w and i_y <= max_h:

            pixels.append(self.find_pixel(i_x, i_y))
            if i_x == max_w:
                # Appends the pixels
                final_array.append(pixels)
                # Resets the array
                pixels = []
                # New y direction to check
                i_y += 1
                # Resets i_x so it can loop through the new y direction
                i_x = min(c2_x, c1_x)
            else:
                i_x += 1

        if convert_to_np:
            np_array = np.array(final_array, dtype=float)
            return np_array
        else:
            return final_array

imh = ImageHandler('s1a-iw-grd-vh-20160822t170151-20160822t170216-012716-013ff7-002.tiff')


def virus(image, upper_intensity = 150, lower_intensity = 100):
    start = time.time()

    print('Starting search...')

    shipborders = []
    ships = []

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    for cy, y in enumerate(image):

        whitelist = []
        blacklist = []

        for cx, x in enumerate(y):

            if x > upper_intensity:
                if not any((cx, cy) in ship for ship in ships):

                    whitelist.append((cx, cy))

                    while True:
                        for coords in whitelist:

                            wx, wy = coords

                            for direction in directions:
                                dy, dx = direction

                                try:
                                    if image[wy+dy][wx+dx] >= lower_intensity:
                                        if (wx+dx, wy+dy) not in whitelist:

                                            whitelist.append((wx+dx, wy+dy))

                                    else:
                                        if (wx + dx, wy + dy) not in blacklist:

                                            blacklist.append((wx + dx, wy + dy))

                                except IndexError:
                                    pass
                        else:
                            break

                    ships.append(whitelist)
                    shipborders.append(blacklist)
                    print('=> Possible ship has been located')

        end = time.time()

    return ships, shipborders, print(str(len(ships)) + " ships found in " + str(end - start) + " seconds")


def kassertilnicolai(image, upper_intensity = 150, lower_intensity = 100):
    kasser = []
    ships, shipborders, nothing = virus(image, upper_intensity = 150, lower_intensity = 100)
    for borders in shipborders:
        max_x = max(borders, key=lambda item: item[0])[0]
        min_x = min(borders, key=lambda item: item[0])[0]

        max_y = max(borders, key=lambda item: item[1])[1]
        min_y = min(borders, key=lambda item: item[1])[1]

        kasser.append([(min_x, min_y), (max_x, max_y)])
    return kasser





#image = imh.square_image((9523-30, 805+30), (9960+30, 365-20),convert_to_np=False)
image = imh.square_image((0, 0), (5000, 5000),convert_to_np=False)

kasser = kassertilnicolai(image)

print(kasser)
"""
for i in range(len(shipborders)):
    for ele in shipborders[i]:
        x, y = ele
        image[y][x] = 400
"""

x_kasse, y_kasse = kasser[0]

kasse = imh.square_image(x_kasse, y_kasse)

plt.imshow(kasse,cmap='gray')
plt.show()



