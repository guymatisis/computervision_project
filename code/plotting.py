import cv2


def plot(mod_image_hor, mod_image_ver, line_image_hor, line_image_ver, warped_img, drawn_field, frame, out,
         white_filter):
    lines_edges_hor = cv2.addWeighted(mod_image_hor, 1, line_image_hor, 1, 0)
    lines_edges_ver = cv2.addWeighted(mod_image_ver, 1, line_image_ver, 1, 0)

    # cv2.imshow("white filter", white_filter)
    cv2.imshow('frame_window', frame)

    if warped_img.size != 0:
        cv2.imshow("draw", drawn_field)
        cv2.imshow('homography', warped_img)
        cv2.imshow("drawn field", drawn_field)

        white_filter = cv2.cvtColor(white_filter, cv2.COLOR_GRAY2BGR)
        white_filter_resize = cv2.resize(white_filter, (300, 500))
        drawn_field = cv2.resize(drawn_field, (300, 500))
        frame_resize = cv2.resize(frame, (300, 500))
        warped_img_resize = cv2.resize(warped_img, (300, 500))
        multiple_imgs = cv2.hconcat([frame_resize, white_filter_resize, warped_img_resize, drawn_field])
        cv2.imshow("multiple", multiple_imgs)
        out.write(multiple_imgs)

    cv2.imshow("horizontal lines", lines_edges_hor)
    cv2.imshow("vertical lines", lines_edges_ver)
    # multiple_imgs = cv2.hconcat([frame, white_filter]);
