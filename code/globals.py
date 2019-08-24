import numpy as np

# IMAGE
img_width_scale = 500
img_height_scale = 500

# PARAMETERS

frame_count = 0
# TRACKBAR
B_min_start_val = 7
G_min_start_val = 0
R_min_start_val = 0
B_max_start_val = 40
G_max_start_val = 40
R_max_start_val = 40
trackbar_max_val = 255

# -----------HOUGHS LINE ALGORITHM PARAMETERS--------------------
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 200
min_ver_line_length = 200
min_hor_line_length = 100
ver_max_line_gap = 45
hor_max_line_gap = 0

ver_line_angle = 0
cam_move_init = True
cam_move_count = 0
cam_move_sum = 0
cam_move_avg = 0
cam_move_line = 0
cam_move_old_line = 0
cam_move_frame_countdown = 0
moving_left = False
moving_right = False
left_corner = False
right_corner = False
drawn_field = np.array([])
left_corner = right_corner = False
