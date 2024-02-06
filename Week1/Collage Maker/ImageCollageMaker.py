import cv2
import numpy as np
import glob


collage_width = 800
collage_height = 600


image_paths = glob.glob("images/*.jpg") + glob.glob("images/*.jpeg") + glob.glob("images/*.png")
images = []
for path in image_paths:
    image = cv2.imread(path)
    images.append(image)


resized_images = []
for image in images:
    resized_image = cv2.resize(image, (collage_width // len(images), collage_height))
    resized_images.append(resized_image)


collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)


x_offset = 0
for image in resized_images:
    collage[:, x_offset:x_offset + image.shape[1]] = image
    x_offset += image.shape[1]


cv2.imshow("Collage Maker", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
