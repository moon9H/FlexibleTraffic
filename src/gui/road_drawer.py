from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QLabel

class RoadDrawer:
    def __init__(self, scene, scene_width, scene_height, parent=None):
        self.scene = scene
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.parent = parent
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
        white_pen = QPen(QColor("white")); white_pen.setWidth(2); white_pen.setStyle(Qt.DashLine)
        yellow_pen = QPen(QColor("yellow")); yellow_pen.setWidth(3)
        stop_pen = QPen(QColor("white")); stop_pen.setWidth(4)  # 정지선은 더 두껍게
        border_pen = QPen(QColor("white")); border_pen.setWidth(2)  # 도로 외곽선


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
        
        # 각 도로의 정지선(더 두껍게)
        # 위쪽
        self.scene.addLine(csx - vrw / 2, csy - cb_size / 2, csx + vrw / 2, csy - cb_size / 2, stop_pen)
        # 아래쪽
        self.scene.addLine(csx - vrw / 2, csy + cb_size / 2, csx + vrw / 2, csy + cb_size / 2, stop_pen)
        # 왼쪽
        self.scene.addLine(csx - cb_size / 2, csy - hrh / 2, csx - cb_size / 2, csy + hrh / 2, stop_pen)
        # 오른쪽
        self.scene.addLine(csx + cb_size / 2, csy - hrh / 2, csx + cb_size / 2, csy + hrh / 2, stop_pen)

        # 도로 전체 외곽선 추가
        # 세로 도로 외곽
        self.scene.addRect(csx - vrw / 2, 0, vrw, self.scene_height, border_pen)
        # 가로 도로 외곽
        self.scene.addRect(0, csy - hrh / 2, self.scene_width, hrh, border_pen)
    
    def add_road_labels(self, labels):
        # 도로 이름을 교차로 주변에 표시
        label_positions = [
            (450, 10),    # 위쪽 (Road #1)
            (800, 320),   # 오른쪽 (Road #2)
            (350, 860),   # 아래쪽 (Road #3)
            (10, 550),    # 왼쪽 (Road #4)
        ]
        for i, (x, y) in enumerate(label_positions):
            road_label = QLabel(labels[i], self.parent)
            road_label.setGeometry(x, y, 100, 30)
            road_label.setAlignment(Qt.AlignCenter)
            road_label.setStyleSheet("font-weight: bold; font-size: 16px; background: rgba(255,255,255,180); border-radius: 8px;")