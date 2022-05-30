from rc4 import RC4_IMAGE
import cv2 as cv
import math
import numpy as np


img = cv.imread("./ANH/Team3.png", 0)
cv.imshow("input img", img)
print(type(img[0, 0]))
shape = img.shape
print(shape)
myRC4 = RC4_IMAGE(img, 'HMS')
result = myRC4.encrypt().reshape(shape)
cv.imshow("Encrypted img", result)
decrypt = myRC4.decrypt(result).reshape(shape)
cv.imshow("Decrypted img", decrypt)
# print(img.shape)

cv.waitKey(0);
cv.destroyAllWindows()