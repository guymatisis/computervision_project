# ***********   IMPORTS  ****************
import numpy as np
import perm_line as pl
import point

# ************* GLOBALS *******************

slope_global = 0
slope_buffer = []
temp_hor_lines_list = []
temp_ver_lines_list = []


# ************************** CLASSES ************* *********************


class Temp_Line:
    def __init__(self, mid_pt, slope, pt1, pt2, length, horizontal):
        self.mid_pt = mid_pt
        self.slope = slope
        self.occurances = 1
        self.ID = 0
        self.last_seen = 0
        self.delete = False
        self.pt1 = pt1
        self.pt2 = pt2
        self.length = length

        # ------------------BOTTOM/RIGHT POINT IS ALWAYS PT1, TOP/LEFT POINT = PT2
        if (horizontal):  # slope<1= horizontal, >1 = vertical
            if pt1.x <= pt2.x:
                self.pt1 = pt1
                self.pt2 = pt2
            else:
                self.pt1 = pt2
                self.pt2 = pt1
        else:
            if pt1.y >= pt2.y:
                self.pt1 = pt1
                self.pt2 = pt2
            else:
                self.pt1 = pt2
                self.pt2 = pt1

    # ********************  DELETE LINE**********************
    def delete_line(self, frame_count, pline_list):
        if self.ID == 0:
            return
        else:
            perm_line = [o for o in pline_list if (o.ID == self.ID)][0]
            perm_line.frame_at_deletion = frame_count
            if (self.x < 500):
                perm_line.side_at_deletion = pl.Side.Left
            else:
                perm_line.side_at_deletion = pl.Side.Right
            perm_line.on_screen = False

    # ******************** UPDATE PERMANENT LINES **********************
    def update_perm_line(self, frame_count, temp_lines_list, pline_list, horizontal):
        if len(pline_list) == 0:
            self.ID = 10
            pline_list.append(pl.Perm_Line(self.ID, frame_count))
        else:
            on_screen_lines = [o for o in temp_lines_list if (o.ID != 0)]
            if len(on_screen_lines) > 0:
                closest_line = find_closest_line(self, on_screen_lines, horizontal)
                if horizontal == False:
                    side = pl.Side.Left if ([o.mid_pt.x for o in temp_lines_list if (o.ID == closest_line.ID)][
                                                0] > self.mid_pt.x) else pl.Side.Right
                else:
                    side = pl.Side.Top if ([o.mid_pt.y for o in temp_lines_list if (o.ID == closest_line.ID)][
                                               0] > self.mid_pt.y) else pl.Side.Bottom

                if side == pl.Side.Left:  # LEFT/TOP SIDE
                    if (any([p for p in pline_list if p.ID == closest_line.ID - 1 and p.on_screen == False])):
                        self.ID = closest_line.ID - 1
                        [p for p in pline_list if p.ID == closest_line.ID - 1][0].on_screen = True
                    else:
                        if closest_line.ID > 10:
                            for pline in pline_list:
                                if pline.ID >= closest_line.ID:
                                    pline.ID = pline.ID + 1
                            for tline in temp_lines_list:
                                if tline.ID >= closest_line.ID and tline.ID != 0:
                                    tline.ID = tline.ID + 1
                            self.ID = closest_line.ID
                            pline_list.append(pl.Perm_Line(self.ID, frame_count))
                        else:
                            for pline in pline_list:
                                if pline.ID < closest_line.ID:
                                    pline.ID = pline.ID - 1
                            for tline in temp_lines_list:
                                if tline.ID < closest_line.ID and tline.ID != 0:
                                    tline.ID = tline.ID - 1
                            self.ID = closest_line.ID - 1
                            pline_list.append(pl.Perm_Line(self.ID, frame_count))
                else:  # RIGHT/BOTTOM SIDE
                    if (any([p for p in pline_list if p.ID == closest_line.ID + 1 and p.on_screen == False])):
                        self.ID = closest_line.ID + 1
                        [p for p in pline_list if p.ID == closest_line.ID + 1][0].on_screen = True
                    else:
                        if closest_line.ID >= 10:
                            for pline in pline_list:
                                if pline.ID > closest_line.ID:
                                    pline.ID = pline.ID + 1
                            for tline in temp_lines_list:
                                if tline.ID > closest_line.ID and tline.ID != 0:
                                    tline.ID = tline.ID + 1
                            self.ID = closest_line.ID + 1
                            pline_list.append(pl.Perm_Line(self.ID, frame_count))
                        else:
                            for pline in pline_list:
                                if pline.ID <= closest_line.ID:
                                    pline.ID = pline.ID - 1
                            for tline in temp_lines_list:
                                if tline.ID <= closest_line.ID and tline.ID != 0:
                                    tline.ID = tline.ID - 1
                            self.ID = closest_line.ID
                            pline_list.append(pl.Perm_Line(self.ID, frame_count))


            else:
                frame_at_deletion = [o.frame_at_deletion for o in pline_list]
                last_seen_pl = [l for l in pline_list if (l.frame_at_deletion == max(frame_at_deletion))][0]
                side = pl.Side.Left if (last_seen_pl.side_at_deletion == pl.Side.Left) else pl.Side.Right
                if side == pl.Side.Left:
                    if len([o for o in pline_list if (o.ID == last_seen_pl.ID - 1)]) > 0:  # alread exists a line
                        self.ID = last_seen_pl.ID - 1
                    else:
                        pline_list.append(pl.Perm_Line(min([o.ID for o in pline_list]) - 1, frame_count))
                        self.ID = last_seen_pl.ID - 1
                else:
                    if len([o for o in pline_list if (o.ID == last_seen_pl.ID + 1)]) > 0:  # alread exists a line
                        self.ID = last_seen_pl.ID + 1
                    else:
                        pline_list.append(pl.Perm_Line(max([o.ID for o in pline_list]) + 1, frame_count))
                        self.ID = last_seen_pl.ID + 1


