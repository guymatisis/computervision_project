import point

hor_pline_list = []
ver_pline_list = []


class Perm_Line:
    def __init__(self, ID, frame_count):
        self.initial_frame_count = frame_count
        self.ID = ID
        self.side_at_deletion = Side.Left
        self.frame_at_deletion = 0
        self.on_screen = True
        self.horizontal = True
        self.pt1 = point.pt(0, 0)
        self.pt2 = point.pt(0, 0)
        self.slope = 0


class Side:
    Left = 0
    Right = 1
    Top = 0
    Bottom = 1
