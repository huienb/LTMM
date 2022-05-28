from rc4 import RC4_IMAGE
import cv2 as cv
import math
import numpy as np


img = cv.imread("./Z_Zn.png", 0)
print(type(img[0, 0]))
shape = img.shape
print(shape)
myRC4 = RC4_IMAGE(img, 'HMS')
result = myRC4.encrypt().reshape(shape)
cv.imshow("OK", result)
decrypt = myRC4.decrypt(result).reshape(shape)
cv.imshow("FROG", decrypt)
# print(img.shape)

cv.waitKey(0);
cv.destroyAllWindows()