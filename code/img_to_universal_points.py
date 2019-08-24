import numpy as np
import temp_line
import globals
import draw_field


# -------------------------------    FUNCTIONS   -----------------------------------------


def find_points_on_field(moving_left, moving_right):
    # FIND  VERTICAL LINES FARTHEST APART
    if (moving_left or moving_right):
        vline_right = [(line.mid_pt, line.slope, line.ID) for line in temp_line.temp_ver_lines_list if line.ID == max(
            [l.ID for l in temp_line.temp_ver_lines_list if l.ID != 0 and l.ID > 5 and l.ID < 15])][0]
        vline_left = [(line2.mid_pt, line2.slope, line2.ID) for line2 in temp_line.temp_ver_lines_list if
                      line2.ID == min([l.ID for l in temp_line.temp_ver_lines_list if l.ID != 0])][0]
        bottom_mid_pt, hor_slope_bot, hor_ID_bott = \
        [(line.mid_pt, line.slope, line.ID) for line in temp_line.temp_hor_lines_list if (line.ID == 10)][0]
        top_mid_pt, hor_slope_top, hor_ID_top = \
        [(line.mid_pt, line.slope, line.ID) for line in temp_line.temp_hor_lines_list if (line.ID == 9)][0]

    else:
        vline_right = [(line.pt1, line.slope, line.ID) for line in temp_line.temp_ver_lines_list if
                       line.ID == max([l.ID for l in temp_line.temp_ver_lines_list if l.ID != 0])][0]
        vline_left = [(line2.pt1, line2.slope, line2.ID) for line2 in temp_line.temp_ver_lines_list if
                      line2.ID == min([l.ID for l in temp_line.temp_ver_lines_list if l.ID != 0])][0]
        bottom_mid_pt, hor_slope_bot, hor_ID_bott = \
        [(line.pt1, line.slope, line.ID) for line in temp_line.temp_hor_lines_list if (line.ID == 10)][0]
        top_mid_pt, hor_slope_top, hor_ID_top = \
        [(line.pt1, line.slope, line.ID) for line in temp_line.temp_hor_lines_list if (line.ID == 9)][0]

    left_pt, ver_slope_left, ver_ID_left = vline_left
    right_pt, ver_slope_right, ver_ID_right = vline_right

    drawn_field = draw_field.draw_field(ver_ID_left, ver_ID_right)

    int_bot_left = (x, y) = line_intersection(left_pt, ver_slope_left, bottom_mid_pt, hor_slope_bot)
    int_top_left = (x, y) = line_intersection(left_pt, ver_slope_left, top_mid_pt, hor_slope_top)
    int_top_right = (x, y) = line_intersection(right_pt, ver_slope_right, top_mid_pt, hor_slope_top)
    int_bot_right = (x, y) = line_intersection(right_pt, ver_slope_right, bottom_mid_pt, hor_slope_bot)
    src_pts = np.array([[int_bot_left], [int_top_left], [int_top_right], [int_bot_right]])

    vscale = 3
    hscale = 10
    ver_line_des_pts = {6: 0 * vscale, 7: 5 * vscale, 8: 27 * vscale, 9: 36.5 * vscale, 10: 46.5 * vscale,
                        11: 56.5 * vscale, 12: 66 * vscale, 13: 86 * vscale, 14: 91 * vscale}
    hor_line_des_pts = {10: globals.img_height_scale - (5 * hscale), 9: globals.img_height_scale - (15 * hscale)}

    des_pts = np.array([[ver_line_des_pts[ver_ID_left],
                         hor_line_des_pts[hor_ID_bott]],
                        [ver_line_des_pts[ver_ID_left],
                         hor_line_des_pts[hor_ID_top]],
                        [ver_line_des_pts[ver_ID_right],
                         hor_line_des_pts[hor_ID_top]],
                        [ver_line_des_pts[ver_ID_right],
                         hor_line_des_pts[hor_ID_bott]]])
    return src_pts, des_pts, drawn_field


def line_intersection(p1, m1, p2, m2):
    x = (m1 * p1.x - m2 * p2.x - p1.y + p2.y) / (m1 - m2)
    y = m1 * (x - p1.x) + p1.y
    return x, y
