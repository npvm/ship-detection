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

    def virus(self, upper_corner, lower_corner, upper_intensity=150, lower_intensity=100):
        start = time.time()

        print('Starting search...')

        x1, y1 = upper_corner
        x2, y2 = lower_corner

        image = self.img[y1:y2, x1:x2]

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
                                        if image[wy + dy][wx + dx] >= lower_intensity:
                                            if (wx + dx, wy + dy) not in whitelist:
                                                whitelist.append((wx + dx, wy + dy))

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

    def kassertilnicolai(self, upper_corner, lower_corner, upper_intensity=150, lower_intensity=100):
        kasser = []
        ships, shipborders, nothing = self.virus(upper_corner, lower_corner, upper_intensity=150, lower_intensity=100)
        for borders in shipborders:
            max_x = max(borders, key=lambda item: item[0])[0]
            min_x = min(borders, key=lambda item: item[0])[0]

            max_y = max(borders, key=lambda item: item[1])[1]
            min_y = min(borders, key=lambda item: item[1])[1]

            kasser.append([(min_x, min_y), (max_x, max_y)])
        return kasser

    def plotkasser(self, upper_corner, lower_corner, upper_intensity=150, lower_intensity=100):
        kasser = self.kassertilnicolai(upper_corner, lower_corner, upper_intensity=150, lower_intensity=100)
        print('Plotting...')
        image = self.img
        for i, coords in enumerate(kasser):
            upper, lower = coords
            x1, y1 = upper
            x2, y2 = lower
            plt.subplot(2, 1, i+1)
            plt.imshow(image[y1:y2, x1:x2], cmap='gray')
        plt.show()

    def plotborders(self, upper_corner, lower_corner, upper_intensity=150, lower_intensity=100):
        ships, shipborders, nothing = self.virus(upper_corner, lower_corner, upper_intensity=150, lower_intensity=100)
        print('Plotting...')
        image = self.img
        for ship in shipborders:
            for coords in ship:
                x, y = coords
                image[y][x] = 500
        x1, y1 = upper_corner
        x2, y2 = lower_corner
        imageshow = self.img[y1:y2, x1:x2]
        plt.imshow(imageshow, cmap='gray')
        plt.show()

img = ImageHandler('s1a-iw-grd-vh-20160822t170151-20160822t170216-012716-013ff7-002.tiff')

img.plotkasser((0,0),(5000,5000))



