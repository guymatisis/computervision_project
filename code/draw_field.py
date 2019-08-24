import numpy as np
import cv2

vert_multiply = 5
vert_add = 10
hor_multiply = 5
hor_add = -10
img_height = hor_multiply * 63 - 2 * hor_add
img_width = vert_multiply * 91 + 2 * vert_add
xpts = {6: 0 * vert_multiply + vert_add, 7: 5 * vert_multiply + vert_add, 8: 27 * vert_multiply + vert_add,
        9: 36.5 * vert_multiply + vert_add, 10: 46.5 * vert_multiply + vert_add, 11: 56.5 * vert_multiply + vert_add,
        12: 66 * vert_multiply + vert_add, 13: 86 * vert_multiply + vert_add, 14: 91 * vert_multiply + vert_add}
ypts = {10: img_height - (5 * hor_multiply) + hor_add, 9: img_height - (15 * hor_multiply) + hor_add,
        11: img_height + hor_add, 8: img_height - ((63 - 15) * hor_multiply) + hor_add,
        7: img_height - ((63 - 5) * hor_multiply) + hor_add, 6: img_height - (63 * hor_multiply) + hor_add}


def draw_field(id_left, id_right):
    new_image = np.zeros((img_height, img_width, 3), np.uint8)
    for x in range(id_left, id_right + 1):
        cv2.line(new_image, (int(xpts[x]), int(ypts[11])), (int(xpts[x]), int(ypts[6])), [255, 100, 100], 5)
    cv2.line(new_image, (int(xpts[id_left]), int(ypts[11])), (int(xpts[id_right]), int(ypts[11])), [255, 100, 100], 5)
    cv2.line(new_image, (int(xpts[id_left]), int(ypts[6])), (int(xpts[id_right]), int(ypts[6])), [255, 100, 100], 5)
    return new_image
