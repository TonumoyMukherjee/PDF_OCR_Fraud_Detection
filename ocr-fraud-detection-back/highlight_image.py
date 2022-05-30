import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import imageio
# read image
image = imageio.v2.imread("output_000.jpg")
# image dimention
image_height = image.shape[0]
image_width = image.shape[1]
print(image_height, image_width)
# highlight array
highlight_points = [[3300,620],[4500,620]]

plt.imshow(image)
ax.imshow(image)
ax = plt.gca()

for i in highlight_points:
    print(i[0])
    rect = patches.Rectangle((0,i[0]),
                     image_width,
                     200,
                     alpha=0.3,
                     linewidth=0,
                     color='red',
                     fill = True)
    ax.add_patch(rect)
    
    
# plt.show()
plt.imsave('foo.jpg',image)
# mpimg.imsave("out.png", image)