# ********************  FIND CLOSEST LINE**********************
def find_closest_line(single_line, line_list, horizontal):
    min_dist = 1000000
    return_line = None
    for line in line_list:
        if (horizontal == False):
            if abs(line.mid_pt.x - single_line.mid_pt.x) < min_dist:
                return_line = line
                min_dist = abs(line.mid_pt.x - single_line.mid_pt.x)
        else:
            if abs(line.mid_pt.y - single_line.mid_pt.y) < min_dist:
                return_line = line
                min_dist = abs(line.mid_pt.y - single_line.mid_pt.y)
    return return_line


# ******************** UPDATE LINE **********************
def update_line(mid_pt, slope, frame_count, temp_lines_list, pt1, pt2, horizontal, moving):
    for line in temp_lines_list:  # itterate through all lines
        line_buffer = 25
        slope_buffer = 10
        global scope_global
        if ((mid_pt.x < (line.mid_pt.x + line_buffer)) & (mid_pt.x > (line.mid_pt.x - line_buffer)) & (
            mid_pt.y < (line.mid_pt.y + line_buffer)) & (mid_pt.y > (line.mid_pt.y - line_buffer))):  # &
            # ((line.slope< slope_buffer+ slope_global) & (line.slope> slope_global - slope_buffer) or slope_global==0)):      #temp line is previously seen line

            # ------------------- UPDATE POINT 1 and POINT 2 -------------------
            if (horizontal == True):
                if pt1.x <= line.pt1.x + 5:
                    line.pt1 = pt1
                if pt2.x <= line.pt1.x + 5:
                    line.pt1 = pt2
                if pt1.x >= line.pt2.x - 5:
                    line.pt2 = pt1
                if pt2.x >= line.pt2.x - 5:
                    line.pt2 = pt2
            else:
                if pt1.y >= line.pt1.y - 5:
                    line.pt1 = pt1
                if pt2.y >= line.pt1.y - 5:
                    line.pt1 = pt2
                if pt1.y <= line.pt2.y + 5:
                    line.pt2 = pt1
                if pt2.y <= line.pt2.y + 5:
                    line.pt2 = pt2
            if (moving):
                if horizontal == True:
                    if pt1.x <= pt2.x:
                        line.pt1 = pt1
                        line.pt2 = pt2
                    else:
                        line.pt1 = pt2
                        line.pt2 = pt1
                else:
                    if pt1.y >= pt2.y:
                        line.pt1 = pt1
                        line.pt2 = pt2
                    else:
                        line.pt1 = pt2
                        line.pt2 = pt1

            if (line.pt1.x - line.pt2.x) == 0:
                line.slope = 10
            else:
                line.slope = (line.pt1.y - line.pt2.y) / (line.pt1.x - line.pt2.x)
            line.mid_pt.x = mid_pt.x
            line.mid_pt.y = mid_pt.y
            line.occurances = line.occurances + 1
            line.last_seen = 0
            line.length = int((abs(line.pt1.x - line.pt2.x) ** 2 + abs(line.pt1.y - line.pt2.y) ** 2) ** (.5))
            return temp_lines_list
    length = int((abs(pt1.x - pt2.x) ** 2 + abs(pt1.y - pt2.y) ** 2) ** (.5))
    temp_lines_list.append(Temp_Line(mid_pt, slope, pt1, pt2, length, horizontal))  # create new line
    return temp_lines_list


