import cv2
import numpy as np


def filter(frame, lower, upper, mov_left, mov_right):
    # --------IMG MINUS GAUSSIAN BLUR/ WHITE FILTER----------
    gaus_blur = cv2.GaussianBlur(frame, (15, 1), 0)
    img_min_gaus = cv2.subtract(frame, gaus_blur)
    white_filter = cv2.inRange(img_min_gaus, lower, upper)

    # --------- OPENING AND CLOSING---------------------
    kernel_hor = kernel_hor1 = np.ones((1, 3), np.uint8)
    kernel_ver = np.ones((3, 1), np.uint8)
    dialate_iterations = 20
    kernel_reg = np.ones((3, 3), np.uint8)
    mod_image = np.copy(white_filter)
    if (mov_left):
        dialate_iterations = 2
        kernel_hor = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
                               ]
                              , np.uint8)
    if (mov_right):
        dialate_iterations = 2
        kernel_hor = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                               ]
                              , np.uint8)

    mod_image_hor = cv2.erode(mod_image, kernel_hor1, iterations=1)
    mod_image_hor = cv2.dilate(mod_image_hor, kernel_hor, iterations=dialate_iterations)
    mod_image_hor = cv2.erode(mod_image_hor, kernel_hor1, iterations=1)
    mod_image_ver = cv2.erode(mod_image, kernel_ver, iterations=1)
    mod_image_ver = cv2.dilate(mod_image_ver, kernel_reg, iterations=2)

    return mod_image_hor, mod_image_ver, white_filter
