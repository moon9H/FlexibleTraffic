from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt

class RoadDrawer:
    def __init__(self, scene, scene_width, scene_height):
        self.scene = scene
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.vert_road_width = 200
        self.horiz_road_height = 200
        self.center_box_size = 200
        self.center_x = self.scene_width / 2
        self.center_y = self.scene_height / 2

    def draw_intersection(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb_size = self.center_box_size
        self.scene.addRect(QRectF(csx - vrw / 2, 0, vrw, self.scene_height), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(0, csy - hrh / 2, self.scene_width, hrh), brush=QBrush(QColor("dimgray")))
        self.scene.addRect(QRectF(csx - cb_size / 2, csy - cb_size / 2, cb_size, cb_size), brush=QBrush(QColor("dimgray")))

    def draw_lane_markings(self):
        csx, csy = self.center_x, self.center_y
        vrw = self.vert_road_width
        hrh = self.horiz_road_height
        cb_size = self.center_box_size
        white_pen = QPen(QColor("white")); white_pen.setWidth(2)
        yellow_pen = QPen(QColor("yellow")); yellow_pen.setWidth(3); yellow_pen.setStyle(Qt.DashLine)
        self.scene.addLine(csx, 0, csx, csy - cb_size / 2, yellow_pen)
        self.scene.addLine(csx, csy + cb_size / 2, csx, self.scene_height, yellow_pen)
        for x in [csx - vrw / 4, csx + vrw / 4]:
            self.scene.addLine(x, 0, x, csy - cb_size / 2, white_pen)
            self.scene.addLine(x, csy + cb_size / 2, x, self.scene_height, white_pen)
        self.scene.addLine(0, csy, csx - cb_size / 2, csy, yellow_pen)
        self.scene.addLine(csx + cb_size / 2, csy, self.scene_width, csy, yellow_pen)
        for y in [csy - hrh / 4, csy + hrh / 4]:
            self.scene.addLine(0, y, csx - cb_size / 2, y, white_pen)
            self.scene.addLine(csx + cb_size / 2, y, self.scene_width, y, white_pen)