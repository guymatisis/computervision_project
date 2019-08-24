# -----------------_IMPORTS_-------------------
from __future__ import print_function
from __future__ import division
import cv2
import numpy as np
import temp_line
import perm_line
import point
import img_to_universal_points as ImgToUni
import globals as glob
import image_filtering as imfil
import movement as mov
import plotting as plot


# ---------------track bar callback-------------------
def trackbar_callback(track_value):
    return


# -------------------------------    TRACK BAR   -----------------------------------------

'''cv2.namedWindow('window')
cv2.createTrackbar('B_trackbar_min', 'window', B_min_start_val,trackbar_max_val , trackbar_callback)
cv2.createTrackbar('G_trackbar_min', 'window', G_min_start_val,trackbar_max_val , trackbar_callback)
cv2.createTrackbar('R_trackbar_min', 'window', R_min_start_val,trackbar_max_val , trackbar_callback)
cv2.createTrackbar('B_trackbar_max', 'window', B_max_start_val,trackbar_max_val , trackbar_callback)
cv2.createTrackbar('G_trackbar_max', 'window', G_max_start_val,trackbar_max_val , trackbar_callback)
cv2.createTrackbar('R_trackbar_max', 'window', R_max_start_val,trackbar_max_val , trackbar_callback)'''

# -------------------------------------   VIDEO LOOP  -------------------------------------
cap = cv2.VideoCapture('/home/guy/Studies/clearvuze/rugby_sunny_4min.mp4')
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (300 * 4, glob.img_height_scale))
while (True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (glob.img_width_scale, glob.img_height_scale))

    #           --------Get Track Bar Values---------
    '''
    B_trackbar_min_val =cv2.getTrackbarPos("B_trackbar_min", "window")
    G_trackbar_min_val =cv2.getTrackbarPos("G_trackbar_min", "window")
    R_trackbar_min_val =cv2.getTrackbarPos("R_trackbar_min", "window")
    B_trackbar_max_val = cv2.getTrackbarPos("B_trackbar_max", "window")
    G_trackbar_max_val = cv2.getTrackbarPos("G_trackbar_max", "window")
    R_trackbar_max_val = cv2.getTrackbarPos("R_trackbar_max", "window")'''
    B_trackbar_min_val = glob.B_min_start_val
    G_trackbar_min_val = glob.G_min_start_val
    R_trackbar_min_val = glob.R_min_start_val
    B_trackbar_max_val = glob.B_max_start_val
    G_trackbar_max_val = glob.G_max_start_val
    R_trackbar_max_val = glob.R_max_start_val
    lower = np.uint8([B_trackbar_min_val, G_trackbar_min_val, R_trackbar_min_val])
    upper = np.uint8([B_trackbar_max_val, G_trackbar_max_val, R_trackbar_max_val])

    # IMAGE FILTERING
    mod_image_hor, mod_image_ver, white_filter = imfil.filter(frame, lower, upper, glob.moving_left or glob.left_corner,
                                                              glob.moving_right or glob.right_corner)

    # ----------------LINE DETECTION --------------------
    line_image_ver = np.copy(mod_image_ver) * 0
    line_image_hor = np.copy(mod_image_hor) * 0  # creating a blank to draw lines on
    lines_hor = cv2.HoughLinesP(mod_image_hor, glob.rho, glob.theta, glob.threshold, np.array([]),
                                glob.min_hor_line_length, glob.hor_max_line_gap)
    lines_ver = cv2.HoughLinesP(mod_image_ver, glob.rho, glob.theta, glob.threshold, np.array([]),
                                glob.min_ver_line_length, glob.ver_max_line_gap)

    # ----------------------------------- HORIZONTAL LINES -----------------------------------
    count = 0
    if not lines_hor is None:
        for line in lines_hor:
            for x1, y1, x2, y2 in line:
                count = count + 1
                pt1 = point.pt(x1, y1)
                pt2 = point.pt(x2, y2)
                y, x, slope = temp_line.calculate_hor_line_image_midpoint(pt1, pt2, glob.img_width_scale,
                                                                          glob.img_height_scale)
                mid_pt = point.pt(x, y)
                temp_line.temp_hor_lines_list = temp_line.update_line(mid_pt, slope, glob.frame_count,
                                                                      temp_line.temp_hor_lines_list, pt1, pt2, True, (
                                                                      glob.cam_move_frame_countdown > 0 and glob.cam_move_frame_countdown % 9 == 0 and count == 1))
                cv2.circle(line_image_hor, (x, y), 20, [255, 0, 0], -1)
                cv2.line(line_image_hor, (x1, y1), (x2, y2), [255, 100, 100], 5)
        temp_line.temp_hor_lines_list = temp_line.update_temp_line_list(glob.frame_count, temp_line.temp_hor_lines_list,
                                                                        perm_line.hor_pline_list, True,
                                                                        glob.img_height_scale)

    # ----------------------------------- VERTICAL LINES -----------------------------------
    count = 0
    if not lines_ver is None:
        for line in lines_ver:
            for x1, y1, x2, y2 in line:
                count = count + 1
                pt1 = point.pt(x1, y1)
                pt2 = point.pt(x2, y2)
                x, y, slope = temp_line.calculate_ver_line_image_midpoint(pt1, pt2, glob.img_width_scale,
                                                                          glob.img_height_scale)
                mid_pt = point.pt(x, y)
                temp_line.temp_ver_lines_list = temp_line.update_line(mid_pt, slope, glob.frame_count,
                                                                      temp_line.temp_ver_lines_list, pt1, pt2, False, (
                                                                      glob.cam_move_frame_countdown > 0 and glob.cam_move_frame_countdown % 9 == 0 and count == 1))
                cv2.circle(line_image_ver, (x, y), 20, [255, 0, 0], -1)
                cv2.line(line_image_ver, (x1, y1), (x2, y2), (255, 0, 0), 5)
        temp_line.temp_ver_lines_list = temp_line.update_temp_line_list(glob.frame_count, temp_line.temp_ver_lines_list,
                                                                        perm_line.ver_pline_list, False,
                                                                        glob.img_height_scale)

    # --------------------- IS CAMERA MOVING? ----------------------------------------
    glob.cam_move_frame_countdown, glob.cam_move_old_line, glob.cam_move_init, glob.cam_move_sum, glob.cam_move_count, glob.moving_left, glob.moving_right = mov.moving(
        glob.cam_move_frame_countdown, glob.cam_move_old_line, glob.cam_move_init, glob.cam_move_sum,
        glob.cam_move_count, glob.moving_left, glob.moving_right)

    # --------------------- are we in corner of the field? ----------------------------------------
    left_corner, right_corner = mov.corner(perm_line.ver_pline_list)

    # --------------------- CREATE HOMOGRAPHY ----------------------------------------

    if ((glob.frame_count % 10 == 0) or not (glob.moving_left or glob.moving_right)):
        if len([h for h in temp_line.temp_hor_lines_list if h.ID != 0]) >= 2 and len(
                [v for v in temp_line.temp_ver_lines_list if
                 v.ID != 0]) >= 2:  # ver_pline list must ==7 once whole field is calculated.

            src_pts, des_pts, glob.drawn_field = ImgToUni.find_points_on_field(glob.moving_left, glob.moving_right)
            h, status = cv2.findHomography(src_pts, des_pts)
            # if(status[0,0] != 0):
    warped_img = np.array([])
    if ('h' in locals()):
        warped_img = cv2.warpPerspective(frame, h, (int(glob.img_width_scale), int(glob.img_height_scale)))


        # -------------PLOTING --------------------------
    plot.plot(mod_image_hor, mod_image_ver, line_image_hor, line_image_ver, warped_img, glob.drawn_field, frame, out,
              white_filter)

    glob.frame_count = glob.frame_count + 1
    k = cv2.waitKey(1)
