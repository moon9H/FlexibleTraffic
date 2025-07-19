from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import QTimer

"""
20250719 https://github.com/jaeyoung0710/swproject/blob/main/teamproject/test4.py 와 merge 진행
"""

class VehicleItem(QGraphicsRectItem):
    def __init__(self, direction, x, y, width=40, height=25, color=QColor(30, 144, 255)):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setPos(x, y)
        self.direction = direction
        self.speed = 3
    
    def move_forward(self):
        dx, dy = 0, 0
        if self.direction == 'north':
            dy = self.speed
        elif self.direction == 'south':
            dy = -self.speed
        elif self.direction == 'east':
            dx = self.speed
        elif self.direction == 'west':
            dx = -self.speed
        self.moveBy(dx, dy)

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
        self.view = QGraphicsView(self.scene, self.parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.vehicles = []


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



    def add_detected_vehicles(self, vehicle_counts):
        car_width, car_height = 40, 25
        lane_spacing = 30
        car_spacing = 10
        center_x, center_y = 500, 500
        vrw, hrh = 200, 200

        def distribute(count):
            half = count // 2
            return [half + (count % 2), half]

        # 북쪽 ↓
        north_lanes = [center_x - vrw / 4 - lane_spacing-14, center_x - vrw / 4 + lane_spacing-25]
        for i, x in enumerate(north_lanes):
            for j in range(distribute(vehicle_counts[0])[i]):
                y = 0 - j * (car_height + car_spacing)
                car = VehicleItem("north", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 남쪽 ↑
        south_lanes = [center_x + vrw / 4  -4, center_x + vrw / 4 + lane_spacing+16]
        for i, x in enumerate(south_lanes):
            for j in range(distribute(vehicle_counts[3])[i]):
                y = 1000 + j * (car_height + car_spacing)
                car = VehicleItem("south", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 서쪽 ←
        west_lanes = [center_y - hrh / 4 - lane_spacing+20, center_y - hrh / 4 + lane_spacing+5]
        for i, y in enumerate(west_lanes):
            for j in range(distribute(vehicle_counts[3])[i]):
                x = 1000 + j * (car_width + car_spacing)
                car = VehicleItem("west", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)

        # 동쪽 →
        east_lanes = [center_y + hrh / 4 - lane_spacing-10, center_y + hrh / 4 + lane_spacing-14]
        for i, y in enumerate(east_lanes):
            for j in range(distribute(vehicle_counts[2])[i]):
                x = 0 - j * (car_width + car_spacing)
                car = VehicleItem("east", x, y)
                self.scene.addItem(car)
                self.vehicles.append(car)


    def update_simulation(self):
        for car in self.vehicles:
            car.move_forward()

    def animate_vehicles(self, vehicle_counts):
        # 기존 차량 제거
        for item in self.vehicles:
            self.scene.removeItem(item)
        self.add_detected_vehicles(vehicle_counts)
        self.timer.start(30)