# ******************** UPDATE TEMP LINE LIST **********************
def update_temp_line_list(frame_count, temp_lines_list, pline_list, horizontal, img_height):
    for l in temp_lines_list: l.last_seen = l.last_seen + 1
    # Permenent line detected
    temp_line_occurances_20 = [line for line in temp_lines_list if (line.occurances > 20 and line.ID == 0)]
    for l in temp_line_occurances_20:
        if (horizontal == False or l.mid_pt.y > (img_height / 2)):
            l.update_perm_line(frame_count, temp_lines_list, pline_list, horizontal)

    # DELETES LINES FROM TEMP_LIST WHICH HAVENT BEEN SEEN IN 10 FRAMES
    lines_to_delete = [(i, o) for i, o in enumerate(temp_lines_list) if (o.last_seen >= 10)]
    if len(lines_to_delete) > 0:
        for p in pline_list:
            if p.ID in [o.ID for o in temp_lines_list if o.last_seen >= 10]:
                p.on_screen = False
        # for line in np.array(lines_to_delete)[:,1]: line.delete_line(frame_count,pline_list)
        count = 0
        for i in np.array(lines_to_delete)[:, 0]:
            temp_lines_list.pop(i - count)
            count = count + 1

    # DELETE HORIZONTAL LINES THAT ARE TOO STEEP
    if (horizontal):
        lines_to_delete = [(i, o) for i, o in enumerate(temp_lines_list) if o.slope > 1 or o.slope < -1]
        if len(lines_to_delete) > 0:
            count = 0
            for i in np.array(lines_to_delete)[:, 0]:
                temp_lines_list.pop(i - count)
                count = count + 1

                # update global slope
    update_slope_buffer(sum([o.slope for o in temp_lines_list]) / len(temp_lines_list))
    return temp_lines_list


# ********************  CALCULATE MIDPOINT **********************
def calculate_ver_line_image_midpoint(pt1, pt2, img_w, img_h):
    if (pt2.x - pt1.x) == 0:  # divide by zero
        return int(pt1.x), int(img_h / 2), 1000
    slope = (pt2.y - pt1.y) / (pt2.x - pt1.x)
    # if slope == 0:

    x = pt1.x + (img_h / 2 - pt1.y) / slope
    return int(x), int(img_h / 2), slope


def calculate_hor_line_image_midpoint(pt1, pt2, img_w, img_h):
    if (pt2.x - pt1.x) == 0:  # divide by zero
        return int(pt1.y), int(img_w / 2), 0
    slope = (pt2.y - pt1.y) / (pt2.x - pt1.x)
    y = pt1.y + (img_w / 2 - pt1.x) * slope
    return int(y), int(img_w / 2), slope


# ********************  UPDATE SLOPE BUFFER **********************
def update_slope_buffer(slope):
    global slope_global
    global slope_buffer
    slope_buffer.append(slope)
    buffer_len = 10
    if (len(slope_buffer) >= buffer_len):
        slope_buffer.pop(0)
    slope_global = sum([x for x in slope_buffer]) / len(slope_buffer)

# def name_line(line,temp_line_list):
#    for other_line in temp_line_list:
#        if(other_line != line):
#            
#    return ID
