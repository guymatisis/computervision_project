import temp_line


def moving(cam_move_frame_countdown, cam_move_old_line, cam_move_init, cam_move_sum, cam_move_count, moving_left,
           moving_right):
    if cam_move_frame_countdown > 0:
        cam_move_frame_countdown = cam_move_frame_countdown - 1
    else:
        moving_right = False
        moving_left = False
    if (cam_move_old_line == 0):
        cam_move_line = [vline for vline in temp_line.temp_ver_lines_list if
                         (vline.ID != 0 and vline.last_seen < 2)]  # get initial line
    else:
        cam_move_line = [vline for vline in temp_line.temp_ver_lines_list if
                         (vline.ID == cam_move_old_line.ID)]  # get same line as last time
        if (cam_move_line == 0):
            cam_move_line = [vline for vline in temp_line.temp_ver_lines_list if
                             (vline.ID != 0 and vline.last_seen < 2)]  # if can find smae line, get new one

    if (len(cam_move_line) != 0):
        cam_move_line = cam_move_line[0]
        cam_move_old_line = cam_move_line
        if (cam_move_init == True):
            cam_move_sum = cam_move_sum + cam_move_line.mid_pt.x
            cam_move_count = cam_move_count + 1
        if (cam_move_count == 10):
            cam_move_init = False;
            cam_move_avg = cam_move_sum / cam_move_count
        if (not cam_move_init):
            if cam_move_line.mid_pt.x > cam_move_avg + 40:
                cam_move_init = True
                cam_move_count = 0
                cam_move_sum = 0
                moving_left = True
                cam_move_frame_countdown = 200
            elif cam_move_line.mid_pt.x < cam_move_avg - 40:
                cam_move_init = True
                cam_move_count = 0
                cam_move_sum = 0
                moving_right = True
                cam_move_frame_countdown = 200

    return cam_move_frame_countdown, cam_move_old_line, cam_move_init, cam_move_sum, cam_move_count, moving_left, moving_right


def corner(line_list):
    left_corner = right_corner = False
    for line in line_list:
        if (line.ID == 6 or line.ID == 7) and line.on_screen == True:
            left_corner = True
        if (line.ID == 13 or line.ID == 14) and line.on_screen == True:
            right_corner = True
        if line.ID == 9 and line.on_screen == True:
            right_corner = False
        if line.ID == 11 and line.on_screen == True:
            left_corner = False
    return left_corner, right_corner
